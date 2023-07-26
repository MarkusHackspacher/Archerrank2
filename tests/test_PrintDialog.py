import unittest
from modules.gui.printdialog import DlgPrint


def test_handle_print(qtbot):
    dialog = DlgPrint()
    qtbot.addWidget(dialog)
    editor = dialog.editor
    editor.setText('This is a test')
    dialog.handle_print()
    assert dialog.buttonPrint.isEnabled()


def test_handle_preview(qtbot):
    dialog = DlgPrint()
    qtbot.addWidget(dialog)
    editor = dialog.editor
    editor.setText('This is a test')
    dialog.handle_preview()
    assert dialog.buttonPreview.isEnabled()

if __name__ == "__main__":
    unittest.main()
