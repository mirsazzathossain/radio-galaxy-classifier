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
import torch
from astropy import units as u
from astropy.coordinates import SkyCoord
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

    :raises _ImageMaskDimensionError: If the dimensions of the image and mask do not match.
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
    """
    Mask a directory of images with a directory of mask images.

    :param image_dir: The path to the directory containing the images.
    :type image_dir: str

    :param mask_dir: The path to the directory containing the mask images.
    :type mask_dir: str

    :param masked_dir: The path to the directory to save the masked images.
    :type masked_dir: str

    :raises _FileNotFoundError: If no images or masks are found in the directories.
    :raises _ImageMaskCountMismatchError: If the number of images and masks do not match.
    """
    image_paths = sorted(Path(image_dir).glob("*.png"))
    mask_paths = sorted(Path(mask_dir).glob("*.png"))

    if len(image_paths) == 0 or len(mask_paths) == 0:
        raise _FileNotFoundError()

    if len(image_paths) != len(mask_paths):
        raise _ImageMaskCountMismatchError() from None

    os.makedirs(masked_dir, exist_ok=True)

    for image_path in image_paths:
        mask_path = Path(mask_dir) / image_path.name

        if not mask_path.exists():
            print(f"Skipping {image_path.name} due to missing mask.")
            continue

        image = Image.open(image_path)
        mask = Image.open(mask_path)

        if image.size != mask.size:
            print(f"Skipping {image_path.name} due to mismatched dimensions.")
            continue
        else:
            masked_image = mask_image(image, mask)

        masked_image.save(Path(masked_dir) / image_path.name)


class _ColumnNotFoundError(Exception):
    """
    An exception to be raised when a specified column is not found in the catalog.
    """

    def __init__(self, column: str) -> None:
        super().__init__(f"Column {column} not found in the catalog.")


def _get_class_labels(catalog: pd.Series, classes: dict, cls_col: str) -> str:
    """
    Get the class labels for the celestial objects in the catalog.

    :param catalog: A pandas Series representing a row in the catalog of celestial objects.
    :type catalog: pd.Series

    :param classes: A dictionary containing the classes of the celestial objects.
    :type classes: dict

    :param cls_col: The name of the column containing the class labels.
    :type cls_col: str

    :return: Class labels for the celestial objects in the catalog.
    :rtype: str

    :raises _ColumnNotFoundError: If the specified column is not found in the catalog.
    """
    if cls_col not in catalog.index:
        raise _ColumnNotFoundError(cls_col)

    value = catalog[cls_col]
    for key, label in classes.items():
        if key in value:
            return str(label)

    return ""


def celestial_capture_bulk(
    catalog: pd.DataFrame, survey: str, img_dir: str, classes: Optional[dict] = None, cls_col: Optional[str] = None
) -> None:
    """
    Capture celestial images for a catalog of celestial objects.

    :param catalog: A pandas DataFrame containing the catalog of celestial objects.
    :type catalog: pd.DataFrame

    :param survey: The name of the survey to be used e.g. 'VLA FIRST (1.4 GHz)'.
    :type survey: str

    :param img_dir: The path to the directory to save the images.
    :type img_dir: str

    :param classes: A dictionary containing the classes of the celestial objects.
    :type classes: dict

    :param cls_col: The name of the column containing the class labels.

    :raises _InvalidCoordinatesError: If coordinates are invalid.
    """
    failed = pd.DataFrame(columns=catalog.columns)
    for _, entry in catalog.iterrows():
        try:
            tag = celestial_tag(entry)
            coordinate = SkyCoord(tag, unit=(u.hourangle, u.deg))

            right_ascension = coordinate.ra.deg
            declination = coordinate.dec.deg

            label = _get_class_labels(entry, classes, cls_col) if classes is not None and cls_col is not None else ""

            if "filename" in catalog.columns:
                filename = f'{img_dir}/{label}_{entry["filename"]}.fits'
            else:
                filename = f"{img_dir}/{label}_{tag}.fits"

            celestial_capture(survey, right_ascension, declination, filename)
        except Exception as err:
            series = entry.to_frame().T
            failed = pd.concat([failed, series], ignore_index=True)
            print(f"Failed to capture image. {err}")


def dataframe_to_html(catalog: pd.DataFrame, save_dir: str) -> None:
    """
    Save the catalog as an HTML file.

    :param catalog: Catalog of the astronomical objects
    :type catalog: pd.DataFrame
    :param save_dir: Path to the directory to save the HTML file
    :type save_dir: str
    """
    Path(save_dir).mkdir(parents=True, exist_ok=True)
    catalog.to_html(os.path.join(save_dir, "catalog.html"))


def compute_mean_std(dataloader: torch.utils.data.DataLoader) -> tuple[torch.Tensor, torch.Tensor]:
    """
    Compute the mean and standard deviation of the dataset.

    :param dataloader: The dataloader for the dataset.
    :type dataloader: torch.utils.data.DataLoader

    :return: The mean and standard deviation of the dataset.
    :rtype: tuple[torch.Tensor, torch.Tensor]
    """
    data = torch.tensor([])
    for batch in dataloader:
        data = torch.cat((data, batch[0]), 0)

    mean = torch.mean(data, dim=(0, 2, 3))
    std = torch.std(data, dim=(0, 2, 3))

    return mean, std


def remove_artifacts(folder: str, extension: list[str]) -> None:
    """
    Remove files with the given extensions from a folder.

    :param folder: Path to the folder to clear
    :type folder: str
    :param extension: List of file with the given extensions to keep
    :type extension: list
    """
    for file in os.listdir(folder):
        if not file.endswith(tuple(extension)):
            os.remove(os.path.join(folder, file))

    print(f"Artifacts removed from {folder} with extensions {', '.join(extension)}")
