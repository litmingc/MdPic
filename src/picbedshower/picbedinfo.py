"""
=================================================
图库信息，仓库地址，授权信息
@Author：LitMingC
@Last modified by：LitMingC/2020-07-23
=================================================
"""

from dataclasses import dataclass, field


@dataclass
class PicBedInfo():
    username:str
    repository:str
    accessToken:str
    url:str
    branch:str = "master"
    path:str = ""
