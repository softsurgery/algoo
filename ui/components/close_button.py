"""
Reusable Close (×) icon button matching the tab close button style.
"""

import os
from typing import Callable, Optional
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QImageReader
from PyQt5.QtWidgets import QToolButton, QWidget

from ui.platform_utils import get_resource_path


def _close_asset_path(is_dark: bool, hover: bool = False) -> str:
    ext = "svg" if b"svg" in QImageReader.supportedImageFormats() else "png"
    mode = "dark" if is_dark else "light"
    suffix = "_hover" if hover else ""
    return get_resource_path("ui", "assets", f"tab_close_{mode}{suffix}.{ext}").replace("\\", "/")


class AppCloseButton(QToolButton):
    """Compact icon-only close button using the same close icon assets as algo tabs."""

    def __init__(
        self,
        parent: Optional[QWidget] = None,
        *,
        tooltip: str = "Fermer",
        is_dark: bool = False,
        size: int = 24,
        icon_size: int = 14,
        on_clicked: Optional[Callable[[], None]] = None,
    ):
        super().__init__(parent)
        self._is_dark = is_dark
        self._normal_icon = QIcon()
        self._hover_icon = QIcon()
        self.setAutoRaise(True)
        self.setFixedSize(size, size)
        self.setIconSize(QSize(icon_size, icon_size))
        self.setCursor(Qt.PointingHandCursor)
        self.setToolTip(tooltip)
        if on_clicked is not None:
            self.clicked.connect(on_clicked)
        self.set_dark_mode(is_dark)

    def set_dark_mode(self, is_dark: bool) -> None:
        self._is_dark = is_dark
        normal_path = _close_asset_path(is_dark, hover=False)
        hover_path = _close_asset_path(is_dark, hover=True)
        self._normal_icon = QIcon(normal_path) if os.path.exists(normal_path) else QIcon()
        self._hover_icon = QIcon(hover_path) if os.path.exists(hover_path) else self._normal_icon
        self.setIcon(self._normal_icon)

        hover_bg = "#313244" if is_dark else "#fee2e2"
        pressed_bg = "#45475a" if is_dark else "#fecaca"
        self.setStyleSheet(
            f"""
            QToolButton {{
                border: none;
                background: transparent;
                border-radius: 3px;
                padding: 2px;
            }}
            QToolButton:hover {{
                background-color: {hover_bg};
            }}
            QToolButton:pressed {{
                background-color: {pressed_bg};
            }}
            """
        )

    def enterEvent(self, event) -> None:
        if not self._hover_icon.isNull():
            self.setIcon(self._hover_icon)
        super().enterEvent(event)

    def leaveEvent(self, event) -> None:
        if not self._normal_icon.isNull():
            self.setIcon(self._normal_icon)
        super().leaveEvent(event)
