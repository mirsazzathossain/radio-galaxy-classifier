import pandas as pd
import pytest

from rgc.utils.data import _ColumnNotFoundError, _get_class_labels


def test_get_class_labels():
    # Sample data
    catalog = pd.Series({"object_name": "Object1", "class_col": "Galaxy"})
    classes = {"Galaxy": "Galactic", "Star": "Stellar"}

    # Test with valid column and key
    result = _get_class_labels(catalog, classes, "class_col")
    assert result == "Galactic", "Should return 'Galactic' for 'Galaxy'"

    # Test with invalid column
    with pytest.raises(_ColumnNotFoundError):
        _get_class_labels(catalog, classes, "invalid_col")

    # Test with no matching key
    result = _get_class_labels(catalog, classes, "object_name")
    assert result == "", "Should return '' if no matching key is found"
