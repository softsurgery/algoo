"""
Reusable Key-Value Info Table component with declarative props and light/dark theming.
"""

from typing import Optional, Sequence, Tuple
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QFrame,
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
)


class AppInfoTable(QTableWidget):
    """Themed, read-only two-column key-value table for metadata/about views."""

    def __init__(
        self,
        rows: Optional[Sequence[Tuple[str, str]]] = None,
        parent: Optional[QWidget] = None,
        *,
        row_height: int = 30,
        is_dark: Optional[bool] = None,
        object_name: Optional[str] = None,
    ):
        super().__init__(parent)
        self._row_height = row_height
        self._is_dark = is_dark

        self.setColumnCount(2)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setFocusPolicy(Qt.NoFocus)
        self.setFrameShape(QFrame.NoFrame)
        self.setShowGrid(False)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if object_name is not None:
            self.setObjectName(object_name)

        if rows is not None:
            self.set_rows(rows)

        if is_dark is not None:
            self.set_dark_mode(is_dark)

    def set_rows(self, rows: Sequence[Tuple[str, str]]) -> None:
        """Populates the table from a sequence of (key, value) tuples."""
        self.setRowCount(len(rows))
        key_font = QFont()
        key_font.setBold(True)

        for r, (key, value) in enumerate(rows):
            key_item = QTableWidgetItem(str(key))
            key_item.setFont(key_font)
            key_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.setItem(r, 0, key_item)

            val_item = QTableWidgetItem(str(value))
            val_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.setItem(r, 1, val_item)

            self.setRowHeight(r, self._row_height)

        self.setFixedHeight(len(rows) * self._row_height + 2)

    def set_dark_mode(self, is_dark: bool) -> None:
        """Applies explicit light or dark styling to the table."""
        self._is_dark = is_dark
        if is_dark:
            fg = "#cdd6f4"
            sep = "#313244"
        else:
            fg = "#334155"
            sep = "#e2e8f0"

        self.setStyleSheet(
            f"""
            QTableWidget {{
                background: transparent;
                color: {fg};
                border: none;
                font-size: 13px;
            }}
            QTableWidget::item {{
                padding: 4px 2px;
                border-bottom: 1px solid {sep};
            }}
            """
        )
