import pytest
import allure
from utils.requesttool import request,loadcase
from utils.pysql import PyMySQL,PyMySQL_EXECUTE
from utils.loaddata import LoadEnvData

class CASE():

    # case_list = []
    @classmethod
    def casedata(cls,case_list):
        cls_instance = cls()
        datalist = [ele(cls_instance) for ele in case_list]
        return datalist
