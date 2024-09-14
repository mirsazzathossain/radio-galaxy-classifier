import unittest
from unittest.mock import MagicMock, patch

import numpy as np

from rgc.utils.data import _FileNotFoundError, fits_to_png


class TestFitsToPng(unittest.TestCase):
    @patch("rgc.utils.data.fits.getdata")
    @patch("rgc.utils.data.fits.getheader")
    @patch("rgc.utils.data.Image.fromarray")
    def test_fits_to_png_success(self, mock_fromarray, mock_getheader, mock_getdata):
        # Mock FITS data and header
        mock_getdata.return_value = np.array([[1, 2], [3, 4]], dtype=np.float32)
        mock_getheader.return_value = {"NAXIS1": 2, "NAXIS2": 2}

        # Mock PIL Image object
        mock_image = MagicMock()
        mock_fromarray.return_value = mock_image

        # Call function
        result = fits_to_png("mock.fits")

        # Extract the array passed to fromarray and check equality
        args, kwargs = mock_fromarray.call_args
        np.testing.assert_array_equal(args[0], np.array([[0, 85], [170, 255]], dtype=np.uint8))
        self.assertEqual(kwargs.get("mode"), "L")
        self.assertEqual(result, mock_image)

    @patch("rgc.utils.data.fits.getdata")
    @patch("rgc.utils.data.fits.getheader")
    @patch("rgc.utils.data.Image.fromarray")
    def test_fits_to_png_with_img_size(self, mock_fromarray, mock_getheader, mock_getdata):
        # Mock FITS data and header
        mock_getdata.return_value = np.array([1, 2, 3, 4], dtype=np.float32)
        mock_getheader.return_value = {"NAXIS1": 2, "NAXIS2": 2}

        # Mock PIL Image object
        mock_image = MagicMock()
        mock_fromarray.return_value = mock_image

        # Call function with specific image size
        _ = fits_to_png("mock.fits", img_size=(4, 1))

        # Extract the array passed to fromarray and check equality
        expected_image = np.array([0, 85, 170, 255], dtype=np.uint8).reshape((4, 1))
        args, kwargs = mock_fromarray.call_args
        np.testing.assert_array_equal(args[0].T, expected_image)
        self.assertEqual(kwargs.get("mode"), "L")

    @patch("rgc.utils.data.fits.getdata")
    @patch("rgc.utils.data.fits.getheader")
    def test_fits_to_png_file_not_found(self, mock_getheader, mock_getdata):
        # Mock FileNotFoundError
        mock_getdata.side_effect = FileNotFoundError

        # Test FileNotFoundError
        with self.assertRaises(_FileNotFoundError):
            fits_to_png("mock.fits")


if __name__ == "__main__":
    unittest.main()
