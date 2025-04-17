'''Load JSON data'''
import json
from pathlib import Path
from typing import Any


def create_directory_if_not_exists(folder_name: str) -> Path:
    """Creates a directory, named `folder_name`, if it doesn't exist.
    Args:
        folder_name (str): name of the folder.
    Returns:
        Path: directory path object.
    """

    directory = Path(folder_name)
    directory.mkdir(exist_ok=True)
    return directory


def to_json(data: dict[str, Any], base_folder: str, file_name: str):
    """Creates a JSON by the directory"""
    directory = create_directory_if_not_exists(base_folder)
    with open(directory / file_name, mode="w", encoding="utf8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
