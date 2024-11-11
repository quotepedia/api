"""Functions for manipulating images and image files."""

from typing import TypeVar, cast

from PIL.Image import Image

TImage = TypeVar("TImage", bound=Image)


def crop_image_to_square(image: TImage) -> TImage:
    """Crops an image to a square, preserving the aspect ratio.

    Args:
        image (TImage): The input image to be cropped.

    Returns:
        TImage: The cropped square image.
    """

    width, height = image.size

    if width == height:
        return image

    new_side = min(width, height)
    left = (width - new_side) / 2
    top = (height - new_side) / 2
    right = (width + new_side) / 2
    bottom = (height + new_side) / 2
    cropped_image = image.crop((left, top, right, bottom))

    return cast(TImage, cropped_image)
