from unittest.mock import MagicMock, patch

import pandas as pd

from rgc.utils.data import celestial_capture_bulk


@patch("rgc.utils.data.celestial_tag")
@patch("rgc.utils.data.SkyCoord")
@patch("rgc.utils.data.celestial_capture")
def test_celestial_capture_bulk(mock_celestial_capture, mock_SkyCoord, mock_celestial_tag):
    # Mock data
    mock_celestial_tag.return_value = "10h00m00s +10d00m00s"
    mock_SkyCoord.return_value = MagicMock(ra=MagicMock(deg=10), dec=MagicMock(deg=20))

    catalog = pd.DataFrame({"label": ["WAT"], "object_name": ["test"]})
    classes = {"WAT": 100, "NAT": 200}
    img_dir = "/path/to/images"

    # Run the function
    celestial_capture_bulk(catalog, "VLA FIRST (1.4 GHz)", img_dir, classes, "label")

    # Check that celestial_capture was called with the expected arguments
    mock_celestial_capture.assert_called_once_with(
        "VLA FIRST (1.4 GHz)", 10, 20, "/path/to/images/100_10h00m00s +10d00m00s.fits"
    )

    # Test failure handling
    mock_celestial_capture.reset_mock()
    mock_celestial_tag.side_effect = Exception("Test exception")

    with patch("builtins.print") as mock_print:
        celestial_capture_bulk(catalog, "VLA FIRST (1.4 GHz)", img_dir, classes, "object_name")
        mock_print.assert_called_once_with("Failed to capture image. Test exception")


@patch("rgc.utils.data.celestial_tag")
@patch("rgc.utils.data.SkyCoord")
@patch("rgc.utils.data.celestial_capture")
def test_celestial_capture_bulk_with_filename(mock_celestial_capture, mock_SkyCoord, mock_celestial_tag):
    # Mock data
    mock_celestial_tag.return_value = "10h00m00s +10d00m00s"
    mock_SkyCoord.return_value = MagicMock(ra=MagicMock(deg=10), dec=MagicMock(deg=20))

    # Catalog with filename column
    catalog = pd.DataFrame({"label": ["WAT"], "filename": ["image1"], "object_name": ["test"]})
    classes = {"WAT": 100, "NAT": 200}
    img_dir = "/path/to/images"

    # Run the function
    celestial_capture_bulk(catalog, "VLA FIRST (1.4 GHz)", img_dir, classes, "label")

    # Check that celestial_capture was called with the expected filename
    mock_celestial_capture.assert_called_once_with("VLA FIRST (1.4 GHz)", 10, 20, "/path/to/images/100_image1.fits")
