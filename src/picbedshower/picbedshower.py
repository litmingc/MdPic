'''
=================================================
图册的展示
@Author：LitMingC
@Last modified by：LitMingC/2020-07-
=================================================
'''

from PySide2.QtGui import QDragEnterEvent, QDropEvent, QImage, QPixmap
import qtawesome as qta
from PySide2.QtCore import Slot
from PySide2.QtWidgets import (QCheckBox, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QScrollArea, QSizePolicy, QVBoxLayout, QWidget)

from src.picbedshower.picshower import PicShower
from src.uitoy.flowlayer import FlowLayout


class PicBedShower(QWidget):

    def __init__(self, parent: any = None) -> None:
        super().__init__(parent=parent)
        # 接收拖放
        self.setAcceptDrops(True)

        # info
        self.infoGroupBox = QGroupBox("图床信息：", self)
        self.infodata = None  # TODO:默认无信息，需要触发初始化
        # buttons
        self.copyBtn = QPushButton(qta.icon("fa5s.copy"), None, self)
        self.copyBtn.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)  # 固定
        self.copyBtn.clicked.connect(self.multiCopy)

        self.delBtn = QPushButton(qta.icon("fa5s.trash-alt"), None, self)
        self.delBtn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.delBtn.clicked.connect(self.multiDel)

        self.checkBtn = QCheckBox("全选", self)
        self.checkBtn.setSizePolicy(
            QSizePolicy.Fixed, QSizePolicy.Fixed)  # 固定宽高
        self.checkBtn.stateChanged.connect(self.allChecked)

        self.indexChecked = []  # 记录已选中
        # 图片集控件
        self.picsShower = QWidget()
        self.picslay = FlowLayout(self.picsShower)  # 图片浮动布局，作为成员变量增减

        # 初始化图片集
        self.initAllPicShower()
        # 布局
        self.initLay()

    def initLay(self):
        # info中显示的控件
        ownerlab = QLabel("Owner:", self.infoGroupBox)
        repolab = QLabel("Repo :", self.infoGroupBox)
        pathlab = QLabel("Path :", self.infoGroupBox)
        ownerEditLine = QLineEdit(self.infoGroupBox)
        ownerEditLine.setObjectName("owner")
        repoEditLine = QLineEdit(self.infoGroupBox)
        repoEditLine.setObjectName("repo")
        pathEditLine = QLineEdit(self.infoGroupBox)
        pathEditLine.setObjectName("path")
        for i in self.infoGroupBox.findChildren(QLineEdit):
            # 初始化，设置不可编辑
            i.setEnabled(False)
            i.setText(i.objectName())
        # 图床信息控件横向布局
        infogridlay = QGridLayout(self.infoGroupBox)
        infogridlay.addWidget(ownerlab, 1, 1)
        infogridlay.addWidget(repolab, 2, 1)
        infogridlay.addWidget(pathlab, 3, 1)
        infogridlay.addWidget(ownerEditLine, 1, 2)
        infogridlay.addWidget(repoEditLine, 2, 2)
        infogridlay.addWidget(pathEditLine, 3, 2)
        # infogridlay.setColumnStretch(2, 1)
        infogridlay.setColumnStretch(3, 1)

        # 设置滑动显示
        # self.picsShower.setMinimumSize(575,300)
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.picsShower)
        scrollArea.setWidgetResizable(True)  # 重要，控件大小可变

        # 图片展示模块的横向布局
        picshowhbox = QHBoxLayout()
        picshowhbox.addWidget(scrollArea)

        # 按钮组合的横向布局
        buttonhbox = QHBoxLayout()
        buttonhbox.addStretch(1)
        buttonhbox.addWidget(self.copyBtn)
        buttonhbox.addWidget(self.delBtn)
        buttonhbox.addWidget(self.checkBtn)

        # 创建布局管理器
        vbox = QVBoxLayout(self)  # 整体布局

        vbox.addWidget(self.infoGroupBox)
        vbox.addLayout(picshowhbox, 1)
        # vbox.addStretch(1)
        vbox.addLayout(buttonhbox)

    # TODO:初始化所有图片显示控件
    def initAllPicShower(self, size: int = 100, width: int = 575):
        self.picsShower.setMinimumSize(width, size)
        pass

    # 更新图库信息infobox
    def updateInfo(self, bedinfo: any = None):
        if bedinfo:
            self.infodata = bedinfo
        self.infoGroupBox.findChild(
            QLineEdit, 'owner').setText(self.infodata.owner)
        self.infoGroupBox.findChild(
            QLineEdit, 'repo').setText(self.infodata.repo)
        self.infoGroupBox.findChild(
            QLineEdit, 'path').setText(self.infodata.path)

    # 本地文件上传，需要上传图片到图库，图片可由本地获取
    # 初始化图库，将图库中图片显示，从图床获取图片信息
    # TODO:添加一个图片
    def addOnePic(self, picinfo: any, size: int = [100, 100], img: any = None):
        tmp = PicShower(
            "tmp", picsize=size, parent=self.picsShower)
        tmp.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        # 绑定槽函数
        tmp.signalChecked.connect(self.oneChecked)
        tmp.signalDeleted.connect(self.oneDel)
        tmp.signalCopyEntered.connect(self.oneCopy)
        self.picslay.addWidget(tmp)

        if img and isinstance(img, QImage):
            # 有图片信息
            tmp.picLab.setPixmap(QPixmap().fromImage(img))
        else:
            tmp.picLab.setText(str(picinfo))

    # 全选
    @Slot(int)
    def allChecked(self, checkstate: int):
        for iterm in self.picsShower.findChildren(PicShower):  # 选择Picshower类型的
            iterm.checkBtn.setChecked(checkstate)

    # TODO:批量copy
    @Slot()
    def multiCopy(self):
        print("图片数量", len(self.picsShower.findChildren(PicShower)))
        pass

    # TODO:批量del
    @Slot()
    def multiDel(self):
        for iterm in self.indexChecked:
            iterm.deleteLater()
        self.indexChecked.clear()

    # 单个图片被选中
    # TODO:准备被复制或删除，为批量操作作准备
    @Slot()
    def oneChecked(self, state: int, obj: PicShower):
        if state:
            self.indexChecked.append(obj)
        else:
            self.indexChecked.remove(obj)

    # TODO:单图触发copy
    @Slot()
    def oneCopy(self, obj):
        pass

    # TODO:单图触发del
    # 删除对应控件
    @Slot()
    def oneDel(self, obj):
        obj.deleteLater()  # 删除控件

    # TODO:拖动进入
    def dragEnterEvent(self, event: QDragEnterEvent):
        eMimeData = event.mimeData()
        if(eMimeData.hasUrls() or eMimeData.hasImage()):  # url包括文件
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event: QDropEvent):
        eMimeData = event.mimeData()
        if(eMimeData.hasImage()):  # 直接是QImage, 需要优先处理
            self.addOnePic("picinfo", img=eMimeData.imageData())
        elif(eMimeData.hasUrls()):  # url包括文件
            print(eMimeData.text())
