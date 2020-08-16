"""
=================================================
图床管理的主体，增删图片
@Author：LitMingC
@Last modified by：LitMingC/2020-07-23
=================================================
"""

import sys
from PySide2.QtCore import Qt, Slot

from PySide2.QtGui import QResizeEvent
from PySide2.QtWidgets import (
    QAction, QApplication, QHBoxLayout, QMainWindow, QMenu, QPushButton, QSizePolicy, QSpacerItem, QToolBox, QVBoxLayout, QWidget)
from src.picbedshower.picbedshower import PicBedShower
from dataclasses import dataclass
from src.uitoy.buttonlist import ButtonList
from src.picbedshower.addpicbed import AddPicBedDialog
from src.picbedshower.model.models import PicBedModel
from src.picbedshower.model.dbtools import DBThread

debugFlag = True


def class_name(o):
    return o.metaObject().className()


@dataclass
class BedAndButton:
    button: QPushButton
    bed: PicBedModel


def embed_into_hbox_layout(w, margin=5):
    """Embed a widget into a layout to give it a frame"""
    result = QWidget()
    layout = QHBoxLayout(result)
    layout.setContentsMargins(margin, margin, margin, margin)
    layout.addWidget(w)
    return result


class PicManager(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.initUI()

        self.bedPool = {}  # key为button，value为bedmodel
        self.bedDBthread = DBThread("./data.db")  # 数据库操作

        self.bedDBthread.signalBeds.connect(self.bedListBtnInit)
        self.bedDBthread.queryAllBed()  # 查询所有床

    def initUI(self):
        # 右侧图床列表box
        self.bedListQbtn = ButtonList("添加图床")
        self.bedListQbtn.signalBtnAdded.connect(self.newPicBed)
        self.bedListQbtn.signalBtnDeleted.connect(self.delPicBed)
        self.bedListQbtn.signalBtnClicked.connect(self.clickPicBed)

        # 工具box
        self.picRepository = QToolBox(self)
        self.picRepository.setSizePolicy(
            QSizePolicy.Preferred, QSizePolicy.Expanding)

        self.picRepository.addItem(self.bedListQbtn, "gitee图库")

        self.leftvbox = QVBoxLayout()
        self.leftvbox.addWidget(self.picRepository)
        self.leftvbox.setContentsMargins(1, 15, 1, 1)

        # 中间picbedshower
        self.midvbox = QVBoxLayout()
        self.picbedshower = PicBedShower()  # 需要动态修改
        self.midvbox.addWidget(self.picbedshower)

        # TODO:或者用dockwidget
        self.rightvbox = QVBoxLayout()

        hbox = QHBoxLayout(self)  # 设置整体布局
        hbox.setMargin(5)
        hbox.addLayout(self.leftvbox, 2)
        hbox.addLayout(self.midvbox, 6)
        hbox.addLayout(self.rightvbox, 1)

    # 点击新建图床
    # @param btn:新建的按钮
    @Slot(QPushButton)
    def newPicBed(self, btn: QPushButton) -> None:
        ok, newPicBed = AddPicBedDialog().getBedinfo()
        if ok:
            self.bedPool[btn] = newPicBed
            btn.setText(newPicBed.verboseName)
            self.bedDBthread.insertBed(newPicBed)
        else:
            # 取消时删除按钮
            btn.deleteLater()

    # 删除图床按钮
    @Slot()
    def delPicBed(self, btn: QPushButton):
        self.bedDBthread.deleteBed(self.bedPool[btn])  # 数据库中删除图床信息
        self.bedPool.pop(btn)  # 清理

    # TODO:点击图床按钮
    @Slot(QPushButton)
    def clickPicBed(self, btn: QPushButton):
        btn.setDown(True)
        self.picbedshower.updateInfo(self.bedPool[btn])
        self.picbedshower.initAllPicShower()


    @Slot(list)
    # 初始化按钮功能，初始化图床信息
    def bedListBtnInit(self, object:list):
        for iterm in object:
            index = self.bedListQbtn.layUp.count()  # 添加的按钮在布局中的索引位置，起始0
            button = QPushButton(iterm.verboseName)
            button.clicked.connect(lambda: self.bedListQbtn.button_clicked(button))

            button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

            def on_context_menu(point):
                # 弹出菜单
                menu.exec_(button.mapToGlobal(point))  # 把相对于按钮的位置转为相对于全局的位置

            button.setContextMenuPolicy(Qt.CustomContextMenu)  # 菜单策略，自定义
            button.customContextMenuRequested.connect(on_context_menu)  # 触发信号

            # 设置右击删除菜单
            menu = QMenu(button)
            delQAction = QAction("删除", button)
            delQAction.triggered.connect(lambda: self.bedListQbtn.deleteButton(button))
            menu.addAction(delQAction)

            self.bedListQbtn.layUp.insertWidget(index, button)  # 添加按钮到布局中

            self.bedPool[button] = iterm  # 关联图床与按钮


    def resizeEvent(self, event: QResizeEvent):
        # 调节侧边ToolBox的高度与整个窗口一致，宽度为推荐宽度
        self.picRepository.resize(
            self.picRepository.width(), self.height()-10)  # 高度-10，让出状态栏的大小


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("MdPic")
        self.resize(600, 600)
        self.statusBar()  # 创建状态栏
        self.creatMenu()  # 创建菜单
        # 设置中心控件
        self.main = PicManager()
        self.setCentralWidget(self.main)

    def creatMenu(self):
        '''生成菜单栏'''
        # view菜单
        viewMenu = self.menuBar().addMenu("&View")
        logWinQact = QAction(r"日志", parent=viewMenu)
        # logWinQact.setToolTip(r"日志")
        logWinQact.setStatusTip(r"日志")
        logWinQact.setCheckable(True)
        logWinQact.triggered.connect(
            lambda: self.showLogWin(logWinQact.isChecked()))
        viewMenu.addAction(logWinQact)
        # about菜单
        aboutMenu = self.menuBar().addMenu("&About")
        aboutQact = QAction("About &Qt", self,
                            triggered=QApplication.instance().aboutQt)
        aboutMenu.addAction(aboutQact)

    # TODO:显示or不显示日志栏
    def showLogWin(self, flag):
        '''是否显示日志窗口

        Args:
            flag(bool):True显示窗口
        '''
        print(flag)
