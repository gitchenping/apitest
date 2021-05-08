from data.login_sms_returncode_enum import LoginSmsReturnCodeEnum,LoginSmsDbResult
from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL,PyMySQL_EXECUTE
import datetime

@LoadEnvData(host="test_loginapi",path="login_sms_path",data="login_sms.yml")
class LoingSms(CASE):

    loginsmslist=[]

    def __init__(self):

        pass


    @loadcase(loginsmslist)
    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)

        params_dict['appkey'] = '199999'
        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_APPKEY_NOT_ALLOW.value

        return params_dict, status_error_code

    @loadcase(loginsmslist)
    def phone_empty(self):
        '''手机号为空'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = ''
        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    @loadcase(loginsmslist)
    def phone_invalid(self):
        '''手机号格式不正确'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = '1234567'
        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    def vcode_empty(self):
        '''密码为空'''
        params_dict = dict(self.initparams)

        params_dict['vcode'] = ''
        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    @loadcase(loginsmslist)
    def custid_notexist(self):
        '''custid 不存在'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = '18811000881'
        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(loginsmslist)
    def custid_cancel(self):
        '''用户注销'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] =self.cf_presetvar.get('login', 'phone_cancel')
        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code

        pass

    @loadcase(loginsmslist)
    def login_sms_fail(self):
        '''通过短信验证码登录，验证失败'''
        params_dict = dict(self.initparams)

        #通过appkey判断是否是短信登录(如：20020001, BD的android客户端短信登录；20010001, BD的iphone客户端短信登录)
        params_dict['appkey'] ='20020001'
        params_dict['vcode']='999999'

        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_SMS_FAIL.value
        return params_dict, status_error_code

        pass

    @loadcase(loginsmslist)
    def login_sms_success(self):
        '''通过短信验证码登录，验证通过'''

        params_dict = dict(self.initparams)

        status_error_code = LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_SUCCESS.value
        return params_dict, status_error_code


#初始化,插入一条验证码
def setup_module():
    mobile_phone=LoingSms.initparams['mobile_phone']

    #1.清除
    PyMySQL().mysqldel('customer_verify_sms',{'verify_mobile':mobile_phone})

    #2.插入
    #vcode='345678'
    #LoingSms.initparams['vcode']=vcode
    #已请求参数中的vcode作为构造值
    vcode=LoingSms.initparams['vcode']

    now = datetime.datetime.now()
    now_2=now+datetime.timedelta(days = 1)


    sql="insert into customer_verify_sms(cust_id,verify_mobile,verify_type,verify_code,verify_send_date," \
        "verify_date,verify_timeout_date,verify_status,creation_date) "\
              "values({},{},{},{},{},{},{},{},{});".format(0,'"'+str(mobile_phone)+ '"',7,'"'+str(vcode)+ '"', '"'+str(now)+ '"',
                                                           '"'+str(now)+ '"','"'+str(now_2)+'"',0,'"'+str(now)+'"')

    PyMySQL_EXECUTE()(sql)

#销毁数据
def teardown_function():

    PyMySQL().mysqldel('customer_login_log',{'login_ip':LoingSms.initparams['ip_address']})


@pytest.fixture(params=LoingSms.casedata(LoingSms.loginsmslist))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.login_sms
@pytest.mark.flaky(reruns=0,reruns_delay=10)
def test_LoginSms(pyfixture):

    #请求
    url=LoingSms.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    assert LoginSmsDbResult().dbcheckok(pyfixture) is True









