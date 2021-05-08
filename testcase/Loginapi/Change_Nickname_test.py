import pytest
import allure
import random
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.change_nickname_returncode_enum import ChangeNicknameReturnCodeEnum
from utils.requesttool import loadcase
from utils.pysql import PyMySQL
from utils.log import changenicknamelogger,callback_log

changenicknamelist=[]

@LoadEnvData(host="test_loginapi",path="change_nickname_path",data="change_nickname.yml")
class ChangeNickname():

    def __init__(self):
        pass


    @loadcase(changenicknamelist)
    def nickname_exist(self):
        '''新昵称已存在'''
        params_dict = dict(self.initparams)

        sql = "select cust_nickname from customer where cust_nickname !=''  limit 1"

        nickname = PyMySQL().mysqlget(sql)
        params_dict['new_nickname'] = nickname.strip(" ")
        params_dict['isFrontendCall']='no'
        status_error_code = ChangeNicknameReturnCodeEnum.NICKNAME_EXISTS.value

        return params_dict, status_error_code

    @loadcase(changenicknamelist)
    def params_custid_invalid(self):
        '''参数格式不正确'''
        params_dict = dict(self.initparams)

        params_dict['custid'] = ''
        status_error_code = ChangeNicknameReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(changenicknamelist)
    def params_type_invalid(self):
        '''参数格式不正确'''
        params_dict = dict(self.initparams)

        params_dict['type'] = ''
        status_error_code = ChangeNicknameReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(changenicknamelist)
    def clientIP_invalid(self):
        '''ip格式不正确'''
        params_dict = dict(self.initparams)

        params_dict['ip_address'] = '192.168.0.256'
        status_error_code = ChangeNicknameReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(changenicknamelist)
    def custid_notexist(self):
        '''custid 不存在'''
        params_dict = dict(self.initparams)

        params_dict['custid'] = '18811000881'
        status_error_code = ChangeNicknameReturnCodeEnum.USER_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(changenicknamelist)
    def success(self):
        '''更新成功'''
        params_dict = dict(self.initparams)

        params_dict['new_nickname'] = 'tester_'+str(random.randint(1,100))
        status_error_code = ChangeNicknameReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code


changenickname=ChangeNickname()
datalist=[ele(changenickname) for ele in changenicknamelist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.change_nickname
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_ChangeNickname(pyfixture,hook=callback_log):

    #请求
    url=ChangeNickname.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    if hook:  # 写日志,写在assert断言之前
        callback_log(url, data, res, changenicknamelogger,return_msg=pyfixture[1][1])

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True









