"""
=================================================
单张图片展示控件.根据markdown链接显示图片
@Author：LitMingC
@Last modified by：LitMingC/2020-07-24
    完成基础展示功能，即布局控件的罗列。
    未完成角标、图片以及附带信息的相关操作。
=================================================
"""

from PySide2.QtGui import QBrush, QColor, QMovie, QPainter, QPen, QPixmap
import qtawesome as qta
from PySide2.QtCore import QBuffer, QByteArray, QIODevice, QMargins, QPoint, QRect, QSize, QTextStream, QThread, QUrl, Qt, Signal, Slot
from PySide2.QtWidgets import (QCheckBox, QHBoxLayout, QLabel, QLayout, QPushButton,
                               QSizePolicy, QVBoxLayout, QWidget)
from PySide2.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
import requests

from src.picbedshower.model.apithread import HttpThread

suffixPix = ['png', "PNG", 'BMP', 'bmp']
suffixGif = ['gif', "GIF"]


class PicShower(QWidget):

    # TODO:发送图片数据
    signalChecked = Signal(int, object)
    signalDeleted = Signal(object)
    signalCopyEntered = Signal(object)

    signalGetPicBinary = Signal(bytes)

    def __init__(self, picinfo, picsize:list=[100,100], parent=None) -> None:
        super().__init__(parent=parent)
        self.picinfo = picinfo

        self.requestThread = HttpThread(self)  # 线程获取图片数据
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
        self.signalChecked.emit(state, self)
        self.delBtn.setDisabled(state)
        self.copyBtn.setDisabled(state)

    # TODO:设置图片
    def setPicContent(self, path: str):
        if path.split(".")[-1] in suffixPix:
            pixmap = QPixmap(path)
            self.picLab.setPixmap(pixmap)
        elif path.split(".")[-1] in suffixGif:
            movie = QMovie(path)
            self.picLab.setMovie(movie)
            movie.start()  # 播放,必须在show之前
        else:
            pass

    # 从PicModel的content中设置图片
    def loadPictureFormContent(self):
        if self.picinfo.mdLink.split(".")[-1] in suffixGif:
            # self.dataBytesArray = QByteArray.fromBase64(self.picinfo.content.encode())  # 这个变量必须存在一直存在，不能为局部变量。在QBuffer的生命周期里，它必须一直存在
            dataBuffer = QBuffer(parent=self)  # 这个变量必须存在一直存在，不能为局部变量.作为成员变量，或者设置parent
            dataBuffer.setData(QByteArray.fromBase64(self.picinfo.content.encode()))  # 在open之前
            dataBuffer.open(QIODevice.ReadOnly)  # 也许是要保持open的状态
            movie = QMovie(dataBuffer)  # 提供QByteArray(b'gif')时，无法显示图片。显示图片会比Pixmap模糊很多
            self.picLab.setMovie(movie)
            movie.start()
        else:
            pixmap = QPixmap()
            if pixmap.loadFromData(QByteArray.fromBase64(self.picinfo.content.encode())):
                self.picLab.setPixmap(pixmap)
            else:
                self.picLab.setText("图片加载失败")
    
    # 从PicModel的markdown链接获取信息，并触发设置
    def loadPictureFormMDLink(self):
        movie = QMovie('loading.gif')
        self.picLab.setMovie(movie)
        movie.start()
        self.signalGetPicBinary.connect(self.setPictureFormbinary)

        def request():
            '''发送self.picinfo.mdLink的get请求，通过信号槽传回'''
            re = requests.get(self.picinfo.mdLink)
            reBinary = re.content
            self.signalGetPicBinary.emit(reBinary)

        self.requestThread.doRequest(request)

    @Slot(bytes)
    def setPictureFormbinary(self,bdata:bytes):
        if self.picinfo.mdLink.split(".")[-1] in suffixGif:
            dataBuffer = QBuffer(parent=self)
            dataBuffer.setData(QByteArray(bdata))
            dataBuffer.open(QIODevice.ReadOnly)
            movie = QMovie(dataBuffer)
            movie.setCacheMode(QMovie.CacheAll)
            self.picLab.setMovie(movie)
            movie.start()
        else:
            pixmap = QPixmap()
            if pixmap.loadFromData(QByteArray(bdata)):
                self.picLab.setPixmap(pixmap)
            else:
                self.picLab.setText("图片加载失败")

    # TODO:复制markdown链接
    @Slot()
    def copyBtnClicked(self):
        self.signalCopyEntered.emit(self)

    # TODO:删除图片
    @Slot()
    def delBtnClicked(self):
        if x:=self.findChild(QBuffer):
            x.close()                   # 关不关都没事儿
            self.picLab.movie().stop()  # 不stop的时候会闪退，不懂为啥。QMovie直接读图片时，不stop也没事儿
        self.requestThread.stop()
        self.signalDeleted.emit(self)

