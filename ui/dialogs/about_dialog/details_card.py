"""
Card container displaying technical metadata for AboutDialog.
"""

from PyQt5.QtWidgets import QFrame, QVBoxLayout

from ui.components import AppInfoTable


class AboutDetailsCard(QFrame):
    """Card container displaying version and developer details in a styled table."""

    def __init__(self, parent=None, is_dark: bool = False):
        super().__init__(parent)
        self.setObjectName("about_card")
        self._is_dark = is_dark
        self._setup_ui()

    def _setup_ui(self):
        card_layout = QVBoxLayout(self)
        card_layout.setContentsMargins(16, 12, 16, 12)
        card_layout.setSpacing(6)

        self.details_table = AppInfoTable(
            rows=[
                ("Développeur", "softsurgery"),
                ("Moteur", "Python 3 + NumPy"),
                ("Interface", "PyQt5"),
            ],
            parent=self,
            is_dark=self._is_dark,
            object_name="about_details_table",
        )
        card_layout.addWidget(self.details_table)
