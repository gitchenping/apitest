import os
from .readini import readini
from .readyaml import readyml

#给每个类添加数据属性
def LoadData(obj):

    #添加数据属性
    father_path = os.path.dirname(os.path.dirname(__file__))
    presetvarinifilepath = os.path.join(father_path,"config", "presetvar.ini")
    testenvinifilepath =  os.path.join(father_path,"config", "testenv.ini")

    obj.cf_presetvar = readini(presetvarinifilepath)
    obj.cf_testenv = readini(testenvinifilepath)

    return obj



def LoadEnvData(**kwargs):

    def add(obj):
        # 添加数据属性
        father_path = os.path.dirname(os.path.dirname(__file__))
        presetvarinifilepath = os.path.join(father_path, "config", "presetvar.ini")
        testenvinifilepath = os.path.join(father_path, "config", "testenv.ini")
        yamlfilepath = os.path.join(father_path, "data", kwargs['data'])

        obj.cf_presetvar = readini(presetvarinifilepath)
        obj.cf_testenv = readini(testenvinifilepath)
        obj.initparams = readyml(yamlfilepath)

        '''
        for key,val in kwargs.items():
            setattr(obj,key,val)
        '''

        obj.url = obj.cf_testenv.get(kwargs['host'], 'host') + obj.cf_testenv.get(kwargs['host'],kwargs['path'])
        return obj
    return add

