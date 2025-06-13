from map import Map
from tileset import Tileset
from typing import Dict, Tuple


class State:
    def __init__(self):
        """
        Initialize the State object to manage tilesets, maps, and remapping logic.
        """
        self.tilesets: Dict[str, Tileset] = {}
        self.maps: Dict[str, Map] = {}
        self.tileset_tile_count: Dict[str, int] = {}
        self.unified_tilemap: Dict[str, Dict[str, Dict[int, int]]] = {}
        self.first_gid: int = 1

    def get_unified_tilemap(self, tileset_key: str) -> Dict[str, Dict[int, int]]:
        """
        Retrieve or initialize the unified tilemap for a given tileset key.
        """
        if tileset_key not in self.unified_tilemap:
            self.unified_tilemap[tileset_key] = {}
        return self.unified_tilemap[tileset_key]

    def generate_remap_ids(self) -> None:
        """
        Generate remapped IDs for all tiles in the unified tilemap.
        """
        for tileset_size_key, sources in self.unified_tilemap.items():
            remap_counter = 0
            for source, tiles in sources.items():
                for local_tile_id in tiles:
                    tiles[local_tile_id] = remap_counter
                    remap_counter += 1
            self.tileset_tile_count[tileset_size_key] = remap_counter

    def get_remapped_id(
        self, tileset_size_key: str, source: str, raw_tile_id: int, local_tile_id: int
    ) -> int:
        """
        Retrieve the remapped ID for a given tile, including metadata flags.
        """
        if local_tile_id not in self.unified_tilemap[tileset_size_key][source]:
            raise ValueError(
                f"Cannot find a remapped ID for: {tileset_size_key}, {source}, {local_tile_id}"
            )
        remapped_id = self.unified_tilemap[tileset_size_key][source][local_tile_id]
        return remapped_id | (raw_tile_id & 0xF0000000)

    def get_remapped_id2(
        self,
        tileset_size_key: str,
        source: str,
        first_gid: int,
        raw_tile_id: int,
        local_tile_id: int,
    ) -> int:
        """
        Retrieve the remapped ID for a given tile, including metadata flags, with a first GID offset.
        """
        if local_tile_id not in self.unified_tilemap[tileset_size_key][source]:
            raise ValueError(
                f"Cannot find a remapped ID for: {tileset_size_key}, {source}, {local_tile_id}"
            )
        remapped_id = (
            first_gid + self.unified_tilemap[tileset_size_key][source][local_tile_id]
        )
        return remapped_id | (raw_tile_id & 0xF0000000)

    def get_source_and_local_id(self, map: Map, raw_tile_id: int) -> Tuple[str, int]:
        """
        Extract the source tileset and local tile ID from a raw tile ID.
        """
        global_tile_id = map.parse_raw_tile_id(raw_tile_id)
        first_gid, source = map.get_map_tileset_for_global_id(global_tile_id)
        return source, global_tile_id - first_gid

    def add_global_id_to_state(self, map: Map, raw_tile_id: int) -> None:
        """
        Add a global tile ID to the state, initializing its unified tilemap entry if necessary.
        """
        source, local_tile_id = self.get_source_and_local_id(map, raw_tile_id)

        if source not in self.tilesets:
            raise ValueError(f"Tileset {source} not found in the game.")

        tileset = self.tilesets[source]
        tileset_key = tileset.tileset_key
        unified_tilemap = self.get_unified_tilemap(tileset_key)

        if source not in unified_tilemap:
            unified_tilemap[source] = {}

        if local_tile_id not in unified_tilemap[source]:
            unified_tilemap[source][local_tile_id] = 0

        # Handle animations for the tile
        tile = tileset.find_tile(local_tile_id)
        if tile and "animation" in tile:
            for frame in tile["animation"]:
                unified_tilemap[source][frame["tileid"]] = 0

    def rebuild_map(self, map: Map) -> None:
        """
        Rebuild the map by remapping its layers and tilesets.
        """
        layer_count = len(map.json["layers"])
        map.remap_state.layers = [[] for _ in range(layer_count)]

        # Identify tilesets in use
        for layer in map.json["layers"]:
            if "data" not in layer:
                continue

            for raw_tile_id in layer["data"]:
                if raw_tile_id == 0:
                    continue

                source, _ = self.get_source_and_local_id(map, raw_tile_id)
                tileset = self.tilesets[source]

                if tileset.tileset_key not in map.tilesets_in_use:
                    map.tilesets_in_use.append(tileset.tileset_key)

        # Assign first GIDs to tilesets in use
        gid_counter = 1
        for tileset_key in map.tilesets_in_use:
            map.first_gids[tileset_key] = gid_counter
            gid_counter += self.tileset_tile_count[tileset_key]

        # Remap layers
        for layer_index, layer in enumerate(map.json["layers"]):
            if "data" not in layer:
                continue

            map.remap_state.layers[layer_index] = [0] * len(layer["data"])

            for i, raw_tile_id in enumerate(layer["data"]):
                if raw_tile_id == 0:
                    continue

                source, local_tile_id = self.get_source_and_local_id(map, raw_tile_id)
                tileset = self.tilesets[source]

                remapped_tileset_file_name = (
                    f"./data/tilesets/sunnyvale-{tileset.tileset_key}.json"
                )

                if not any(
                    tileset_record["source"] == remapped_tileset_file_name
                    for tileset_record in map.remap_state.tilesets
                ):
                    map.remap_state.tilesets.append(
                        {
                            "source": remapped_tileset_file_name,
                            "firstgid": map.first_gids[tileset.tileset_key],
                        }
                    )

                tileset_first_gid = map.first_gids[tileset.tileset_key]
                remapped_id = self.get_remapped_id2(
                    tileset.tileset_key,
                    source,
                    tileset_first_gid,
                    raw_tile_id,
                    local_tile_id,
                )
                map.remap_state.layers[layer_index][i] = remapped_id

            layer["data"] = map.remap_state.layers[layer_index]
