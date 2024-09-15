from unittest.mock import patch

import pandas as pd

from rgc.utils.data import dataframe_to_html


@patch("rgc.utils.data.Path.mkdir")
@patch("rgc.utils.data.pd.DataFrame.to_html")
@patch("rgc.utils.data.os.path.join", return_value="/mocked/path/catalog.html")
def test_dataframe_to_html(mock_join, mock_to_html, mock_mkdir):
    # Sample catalog
    catalog = pd.DataFrame({"object_name": ["Object1", "Object2"], "ra": [10.5, 20.3], "dec": [-30.1, 45.2]})

    save_dir = "/mocked/directory"

    # Run the function
    dataframe_to_html(catalog, save_dir)

    # Check that the directory was created
    mock_mkdir.assert_called_once_with(parents=True, exist_ok=True)

    # Check that the catalog was saved as HTML
    mock_to_html.assert_called_once_with("/mocked/path/catalog.html")

    # Check that os.path.join was called with the correct parameters
    mock_join.assert_called_once_with(save_dir, "catalog.html")
