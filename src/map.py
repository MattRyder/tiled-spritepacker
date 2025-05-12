import os
from jsonable import Jsonable
from dataclasses import dataclass
from typing import List, Dict, Tuple


@dataclass
class MapRemapState:
    layers: List[List[int]]
    tilesets: List[Dict]


class Map(Jsonable):
    def __init__(self, path: str):
        """
        Initialize the Map object by loading the JSON data and setting up initial state.
        """
        super().__init__(path)
        self.load()

        # State for remapping tiles
        self.remap_state: MapRemapState = MapRemapState([], [])
        self.tilesets_in_use: List[str] = []
        self.first_gids: Dict[str, int] = {}

    def parse_raw_tile_id(self, raw_tile_id: int) -> int:
        """
        Extract the actual tile ID from a raw tile ID by masking out metadata bits.
        """
        return raw_tile_id & ~0xF0000000

    def get_map_tileset_for_global_id(self, global_id: int) -> Tuple[int, str]:
        """
        Find the tileset corresponding to a given global tile ID.

        Args:
            global_id (int): The global tile ID to look up.

        Returns:
            Tuple[int, str]: A tuple containing the first GID of the tileset and the tileset's filename.
        """
        current_firstgid = 0
        target_tilemap = ""

        for tileset in self.json["tilesets"]:
            # If the current tileset's firstgid is greater than the global_id, return the previous tileset
            if tileset["firstgid"] > global_id:
                return (current_firstgid, os.path.basename(target_tilemap))

            # Update to the current tileset
            target_tilemap = tileset["source"]
            current_firstgid = tileset["firstgid"]

        # Return the last tileset if no match was found earlier
        return (current_firstgid, os.path.basename(target_tilemap))
