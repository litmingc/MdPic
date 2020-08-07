'''
=================================================
数据库相关操作函数
@Author：LitMingC
@Last modified by：LitMingC/2020-07
=================================================
'''
from PySide2.QtCore import QMutex, QMutexLocker, QThread, QWaitCondition, Signal
import sqlite3
from functools import partial
from src.picbedshower.model.models import *
from dataclasses import dataclass


class DBThread(QThread):
    @dataclass
    class ExecuteData:
        '''数据类，包含一次数据库处理的参数，信号等
        '''
        sql: str
        signal: object
        parameters: tuple = ()
        dealre: object = None

    signalBeds = Signal(object)  # 返回bed列表
    signalBedPics = Signal(object)  # 返回pic列表（某图库的）
    signaladdBed = Signal(object)  # 插入
    signaladdPic = Signal(object)  # 图片增
    signaldelBed = Signal(object)  # 删除
    signaldelPic = Signal(object)  # 图片删
    signalupdateBed = Signal(object)  # 图床更新

    def __init__(self, dbfile: str = None) -> None:
        super().__init__()
        if dbfile:
            self.connectFunc = partial(sqlite3.connect, dbfile)
        else:
            self.connectFunc = partial(sqlite3.connect, ":memory:")
        self.initDBsql()
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.dealList = []

    def initDBsql(self):
        dbcon = self.connectFunc()
        sql_create_picbed_table = '''
            DROP TABLE IF EXISTS "picbed_table";
            CREATE TABLE "picbed_table" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "owner" TEXT NOT NULL,
                "repo" TEXT NOT NULL,
                "verbose_name" TEXT,
                "branch" TEXT DEFAULT master,
                "path" TEXT,
                "access_token" TEXT,
                "custom_path" TEXT,
                "creat_time" TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                "update_time" TEXT
            );'''
        sql_create_pic_table = '''
            DROP TABLE IF EXISTS "pic_table";
            CREATE TABLE "pic_table" (
                "id" INTEGER NOT NULL,
                "filename" TEXT NOT NULL,
                "mdlink" TEXT NOT NULL,
                "selfurl" TEXT NOT NULL,
                "sha" TEXT NOT NULL,
                "parent" TEXT NOT NULL,
                "size" REAL,
                "content" TEXT,
                "create_time" TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                PRIMARY KEY ("id"),
                CONSTRAINT "parent" FOREIGN KEY ("parent") REFERENCES "picbed_table" ("id") ON DELETE CASCADE ON UPDATE CASCADE
            );'''
        cur = dbcon.execute(
            "select name from sqlite_master where type='table' and name in ('picbed_table', 'pic_table') order by name")
        if len(x := cur.fetchall()) < 2:  # 表不全
            dbcon.executescript(sql_create_picbed_table)
            dbcon.executescript(sql_create_pic_table)
        dbcon.close()

    def queryAllBed(self):
        sql = '''select id,owner,repo,verbose_name,branch,path,access_token,custom_path from picbed_table;'''

        def TOPicBedModel(iterms: list) -> list:
            result = []
            for iterm in iterms:
                result.append(PicBedModel(
                    id=iterm[0],
                    owner=iterm[1],
                    repo=iterm[2],
                    verboseName=iterm[3],
                    branch=iterm[4],
                    path=iterm[5],
                    access_token=iterm[6])
                )
            return result

        self.doExecute(sql, self.signalBeds, dealre=TOPicBedModel)

    def queryBedPics(self, index: int):
        # id图床的id
        sql = '''select id,filename,mdlink,selfurl,sha,size,content from pic_table where parent = {};'''.format(
            index)

        def PicToPicModel(iterms: list) -> list:
            result = []
            for iterm in iterms:
                result.append(PicModel(
                    id=iterm[0],
                    fileName=iterm[1],
                    mdLink=iterm[2],
                    selfurl=iterm[3],
                    sha=iterm[4],
                    parent=iterm[5],
                    size=iterm[6],
                    content=iterm[7]
                ))

        self.doExecute(sql, self.signalBedPics, dealre=PicToPicModel)

    # 插入图片
    def insertPic(self, iterm: PicModel):
        # sql = '''insert into pic_table (filename,mdlink,selfurl,sha,size,content,parent) values ({filename},{mdlink},{selfurl},{sha},{size},{content},{parent});'''\
        #     .format(
        #         filename=iterm.fileName,
        #         mdlink=iterm.mdLink,
        #         selfurl=iterm.selfurl,
        #         sha=iterm.sha,
        #         size=iterm.size,
        #         content=iterm.content,
        #         parent=iterm.parent
        #     )
        sql = '''insert into pic_table (filename,mdlink,selfurl,sha,size,content,parent) values (?,?,?,?,?,?,?);'''
        self.doExecute(sql, self.signaladdPic, sqlparameters=(
            iterm.fileName, iterm.mdLink, iterm.selfurl, iterm.sha, iterm.size, iterm.content, iterm.parent))

    # TODO：更新图片
    def updatePic(self, iterm: PicModel):
        pass

    # TODO: 根据id更新图床
    def updateBed(self, iterm: PicBedModel):
        sql = '''UPDATE picbed_table SET owner = ?,repo = ?,verbose_name = ?,branch = ?,path = ?,access_token = ?,custom_path = ? WHERE id = ?'''
        self.doExecute(sql, self.signalupdateBed, sqlparameters=(iterm.owner, iterm.repo,
                                                                 iterm.verboseName, iterm.branch, iterm.path,
                                                                 iterm.access_token, iterm.customPath, iterm.id))

    # 插入图床
    def insertBed(self, iterm: PicBedModel):
        # sql = '''insert into picbed_table (owner,repo,verbose_name,branch,path,access_token, custom_path) values ({owner},{repo},{verbose_name},{branch},{path},{access_token},{custom_path});'''\
        #     .format(owner=iterm.owner, repo=iterm.repo, verbose_name=iterm.verboseName, branch=iterm.branch,
        #             path=iterm.path, access_token=iterm.access_token, custom_path=iterm.customPath
        #             )
        sql = '''insert into picbed_table (owner,repo,verbose_name,branch,path,access_token, custom_path) values (?,?,?,?,?,?,?);'''
        self.doExecute(sql, self.signaladdPic, sqlparameters=(iterm.owner, iterm.repo, iterm.verboseName, iterm.branch,
                                                              iterm.path, iterm.access_token, iterm.customPath))

    # TODO:删除图片
    def deletePic(self, iterm: PicModel):
        sql = '''DELETE FROM pic_table WHERE id = ? '''
        self.doExecute(sql, self.signaldelBed, sqlparameters=(iterm.id))

    # TODO:删除图床
    def deleteBed(self, iterm: PicBedModel):
        sql = '''DELETE FROM picbed_table WHERE owner = ? and repo = ? and path = ?'''
        self.doExecute(sql, self.signaldelBed, sqlparameters=(
            iterm.owner, iterm.repo, iterm.path))

    def doExecute(self, sql, signal, *, sqlparameters: tuple = None, dealre=None):
        # sql语句
        # @param signal:发送sql结果，或者dealre处理的结果
        # @param dealre:可选参数，处理sql查询结果
        if not sqlparameters:  # 默认sql参数为空
            sqlparameters = ()
        locker = QMutexLocker(self.mutex)
        self.dealList.append((sql, sqlparameters, signal, dealre))
        if self.isRunning():
            self.condition.wakeOne()
        else:
            self.start(QThread.LowPriority)

    def run(self):
        dbcon = self.connectFunc()
        with dbcon:
            self.mutex.lock()
            if self.dealList:
                tmptuple = self.dealList.pop(0)
                re = dbcon.execute(tmptuple[0], tmptuple[1]).fetchall()
                if tmptuple[3]:
                    re = tmptuple[3](re)
                tmptuple[2].emit(re)
            else:
                self.condition.wait(self.mutex, 1000*60*60*72)
            self.mutex.unlock()
