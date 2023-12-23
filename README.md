# Image Range Converter

This Python script, `imcvt.py`, is used to convert images between full range (0-255) and limited range (16-235).

## Dependencies

The script requires the following Python packages:

- opencv-python
- numpy

You can install these dependencies using pip:

```bash
pip install -r requirements.txt
```

## Usage

You can use the script in two ways:

**Automatic Conversion:** If no arguments are given, the script will attempt to locate files in an IMAGES folder and convert them from limited to full range if they have not already been converted. The images will be saved to ../IMAGES/full folder

```bash
python imcvt.py
```

**Manual Conversion:** You can specify the conversion type ('full' or 'limited') and the image files to convert as command line arguments.

```bash
python imcvt.py [full|limited] [file1] [file2] ...
```

For example, to convert an image from limited range to full range:

```bash
python imcvt.py full image1.jpg
```

Or to convert an image from full range to limited range:

```bash
python imcvt.py limited image1.jpg
```

The converted images will be saved in the same directory as the original images, with a suffix indicating the conversion type ('_full' or '_limited').

## Example Use Case
1. Several images have been saved on an SD card in the IMAGES folder
2. The SD card is inserted into a macOS computer
3. python imcvt.py
4. The images are converted from limited to full range and saved to the ../IMAGES/full folder with a _full suffix added to the new filename.
5. Any images that have already been converted are skipped.
6. The SD card is removed from the computer

## Note

The automatic conversion feature is currently supported on macOS only.
