import pytest
from utils.requesttool import request,loadcase
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from data.register_returncode_enum import EnumRegisterStatus
from utils import readyaml



alist=[1,[2,3,[5,6]]]

def platlist(alist):
    temp=[]
    for ele in alist:
        if not isinstance(ele,list):
            temp.append(ele)
        else:
            temp.extend(platlist(ele))
    return temp

print(platlist(alist))


