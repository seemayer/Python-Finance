import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow
)
from test.control_panel_ui import Ui_Form

class Window(QMainWindow, Ui_Form):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
 


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())