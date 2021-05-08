import pytest
import allure
import random
from utils.requesttool import request
from utils.pysql import  PyMySQL
from utils.loaddata import LoadEnvData
from data.change_emailorpassword_returncode_enum import ChangeEmailorPasswordReturnCodeEnum
from utils.requesttool import loadcase

changeemailorpasswordlist=[]

@LoadEnvData(host="test_loginapi",path="change_email_or_password_path",data="change_emailorpassword.yml")
class Change_Email_or_Password():

    def __init__(self):
        pass

    @loadcase(changeemailorpasswordlist)
    def custid_empty(self):
        '''custid为空'''
        params_dict = dict(self.initparams)

        params_dict['custid'] = ''
        status_error_code = ChangeEmailorPasswordReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(changeemailorpasswordlist)
    def operator_empty(self):
        '''客服名字为空'''
        params_dict = dict(self.initparams)

        params_dict['operator'] = ''
        status_error_code = ChangeEmailorPasswordReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(changeemailorpasswordlist)
    def authkey_wrong(self):
        '''认证码错误'''
        params_dict = dict(self.initparams)

        params_dict['authKey'] = 'authkey'
        status_error_code = ChangeEmailorPasswordReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(changeemailorpasswordlist)
    def newemail_exist(self):
        '''新邮箱已存在'''
        params_dict = dict(self.initparams)
        params_dict['newPassword']=''     #密码置空

        sql=" select cust_email from customer where cust_email!='' limit 1"
        email=PyMySQL().mysqlget(sql)
        params_dict['newEmail'] =email

        status_error_code = ChangeEmailorPasswordReturnCodeEnum.EMAIL_EXISTS.value
        return params_dict, status_error_code

    @loadcase(changeemailorpasswordlist)
    def newemail_success(self):
        '''新邮箱更新成功'''
        params_dict = dict(self.initparams)

        params_dict['newEmail'] = params_dict['newEmail']+str(random.randint(1,200))
        status_error_code = ChangeEmailorPasswordReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

    @loadcase(changeemailorpasswordlist)
    def newpassword_same(self):
        '''新密码和支付密码相同'''
        params_dict = dict(self.initparams)

        status_error_code=ChangeEmailorPasswordReturnCodeEnum.NEW_PASS_IS_SAME.value

        return params_dict,status_error_code

    @loadcase(changeemailorpasswordlist)
    def newpassword_newemail_both_no_empty(self):
        '''新邮箱和新密码同时不为空'''
        params_dict = dict(self.initparams)

        status_error_code = ChangeEmailorPasswordReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code


changeemailpassword=Change_Email_or_Password()
datalist=[ele(changeemailpassword) for ele in changeemailorpasswordlist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.change_email_or_password
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_ChangeEmailPassword(pyfixture):

    #请求
    url=Change_Email_or_Password.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True









