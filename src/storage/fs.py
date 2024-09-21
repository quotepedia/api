"""Functions for managing file operations in the system."""

import os
import sys
import uuid
from typing import BinaryIO

from src.config import settings


def save(file: BinaryIO) -> str:
    """Saves the provided binary file to the system with a unique name.

    This function generates a unique file name for the given binary file,
    determines the appropriate system path for saving the file, and writes
    the file's content to that path.

    Args:
        file (BinaryIO): A binary object that contains the data to be saved.

    Returns:
        str: The unique name of the saved file.
    """

    name = generate_unique_file_name(file)
    path = get_system_path(name)

    with open(path, "wb") as buffer:
        content = file.read()
        buffer.write(content)

    return name


def remove(name: str) -> None:
    """Removes the file with the specified name from the system if exists.

    Args:
        name (str): The name of the file to be removed.
    """

    if exists(name):
        os.remove(get_system_path(name))


def exists(filename: str) -> bool:
    """Determines whether a file with the specified name exists in the system.

    Args:
        filename (str): The name of the file to check for existence.

    Returns:
        bool: A value indicating whether file exists.
    """

    return os.path.exists(get_system_path(filename))


def get_system_path(name: str) -> str:
    """Constructs the full system path for the specified file name.

    Args:
        name (str): The name of the file for which to construct the path.

    Returns:
        str: The full system path for the specified file name.
    """

    return os.path.join(settings.path.media, name)


def generate_unique_file_name(file: BinaryIO) -> str:
    """Generates a unique filename based on the extension of the provided file.

    Args:
        file (BinaryIO): The file object to extract the file extension from.

    Returns:
        str: The unique filename with the extracted file extension.
    """

    _, extension = os.path.splitext(file.name)
    return generate_unique_file_name_from_extension(extension)


def generate_unique_file_name_from_extension(extension: str) -> str:
    """Generates a unique file name with the provided extension.

    Args:
        extension (str): The file extension to use for the generated name.

    Returns:
        str: The unique file name with the provided extension.
    """

    name = str(uuid.uuid4())
    extension = extension.lower()

    if extension.startswith(os.path.extsep):
        return name + extension

    return name + os.path.extsep + extension


def is_size_in_range(file: BinaryIO, min_size: int = 0, max_size: int = sys.maxsize) -> bool:
    """Determines whether the size of the provided binary file is within the specified range.

    Args:
        file (BinaryIO): A binary object whose size is to be checked.
        min_size (int, optional): The minimum size in bytes. Defaults to 0.
        max_size (int, optional): The maximum size in bytes. Defaults to sys.maxsize.

    Returns:
        bool: A value indicating whether the file size is within the specified range.
    """

    contents = file.read()
    size = len(contents)

    return size in range(min_size, max_size)
