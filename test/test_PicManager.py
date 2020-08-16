import sys

from PySide2.QtWidgets import QApplication

sys.path.append(".")

from src.picmanager import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = MainWindow()
    example.show()
    sys.exit(app.exec_())
