from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.check_sms_vcode_returncode_enum import EnumSendAndCheckSmsVcode
import datetime


@LoadEnvData(host="test_loginapi",path="check_sms_vcode_path",data="check_sms_vcode.yml")
class Check_Sms_Vcode(CASE):

    case_list=[]

    def __init__(self):
        pass


    @loadcase(case_list)
    def sms_vcode_empty(self):
        '''sms_vcode 为空'''
        params_dict = dict(self.initparams)

        params_dict['sms_vcode'] = ''
        status_error_code =EnumSendAndCheckSmsVcode.FORMAT_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def sms_vcode_invalid(self):
        '''sms_vcode 非法'''
        params_dict = dict(self.initparams)
        params_dict['sms_vcode']='9806'

        status_error_code = EnumSendAndCheckSmsVcode.FORMAT_ERROR.value
        return params_dict, status_error_code


    @loadcase(case_list)
    def verifytype_invalid(self):
        '''verify_type 非法'''
        params_dict = dict(self.initparams)
        params_dict['verify_type']='qw'

        status_error_code=EnumSendAndCheckSmsVcode.FORMAT_ERROR.value

        return params_dict,status_error_code

    @loadcase(case_list)
    def verifytype_not_in_conf(self):
        '''verify_type 非法'''
        params_dict = dict(self.initparams)
        params_dict['verify_type'] = 76

        status_error_code = EnumSendAndCheckSmsVcode.VERIFY_TYPE_NOT_IN_CONF.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def success(self):
        '''成功'''
        params_dict = dict(self.initparams)

        status_error_code = EnumSendAndCheckSmsVcode.SUCCESS.value

        return params_dict, status_error_code


def setup_module():
    '''用例数据初始化'''
    #向email_verify 表中插入一条数据
    s_date_date=datetime.datetime.now()
    s_date=s_date_date.strftime("%Y-%m-%d %H:%M:%S")
    e_date_date=s_date_date+datetime.timedelta(days=1)
    e_date=e_date_date.strftime("%Y-%m-%d %H:%M:%S")

    insert_data={
        'cust_id':Check_Sms_Vcode.initparams['custid'],
        'verify_mobile':Check_Sms_Vcode.initparams['mobile_phone'],
        'verify_type':Check_Sms_Vcode.initparams['verify_type'],
        'verify_code':Check_Sms_Vcode.initparams['sms_vcode'],
        'verify_send_date': s_date,
        'verify_timeout_date':e_date,
        'verify_status': 0,
        'creation_date':s_date
    }

    PyMySQL().mysqlinsert("customer_verify_sms",insert_data)

def teardown_module():
    '''用例结果数据销毁'''

    PyMySQL().mysqldel('customer_verify_sms',{
        'cust_id':Check_Sms_Vcode.initparams['custid'],
                       'verify_mobile':Check_Sms_Vcode.initparams['mobile_phone']})


    pass



@pytest.fixture(params=Check_Sms_Vcode.casedata(Check_Sms_Vcode.case_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.check_sms_vcode
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_Check_Sms_Vcode(pyfixture):

    #请求
    url=Check_Sms_Vcode.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True