class TileStatus:
    """
    This class holds all properties of a tile, which describe how a tile IS modified
    E.G the tile is flipped, rotated or set to empty
    """
    def __init__(self):
        self.x_flip = False
        self.y_flip = False
        self.rot = False
        self.empty = False

    def __copy__(self) -> "TileStatus":
        t = TileStatus()
        t.x_flip = self.x_flip
        t.y_flip = self.y_flip
        t.rot = self.rot
        t.empty = self.empty
        return t

    def xFlip(self):
        status = self.__copy__()
        status.x_flip = not self.x_flip
        return status

    def yFlip(self):
        status = self.__copy__()
        status.y_flip = not self.y_flip
        return status

    def rotate(self):
        """
        rotate 90 degrees
        NOTE: rotated can only be on or off, rotated by 180 degree means NOT rotated, yflipped and xflipped,
        while rotated by 270 degree means yflipped, xflipped and rotated
        """
        status = self.__copy__()
        if self.rot:
            status.rot = False
            status.x_flip = not self.x_flip
            status.y_flip = not self.y_flip
        else:
            status.rot = True
        return status

    def __eq__(self, other):
        if isinstance(other, TileStatus):
            return self.x_flip == other.x_flip and \
                self.y_flip == other.y_flip and \
                self.rot == other.rot and \
                self.empty == other.empty
        raise NotImplementedError
