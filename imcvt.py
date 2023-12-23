"""Converts images between full range (0-255) and limited range (16-235)"""
import cv2
import numpy as np
import os
import sys


def convert_image(image: np.ndarray, new_max: int, new_min: int, old_max: int, old_min: int) -> np.ndarray:
    """Convert the image from old range to new range"""
    # warn if any values are outside the old range
    if image.min() < old_min or image.max() > old_max:
        print(f'WARNING: Values outside ({old_min}-{old_max}) will be clipped')

    # clip image to old range
    image = image.clip(old_min, old_max).astype('uint8')

    # convert the image from old range to new range
    image = ((image - old_min) * ((new_max - new_min) / (old_max - old_min))) + new_min

    # clip image to new range
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

    # get the directory and file name
    path, name = os.path.split(file_name)
    # get the image extension
    name, ext = os.path.splitext(name)
    # get the new file name
    new_name = name+'_'+convert_to+ext

    # if the use_subdir param is True, create a subdirectory for the converted images
    if use_subdir:
        new_path = os.path.join(path, convert_to)
        # create the subdirectory if it does not exist
        if not os.path.exists(new_path):
            os.mkdir(new_path)
        # add the subdirectory to the file name
        new_file_name = os.path.join(new_path, new_name)
    else:
        # get the new file name
        new_file_name = os.path.join(path, new_name)
    # If the image already exists skip it
    if os.path.isfile(new_file_name):
        print(f'Skipping {file_name}')
        return
    print('Converting ' + file_name)

    # read the image
    image = cv2.imread(file_name)
    # convert the image
    if convert_to == 'full':
        converted_image = limited_to_full(image)
    else:
        converted_image = full_to_limited(image)
    # save the image
    cv2.imwrite(new_file_name, converted_image)


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
                    if not file_name.startswith('.'):
                        if file_name.endswith('.jpg') or file_name.endswith('.png'):
                            convert_image_file(os.path.join(images_dir, file_name),
                                               convert_to='full', use_subdir=True)
            break


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
    else:
        # Convert all the files listed on the command line to the specified range
        for file in sys.argv[2:]:
            convert_image_file(file, sys.argv[1])
