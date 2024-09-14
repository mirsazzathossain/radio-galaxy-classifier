import unittest

import numpy as np
from PIL import Image

from rgc.utils.data import _ImageMaskDimensionError, mask_image


class TestMaskImage(unittest.TestCase):
    def setUp(self):
        # Create sample images and masks for testing
        self.image_array = np.array([[100, 150, 200], [50, 75, 100], [0, 25, 50]], dtype=np.uint8)
        self.mask_array = np.array([[1, 0, 1], [0, 1, 0], [1, 1, 0]], dtype=np.uint8)
        self.image = Image.fromarray(self.image_array, mode="L")
        self.mask = Image.fromarray(self.mask_array, mode="L")

    def test_mask_all_zeros(self):
        zero_mask_array = np.zeros_like(self.mask_array)
        zero_mask = Image.fromarray(zero_mask_array, mode="L")

        expected_array = np.zeros_like(self.image_array)
        _ = Image.fromarray(expected_array, mode="L")

        result_image = mask_image(self.image, zero_mask)
        result_array = np.array(result_image)

        np.testing.assert_array_equal(result_array, expected_array)

    def test_mask_all_ones(self):
        ones_mask_array = np.ones_like(self.mask_array)
        ones_mask = Image.fromarray(ones_mask_array, mode="L")

        expected_array = self.image_array.copy()
        _ = Image.fromarray(expected_array, mode="L")

        result_image = mask_image(self.image, ones_mask)
        result_array = np.array(result_image)

        np.testing.assert_array_equal(result_array, expected_array)

    def test_non_matching_dimension(self):
        small_mask_array = np.array([[1, 0]], dtype=np.uint8)
        small_mask = Image.fromarray(small_mask_array, mode="L")

        with self.assertRaises(_ImageMaskDimensionError):
            mask_image(self.image, small_mask)

    def test_empty_image(self):
        empty_image_array = np.array([[]], dtype=np.uint8)
        empty_image = Image.fromarray(empty_image_array, mode="L")

        with self.assertRaises(_ImageMaskDimensionError):
            mask_image(empty_image, self.mask)

    def test_empty_mask(self):
        empty_mask_array = np.array([[]], dtype=np.uint8)
        empty_mask = Image.fromarray(empty_mask_array, mode="L")

        with self.assertRaises(_ImageMaskDimensionError):
            mask_image(self.image, empty_mask)


if __name__ == "__main__":
    unittest.main()
