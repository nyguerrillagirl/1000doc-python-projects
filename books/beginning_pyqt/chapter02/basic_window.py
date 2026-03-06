# basic_window.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class EmptyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        '''
        Initialize the window and display its contents to the screen.
        :return:
        '''
        self.setGeometry(1500, 800, 640,480)
        self.setWindowTitle('Empty Window in PyQt')
        self.show()

# Run program
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = EmptyWindow()
    sys.exit(app.exec_())