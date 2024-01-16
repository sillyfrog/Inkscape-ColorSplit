# Inkscape-ColorSplit
An Inkscape extension that separates out elements based on color (for laser cutting and CNC)

## Installation

1. Download the .zip file under Code > Download ZIP
2. Unzip the file
3. Copy the `ColorSplit.inx` and `ColorSplit.py` files to your Inkscape extensions directory
    * On Windows, this is usually `C:\Program Files\Inkscape\share\extensions`
    * On Mac, this is usually `/Applications/Inkscape.app/Contents/Resources/share/inkscape/extensions`
    * On Linux, this is usually `/usr/share/inkscape/extensions`
    * You can find the exact location by opening Inkscape and going to `Preferences > System > User extensions`
4. Restart Inkscape

## Usage

1. Open your SVG file in Inkscape
2. Select Extensions > CNC Tools > Split Elements by Color
3. You can optionally enter a "mapping" from a color code (eg: `#FF0000`) to a name (eg: `cutting`), each line in the text area should be a new mapping, the color should be split by a space
4. Click Apply

There will be a new file created for each color used in the SVG file. The file name will be in the format `original_file_name-color.svg`. If you specified a mapping, the color will be replaced with the name you specified.

This was originally designed to be used with the output from [TabbedBoxMaker](https://github.com/sillyfrog/TabbedBoxMaker), for use with Snapmaker Luban so I could easily split out the text from the cut lines. I also use it for CNC where I need to ensure the order is correct (ie: cutout the inside before the outside).