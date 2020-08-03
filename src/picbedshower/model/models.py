'''
=================================================
图床数据结构
@Author：LitMingC
@Last modified by：LitMingC/
=================================================
'''
from dataclasses import dataclass, field
import datetime as DT


def genTimeStr():
    return str(DT.datetime.now().strftime("%Y-%m-%d %H:%M"))


@dataclass
class PicBedModel:
    owner: str
    repo: str
    verboseName: str = field(default_factory=genTimeStr)
    branch: str = "master"
    path: str = ""
    access_token: str = ""
    customPath: str = None
    id: int = None

    # 请求图库目录下文件的api的url
    def getcontenturl(self, ref: str = "master"):
        return "https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{path}?ref={ref}"\
            .format(owner=self.owner, repo=self.repo, path=self.path, ref=ref)


@dataclass
class PicModel:
    fileName: str
    mdLink: str
    selfurl: str
    sha: str
    parent: PicBedModel
    size: int = None
    content: str = None
    id: int = None

    # 返回添加文件的POST方法的url，不包含其他数据
    def postcontenturl(self):
        return "https://gitee.com/api/v5/repos/{owner}/{repo}/contents/{path}/{filename}"\
            .format(owner=self.parent.owner, repo=self.parent.repo, path=self.parent.path, filename=self.filename)

    # DELETE的url
    def deleteurl(self):
        return self.postcontenturl()  # api的url与POST是一样的
