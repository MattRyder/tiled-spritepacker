import os
from typing import Optional, Dict, Any
from jsonable import Jsonable


class Tileset(Jsonable):
    def __init__(self, path: str):
        """
        Initialize a Tileset object.

        Args:
            path (str): Path to the tileset JSON file.
        """
        super().__init__(path)
        self.tile_id_remap: Dict[int, int] = {}
        self.source: str = os.path.basename(path)
        self.tileset_key: str = ""
        self.load()

        if self.json:
            self.tileset_key = (
                f"{self.json.get('tilewidth', 0)}x{self.json.get('tileheight', 0)}"
            )

    def find_tile(self, tile_id: int) -> Optional[Dict[str, Any]]:
        """
        Find a tile by its ID.

        Args:
            tile_id (int): The ID of the tile to find.

        Returns:
            Optional[Dict[str, Any]]: The tile data if found, otherwise None.
        """
        tiles = self.json.get("tiles", [])
        return next((tile for tile in tiles if tile.get("id") == tile_id), None)

    def tile_width(self) -> int:
        """
        Get the width of a tile.

        Returns:
            int: The width of a tile.
        """
        return self.json.get("tilewidth", 0)

    def tile_height(self) -> int:
        """
        Get the height of a tile.

        Returns:
            int: The height of a tile.
        """
        return self.json.get("tileheight", 0)
