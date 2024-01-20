#!/usr/bin/env python3

import pathlib
import sys
import logging

import inkex

# Uncomment the following to setup logging to /tmp/log.txt
# logging.basicConfig(filename="/tmp/log.txt", level=logging.DEBUG)


ELEMENTS_XPATH = (
    "//svg:path | //svg:rect | //svg:circle | //svg:ellipse | //svg:line | "
    "//svg:polyline | //svg:polygon"
)


def fatal_error(msg):
    sys.stderr.write(msg + "\n")
    sys.exit(1)


class SplitPathByColor(inkex.Effect):
    def add_arguments(self, parser):
        super().add_arguments(parser)

        parser.add_argument(
            "--color_name_mapping",
            default="",
            help="String of color to name mappings",
        )
        parser.add_argument(
            "--remove_text_elements",
            type=inkex.Boolean,
            default=False,
            help="If True, remove all text elements from the output documents",
        )
        parser.add_argument(
            "--remove_hidden_elements",
            type=inkex.Boolean,
            default=True,
            help="If True, remove and ignore all hidden (display: none) elements",
        )
        parser.add_argument(
            "--testnumber",
            default="",
        )

    def update_mappings(self):
        self.color_name_mapping = {}
        mappings_str = self.options.color_name_mapping.strip()
        if mappings_str:
            # It's passed through as a the string `\n`, not a real newline
            for mapping in mappings_str.split("\\n"):
                color, name = mapping.split(" ", 1)
                if color.startswith("#"):
                    color = color[1:]
                name = name.strip()
                self.color_name_mapping[color] = name

    def effect(self):
        pth = self.document_path()
        if not pth:
            fatal_error("Document has not been saved or Inkscape too old")
        self.source_path = pathlib.Path(pth)
        logging.info("Source path: %s", self.source_path)

        self.update_mappings()
        # Find all the basic shape elements, including path, rect, circle, ellipse, line, polyline, polygon
        elements = self.svg.xpath(ELEMENTS_XPATH, namespaces=inkex.NSS)
        path_colors = {}
        for element in elements:
            style = element.specified_style()
            if self.options.remove_hidden_elements:
                if style.get("display", "").lower() == "none":
                    logging.debug("Skipping hidden element %s", element.attrib["id"])
                    continue

            # Get the stroke-color attribute if set
            color = element.get("stroke")
            if color is None:
                color = style.get("stroke")
                if color is None:
                    color = element.get("fill")
                    if color is None:
                        color = style.get("fill")

            if color is None:
                # No color specified, skip this path
                logging.error("No color specified for path %s", element.attrib["id"])
                continue

            if color.startswith("#"):
                color = color[1:]
            color_name = self.color_name_mapping.get(color, color)
            if color_name not in path_colors:
                path_colors[color_name] = []
                logging.debug(
                    "New color %s with element ID: %s", color_name, element.attrib["id"]
                )
            path_colors[color_name].append(element.attrib["id"])

        # For each color, make a copy of the document, and remove all the colors that are not the current color
        for color_name, path_ids in path_colors.items():
            logging.info("Color %s", color_name)
            svg = self.svg.copy()
            # Delete _all_ the unwanted paths
            if self.options.remove_text_elements:
                search_path = ELEMENTS_XPATH + " | //svg:text "
            else:
                search_path = ELEMENTS_XPATH
            svg_elements = svg.xpath(search_path, namespaces=inkex.NSS)
            logging.debug("Found %d elements", len(svg_elements))
            for element in svg_elements:
                path_id = element.attrib["id"]
                if path_id not in path_ids:
                    element.getparent().remove(element)
            # Save the document to a file
            svg_file = (
                self.source_path.parent / f"{self.source_path.stem}_{color_name}.svg"
            )
            logging.debug("Saving to %s", svg_file)
            with svg_file.open("wb") as f:
                f.write(svg.tostring())


if __name__ == "__main__":
    SplitPathByColor().run()
