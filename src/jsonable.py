import json
from typing import Any


class Jsonable:
    def __init__(self, file_path: str):
        """
        Initialize the Jsonable object with the path to the JSON file.

        Args:
            file_path (str): Path to the JSON file.
        """
        self.file_path = file_path
        self.json: Any = None

    def load(self) -> None:
        """
        Load the JSON data from the file into the `json` attribute.

        Raises:
            FileNotFoundError: If the file does not exist.
            json.JSONDecodeError: If the file contains invalid JSON.
        """
        try:
            with open(self.file_path, "r") as file:
                self.json = json.load(file)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"File not found: {self.file_path}") from e
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in file: {self.file_path}", e.doc, e.pos
            )
