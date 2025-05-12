# Matt's Sprite Packer for Tiled Maps

## Overview

Matt's Sprite Packer is a tool designed to process tilesets and maps created in the Tiled map editor.
This tool remaps tile IDs, generates sprite atlases, and outputs remapped tilesets and maps for efficient use in your game engine.

> [!IMPORTANT]  
> I've written this for my own needs. As such, there's a lot of junk in here that will want sorting out. Don't expect to use this tool without requiring a few modifications first.
>
> Pull request are graciously appreciated.

## Features

If you're looking for this kinda tool, you've probably got a few massive sprite atlases from your artist, and found that your game takes an age to load them - especially if you're only using a few from each atlas.

This sprite packer will work it's magic and reduce your load times by:

- Locating which sprites are being used by your maps
- Pulling out the sprites into a single image file, segregated on tile size
- Remapping the IDs in your maps to correctly reference the tiles on the atlas (including in animations)
- Preserving any other data not related to sprites, such as properties / objects etc.

## Requirements

- Python 3.10 or higher
- [Pillow](https://python-pillow.org/) (Python Imaging Library fork)

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MattRyder/tiled-spritepacker.git
   cd tiled-spritepacker
   ```

2. Install dependencies:

    ```bash
    pip install
    ```

## Usage

Run the script with the following command:

```bash
python src/main.py <tileset_directory_path> <maps_directory_path> <remapped_tileset_directory_path> <remapped_maps_output_directory_path>
```

### Arguments

- `<tileset_directory_path>`: Path to the directory containing tileset JSON files.
- `<maps_directory_path>`: Path to the directory containing map JSON files.
- `<remapped_tileset_directory_path>`: Output directory for remapped tilesets.
- `<remapped_maps_output_directory_path>`: Output directory for remapped maps.

_n.b. Use separate directories for the source and remapped tilesets/maps. I am not responsible for you overwriting work not in your source control. You've been warned._

### Example

```bash
python src/main.py assets/tilesets assets/maps output/tilesets output/maps
```

## Configuration

At the time of you casting your eyes on this, I've got some hardcoded configuration in `main.py` that's probably of interest to you, dear reader:

- output_file_name: Base name for generated sprite atlases.
- tileset_image_width: Maximum width of the generated sprite atlas.
- image_output_path: Directory where sprite atlases are saved.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests to improve the tool.

## License

This project is licensed under the AGPLv3 License. [View the license terms here](https://www.gnu.org/licenses/agpl-3.0.html).
