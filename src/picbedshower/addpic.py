'''
=================================================
添加图片的界面弹窗，调用实例的getPic()方法，返回元
组(1,0;文件名;文件数据base64编码)
@Author：LitMingC
@Last modified by：LitMingC/2020-08
=================================================
'''
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QFileDialog, QGridLayout, QGroupBox, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
import qtawesome as qta
from pathlib import Path
import datetime as DT


class AddPicDialog(QDialog):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.dataReturn = None
        self.groupBox = QGroupBox("文件重命名", self)
        # 信息输入组件

        self.editFileName = QLineEdit(self.groupBox)
        self.editFileName.setPlaceholderText("默认")

        self.buttonBox = QDialogButtonBox(self)
        self.acceptButton = self.buttonBox.addButton(QDialogButtonBox.Save)
        self.acceptButton.clicked.connect(self.accept)
        self.rejectButton = self.buttonBox.addButton(QDialogButtonBox.Cancel)
        self.rejectButton.clicked.connect(self.reject)

        self.initUI()
        self.setModal(True)
        self.setWindowTitle("添加图床")
        self.setWindowFlags(Qt.WindowCloseButtonHint)
        self.setWindowIcon(qta.icon("fa5.edit"))

    def initUI(self):
        gridLay = QGridLayout(self.groupBox)
        gridLay.addWidget(QLabel("文件名", self.groupBox), 1, 2)
        gridLay.addWidget(self.editFileName, 1, 4)
        gridLay.addWidget(QLabel(), 8, 0, 1, 4)  # 占位控件
        gridLay.addWidget(self.buttonBox, 8, 4)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.groupBox)

    def getPic(self):
        '''打开模态框，获取bedinfo
        '''
        filePath, fileFilter = QFileDialog.getOpenFileName(
            parent=self, caption='选择图片', dir='', filter="Image Files (*.png *.jpg *.bmp *.gif)", options=QFileDialog.DontUseNativeDialog)
        if filePath:
            fileName = Path(filePath).parts[-1]
        else:
            fileName = None
            filePath = None
            self.setResult(0)
            return self.result(), fileName, filePath

        return self.setFileName(fileName, filePath)

    def setFileName(self, fileName:str, filePath):
        defaultFileName = "{}_[{}].{}".format(fileName.rsplit('.', 1)[0], DT.datetime.now().strftime("%Y-%m-%d_%H:%M:%S"), fileName.rsplit('.', 1)[-1])
        defaultFileName.replace(" ", "_")  # 替换掉空格
        self.editFileName.setText(defaultFileName)

        self.exec_()  # 阻塞显示
        if self.editFileName.text() == "":
            fileName = defaultFileName
        else:
            fileName = self.editFileName.text()
        return self.result(), fileName.replace(" ", "_"), filePath  # 文件名替换掉空格

    def reject(self):
        self.hide()
        self.setResult(0)

    def accept(self):
        self.dataReturn = None
        self.hide()
        self.setResult(1)
