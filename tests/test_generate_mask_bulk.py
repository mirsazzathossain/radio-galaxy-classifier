import unittest
from unittest.mock import call, patch

import pandas as pd

from rgc.utils.data import generate_mask_bulk


class TestGenerateMaskBulk(unittest.TestCase):
    @patch("rgc.utils.data.generate_mask")
    @patch("rgc.utils.data.os.path.join", return_value="mock_image_path.fits")
    @patch("rgc.utils.data.print")  # Mock print to suppress output during the test
    def test_generate_mask_bulk_success(self, mock_print, mock_join, mock_generate_mask):
        # Create a mock catalog DataFrame
        data = {
            "filename": ["image1", "image2"],
            "dilation": [2, 3],
            "background sigma": [5.0, 6.0],
            "foreground sigma": [3.0, 4.0],
        }
        catalog = pd.DataFrame(data)

        # Test parameters
        img_dir = "mock/img/dir"
        mask_dir = "mock/mask/dir"
        freq = 1400.0
        beam = (5.0, 5.0, 5.0)

        # Run the function
        generate_mask_bulk(
            catalog=catalog,
            img_dir=img_dir,
            mask_dir=mask_dir,
            freq=freq,
            beam=beam,
        )

        # Check that os.path.join was called with the correct parameters
        expected_calls = [call(img_dir, "image1.fits"), call(img_dir, "image2.fits")]
        mock_join.assert_has_calls(expected_calls, any_order=False)

        # Check that generate_mask was called twice with the correct parameters
        expected_mask_calls = [
            call(
                "mock_image_path.fits",
                mask_dir,
                freq,
                beam,
                2,  # dilation for image1
                5.0,  # background sigma for image1
                3.0,  # foreground sigma for image1
            ),
            call(
                "mock_image_path.fits",
                mask_dir,
                freq,
                beam,
                3,  # dilation for image2
                6.0,  # background sigma for image2
                4.0,  # foreground sigma for image2
            ),
        ]
        mock_generate_mask.assert_has_calls(expected_mask_calls, any_order=False)

        # Ensure no errors were printed
        mock_print.assert_not_called()

    @patch("rgc.utils.data.generate_mask", side_effect=Exception("Mocked error"))
    @patch("rgc.utils.data.os.path.join", return_value="mock_image_path.fits")
    @patch("rgc.utils.data.print")
    def test_generate_mask_bulk_failure(self, mock_print, mock_join, mock_generate_mask):
        # Create a mock catalog DataFrame
        data = {
            "filename": ["image1"],
            "dilation": [2],
            "background sigma": [5.0],
            "foreground sigma": [3.0],
        }
        catalog = pd.DataFrame(data)

        # Test parameters
        img_dir = "mock/img/dir"
        mask_dir = "mock/mask/dir"
        freq = 1400.0
        beam = (5.0, 5.0, 5.0)

        # Run the function
        generate_mask_bulk(
            catalog=catalog,
            img_dir=img_dir,
            mask_dir=mask_dir,
            freq=freq,
            beam=beam,
        )

        # Verify that the error message was printed
        mock_print.assert_called_once_with("Failed to generate mask. Mocked error")

        # Check that generate_mask was called once before the exception
        mock_generate_mask.assert_called_once()


if __name__ == "__main__":
    unittest.main()
