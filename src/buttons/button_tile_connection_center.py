from typing import TYPE_CHECKING, Optional

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter, QPen, QColor
from PyQt6.QtWidgets import QGridLayout, QCheckBox

from src.buttons.button_tile_connection import TileConnectionButton

if TYPE_CHECKING:
    from src.widgets.widget_tile import Tile


class TileConnectionCenterButton(TileConnectionButton):
    def __init__(self, tile: "Tile", button_id, parent=None):
        super().__init__(button_id, parent)
        self._tile = tile
        self._main = True
        self._state = 1  # full, default state
        self._num_states = 2  # this tile can only be full or empty
        layout = QGridLayout()
        checkbox_contents = [
            ["X-Flip", "Allow center tile to be flipped horizontally (left <-> right)"],
            ["Y-Flip", "Allow center tile to be flipped vertically (top <-> bottom)"],
            ["Rotate", "Allow center tile to be rotated"],
            ["Empty", "Allow center tile to be placed on empty blocks"],
        ]
        self.checkboxes = []
        for i, (name, tool_tip) in enumerate(checkbox_contents):
            widget = QCheckBox(name)
            widget.setToolTip(tool_tip)
            self.checkboxes.append(widget)
            layout.addWidget(widget, i // 2, i % 2)

        # these are maybe not required but nice to have
        self.box_x_flip = self.checkboxes[0]
        self.box_y_flip = self.checkboxes[1]
        self.box_rot = self.checkboxes[2]
        self.box_empty = self.checkboxes[3]

        self.box_x_flip.stateChanged.connect(self.updateXFlip)
        self.box_y_flip.stateChanged.connect(self.updateYFlip)
        self.box_rot.stateChanged.connect(self.updateRot)
        self.box_empty.stateChanged.connect(self.updateEmpty)

        self.setLayout(layout)

    # override
    def _paintOutline(self, qp: QPainter):
        size = self.size()
        pen = QPen(QColor(0, 0, 0, 255), 1)
        pen.setStyle(Qt.PenStyle.DotLine)
        qp.setPen(pen)
        qp.drawRect(0, 0, size.width() - 1, size.height() - 1)
        pen.setStyle(Qt.PenStyle.SolidLine)
        qp.setPen(pen)

    # override
    def _paintText(self, qp: QPainter):
        pass

    def setTile(self, tile: Optional["Tile"], update_neighbors=True):
        self._tile = tile
        self.box_y_flip.setCheckState(tile.tile_data.mods.can_y_flip)
        self.box_x_flip.setCheckState(tile.tile_data.mods.can_x_flip)
        self.box_rot.setCheckState(tile.tile_data.mods.can_rot)
        self.box_empty.setCheckState(tile.tile_data.status.empty)
        self.update()

    def updateXFlip(self, _):
        value = self.box_x_flip.isChecked()
        self.signal_emitter.modification_signal.emit(0, value)

    def updateYFlip(self, _):
        value = self.box_y_flip.isChecked()
        self.signal_emitter.modification_signal.emit(1, value)

    def updateRot(self, _):
        value = self.box_rot.isChecked()
        self.signal_emitter.modification_signal.emit(2, value)

    def updateEmpty(self, _):
        value = self.box_empty.isChecked()
        self.signal_emitter.modification_signal.emit(3, value)
