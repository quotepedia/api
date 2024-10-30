def truncate(s: str, length: int = 16, ellipsis: str = "…") -> str:
    """
    Truncate a string to a specified length, appending an ellipsis if truncated.

    Args:
        s (str): The string to truncate.
        length (int): The maximum length of the truncated string, including the ellipsis.
        ellipsis (str): The string to append if truncation occurs (default is '…').

    Returns:
        str: The truncated string.

    Examples:
        >>> truncate("This is a long string that needs to be truncated.", 20)
        'This is a long stri…'

        >>> truncate("This is a long string that needs to be truncated.", 10)
        'This is a…'

        >>> truncate("This is a long string that needs to be truncated.", 5)
        'This…'

        >>> truncate("This is a long string that needs to be truncated.", 0)
        ''

        >>> truncate("Short", 10)
        'Short'

        >>> truncate("Short", 5)
        'Short'

        >>> truncate("Short", 3)
        'Sh…'

        >>> truncate("Ellipsis test", 5, '!!')
        'Ell!!'

        >>> truncate("Ellipsis test", 5, '')
        'Ellip'

        >>> truncate("Ellipsis test", 5, '…!!!')
        'E…!!!'

        >>> truncate("Ellipsis test", -1)
        Traceback (most recent call last):
            …
        ValueError: Length must be non-negative
    """

    if length < 0:
        raise ValueError("Length must be non-negative")

    if length == 0:
        return ""

    ellipsis_length = len(ellipsis)

    if len(s) <= length:
        return s

    max_length = length - ellipsis_length

    if max_length < 0:
        return ellipsis[:length]

    return s[:max_length] + ellipsis


if __name__ == "__main__":
    import doctest

    doctest.testmod(verbose=True)
