import pytest

from src.backend.tile_status import TileStatus


class TestTileStatus:
    def test_init(self):
        TileStatus()

    @staticmethod
    def create_tile_status(x_flip, y_flip, rot, empty) -> TileStatus:
        t = TileStatus()
        t.x_flip = x_flip
        t.y_flip = y_flip
        t.rot = rot
        t.empty = empty
        return t

    @staticmethod
    def status_list(create_tile_status):
        return [
            TileStatus(),
            create_tile_status(True, False, True, False),
            create_tile_status(False, False, False, True),
            create_tile_status(True, True, False, True),
            create_tile_status(False, True, False, False),
        ]

    @pytest.mark.parametrize("status", status_list(create_tile_status))
    def test_copy_and_equal(self, status):
        t2 = status.__copy__()
        assert t2 == status
        assert id(t2) != id(status)
        t2.y_flip = not t2.y_flip
        assert t2 != status
        t2.y_flip = not t2.y_flip
        assert t2 == status

    @pytest.mark.parametrize("status", status_list(create_tile_status))
    def test_rot90(self, status):
        rot = status.rot
        rot_status = status.rotate()
        assert rot_status.rot != rot
        assert status == status.rotate().rotate().rotate().rotate()
        # sanity check
        assert status.rotate().rotate() == status.xFlip().yFlip()

    @pytest.mark.parametrize("status", status_list(create_tile_status))
    def test_x_flip(self, status):
        t = status.xFlip()
        assert t != status
        assert t.x_flip != status.x_flip
        assert id(t) != id(status)

    @pytest.mark.parametrize("status", status_list(create_tile_status))
    def test_y_flip(self, status):
        t = status.yFlip()
        assert t != status
        assert t.y_flip != status.y_flip
        assert id(t) != id(status)
