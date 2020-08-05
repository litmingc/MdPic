'''
=================================================
添加图库界面弹窗，调用实例的getBedinfo()方法，返回元
组(1,0;PicBedModel)
@Author：LitMingC
@Last modified by：LitMingC/2020-08
=================================================
'''
from PySide2.QtGui import QInputMethod
from PySide2.QtCore import Qt,QEvent
from PySide2.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QGroupBox, QLabel, QLineEdit, QMessageBox, QPushButton, QVBoxLayout, QWidget
from src.picbedshower.model.models import PicBedModel
import qtawesome as qta

class AddPicBedDialog(QDialog):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.dataReturn = None
        self.groupBox = QGroupBox("输入图床信息", self)
        # 信息输入组件
        self.editverboseName = QLineEdit(self.groupBox)

        self.editowner = QLineEdit(self.groupBox)

        self.editrepo = QLineEdit(self.groupBox)

        self.editbranch = QLineEdit(self.groupBox)
        self.editbranch.setText("master")
        self.editbranch.setPlaceholderText("默认为 master")

        self.editpath = QLineEdit(self.groupBox)
        self.editpath.setPlaceholderText("默认为仓库根目录")

        self.editaccess_token = QLineEdit(self.groupBox)
        self.editaccess_token.setEchoMode(QLineEdit.PasswordEchoOnEdit)
        self.editaccess_token.setAttribute(Qt.WA_InputMethodEnabled, False)

        self.editcustomPath = QLineEdit(self.groupBox)

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
        gridLay.addWidget(QLabel("别名", self.groupBox), 1, 2)
        gridLay.addWidget(self.editverboseName, 1, 4)
        gridLay.addWidget(QLabel("Owner", self.groupBox), 2, 2)
        gridLay.addWidget(self.editowner, 2, 4)
        gridLay.addWidget(QLabel("Repo", self.groupBox), 3, 2)
        gridLay.addWidget(self.editrepo, 3, 4)
        gridLay.addWidget(QLabel("Branch", self.groupBox), 4, 2)
        gridLay.addWidget(self.editbranch, 4, 4)
        gridLay.addWidget(QLabel("Path", self.groupBox), 5, 2)
        gridLay.addWidget(self.editpath, 5, 4)
        gridLay.addWidget(QLabel('AccessToken', self.groupBox), 6, 2)
        gridLay.addWidget(self.editaccess_token, 6, 4)
        gridLay.addWidget(QLabel("customPath", self.groupBox), 7, 2)
        gridLay.addWidget(self.editcustomPath, 7, 4)
        gridLay.addWidget(QLabel(),8,0,1,4)  # 占位控件
        gridLay.addWidget(self.buttonBox, 8, 4)
        # for i in range(1,gridLay.rowCount()):
        #     gridLay.addWidget(QLabel('：'),i,3)
        for i in [1, 2, 3, 6]:
            gridLay.addWidget(QLabel('*'), i, 1)
        gridLay.setColumnStretch(4, 2)
        gridLay.setRowStretch(9,1)

        vbox = QVBoxLayout(self)
        vbox.addWidget(self.groupBox)

    def getBedinfo(self):
        '''打开模态框，获取bedinfo
        '''
        self.exec_()  # 阻塞显示
        return self.result(), self.dataReturn

    def reject(self):
        self.hide()
        self.setResult(0)

    def accept(self):
        # 检查不可为空的
        if not self.hasEmptyLineEdit():
            self.dataReturn = PicBedModel(
                owner=self.editowner.text(),
                repo=self.editrepo.text(),
                verboseName=self.editverboseName.text(),
                branch = self.editbranch.text(),
                path = self.editpath.text(),
                customPath = self.editpath.text(),
                access_token = self.editaccess_token.text()
            )
            self.hide()
            self.setResult(1)

    # 检查必填项目中是否有未填项
    def hasEmptyLineEdit(self):
        hasEmpty = False  # 默认无空
        defaultStyle = QLineEdit().styleSheet()  # 记录默认的QLineEdit的样式

        # 设置为默认样式
        def setDefault(object: QLineEdit):
            object.setStyleSheet(defaultStyle)

        # 设置红色样式，并绑定还原样式的槽函数（编辑后，样式还原）
        def setRed(object: QLineEdit):
            object.textChanged.connect(lambda: setDefault(object))  # 样式还原
            nonlocal hasEmpty
            hasEmpty = True
            object.setPlaceholderText("此项不可为空")
            object.setStyleSheet(
                "QLineEdit{border-style: outset; border-width: 2px; border-color: red;}")

        # 检查argv的文本是否为空，空则调用提示样式
        def check(*argv):
            for i in argv:
                if i.text() == '':
                    setRed(i)

        # 检查必填控件
        check(self.editowner, self.editrepo,
              self.editverboseName, self.editaccess_token)

        return hasEmpty
