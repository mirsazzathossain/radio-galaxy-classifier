from unittest.mock import MagicMock, patch

from rgc.utils.data import celestial_capture


@patch("rgc.utils.data.SkyView")
@patch("rgc.utils.data.Path")
def test_celestial_capture(mock_path, mock_skyview):
    # Mock SkyView.get_images method
    mock_image = MagicMock()
    mock_image[0].header = MagicMock()
    mock_image[0].header.__getitem__.return_value = "Sample comment"
    mock_image[0].header.remove = MagicMock()
    mock_image[0].header.add_comment = MagicMock()
    mock_image.writeto = MagicMock()
    mock_skyview.get_images.return_value = [mock_image]

    # Mock Path functionality
    mock_path_instance = MagicMock()
    mock_path_instance.parent = "mock_folder"
    mock_path.return_value = mock_path_instance

    # Call the function
    celestial_capture("DSS2 Red", 10.684, 41.269, "test_image.fits")

    # Verify that SkyView.get_images was called with correct parameters
    mock_skyview.get_images.assert_called_once_with(
        position="10.684, 41.269", survey="DSS2 Red", coordinates="J2000", pixels=(150, 150)
    )

    # Verify that image.writeto was called with correct filename
    mock_image.writeto.assert_called_once_with("test_image.fits", overwrite=True)

    # Verify Path.mkdir was called to create directories
    mock_path_instance.mkdir.assert_called_once_with(parents=True, exist_ok=True)

    # Verify header methods were called
    mock_image[0].header.remove.assert_called_once_with("comment", "Sample comment", True)
    mock_image[0].header.add_comment.assert_called_once_with("Sample comment")
