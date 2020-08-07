'''
=================================================
获取图库中全部图片的链接信息
@Author：LitMingC
@Last modified by：LitMingC/2020-07
=================================================
'''
from PySide2.QtCore import QMutex, QMutexLocker, QThread, QWaitCondition


class HttpThread(QThread):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.funclist = []  # 请求url
        self.quit = False

    def stop(self):
        self.mutex.lock()
        self.quit = True
        self.condition.wakeOne()
        self.mutex.unlock()

        self.wait(20000)

    def doRequest(self, requestfunc: any):
        locker = QMutexLocker(self.mutex)
        self.funclist.append(requestfunc)
        if not self.isRunning():
            self.start(QThread.LowPriority)
        else:
            self.condition.wakeOne()

    def run(self):
        while not self.quit:
            if self.funclist:
                self.mutex.lock()
                tmp = self.funclist.pop(0)
                self.mutex.unlock()
                re = tmp()
            else:
                self.mutex.lock()
                self.condition.wait(self.mutex, 1000*60 *
                                    60*72)  # 72小时唤醒，forever有问题
                self.mutex.unlock()
