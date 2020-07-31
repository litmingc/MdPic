import sys
from PySide2.QtCore import Slot
sys.path.append(".")

from PySide2.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow,QApplication, QPushButton, QWidget

from src.picbedshower.model.apithread import HttpThread
import requests
from functools import partial

def getrequest(url):
    re = requests.get(url)
    return re

class Main(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.lab = QLabel("",self)
        self.lineedit = QLineEdit(self)
        self.button = QPushButton("txt",self)
        
        self.thread = HttpThread()
        self.thread.signalRespose.connect(self.showRe)
        self.button.clicked.connect(self.btnfunc)
        self.count = 0

        widget = QWidget()
        hbox = QHBoxLayout(widget)
        hbox.addWidget(self.lab)
        hbox.addWidget(self.lineedit)
        hbox.addWidget(self.button)

        self.setCentralWidget(widget)
    
    def btnfunc(self):
        self.count += 1
        self.button.setText("btn"+str(self.count))
        tmp = partial(getrequest, self.lineedit.text())
        self.thread.doGet(tmp)
    
    @Slot(object)
    def showRe(self,re:any):
        print(re.text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = Main()
    # example.resize(300,200)
    example.show()
    sys.exit(app.exec_())
