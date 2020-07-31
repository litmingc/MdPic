'''
=================================================
获取图库中全部图片的链接信息
@Author：LitMingC
@Last modified by：LitMingC/2020-07
=================================================
'''
from PySide2.QtCore import QMutex, QMutexLocker, QThread, QWaitCondition, Signal


class HttpThread(QThread):

    signalRespose = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.funclist = []  # 请求url

    def doGet(self, requestfunc: any):
        locker = QMutexLocker(self.mutex)
        self.funclist.append(requestfunc)
        if not self.isRunning():
            self.start(QThread.LowPriority)
        else:
            self.condition.wakeOne()

    def run(self):
        while True:
            if self.funclist:
                self.mutex.lock()
                tmp = self.funclist.pop(0)
                self.mutex.unlock()
                re = tmp()
                self.signalRespose.emit(re)
            else:
                self.mutex.lock()
                self.condition.wait(self.mutex, 1000*60 *
                                    60*72)  # 72小时唤醒，forever有问题
                self.mutex.unlock()
