import sys
from PySide2.QtCore import Slot

from PySide2.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QWidget

sys.path.append(".")

from src.picbedshower.addpicbed import AddPicBedDialog

class Main(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.lab = QLabel("",self)
        self.lineedit = QLineEdit(self)
        self.button = QPushButton("txt",self)

        self.button.clicked.connect(self.btnfunc)
        self.count = 0

        widget = QWidget()
        hbox = QHBoxLayout(widget)
        hbox.addWidget(self.lab)
        hbox.addWidget(self.lineedit)
        hbox.addWidget(self.button)

        self.setCentralWidget(widget)
    
    def btnfunc(self):
        a = AddPicBedDialog().getBedinfo()
        # a.exec()
        print(a)
    
    @Slot(object)
    def showRe(self,re:any):
        print(re)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = Main()
    # example.resize(300,200)
    example.show()
    sys.exit(app.exec_())
