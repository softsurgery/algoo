"""
Interface & Panels visibility page for PreferencesDialog (remove/restore UI views).
"""

from typing import Dict
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QPushButton, QLabel

from ui.components import AppCheckBox
from ui.dialogs.preferences_dialog.header import create_section_header


class InterfacePage(QWidget):
    """Page for hiding or restoring IDE panels (Symbols bar, Console, Side panel)."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 14, 18, 14)
        layout.setSpacing(16)

        layout.addWidget(create_section_header(
            "Interface et Panneaux",
            "Affichez, masquez ou restaurez les panneaux de l'espace de travail."
        ))

        box = QGroupBox("Composants visibles")
        box_layout = QVBoxLayout(box)
        box_layout.setContentsMargins(16, 18, 16, 16)
        box_layout.setSpacing(12)

        self.chk_symbols_bar = AppCheckBox(
            "Barre de symboles et structures algorithmiques",
            checked=True,
        )
        box_layout.addWidget(self.chk_symbols_bar)

        self.chk_console = AppCheckBox(
            "Console d'exécution (Shell Python 3)",
            checked=True,
        )
        box_layout.addWidget(self.chk_console)

        self.chk_side_panel = AppCheckBox(
            "Panneau latéral (Code Python, TDO, TDNT, Guide et Aide)",
            checked=True,
        )
        box_layout.addWidget(self.chk_side_panel)

        hint = QLabel(
            "Si vous avez fermé un panneau via son bouton ×, cochez-le ici "
            "ou cliquez sur « Restaurer toutes les vues »."
        )
        hint.setWordWrap(True)
        hint.setObjectName("pref_subtitle")
        box_layout.addWidget(hint)

        btn_row = QHBoxLayout()
        self.btn_restore_all = QPushButton("Restaurer toutes les vues")
        self.btn_restore_all.setCursor(Qt.PointingHandCursor)
        self.btn_restore_all.clicked.connect(self.restore_all)
        btn_row.addWidget(self.btn_restore_all)
        btn_row.addStretch()
        box_layout.addLayout(btn_row)

        layout.addWidget(box)
        layout.addStretch()

    def restore_all(self) -> None:
        """Marks all UI panels as visible."""
        self.chk_symbols_bar.setChecked(True)
        self.chk_console.setChecked(True)
        self.chk_side_panel.setChecked(True)

    def get_ui_visibility(self) -> Dict[str, bool]:
        return {
            "symbols_bar": self.chk_symbols_bar.isChecked(),
            "console": self.chk_console.isChecked(),
            "side_panel": self.chk_side_panel.isChecked(),
        }

    def set_ui_visibility(self, visibility: Dict[str, bool]) -> None:
        self.chk_symbols_bar.setChecked(bool(visibility.get("symbols_bar", True)))
        self.chk_console.setChecked(bool(visibility.get("console", True)))
        self.chk_side_panel.setChecked(bool(visibility.get("side_panel", True)))
