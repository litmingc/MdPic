"""
=================================================
自定义控件，按钮的纵向的列表，自带一个添加按钮。
@Author：LitMingC
@Last modified by：LitMingC/2020-07-22
=================================================
"""

debugFlag = True

from PySide2.QtCore import Qt, Signal, Slot
from PySide2.QtWidgets import QAction, QMenu, QVBoxLayout, QPushButton, QSizePolicy, QVBoxLayout, QWidget


class ButtonList(QWidget):

    # 按钮添加时发送信号
    # QPushButton为触发的按钮
    signalBtnAdded = Signal(QPushButton)
    signalBtnDeleted = Signal(QPushButton)
    signalBtnClicked = Signal(QPushButton)

    """按钮列表，默认有一个添加按钮的按钮"""
    def __init__(self, addStr: str, parent: any = None) -> None:
        '''按钮列表，默认有一个添加按钮的按钮

        Args:
            addStr(str):添加按钮上显示的文字
        '''
        super().__init__(parent=parent)

        self.addIterm = QPushButton(addStr, self)
        self.addIterm.setSizePolicy(
            QSizePolicy.Minimum, QSizePolicy.Fixed)
        # self.addIterm.resize(self.addIterm.sizeHint())
        self.addIterm.clicked.connect(self.addBtn_clicked)

        # 添加按钮布局
        self.layDown = QVBoxLayout()
        self.layDown.addWidget(self.addIterm)
        # 按钮布局，与addIterm所处的布局分开，防止删除按钮时布局的神秘错乱（我太菜了）
        self.layUp = QVBoxLayout()
        # 整体外布局
        lay = QVBoxLayout()
        lay.setMargin(3)  # 设置边距
        lay.addLayout(self.layUp)
        lay.addLayout(self.layDown)
        lay.addStretch(1)  # 添加拉伸因子，防止按钮由于父控件大小被纵向拉伸
        self.setLayout(lay)  # 应用布局

    @Slot()
    def addBtn_clicked(self) -> QPushButton:
        index = self.layUp.count()  # 添加的按钮在布局中的索引位置，起始0
        button = QPushButton('btn{}'.format(index))
        button.clicked.connect(lambda: self.button_clicked(button))

        button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)

        def on_context_menu(point):
            # 弹出菜单
            menu.exec_(button.mapToGlobal(point))  # 把相对于按钮的位置转为相对于全局的位置

        button.setContextMenuPolicy(Qt.CustomContextMenu)  # 菜单策略，自定义
        button.customContextMenuRequested.connect(on_context_menu)  # 触发信号

        # 设置右击删除菜单
        menu = QMenu(button)
        delQAction = QAction("删除", button)
        delQAction.triggered.connect(lambda: self.deleteButton(button))
        menu.addAction(delQAction)

        self.layUp.insertWidget(index, button)  # 添加按钮到布局中
        self.signalBtnAdded.emit(button)  # 发送添加信号
        return button

    @Slot(QPushButton)
    def deleteButton(self,button:QPushButton):
        self.signalBtnDeleted.emit(button)  # 发送删除信号
        # self.layUp.removeWidget(button)  # 移除控件
        button.deleteLater()  # 删除控件
    
    @Slot(QPushButton)
    def button_clicked(self,button:QPushButton):
        self.signalBtnClicked.emit(button)  # 发送点击信号
