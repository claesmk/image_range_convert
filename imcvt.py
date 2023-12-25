"""Converts images between full range (0-255) and limited range (16-235)"""
import os
import sys
import glob
import numpy as np
import cv2


def convert_image(image: np.ndarray,
                  new_max: int, new_min: int, old_max: int, old_min: int,
                  show_warning: bool = True) -> np.ndarray:
    """
    Convert the image from old range to new range

    Args:
        image: image to convert
        new_max: new maximum value (255 full, 235 limited)
        new_min: new minimum value (0 full, 16 limited)
        old_max: old maximum value (255 full, 235 limited)
        old_min: old minimum value (0 full, 16 limited)
        show_warning: show a warning if any values are outside the old range

    Examples:
        Convert from full range to limited range:
          convert_image(image, 235, 16, 255, 0)

        Convert from limited range to full range:
          convert_image(image, 255, 0, 235, 16)
    """
    # raise an error if the image is not uint8
    if image.dtype != 'uint8':
        raise TypeError('Currently only 8-bit images are supported')

    # Warn if any old values are outside the old range.  This should only happen when the input image
    # is supposed to be limited range but contains values outside 16-235 (sub-black or super-white)
    if (image.min() < old_min or image.max() > old_max) and show_warning:
        print(f'  WARNING: Image contains values outside ({old_min}-{old_max}) which will be clipped')

    # Clip the image to the expected range to prevent overflow since dtype is uint8
    image = image.clip(old_min, old_max).astype('uint8')

    # convert the image from old range to new range
    image = ((image - old_min) * ((new_max - new_min) / (old_max - old_min))) + new_min

    # round to nearest int to improve conversion accuracy
    image = np.rint(image).astype('uint8')

    # This check should not be necessary since the input image was clipped.  Performing another
    # check here as a safety precaution to prevent out-of-range values
    if (image.min() < new_min or image.max() > new_max) and show_warning:
        print(f'  WARNING: New values outside ({new_min}-{new_max}) will be clipped')
    return image.clip(new_min, new_max).astype('uint8')


def full_to_limited(image: np.ndarray) -> np.ndarray:
    """Convert the image from full range (0-255) to limited range (16-235)"""
    return convert_image(image, 235, 16, 255, 0)


def limited_to_full(image: np.ndarray) -> np.ndarray:
    """Convert the image from limited range (16-235) to full range (0-255)"""
    return convert_image(image, 255, 0, 235, 16)


def convert_image_file(file_name: str, convert_to: str, use_subdir: bool = False):
    """Convert the image file to the specified range"""
    # Check for valid convert_to argument
    if convert_to not in ['full', 'limited']:
        print('Invalid argument: ' + convert_to)
        return

    # Make sure the file exists
    if not os.path.isfile(file_name):
        print(f'File does not exist: {file_name}')
        return

    # get the directory and file name
    path, name = os.path.split(file_name)
    # get the image extension
    name, ext = os.path.splitext(name)

    # It's possible a file could be legitimately named _full.ext or _limited.ext
    # However, for the purpose of this script, we will assume that if this is true
    # we will skip trying to convert it
    if name.endswith('_full') or name.endswith('_limited'):
        print(f'  Skipping {file_name} because it ends with _full or _limited')
        return

    # get the new file name suffix _full.ext or _limited.ext
    new_name = name+'_'+convert_to+ext

    # print the file name
    print(file_name)

    # if the use_subdir param is True, create a subdirectory for the converted images
    if use_subdir:
        new_path = os.path.join(path, convert_to)
        # create the subdirectory if it does not exist
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        # add the subdirectory to the new file name
        new_file_name = os.path.join(new_path, new_name)
    else:
        # get the new file name the same path
        new_file_name = os.path.join(path, new_name)
    # If the image already exists skip it
    if os.path.isfile(new_file_name):
        print(f'  Skipping because {new_file_name} already exists')
        return
    print('  Converting to ' + new_file_name)

    # read the image
    image = cv2.imread(file_name)
    # convert the image
    if convert_to == 'full':
        converted_image = limited_to_full(image)
    else:
        converted_image = full_to_limited(image)

    # save the image
    cv2.imwrite(new_file_name, converted_image)


def process_images_folder(images_dir: str):
    """Prompts the user to convert images in the specified directory"""

    print(f'Found IMAGES folder at {images_dir}')
    # Prompt the user to convert images
    while True:
        try:
            selection = input('Convert images? [y/n]: ').lower()
            assert selection in ['y', 'n']
            break
        except (ValueError, AssertionError):
            print('Invalid selection')
    if selection == 'y':
        # Convert images
        for file_name in os.listdir(images_dir):
            # skip any hidden files
            if not file_name.startswith('.'):
                # only convert jpg and png files
                if file_name.endswith('.jpg') or file_name.endswith('.png'):
                    convert_image_file(os.path.join(images_dir, file_name),
                                       convert_to='full', use_subdir=True)


def find_images():
    """
    Currently supports macOS only.  Looks for images in /Volumes/<dir>/IMAGES and prompts the user if they want to
    convert images in that directory.  If the user selects yes, the images are converted from limited to full range.
    The new image is saved with a _full suffix.  If a _full suffix already exists, the image is skipped.
    """
    # Check for macOS
    if sys.platform != 'darwin':
        print('Automatic find only supported on macos')
        return
    # Look for an IMAGES folder
    print('Looking for IMAGES folder...')
    volumes = [f for f in os.listdir('/Volumes') if not f.startswith('.')]
    for volume in volumes:
        images_dir = os.path.join('/Volumes', volume, 'IMAGES')
        if os.path.isdir(images_dir):
            process_images_folder(images_dir)
            return


if __name__ == '__main__':
    """
    Converts images from full to limited range or limited to full range based on command line arguments.
    If no arguments are given, a brief help message is printed and the program will attempt to locate 
    files in an IMAGES folder and covert them from limited to full range if they have not already been
    converted.
    
    Usage: 
        imcvt.py 
        imcvt.py [full|limited] [file1] [file2] ...
    """
    # if less than one argument is given, print usage
    if len(sys.argv) < 2:
        find_images()
    elif len(sys.argv) > 2:
        # if glob pattern is given, convert all matching files
        if '*' in sys.argv[2]:
            for file in glob.glob(sys.argv[2]):
                convert_image_file(file, sys.argv[1])
        else:
            for file in sys.argv[2:]:
                convert_image_file(file, sys.argv[1])
    else:
        # print usage
        print('Usage: ' + sys.argv[0] + ' [full|limited] [file1] [file2] ...')
