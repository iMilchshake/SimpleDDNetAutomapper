class TileMods:
    """
    This class holds all properties, that describe how a tile can be modified
    """
    def __init__(self, can_x_flip: bool, can_y_flip: bool, can_rot: bool):
        self.can_x_flip = can_x_flip
        self.can_y_flip = can_y_flip
        self.can_rot = can_rot

    def __eq__(self, other):
        if isinstance(other, TileMods):
            return self.can_x_flip == other.can_x_flip and \
                self.can_y_flip == other.can_y_flip and \
                self.can_rot == other.can_rot
        raise NotImplementedError

    def __copy__(self):
        return TileMods(self.can_x_flip, self.can_y_flip, self.can_rot)
