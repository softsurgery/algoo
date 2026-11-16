"""
Preferences pages package.
"""

from ui.dialogs.preferences_dialog.pages.theme_page import ThemePage
from ui.dialogs.preferences_dialog.pages.editor_page import EditorPage
from ui.dialogs.preferences_dialog.pages.colors_page import ColorsPage, SAMPLE_ALGO_CODE
from ui.dialogs.preferences_dialog.pages.interface_page import InterfacePage

__all__ = ["ThemePage", "EditorPage", "ColorsPage", "InterfacePage", "SAMPLE_ALGO_CODE"]
