import sys
from PySide2.QtCore import Slot
sys.path.append(".")
from PySide2.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow,QApplication, QPushButton, QWidget

import requests
from functools import partial
from src.picbedshower.model.dbtools import DBThread

def getrequest(url):
    re = requests.get(url)
    return re

class Main(QMainWindow):
    
    def __init__(self) -> None:
        super().__init__()
        self.lab = QLabel("",self)
        self.lineedit = QLineEdit(self)
        self.button = QPushButton("txt",self)
        
        self.thread = DBThread("./tmp/test20200801.db")
        self.thread.signalBeds.connect(self.showRe)
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
        from src.picbedshower.model.models import PicBedModel
        self.thread.deleteBed(PicBedModel("owner","repo",path="path"))
    
    @Slot(object)
    def showRe(self,re:any):
        print(re)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    example = Main()
    # example.resize(300,200)
    example.show()
    sys.exit(app.exec_())
