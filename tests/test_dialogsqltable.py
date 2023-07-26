import unittest
from dialogsqltable import DialogSQLTable


class TestDialogSQLTable(unittest.TestCase):

    def test_dialog_sql_table(self):
        # Create a new DialogSQLTable object
        dialog = DialogSQLTable()

        # Check that the dialog is created successfully
        self.assertIsInstance(dialog, DialogSQLTable)

        # Check that the dialog has the correct title
        self.assertEqual(dialog.windowTitle(), "DialogSQLTable")

        # Check that the dialog has the correct layout
        self.assertEqual(dialog.layout().count(), 2)

        # Check that the first row in the layout contains the correct widgets
        self.assertEqual(dialog.layout().itemAt(0).widget(), dialog.label_table_name)
        self.assertEqual(dialog.layout().itemAt(1).widget(), dialog.combo_table_name)

        # Check that the second row in the layout contains the correct widgets
        self.assertEqual(dialog.layout().itemAt(2).widget(), dialog.button_ok)
        self.assertEqual(dialog.layout().itemAt(3).widget(), dialog.button_cancel)

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
