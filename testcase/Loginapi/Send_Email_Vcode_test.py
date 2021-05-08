from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.send_email_vcode_returncode_enum import EnumSendAndCheckEmailVcode

@LoadEnvData(host="test_loginapi",path="send_email_vcode_path",data="send_email_vcode.yml")
class Send_Email_Vcode(CASE):

    case_list=[]

    def __init__(self):
        pass


    @loadcase(case_list)
    def email_empty(self):
        '''email_vcode 为空'''
        params_dict = dict(self.initparams)

        params_dict['email'] = ''
        status_error_code =EnumSendAndCheckEmailVcode.FORMAT_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def email_invalid(self):
        '''email 非法'''
        params_dict = dict(self.initparams)
        params_dict['email']='xxxxx'

        status_error_code = EnumSendAndCheckEmailVcode.FORMAT_ERROR.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def verifytype_empty(self):
        '''verify_type 为空'''
        params_dict = dict(self.initparams)
        params_dict['verify_type']=''

        status_error_code=EnumSendAndCheckEmailVcode.FORMAT_ERROR.value

        return params_dict,status_error_code


    @loadcase(case_list)
    def verifytype_invalid(self):
        '''verify_type 非法'''
        params_dict = dict(self.initparams)
        params_dict['verify_type'] = '126'

        status_error_code = EnumSendAndCheckEmailVcode.VERIFY_TYPE_NOT_IN_CONF.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def success(self):
        '''成功'''
        params_dict = dict(self.initparams)

        status_error_code = EnumSendAndCheckEmailVcode.SUCCESS.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def over_max_send_times(self):
        '''超过最大发送次数'''
        params_dict = dict(self.initparams)
        params_dict['max_send_time']=1

        status_error_code = EnumSendAndCheckEmailVcode.READ_TIME_QT_MAX_SEND_TIME.value

        return params_dict, status_error_code



def teardown_module():
    '''用例结果数据销毁'''

    PyMySQL().mysqldel('customer_verify_email',{'verify_email':Send_Email_Vcode.initparams['email']})



@pytest.fixture(params=Send_Email_Vcode.casedata(Send_Email_Vcode.case_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.send_email_vcode
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_Send_Email_Vcode(pyfixture):

    #请求
    url=Send_Email_Vcode.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True