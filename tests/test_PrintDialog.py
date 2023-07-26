import unittest
from modules.gui.printdialog import DlgPrint



class TestDlgPrint(unittest.TestCase):

    def test_handle_print(self):
        dialog = DlgPrint()
        editor = dialog.editor
        editor.setText('This is a test')
        dialog.handle_print()
        self.assertTrue(dialog.buttonPrint.isEnabled())

    def test_handle_preview(self):
        dialog = DlgPrint()
        editor = dialog.editor
        editor.setText('This is a test')
        dialog.handle_preview()
        self.assertTrue(dialog.buttonPreview.isEnabled())

if __name__ == "__main__":
    unittest.main()
