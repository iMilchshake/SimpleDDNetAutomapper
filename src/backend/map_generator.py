import tempfile

import twmap
import numpy as np
from src.backend.tile_status import TileStatus
from src.config.app_state import AppState
from src.dialogs.dialog_check_map import CheckMapDialog


class MapGenerator:
    def __init__(self, file_path):
        self._map = twmap.Map.empty("DDNet06")

        solid_map = np.loadtxt("data/debroijn_torus.txt", dtype=np.uint8)
        solid_map = np.pad(solid_map, 1, mode='constant')  # add gap to borders
        height, width = solid_map.shape

        # add layers
        physics_group = self._map.groups.new_physics()
        physics_layer = physics_group.layers.new_game(width, height)

        # add image
        assert AppState.imagePath()
        path = AppState.imagePath().absolute()
        self._map.images.new_from_file(str(path))

        # set physic tiles
        zeros = np.zeros(solid_map.shape, dtype=np.uint8)
        solid_map_stacked = np.stack([solid_map, zeros], axis=2)
        physics_layer.tiles = solid_map_stacked

        # add tile layer
        tile_layer = physics_group.layers.new_tiles(width, height)
        tile_layer.name = "test"
        tile_layer.image = 0
        tile_layer_map = np.zeros(solid_map_stacked.shape, dtype=np.uint8)

        # TODO twmap doesn't have automappers in the python version yet, so I have to do it manually
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                tile, status = CheckMapDialog.getMapTile(solid_map, x, y)
                if tile:
                    tile_layer_map[y, x, 0] = tile.tile_id
                if status:
                    tile_layer_map[y, x, 1] = MapGenerator._encodeBits(status)
        tile_layer.tiles = tile_layer_map

        # save map
        self._map.save(str(file_path))

    def __del__(self):
        # TODO delete map
        pass

    @staticmethod
    def _encodeBits(status: TileStatus) -> int:
        """DDNet tile flag byte: bit0 XFLIP, bit1 YFLIP, bit3 ROTATE"""
        ret: int = 0
        ret += (status.rot << 3)
        ret += (status.y_flip << 1)
        ret += status.x_flip
        return ret
