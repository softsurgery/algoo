"""
Unit tests for indented block insertion in AlgoCodeEditor and MainWindow.
"""

import unittest
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QTextCursor
from ui.editor import AlgoCodeEditor
from ui.main_window import MainWindow

app = QApplication.instance() or QApplication([])


class TestEditorInsertIndentedBlock(unittest.TestCase):
    def setUp(self):
        self.editor = AlgoCodeEditor()

    def test_insert_si_block_with_indentation(self):
        self.editor.setPlainText("      ")
        c = self.editor.textCursor()
        c.movePosition(QTextCursor.EndOfLine)
        self.editor.setTextCursor(c)

        self.editor.insert_indented_block("Si condition Alors\n    \nFinSi")
        self.assertEqual(
            self.editor.toPlainText(),
            "      Si condition Alors\n          \n      FinSi",
        )

    def test_insert_pour_block_with_tabs(self):
        self.editor.setPlainText("\t\t")
        c = self.editor.textCursor()
        c.movePosition(QTextCursor.EndOfLine)
        self.editor.setTextCursor(c)

        self.editor.insert_indented_block("Pour i de 0 à n - 1 Faire\n    \nFin Pour")
        self.assertEqual(
            self.editor.toPlainText(),
            "\t\tPour i de 0 à n - 1 Faire\n\t\t    \n\t\tFin Pour",
        )

    def test_insert_single_line_symbol_unchanged(self):
        self.editor.setPlainText("    x")
        c = self.editor.textCursor()
        c.movePosition(QTextCursor.EndOfLine)
        self.editor.setTextCursor(c)

        self.editor.insert_indented_block(" ← ")
        self.assertEqual(self.editor.toPlainText(), "    x ← ")

    def test_main_window_on_insert_symbol_preserves_indent(self):
        win = MainWindow()
        editor = win.new_file("temp_indent_test.algo", "    ")
        c = editor.textCursor()
        c.movePosition(QTextCursor.EndOfLine)
        editor.setTextCursor(c)

        win._on_insert_symbol("Selon sélecteur\n    1 : \n    Sinon \nFin Selon")
        self.assertEqual(
            editor.toPlainText(),
            "    Selon sélecteur\n        1 : \n        Sinon \n    Fin Selon",
        )


if __name__ == "__main__":
    unittest.main()
