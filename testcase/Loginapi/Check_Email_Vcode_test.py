import pytest
import allure
import datetime
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from utils.pysql import PyMySQL
from data.check_email_vcode_returncode_enum import EnumSendAndCheckEmailVcode
from utils.requesttool import loadcase

checkemailvcodelist=[]

@LoadEnvData(host="test_loginapi",path="check_email_vcode_path",data="check_email_vcode.yml")
class Check_Email_Vcode():

    def __init__(self):
        pass

    @loadcase(checkemailvcodelist)
    def change_status_ne_0_1(self):
        '''change_status_flg 非0 非1'''
        params_dict = dict(self.initparams)

        params_dict['change_status_flg'] = '10'
        status_error_code = EnumSendAndCheckEmailVcode.FORMAT_ERROR.value

        return params_dict, status_error_code

    @loadcase(checkemailvcodelist)
    def emailvcode_empty(self):
        '''email_vcode 为空'''
        params_dict = dict(self.initparams)

        params_dict['email_vcode'] = ''
        status_error_code =EnumSendAndCheckEmailVcode.FORMAT_ERROR.value

        return params_dict, status_error_code

    @loadcase(checkemailvcodelist)
    def emailvcode_invalid(self):
        '''email_vcode 非法'''
        params_dict = dict(self.initparams)
        params_dict['email_vcode']='98068'

        status_error_code = EnumSendAndCheckEmailVcode.FORMAT_ERROR.value
        return params_dict, status_error_code

    @loadcase(checkemailvcodelist)
    def verifytype_invalid(self):
        '''verify_type 非法'''
        params_dict = dict(self.initparams)
        params_dict['verify_type']=76

        status_error_code=EnumSendAndCheckEmailVcode.VERIFY_TYPE_NOT_IN_CONF.value

        return params_dict,status_error_code

    @loadcase(checkemailvcodelist)
    def emailvcode_fail(self):
        '''读取有效验证码失败'''
        params_dict = dict(self.initparams)

        #设置有效期失效
        # PyMySQL().mysqlupdate('customer_verify_email',
        #                       {'cust_id': Check_Email_Vcode.initparams['custid'],'verify_email':Check_Email_Vcode.initparams['email']},
        #                       {'verify_timeout_date': '2021-04-20 17:14:43'})

        params_dict['custid'] = 987654321    #设置一个不存在的cust_id
        status_error_code =EnumSendAndCheckEmailVcode.READ_TIME_QT_MAX_SEND_TIME.value

        return params_dict, status_error_code

    @loadcase(checkemailvcodelist)
    def success(self):
        '''成功'''
        params_dict = dict(self.initparams)

        status_error_code = EnumSendAndCheckEmailVcode.SUCCESS.value

        return params_dict, status_error_code

def setup_module():
    '''用例数据初始化'''
    #向email_verify 表中插入一条数据
    s_date_date=datetime.datetime.now()
    s_date=s_date_date.strftime("%Y-%m-%d %H:%M:%S")
    e_date_date=s_date_date+datetime.timedelta(days=1)
    e_date=e_date_date.strftime("%Y-%m-%d %H:%M:%S")

    insert_data={
        'cust_id':Check_Email_Vcode.initparams['custid'],
        'verify_email':Check_Email_Vcode.initparams['email'],
        'verify_type':Check_Email_Vcode.initparams['verify_type'],
        'verify_code':Check_Email_Vcode.initparams['email_vcode'],
        'verify_send_date': s_date,
        'verify_timeout_date':e_date,
        'verify_status': 0,
        'creation_date':s_date
    }

    PyMySQL().mysqlinsert("customer_verify_email",insert_data)

def teardown_module():
    '''用例结果数据销毁'''

    #改回原来数据库的值
    PyMySQL().mysqldel('customer_verify_email',{
        'cust_id':Check_Email_Vcode.initparams['custid'],
                       'verify_email':Check_Email_Vcode.initparams['email']})

    #to do,其他表
    pass

changemailvcode=Check_Email_Vcode()
datalist=[ele(changemailvcode) for ele in checkemailvcodelist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.check_email_vcode
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_ChangeMobilePhone(pyfixture):

    #请求
    url=Check_Email_Vcode.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True