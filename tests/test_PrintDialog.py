import unittest
from printdialog import PrintDialog


class TestPrintDialog(unittest.TestCase):

    def test_print_dialog(self):
        # Create a new PrintDialog object
        dialog = PrintDialog()

        # Check that the dialog is created successfully
        self.assertIsInstance(dialog, PrintDialog)

        # Check that the dialog has the correct title
        self.assertEqual(dialog.windowTitle(), "Print Dialog")

        # Check that the dialog has the correct layout
        self.assertEqual(dialog.layout().count(), 3)

        # Check that the first row in the layout contains the correct widgets
        self.assertEqual(dialog.layout().itemAt(0).widget(), dialog.label_archer)
        self.assertEqual(dialog.layout().itemAt(1).widget(), dialog.combo_archer)
        self.assertEqual(dialog.layout().itemAt(2).widget(), dialog.button_ok)

        # Check that the second row in the layout contains the correct widgets
        self.assertEqual(dialog.layout().itemAt(3).widget(), dialog.label_arrow)
        self.assertEqual(dialog.layout().itemAt(4).widget(), dialog.combo_arrow)
        self.assertEqual(dialog.layout().itemAt(5).widget(), dialog.button_cancel)

        # Check that the dialog's `show()` method works correctly
        dialog.show()
        self.assertIsTrue(dialog.isVisible())

        # Check that the dialog's `hide()` method works correctly
        dialog.hide()
        self.assertIsFalse(dialog.isVisible())

        # Check that the dialog's `exec_()` method works correctly
        dialog.exec_()
        self.assertIsFalse(dialog.isVisible())


if __name__ == "__main__":
    unittest.main()
