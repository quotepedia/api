"""Functions for determining file or data content type."""


def is_image(content_type: str | None) -> bool:
    """Determines whether the provided content type indicates an image.

    Args:
        content_type (str | None): The content type of the file or data.

    Returns:
        bool: A value indicating whether image is in the content type.
    """

    return content_type is not None and "image" in content_type
