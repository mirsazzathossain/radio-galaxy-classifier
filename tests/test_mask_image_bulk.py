import os
import shutil
import tempfile
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

from rgc.utils.data import _FileNotFoundError, _ImageMaskCountMismatchError, mask_image_bulk


class TestMaskImageBulk(unittest.TestCase):
    def setUp(self):
        # Create temporary directories for images, masks, and masked images
        self.image_dir = tempfile.mkdtemp()
        self.mask_dir = tempfile.mkdtemp()
        self.masked_dir = tempfile.mkdtemp()

        # Create sample images and masks
        self.image_array = np.array([[100, 150, 200], [50, 75, 100], [0, 25, 50]], dtype=np.uint8)
        self.mask_array = np.array([[1, 0, 1], [0, 1, 0], [1, 1, 0]], dtype=np.uint8)

        # Save sample images and masks
        self.image_path = Path(self.image_dir) / "test_image.png"
        self.mask_path = Path(self.mask_dir) / "test_image.png"  # Ensure the same name

        Image.fromarray(self.image_array, mode="L").save(self.image_path)
        Image.fromarray(self.mask_array, mode="L").save(self.mask_path)

    def tearDown(self):
        # Remove temporary directories
        shutil.rmtree(self.image_dir)
        shutil.rmtree(self.mask_dir)
        shutil.rmtree(self.masked_dir)

    def test_mask_image_bulk(self):
        # Run the bulk masking function
        mask_image_bulk(self.image_dir, self.mask_dir, self.masked_dir)

        # Check if the masked image is created
        masked_file_path = Path(self.masked_dir) / "test_image.png"
        self.assertTrue(masked_file_path.exists(), "Masked image file not created")

        # Load the masked image and verify its content
        masked_image = Image.open(masked_file_path)
        masked_array = np.array(masked_image)

        # Expected result after masking
        expected_array = np.array([[100, 0, 200], [0, 75, 0], [0, 25, 0]], dtype=np.uint8)
        np.testing.assert_array_equal(masked_array, expected_array, "Masked image content is incorrect")

    def test_empty_image_dir(self):
        # Test with an empty image directory
        empty_image_dir = tempfile.mkdtemp()
        with self.assertRaises(_FileNotFoundError):
            mask_image_bulk(empty_image_dir, self.mask_dir, self.masked_dir)
        shutil.rmtree(empty_image_dir)

    def test_empty_mask_dir(self):
        # Test with an empty mask directory
        empty_mask_dir = tempfile.mkdtemp()
        with self.assertRaises(_FileNotFoundError):
            mask_image_bulk(self.image_dir, empty_mask_dir, self.masked_dir)
        shutil.rmtree(empty_mask_dir)

    def test_non_matching_images_and_masks(self):
        # Create a directory with different image and mask counts
        extra_image_dir = tempfile.mkdtemp()
        extra_mask_dir = tempfile.mkdtemp()

        # Create an extra image
        extra_image_path = Path(extra_image_dir) / "extra_image.png"
        Image.fromarray(self.image_array, mode="L").save(extra_image_path)

        # Create another extra image
        extra_image_path = Path(extra_image_dir) / "extra_image_2.png"
        Image.fromarray(self.image_array, mode="L").save(extra_image_path)

        # Run the function and check if the mismatch error is raised
        with self.assertRaises(_ImageMaskCountMismatchError):
            mask_image_bulk(extra_image_dir, self.mask_dir, self.masked_dir)

        # Create an extra mask
        extra_mask_path = Path(extra_mask_dir) / "extra_mask.png"
        Image.fromarray(self.mask_array, mode="L").save(extra_mask_path)

        # Check that masked directory is still empty
        self.assertFalse(
            os.listdir(self.masked_dir), "Masked directory should be empty if image-mask count does not match"
        )

        shutil.rmtree(extra_image_dir)
        shutil.rmtree(extra_mask_dir)


if __name__ == "__main__":
    unittest.main()
