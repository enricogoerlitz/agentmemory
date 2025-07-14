def read_markdown_file(file_path: str) -> str:
    """
    Reads a markdown file and returns its content as a string.

    Args:
        file_path (str): The path to the markdown file.

    Returns:
        str: The content of the markdown file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()
