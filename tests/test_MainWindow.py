import unittest
from mainwindow import MainWindow


class TestMainWindow(unittest.TestCase):

    def test_main_window(self):
        # Create a new MainWindow object
        window = MainWindow()

        # Check that the window is created successfully
        self.assertIsInstance(window, MainWindow)

        # Check that the window has the correct title
        self.assertEqual(window.windowTitle(), "ArcherRank2")

        # Check that the window has the correct layout
        self.assertEqual(window.layout().count(), 4)

        # Check that the first row in the layout contains the correct widgets
        self.assertEqual(window.layout().itemAt(0).widget(), window.label_title)
        self.assertEqual(window.layout().itemAt(1).widget(), window.combo_archer)
        self.assertEqual(window.layout().itemAt(2).widget(), window.button_start)

        # Check that the second row in the layout contains the correct widgets
        self.assertEqual(window.layout().itemAt(3).widget(), window.table_rank)

        # Check that the window's `show()` method works correctly
        window.show()
        self.assertIsTrue(window.isVisible())

        # Check that the window's `hide()` method works correctly
        window.hide()
        self.assertIsFalse(window.isVisible())

        # Check that the window's `exec_()` method works correctly
        window.exec_()
        self.assertIsFalse(window.isVisible())


if __name__ == "__main__":
    unittest.main()
