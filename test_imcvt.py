"""Test cases for imcvt.py"""
import unittest
import os
import numpy as np
import cv2
from imcvt import limited_to_full, full_to_limited


class TestImageConversion(unittest.TestCase):
    """Some test cases to check image conversion is correct"""
    def test_basic_math(self):
        """Test to make sure simple conversion math works correctly"""
        # test full to limited
        full = [[0, 0, 0], [16, 16, 16], [235, 235, 235], [255, 255, 255],  # black, lb, lw, white
                [255, 0, 0],  # red
                [0, 255, 0],  # green
                [0, 0, 255]]  # blue

        lim = [[16, 16, 16], [30, 30, 30], [218, 218, 218], [235, 235, 235],  # black, lb, lw, white
               [235, 16, 16],  # red
               [16, 235, 16],  # green
               [16, 16, 235]]  # blue

        # convert to numpy
        full = np.array(full).astype('uint8')
        lim = np.array(lim).astype('uint8')

        # convert full to limited
        converted = full_to_limited(full)
        self.assertTrue((converted == lim).all())

        # convert limited to full
        converted = limited_to_full(lim)
        self.assertTrue((converted == full).all())

    def test_limited_clipping(self):
        """Test to make sure clipping works correctly"""
        # Some values outside limited range
        lim_invalid = [[15, 16, 17], [236, 235, 234]]
        expected = [[0, 0, 1], [255, 255, 254]]
        lim_invalid = np.array(lim_invalid).astype('uint8')
        expected = np.array(expected).astype('uint8')
        converted = limited_to_full(lim_invalid)
        self.assertTrue((converted == expected).all())

    def test_uint8(self):
        """Test to make sure only uint8 images are supported"""
        uint16 = np.array([[0, 0, 0], [16, 16, 16], [235, 235, 235], [255, 255, 255]], dtype='uint16')
        # make sure an exception is raised when a type uint16 image is passed
        with self.assertRaises(TypeError):
            limited_to_full(uint16)

    def test_create_test_images(self):
        """Creates some images to use for testing if they don't already exist"""
        # The reference image is speedracer_full_range.png
        # Make a limited version of the reference image
        image_full = cv2.imread('test_images/speedracer_full_range.png')
        # convert to limited range
        image_lim = full_to_limited(image_full)
        # save the limited range image if it doesn't already exist
        if not os.path.exists('test_images/speedracer_limited_range.png'):
            cv2.imwrite('test_images/speedracer_limited_range.png', image_lim)

        # Make a limited version of the reference image in jpg
        # JPEG is a lossy compression format. During the compression process, it approximates the
        # content of images which can result in slight changes to pixel values. This can push values
        # just outside the intended 16 to 235 range.
        # The best results are obtained by loading speedracer_limited_range.png and saving it as a jpg
        # with compression set to 100 using Apple Preview.

    def test_limited_to_full(self):
        """test limited to full conversion"""
        # test jpg and png versions of the same image
        for ext in ['png', 'jpg']:
            # load limited range image
            limited = cv2.imread(f'test_images/speedracer_limited_range.{ext}')

            # load full range image
            full = cv2.imread(f'test_images/speedracer_full_range.{ext}')

            # convert limited to full range
            converted = limited_to_full(limited)

            # find absolute difference between the full range image and the converted image
            diff = np.abs(full.astype(np.int64) - converted.astype(np.int64))

            if ext == 'png':
                # allow for rounding error +/- 1 RGB value
                self.assertLessEqual(diff.max(), 1)
                self.assertLessEqual(diff.mean(), 0.026)
            elif ext == 'jpg':
                # allow for jpg lossy compression error +/- 6 RGB values
                self.assertLessEqual(diff.max(), 6)
                self.assertLessEqual(diff.mean(), 0.123)

    def test_full_to_limited(self):
        """test full to limited conversion"""
        # test jpg and png versions of the same image
        for ext in ['png', 'jpg']:
            # load full range image
            full = cv2.imread(f'test_images/speedracer_full_range.{ext}')

            # load limited range image
            limited = cv2.imread(f'test_images/speedracer_limited_range.{ext}')

            # convert full to limited range
            converted = full_to_limited(full)

            # find absolute difference between the limited range image and the converted image
            diff = np.abs(limited.astype(np.int64) - converted.astype(np.int64))

            if ext == 'png':
                # allow for rounding error +/- 1 RGB value
                self.assertLessEqual(diff.max(), 0)
                self.assertLessEqual(diff.mean(), 0.0)
            elif ext == 'jpg':
                # allow for jpg lossy compression error +/- 6 RGB values
                self.assertLessEqual(diff.max(), 5)
                self.assertLessEqual(diff.mean(), 0.1)


if __name__ == '__main__':
    unittest.main()
