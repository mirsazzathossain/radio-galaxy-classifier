"""
A collection of utility functions for data manipulation.

This module contains a collection of utility functions for astronomical data
manipulation.
"""

__author__ = "Mir Sazzat Hossain"


import os
from pathlib import Path
from typing import Optional, cast

import numpy as np
import pandas as pd
from astropy.io import fits
from astroquery.skyview import SkyView
from astroquery.vizier import Vizier
from PIL import Image


def catalog_quest(name: str, service: str = "Vizier") -> pd.DataFrame:
    """
    Fetch a catalog from a given astronomical service e.g. VizieR, Simbad.

    :param name: The name of the catalog to be fetched.
    :type name: str

    :param service: The name of the astronomical service to be used.
    :type service: str

    :return: A pandas DataFrame containing the fetched catalog.
    :rtype: pd.DataFrame

    :raises _UnsupportedServiceError: If an unsupported service is provided.
    """
    if service == "Vizier":
        Vizier.ROW_LIMIT = -1
        catalog = Vizier.get_catalogs(name)
        return cast(pd.DataFrame, catalog[0].to_pandas())
    else:
        raise _UnsupportedServiceError()


class _UnsupportedServiceError(Exception):
    """
    An exception to be raised when an unsupported service is provided.
    """

    def __init__(self) -> None:
        super().__init__("Unsupported service provided. Only 'Vizier' is supported.")


def celestial_capture(survey: str, ra: float, dec: float, filename: str) -> None:
    """
    Capture a celestial image using the SkyView service.

    :param survey: The name of the survey to be used e.g. 'VLA FIRST (1.4 GHz)'.
    :type survey: str

    :param ra: The right ascension of the celestial object.
    :type ra: Skycoord

    :param dec: The declination of the celestial object.
    :type dec: Skycoord

    :param filename: The name of the file to save the image.
    :type filename: str
    """
    image = SkyView.get_images(position=f"{ra}, {dec}", survey=survey, coordinates="J2000", pixels=(150, 150))[0]

    comment = str(image[0].header["COMMENT"])
    comment = comment.replace("\n", " ")
    comment = comment.replace("\t", " ")

    image[0].header.remove("comment", comment, True)
    image[0].header.add_comment(comment)

    folder_path = Path(filename).parent
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    image.writeto(filename, overwrite=True)


def celestial_tag(entry: pd.Series) -> str:
    """
    Generate a name tag for a celestial object based on its coordinates.

    :param entry: A pandas Series entry of the catalog.
    :type entry: pd.Series

    :return: A string containing the name tag.
    :rtype: str

    :raises _NoValidCelestialCoordinatesError: If no valid celestial coordinates are found in the entry.
    """

    def format_dec(dec: str) -> str:
        sign = "+" if float(dec.replace(" ", "")) > 0 else ""
        return f"{sign}{dec}"

    if {"RAJ2000", "DEJ2000"}.issubset(entry.index):
        ra, dec = entry["RAJ2000"], entry["DEJ2000"]
    elif {"RA", "DEC"}.issubset(entry.index):
        ra, dec = entry["RA"], entry["DEC"]
    elif "filename" in entry.index:
        return f"{entry['filename']}"
    elif "FCG" in entry.index:
        return f"{entry['FCG']}"
    else:
        raise _NoValidCelestialCoordinatesError()

    return f"{ra}{format_dec(dec)}"


class _NoValidCelestialCoordinatesError(Exception):
    """
    An exception to be raised when no valid celestial coordinates are found in the entry.
    """

    def __init__(self) -> None:
        super().__init__("No valid celestial coordinates found in the entry to generate a tag.")


class _FileNotFoundError(Exception):
    """
    An exception to be raised when the FITS file is not found.
    """

    def __init__(self, fits_file: str) -> None:
        super().__init__(f"File {fits_file} not found.")


def fits_to_png(fits_file: str, img_size: Optional[tuple[int, int]] = None) -> Image.Image:
    """
    Convert a FITS file to a PNG image.

    :param fits_file: The path to the FITS file.
    :type fits_file: str

    :param img_size: The size of the output image.
    :type img_size: Optional[tuple[int, int]]

    :return: A PIL Image object containing the PNG image.
    :rtype: Image.Image

    :raises _FileNotFoundError: If the FITS file is not found.
    """
    try:
        image = fits.getdata(fits_file)
        header = fits.getheader(fits_file)
    except FileNotFoundError as err:
        raise _FileNotFoundError(fits_file) from err

    if img_size is not None:
        width, height = img_size
    else:
        width, height = header["NAXIS1"], header["NAXIS2"]

    image = np.reshape(image, (height, width))
    image[np.isnan(image)] = np.nanmin(image)

    image = (image - np.nanmin(image)) / (np.nanmax(image) - np.nanmin(image)) * 255
    image = image.astype(np.uint8)
    image = Image.fromarray(image, mode="L")

    return cast(Image.Image, image)


def fits_to_png_bulk(fits_dir: str, png_dir: str, img_size: Optional[tuple[int, int]] = None) -> None:
    """
    Convert a directory of FITS files to PNG images.

    :param fits_dir: The path to the directory containing the FITS files.
    :type fits_dir: str

    :param png_dir: The path to the directory to save the PNG images.
    :type png_dir: str

    :param img_size: The size of the output image.
    :type img_size: Optional[tuple[int, int]]
    """
    fits_files = Path(fits_dir).rglob("*.fits")
    for fits_file in fits_files:
        image = fits_to_png(str(fits_file), img_size)

        png_file = os.path.join(png_dir, fits_file.stem)
        Path(png_file).parent.mkdir(parents=True, exist_ok=True)

        if image is not None:
            image.save(png_file)
