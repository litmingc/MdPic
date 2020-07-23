import sys
from PySide2.QtCore import Qt

from PySide2.QtWidgets import QAction, QApplication, QMainWindow, QMenu, QPushButton

sys.path.append(".")
from src.uitoy.buttonlist import ButtonList

if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = ButtonList("添加图片")
    # example.resize(300,200)
    example.show()
    sys.exit(app.exec_())
