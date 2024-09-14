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
    An exception to be raised when a file is not found.
    """

    def __init__(self, message: str = "File not found.") -> None:
        super().__init__(message)


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


def mask_image(image: Image.Image, mask: Image.Image) -> Image.Image:
    """
    Mask an image with a given mask image.

    :param image: The image to be masked.
    :type image: Image.Image

    :param mask: The mask image.
    :type mask: Image.Image

    :return: A PIL Image object containing the masked image.
    :rtype: Image.Image
    """
    image_array = np.array(image)
    mask_array = np.array(mask)

    if image_array.shape != mask_array.shape:
        raise _ImageMaskDimensionError()

    masked_array = np.where(mask_array == 0, 0, image_array)
    masked_image = Image.fromarray(masked_array, mode="L")

    return cast(Image.Image, masked_image)


class _ImageMaskDimensionError(Exception):
    """
    An exception to be raised when the dimensions of the image and mask do not match.
    """

    def __init__(self) -> None:
        super().__init__("Image and mask must have the same dimensions.")


class _ImageMaskCountMismatchError(Exception):
    """
    An exception to be raised when the number of images and masks do not match.
    """

    def __init__(self, message: str = "Number of images and masks must match and be non-zero.") -> None:
        super().__init__(message)


def mask_image_bulk(image_dir: str, mask_dir: str, masked_dir: str) -> None:
    image_paths = sorted(Path(image_dir).glob("*.png"))
    mask_paths = sorted(Path(mask_dir).glob("*.png"))

    if len(image_paths) == 0 or len(mask_paths) == 0:
        raise _FileNotFoundError()

    if len(image_paths) != len(mask_paths):
        raise _ImageMaskCountMismatchError()

    os.makedirs(masked_dir, exist_ok=True)

    for image_path in image_paths:
        mask_path = Path(mask_dir) / image_path.name

        if not mask_path.exists():
            print(f"Skipping {image_path.name} due to missing mask.")
            continue

        image = Image.open(image_path)
        mask = Image.open(mask_path)

        try:
            masked_image = mask_image(image, mask)
        except _ImageMaskDimensionError:
            print(f"Skipping {image_path.name} due to dimension mismatch.")
            continue

        masked_image.save(Path(masked_dir) / image_path.name)
