import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from rgc.utils.data import fits_to_png_bulk


class TestFitsToPngBulk(unittest.TestCase):
    @patch("rgc.utils.data.fits_to_png")
    @patch("rgc.utils.data.Path.rglob")
    @patch("rgc.utils.data.Path.mkdir")
    @patch("rgc.utils.data.os.path.join")
    def test_fits_to_png_bulk(self, mock_join, mock_mkdir, mock_rglob, mock_fits_to_png):
        # Mock rglob to return a list of fake FITS files
        mock_fits_files = [Path(f"file{i}.fits") for i in range(3)]
        mock_rglob.return_value = mock_fits_files

        # Mock the PNG file path join
        mock_join.side_effect = lambda png_dir, file_stem: f"{png_dir}/{file_stem}.png"

        # Mock the image returned by fits_to_png
        mock_image = MagicMock()
        mock_fits_to_png.return_value = mock_image

        # Call the function
        fits_to_png_bulk("fits_dir", "png_dir", img_size=(100, 100))

        # Assertions
        mock_rglob.assert_called_once_with("*.fits")
        mock_mkdir.assert_called()
        self.assertEqual(mock_fits_to_png.call_count, 3)
        self.assertEqual(mock_image.save.call_count, 3)

        # Verify the image save calls
        mock_image.save.assert_any_call("png_dir/file0.png")
        mock_image.save.assert_any_call("png_dir/file1.png")
        mock_image.save.assert_any_call("png_dir/file2.png")


if __name__ == "__main__":
    unittest.main()
