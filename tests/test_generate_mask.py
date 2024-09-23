import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

from rgc.utils.data import generate_mask


class TestGenerateMask(unittest.TestCase):
    @patch("rgc.utils.data.bdsf.process_image", return_value=MagicMock())
    @patch("rgc.utils.data.Path.mkdir")
    @patch("rgc.utils.data.Path.name", new_callable=MagicMock(return_value="image.fits"))
    @patch("rgc.utils.data.Path", autospec=True)
    @patch("rgc.utils.data.print")
    def test_generate_mask_success(self, mock_print, mock_path, mock_name, mock_mkdir, mock_process_image):
        # Setup mocks
        mock_path_instance = mock_path.return_value
        # Ensure that the truediv operator returns the correct Path
        mock_path_instance.__truediv__.return_value = Path("path/to/mask_dir/image.fits")
        mock_path_instance.parent.mkdir.return_value = None
        mock_path_instance.name = "image.fits"  # Correct the name attribute

        # Setup test parameters
        image_path = "path/to/image.fits"
        mask_dir = "path/to/mask_dir"
        freq = 1400.0
        beam = (5.0, 5.0, 5.0)
        dilation = 2
        threshold_pixel = 5.0
        threshold_island = 3.0

        # Run the function
        generate_mask(
            image_path=image_path,
            mask_dir=mask_dir,
            freq=freq,
            beam=beam,
            dilation=dilation,
            threshold_pixel=threshold_pixel,
            threshold_island=threshold_island,
        )

        # Verify that print was not called
        mock_print.assert_not_called()

        # Verify that the mask file path was generated correctly
        expected_mask_file = Path(mask_dir) / "image.fits"
        mock_path_instance.__truediv__.assert_called_once_with("image.fits")

        # Verify that the parent directory was created
        mock_path_instance.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)

        # Verify that process_image was called correctly
        mock_process_image.assert_called_once_with(
            image_path, beam=beam, thresh_isl=threshold_island, thresh_pix=threshold_pixel, frequency=freq
        )

        # Verify that export_image is called on the mock returned by process_image
        mock_process_image.return_value.export_image.assert_called_once_with(
            img_type="island_mask",
            outfile=expected_mask_file,
            clobber=True,
            mask_dilation=dilation,
        )

    @patch("rgc.utils.data.bdsf.process_image", return_value=MagicMock())
    @patch("rgc.utils.data.Path.mkdir", side_effect=PermissionError("Permission denied"))
    @patch("rgc.utils.data.Path.parent", new_callable=MagicMock)
    @patch("rgc.utils.data.Path.name", new_callable=MagicMock(return_value="image.fits"))
    @patch("rgc.utils.data.Path", autospec=True)
    @patch("rgc.utils.data.print")
    def test_generate_mask_permission_error(
        self, mock_print, mock_path, mock_name, mock_parent, mock_mkdir, mock_process_image
    ):
        # Setup mocks
        mock_path.return_value = Path("/mock/path")
        mock_parent.return_value = mock_path
        mock_process_image.return_value = MagicMock()

        # Setup test parameters
        image_path = "path/to/image.fits"
        mask_dir = "path/to/mask_dir"
        freq = 1400.0
        beam = (5.0, 5.0, 5.0)
        dilation = 2
        threshold_pixel = 5.0
        threshold_island = 3.0

        # Run the function
        generate_mask(
            image_path=image_path,
            mask_dir=mask_dir,
            freq=freq,
            beam=beam,
            dilation=dilation,
            threshold_pixel=threshold_pixel,
            threshold_island=threshold_island,
        )

        # Verify that print was called with the correct error message
        mock_print.assert_called_once_with("Failed to generate mask.")

    @patch("rgc.utils.data.bdsf.process_image", side_effect=Exception("Process failed"))
    @patch("rgc.utils.data.print")
    def test_generate_mask_failure(self, mock_print, mock_process_image):
        # Setup test parameters
        image_path = "path/to/image.fits"
        mask_dir = "path/to/mask_dir"
        freq = 1400.0
        beam = (5.0, 5.0, 5.0)
        dilation = 2
        threshold_pixel = 5.0
        threshold_island = 3.0

        # Run the function
        generate_mask(
            image_path=image_path,
            mask_dir=mask_dir,
            freq=freq,
            beam=beam,
            dilation=dilation,
            threshold_pixel=threshold_pixel,
            threshold_island=threshold_island,
        )

        # Verify that print was called with the correct error message
        mock_print.assert_called_once_with("Failed to generate mask.")
