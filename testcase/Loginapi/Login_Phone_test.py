import pytest
import allure
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.login_phone_returncode_enum import LoginPhoneReturnCodeEnum
from utils.requesttool import loadcase

loginphonelist=[]

@LoadEnvData(host="test_loginapi",path="login_phone_path",data="login_phone.yml")
class LoingPhone():

    def __init__(self):
        pass

    @loadcase(loginphonelist)
    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)

        params_dict['appkey'] = '199999'
        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_APPKEY_NOT_ALLOW.value

        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def phone_empty(self):
        '''手机号为空'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = ''
        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def phone_invalid(self):
        '''手机号格式不正确'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = '1234567'
        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def password_empty(self):
        '''密码为空'''
        params_dict = dict(self.initparams)

        params_dict['password'] = ''
        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def ip_invalid(self):
        '''ip格式不正确'''
        params_dict = dict(self.initparams)

        params_dict['ip_address'] = '192.168.0.256'
        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def phone_in_redis_but_password_wrong(self):
        '''登录密码与redis中的不一致或通过密码登录，验证失败'''
        params_dict = dict(self.initparams)

        params_dict['password'] = '12344321'

        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_PASSWORD_FAIL.value
        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def custid_notexist(self):
        '''custid 不存在'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = '18811000881'
        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def custid_cancel(self):
        '''用户注销'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] =self.cf_presetvar.get('login', 'phone_cancel')
        status_error_code = LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(loginphonelist)
    def login_pwd_success(self):
        '''通过密码登录，验证通过'''
        params_dict = dict(self.initparams)

        status_error_code=LoginPhoneReturnCodeEnum.LOGIN_STATUS_CODE_SUCCESS.value

        return params_dict,status_error_code


loginphone=LoingPhone()
datalist=[ele(loginphone) for ele in loginphonelist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.login_phone
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_LoginPhone(pyfixture):

    #请求
    url=LoingPhone.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True









