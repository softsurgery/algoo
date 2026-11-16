"""
Reusable UI component primitives with declarative props for Algoo IDE.
"""

from ui.components.checkbox import AppCheckBox
from ui.components.close_button import AppCloseButton
from ui.components.chevron import (
    AppRotatingChevron,
    ChevronRotationAnimator,
    chevron_color,
    draw_chevron,
)
from ui.components.markdown_reader import (
    AppMarkdownReader,
    highlight_algo_syntax,
    highlight_python_syntax,
)
from ui.components.radio_button import AppRadioButton
from ui.components.select import AppSelect
from ui.components.tabs import AppTabWidget
from ui.components.tree_view import AppTreeView, NoFocusDelegate

__all__ = [
    "AppCheckBox",
    "AppCloseButton",
    "AppMarkdownReader",
    "AppRadioButton",
    "AppRotatingChevron",
    "AppSelect",
    "AppTabWidget",
    "AppTreeView",
    "ChevronRotationAnimator",
    "NoFocusDelegate",
    "chevron_color",
    "draw_chevron",
    "highlight_algo_syntax",
    "highlight_python_syntax",
]
