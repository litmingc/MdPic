"""
=================================================
单张图片展示控件
@Author：LitMingC
@Last modified by：LitMingC/2020-07-24
    完成基础展示功能，即布局控件的罗列。
    未完成角标、图片以及附带信息的相关操作。
=================================================
"""

from PySide2.QtGui import QBrush, QColor, QMovie, QPainter, QPen, QPixmap
import qtawesome as qta
from PySide2.QtCore import QMargins, QPoint, QRect, QSize, QThread, QUrl, Qt, Signal, Slot
from PySide2.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QLayout, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView


suffix = ['png', "PNG"]
suffix2 = ['gif', "GIF"]


class PicShower(QWidget):

    # TODO:发送图片数据
    signalChecked = Signal(object)
    signalDeleted = Signal(object)
    signalCopyEntered = Signal(object)

    def __init__(self, picinfo, picsize:list=[100,100], parent=None) -> None:
        super().__init__(parent=parent)
        self.picinfo = picinfo

        # self.checkedLab = QLabel("xxxx", self)
        # self.checkedLab.move(20, 20)
        # self.checkedLab.setVisible(False)

        # 按钮和复选框
        self.copyBtn = QPushButton(qta.icon("fa5s.copy"), None, self)
        self.copyBtn.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed)  # 固定高度，保证宽度
        self.copyBtn.clicked.connect(self.copyBtnClicked)

        self.delBtn = QPushButton(qta.icon("fa5s.trash-alt"), None, self)
        self.delBtn.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.delBtn.clicked.connect(self.delBtnClicked)

        self.checkBtn = QCheckBox(None, self)
        self.checkBtn.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)  # 固定宽高
        self.checkBtn.stateChanged.connect(self.checked)

        # 图片显示
        self.picLab = QLabel(parent=self)
        # self.setPicContent('./tmp/unity-lesson3-4.gif')  # 设置默认图片，vscode的默认工作路径为根目录
        self.picLab.setScaledContents(True)
        self.picLab.setFixedSize(*picsize)  # 固定图片大小

        pichbox = QHBoxLayout()
        pichbox.addWidget(self.picLab)

        buttonshbox = QHBoxLayout()
        buttonshbox.addWidget(self.copyBtn, 1)
        buttonshbox.addWidget(self.delBtn, 1)
        buttonshbox.addWidget(self.checkBtn)

        vbox = QVBoxLayout(self)
        vbox.setContentsMargins(QMargins(5,0,5,0))
        vbox.addLayout(pichbox)
        vbox.addLayout(buttonshbox)

    # TODO:选中，其它按钮置灰，记下角标
    @Slot(int)
    def checked(self, state: int):
        self.signalChecked.emit(self)
        self.delBtn.setDisabled(state)
        self.copyBtn.setDisabled(state)

    # TODO:设置图片
    def setPicContent(self, path: str):
        if path.split(".")[-1] in suffix:
            pixmap = QPixmap(path)
            self.picLab.setPixmap(pixmap)
        elif path.split(".")[-1] in suffix2:
            movie = QMovie(path)
            self.picLab.setMovie(movie)
            movie.start()  # 播放,必须在show之前
        else:
            pass

    # TODO:复制markdown链接
    @Slot()
    def copyBtnClicked(self):
        self.signalCopyEntered.emit(self)

    # TODO:删除图片
    @Slot()
    def delBtnClicked(self):
        self.signalDeleted.emit(self)

