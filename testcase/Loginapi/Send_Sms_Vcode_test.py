from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.send_sms_vcode_returncode_enum import EnumStatusCode
import datetime


@LoadEnvData(host="test_loginapi",path="send_sms_vcode_path",data="send_sms_vcode.yml")
class Send_Sms_Vcode(CASE):

    case_list=[]

    def __init__(self):
        self.moible_for_ip_limit=18318318318
        self.ip_limit="192.168.168.168"

        pass


    @loadcase(case_list)
    def mobile_phone_empty(self):
        '''mobile_phone为空'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = ''
        status_error_code =EnumStatusCode.PARAM_ILLEGAL.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def verifytype_invalid(self):
        '''verify_type 不在配置文件中非法'''
        params_dict = dict(self.initparams)
        params_dict['verify_type']=0

        status_error_code=EnumStatusCode.VERIFY_TYPE.value

        return params_dict,status_error_code

    @loadcase(case_list)
    def verifytype_empty(self):
        '''verify_type 为空'''
        params_dict = dict(self.initparams)
        params_dict['verify_type'] = ''

        status_error_code = EnumStatusCode.PARAM_ILLEGAL.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def custid_not_in_db(self):
        '''verify_type 非注册、线下，cust不在库'''
        params_dict = dict(self.initparams)
        params_dict['verify_type'] = 6

        params_dict['custid']=18878868898

        status_error_code = EnumStatusCode.CUST_NOT_FIND.value

        return params_dict, status_error_code

    # @loadcase(case_list)
    def book_store_sms_over_1000(self):
        '''线下实体书店24小时内发送数量超过1000条'''
        params_dict = dict(self.initparams)
        params_dict['verify_type'] = 9

        status_error_code = EnumStatusCode.BOOKSTORE_MAX_TIMES.value

        return params_dict, status_error_code

        pass

    @loadcase(case_list)
    def sms_exceed_max_times(self):
        '''(根据mobile、verify_type)超过24小时内的短信发送次数限制'''
        params_dict = dict(self.initparams)
        params_dict['max_send_time'] = 0

        status_error_code = EnumStatusCode.MAX_TIMES.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def sms_denied_in_2_minutes(self):
        '''(根据mobile)2分钟内不能再次发送'''
        params_dict = dict(self.initparams)

        status_error_code = EnumStatusCode.TIME_INTERVAL.value

        return params_dict, status_error_code

    # @loadcase(case_list)
    def sms_exceed_ip_limit(self):
        '''(根据ip)10分钟内超过1000次'''

        params_dict = dict(self.initparams)
        params_dict['mobile_phone']=self.moible_for_ip_limit
        params_dict['ip_address']=self.ip_limit

        status_error_code = EnumStatusCode.IP_LIMIT.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def sms_send_success(self):
        ''''''

        params_dict = dict(self.initparams)
        params_dict['mobile_phone'] = self.moible_for_ip_limit
        params_dict['ip_address'] = self.ip_limit

        status_error_code = EnumStatusCode.SUCCESS.value

        return params_dict, status_error_code



def setup_module():
    '''用例数据初始化'''
    #向verify_sms 表中插入一条数据
    s_date_date=datetime.datetime.now()
    s_date=s_date_date.strftime("%Y-%m-%d %H:%M:%S")
    e_date_date=s_date_date+datetime.timedelta(days=1)
    e_date=e_date_date.strftime("%Y-%m-%d %H:%M:%S")

    insert_data={
        'cust_id':Send_Sms_Vcode.initparams['custid'],
        'verify_mobile':Send_Sms_Vcode.initparams['mobile_phone'],
        'verify_type':Send_Sms_Vcode.initparams['verify_type'],
        'verify_code':'',
        'verify_send_date': s_date,
        'verify_timeout_date':e_date,
        'verify_status': 0,
        'creation_date':s_date
    }

    PyMySQL().mysqlinsert("customer_verify_sms",insert_data)

    #其他验证码，用于测试ip 限制条数
    # for i in range(5):
    #     insert_data['verify_ip']=Send_Sms_Vcode().ip_limit
    #     insert_data['verify_mobile']=''
    #
    #     PyMySQL().mysqlinsert("customer_verify_sms", insert_data)



def teardown_module():
    '''用例结果数据销毁'''

    PyMySQL().mysqldel('customer_verify_sms',{
        'verify_mobile':Send_Sms_Vcode.initparams['mobile_phone']})
    PyMySQL().mysqldel('customer_verify_sms', {
        'verify_mobile': Send_Sms_Vcode().moible_for_ip_limit})

    pass



@pytest.fixture(params=Send_Sms_Vcode.casedata(Send_Sms_Vcode.case_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.send_sms_vcode
@pytest.mark.flaky(reruns=0,reruns_delay=5)
def test_Check_Sms_Vcode(pyfixture):

    #请求
    url=Send_Sms_Vcode.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True