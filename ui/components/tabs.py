"""
Reusable TabWidget component with declarative props and optional standalone theming.
"""

from typing import Callable, Optional, Sequence, Tuple, Union
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QTabWidget, QWidget


TabItem = Union[
    Tuple[QWidget, str],
    Tuple[QWidget, str, QIcon],
    Tuple[QWidget, str, QIcon, str],
]


class AppTabWidget(QTabWidget):
    """Themed, prop-driven QTabWidget for editor, side-panel, and detail tabs."""

    def __init__(
        self,
        tabs: Optional[Sequence[TabItem]] = None,
        parent: Optional[QWidget] = None,
        *,
        closable: bool = False,
        movable: bool = False,
        document_mode: bool = False,
        tab_position: QTabWidget.TabPosition = QTabWidget.North,
        uses_scroll_buttons: bool = True,
        elide_mode: Optional[Qt.TextElideMode] = None,
        font: Optional[QFont] = None,
        current_index: Optional[int] = None,
        is_dark: Optional[bool] = None,
        on_current_changed: Optional[Callable[[int], None]] = None,
        on_tab_close_requested: Optional[Callable[[int], None]] = None,
        object_name: Optional[str] = None,
    ):
        super().__init__(parent)
        self._is_dark = is_dark

        self.setTabsClosable(closable)
        self.setMovable(movable)
        self.setDocumentMode(document_mode)
        self.setTabPosition(tab_position)
        self.setUsesScrollButtons(uses_scroll_buttons)
        if elide_mode is not None:
            self.setElideMode(elide_mode)
        if font is not None:
            self.setFont(font)
        if object_name is not None:
            self.setObjectName(object_name)

        self.tabBar().setCursor(Qt.PointingHandCursor)

        if tabs:
            self.set_tabs(tabs)
        if current_index is not None and 0 <= current_index < self.count():
            self.setCurrentIndex(current_index)

        if on_current_changed is not None:
            self.currentChanged.connect(on_current_changed)
        if on_tab_close_requested is not None:
            self.tabCloseRequested.connect(on_tab_close_requested)

        if is_dark is not None:
            self.set_dark_mode(is_dark)

    def set_tabs(self, tabs: Sequence[TabItem]) -> None:
        """Replaces all tabs from (widget, label[, icon[, tooltip]]) tuples."""
        self.clear()
        for item in tabs:
            widget = item[0]
            label = item[1]
            icon = item[2] if len(item) >= 3 else None
            tooltip = item[3] if len(item) >= 4 else None
            idx = self.addTab(widget, icon, label) if icon is not None else self.addTab(widget, label)
            if tooltip:
                self.setTabToolTip(idx, tooltip)

    def ensure_tab(
        self,
        widget: QWidget,
        label: str,
        icon: Optional[QIcon] = None,
        index: Optional[int] = None,
    ) -> int:
        """Ensures `widget` is present as a tab and returns its index."""
        existing = self.indexOf(widget)
        if existing != -1:
            if icon is not None:
                self.setTabIcon(existing, icon)
            return existing
        if index is not None and 0 <= index <= self.count():
            idx = self.insertTab(index, widget, icon, label) if icon is not None else self.insertTab(index, widget, label)
        else:
            idx = self.addTab(widget, icon, label) if icon is not None else self.addTab(widget, label)
        return idx

    def remove_tab_widget(self, widget: QWidget) -> bool:
        """Removes `widget` tab if present; returns True if removed."""
        idx = self.indexOf(widget)
        if idx == -1:
            return False
        self.removeTab(idx)
        return True

    def set_dark_mode(self, is_dark: bool) -> None:
        """Applies explicit light or dark styling when used outside global stylesheets."""
        self._is_dark = is_dark
        if is_dark:
            pane_bg = "#1e1e2e"
            pane_border = "#313244"
            tab_bg = "#181825"
            tab_fg = "#a6adc8"
            sel_bg = "#1e1e2e"
            sel_fg = "#cdd6f4"
            accent = "#89b4fa"
            hover_bg = "#313244"
        else:
            pane_bg = "#ffffff"
            pane_border = "#e2e8f0"
            tab_bg = "#edf2f7"
            tab_fg = "#4a5568"
            sel_bg = "#ffffff"
            sel_fg = "#1a202c"
            accent = "#3182ce"
            hover_bg = "#e2e8f0"

        self.setStyleSheet(
            f"""
            QTabWidget::tab-bar {{
                left: 6px;
            }}
            QTabWidget::pane {{
                border: 1px solid {pane_border};
                background-color: {pane_bg};
                border-radius: 3px;
            }}
            QTabBar::tab {{
                background-color: {tab_bg};
                color: {tab_fg};
                margin-left: 0px;
                padding: 8px 22px 8px 18px;
                margin-right: 2px;
                border-top-left-radius: 3px;
                border-top-right-radius: 3px;
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background-color: {sel_bg};
                color: {sel_fg};
                border-top: 2px solid {accent};
                border-left: 1px solid {pane_border};
                border-right: 1px solid {pane_border};
            }}
            QTabBar::tab:hover:!selected {{
                background-color: {hover_bg};
            }}
            """
        )
