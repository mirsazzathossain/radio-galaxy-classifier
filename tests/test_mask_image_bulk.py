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
        self.image_dir = tempfile.mkdtemp()
        self.mask_dir = tempfile.mkdtemp()
        self.masked_dir = tempfile.mkdtemp()

        self.image_array = np.array([[100, 150, 200], [50, 75, 100], [0, 25, 50]], dtype=np.uint8)
        self.mask_array = np.array([[1, 0, 1], [0, 1, 0], [1, 1, 0]], dtype=np.uint8)

        self.image_path = Path(self.image_dir) / "test_image.png"
        self.mask_path = Path(self.mask_dir) / "test_image.png"

        Image.fromarray(self.image_array, mode="L").save(self.image_path)
        Image.fromarray(self.mask_array, mode="L").save(self.mask_path)

    def tearDown(self):
        shutil.rmtree(self.image_dir)
        shutil.rmtree(self.mask_dir)
        shutil.rmtree(self.masked_dir)

    def test_mask_image_bulk(self):
        mask_image_bulk(self.image_dir, self.mask_dir, self.masked_dir)

        masked_file_path = Path(self.masked_dir) / "test_image.png"
        self.assertTrue(masked_file_path.exists())

        masked_image = Image.open(masked_file_path)
        masked_array = np.array(masked_image)

        expected_array = np.array([[100, 0, 200], [0, 75, 0], [0, 25, 0]], dtype=np.uint8)
        np.testing.assert_array_equal(masked_array, expected_array)

    def test_missing_mask_file(self):
        # Create a directory with an image but without a corresponding mask
        missing_mask_dir = tempfile.mkdtemp()
        Image.fromarray(self.image_array, mode="L").save(Path(missing_mask_dir) / "fake_image.png")

        mask_image_bulk(self.image_dir, missing_mask_dir, self.masked_dir)

        # Check that masked directory is still empty
        self.assertFalse(os.listdir(self.masked_dir), "Masked directory should be empty if mask file is missing")

        shutil.rmtree(missing_mask_dir)

    def test_dimension_mismatch(self):
        # Ensure mask_dir is empty
        for mask_file in Path(self.mask_dir).glob("*.png"):
            os.remove(mask_file)

        # Create a mask with a different dimension
        mismatch_mask_array = np.array([[1, 0]], dtype=np.uint8)
        mismatch_mask_path = Path(self.mask_dir) / "mismatch_mask.png"
        Image.fromarray(mismatch_mask_array, mode="L").save(mismatch_mask_path)

        # Ensure image_dir contains only the test image
        for image_file in Path(self.image_dir).glob("*.png"):
            os.remove(image_file)

        Image.fromarray(self.image_array, mode="L").save(Path(self.image_dir) / "test_image.png")

        # Ensure directories are ready for testing
        self.assertEqual(len(list(Path(self.image_dir).glob("*.png"))), 1)
        self.assertEqual(len(list(Path(self.mask_dir).glob("*.png"))), 1)

        # Run the function and check if the dimension mismatch error is handled
        mask_image_bulk(self.image_dir, self.mask_dir, self.masked_dir)

        # Check if masked directory is still empty since the mask has a dimension mismatch
        self.assertFalse(
            list(Path(self.masked_dir).glob("*.png")),
            "Masked directory should be empty if there is a dimension mismatch",
        )

    def test_empty_image_dir(self):
        empty_image_dir = tempfile.mkdtemp()
        with self.assertRaises(_FileNotFoundError):
            mask_image_bulk(empty_image_dir, self.mask_dir, self.masked_dir)
        shutil.rmtree(empty_image_dir)

    def test_empty_mask_dir(self):
        empty_mask_dir = tempfile.mkdtemp()
        with self.assertRaises(_FileNotFoundError):
            mask_image_bulk(self.image_dir, empty_mask_dir, self.masked_dir)
        shutil.rmtree(empty_mask_dir)

    def test_non_matching_images_and_masks(self):
        extra_image_dir = tempfile.mkdtemp()
        extra_mask_dir = tempfile.mkdtemp()

        extra_image_path = Path(extra_image_dir) / "extra_image.png"
        Image.fromarray(self.image_array, mode="L").save(extra_image_path)

        extra_image_path = Path(extra_image_dir) / "extra_image_2.png"
        Image.fromarray(self.image_array, mode="L").save(extra_image_path)

        with self.assertRaises(_ImageMaskCountMismatchError):
            mask_image_bulk(extra_image_dir, self.mask_dir, self.masked_dir)

        extra_mask_path = Path(extra_mask_dir) / "extra_mask.png"
        Image.fromarray(self.mask_array, mode="L").save(extra_mask_path)

        self.assertFalse(os.listdir(self.masked_dir))

        shutil.rmtree(extra_image_dir)
        shutil.rmtree(extra_mask_dir)


if __name__ == "__main__":
    unittest.main()
