# Image Range Converter

This Python script, `imcvt.py`, is used to convert images between full range (0-255) and limited range (16-235).

## macOS Quick Start
Anaconda Python is recommended for macOS since it will not change the system Python installation.  Navigate to
[Anaconda Downloads](https://www.anaconda.com/download) and locate the correct installer for your system 
(Apple Silicon or Intel).  Use the default options when installing.

Git is also required for macOS.  If you do not have Git installed, you can download it 
from [Git Downloads](https://git-scm.com/downloads).  Use the default options when installing.

Once Anaconda and Git are installed, open a new terminal window.  You should see the (base) prefix in
the terminal prompt which indicates you are using the Anaconda Python environment, for example:
```bash
(base) MacBook-Pro:~ user%
```
Execute the following commands to download the script and install the dependencies:

```bash
git clone https://github.com/claesmk/image_range_convert.git
cd image_range_convert
pip install -r requirements.txt
```

You can then insert a SD card or USB drive containing images into your computer and execute the following command:

```bash
python imcvt.py
```

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

### Automatic Conversion

If no arguments are given, the script will attempt to locate files in an IMAGES folder and convert them from limited 
to full range if they have not already been converted.

```bash
python imcvt.py
```

When using automatic conversion, the images will be saved to ../IMAGES/full folder with a _full.jpg suffix.  If this
folder does not exist, it will be created.  If an image with the same name already exists in the full folder, it is 
assumed that image has already been converted and it will not be converted again.

### Manual Conversion 

You can specify the conversion type ('full' or 'limited') and the image files to convert as command line arguments.

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

The converted images will be saved in the same directory as the original images, with a suffix indicating the 
conversion type ('_full' or '_limited').

### Example Auto Convert Use Case
1. Several images have been saved on an SD card in the IMAGES folder
2. The SD card is inserted into a macOS computer
3. Execute *python imcvt.py*
4. The /Volumes folder is searched for a volume with an IMAGES folder
5. If one is found the user is prompted for conversion confirmation
6. The images in the IMAGES folder are converted from limited to full range and saved to the ../IMAGES/full folder 
with a _full suffix added to the filename
7. The SD card is removed from the computer and inserted into the original device
8. The converted images are accessed from the IMAGES/full folder
9. Later, new images are saved to the IMAGES folder mixed in with the older images
10. When steps 2-6 are repeated, the script will only convert the new images that have not already been converted
11. In order to force the script to convert all images again, the IMAGES/full folder should be deleted

## Notes
* The automatic conversion feature is currently supported on macOS only.
* Since the script automatically creates output files named with a _full or _limited suffix, the script will not
allow you to convert an image that already has a _full or _limited suffix.  This is to prevent potential recursion
where an image is named _full_full_full... or _limited_limited_limited...
