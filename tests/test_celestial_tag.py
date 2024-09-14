import unittest

import pandas as pd
import pytest

from rgc.utils.data import _NoValidCelestialCoordinatesError, celestial_tag


class TestCelestialTag:
    def test_celestial_tag_ra_dec_format(self):
        # Test with RA and DEC in degrees, minutes, seconds format
        data = pd.DataFrame([{"RA": "00 01 15.11", "DEC": "-08 26 46.2"}])
        tag = celestial_tag(data.iloc[0])
        assert tag == "00 01 15.11-08 26 46.2"

    def test_celestial_tag_ra_dec_format_negative_dec(self):
        # Test with RA and DEC in degrees, minutes, seconds format with negative DEC
        data = pd.DataFrame([{"RA": "00 01 15.11", "DEC": "-08 26 46.2"}])
        tag = celestial_tag(data.iloc[0])
        assert tag == "00 01 15.11-08 26 46.2"

    def test_celestial_tag_ra_dec_format_without_sign(self):
        # Test with RA and DEC in degrees, minutes, seconds format where DEC is positive but no explicit sign
        data = pd.DataFrame([{"RA": "00 01 15.11", "DEC": "08 26 46.2"}])
        tag = celestial_tag(data.iloc[0])
        assert tag == "00 01 15.11+08 26 46.2"

    def test_celestial_tag_ra_j2000_format(self):
        # Test with RAJ2000 and DEJ2000 format
        data = pd.DataFrame([{"RAJ2000": "00 01 15.11", "DEJ2000": "-08 26 46.2"}])
        tag = celestial_tag(data.iloc[0])
        assert tag == "00 01 15.11-08 26 46.2"

    def test_celestial_tag_filename_format(self):
        # Test with filename format
        data = pd.DataFrame([{"filename": "object123.fits"}])
        tag = celestial_tag(data.iloc[0])
        assert tag == "object123.fits"

    def test_celestial_tag_fcg_format(self):
        # Test with FCG format
        data = pd.DataFrame([{"FCG": "object456"}])
        tag = celestial_tag(data.iloc[0])
        assert tag == "object456"

    def test_celestial_tag_missing_coordinates(self):
        # Test with missing coordinates
        data = pd.DataFrame([{}])
        with pytest.raises(_NoValidCelestialCoordinatesError):
            celestial_tag(data.iloc[0])


if __name__ == "__main__":
    unittest.main()
