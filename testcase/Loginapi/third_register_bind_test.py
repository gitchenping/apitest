from data.third_register_bind_returncode_enum import ThirdRegisterBindStatusEnum
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL
import datetime

@LoadEnvData(host="test_loginapi",path="third_register_bind_path",data="third_register_bind.yml")
class Third_Register_Bind(CASE):
    '''第三方注册绑定 '''

    case_list=[]                    #存放各实例方法

    def __init__(self):
        # self.mobile_indb=''
        pass


    @loadcase(case_list)
    def third_id_empty(self):
        '''third_id为空'''
        params_dict = dict(self.initparams)
        params_dict['cust_third_id'] = ''
        status_error_code = ThirdRegisterBindStatusEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def mobile_invalid(self):
        '''格式错误-mobile格式不正确'''

        params_dict = dict(self.initparams)
        params_dict['mobile'] = 1881134925
        status_error_code = ThirdRegisterBindStatusEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def cust_third_id_binded(self):
        '''cust_third_id 已经被绑定过'''

        params_dict = dict(self.initparams)

        #从数据库中查出一个cust_third_id
        sql="select cust_third_id from customer_third " \
            "where third_id=1105 and cust_status!=-1 limit 1"

        params_dict['cust_third_id'] =PyMySQL().mysqlget(sql)
        status_error_code = ThirdRegisterBindStatusEnum.CUST_THIRD_ID_IS_BIND.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def mobile_not_exist_and_vcode_empty(self):
        '''手机号不在库且没验证码'''

        params_dict = dict(self.initparams)
        params_dict['vcode']=''

        status_error_code = ThirdRegisterBindStatusEnum.VCODE_NOT_EXISTS_MOBILE_NOT_EXISTS.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def mobile_exist_and_vcode_empty(self):
        '''手机号在库但没验证码'''

        params_dict = dict(self.initparams)

        sql = "select cust_mobile from customer where cust_id in (select cust_id from customer_third " \
               "where third_id=1105 and cust_status!=-1) and cust_mobile!='' limit 1"
        mobile_indb = PyMySQL().mysqlget(sql)

        params_dict['mobile'] =mobile_indb
        params_dict['vcode']=''


        status_error_code = ThirdRegisterBindStatusEnum.MOBILEPHONE_IS_BIND.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def vcode_fail(self):
        '''当当线上新用户短信验证码校验失败'''

        params_dict = dict(self.initparams)
        params_dict['vcode'] = '123456'

        status_error_code = ThirdRegisterBindStatusEnum.SMS_VERIFY_FAIL.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def mobile_exist_and_vcode_empty(self):
        '''有验证码，但手机号已被绑定'''

        params_dict = dict(self.initparams)

        # sql = "select cust_mobile from customer where cust_id in (select cust_id from customer_third " \
        #       "where third_id=1105 and cust_status!=-1) and cust_mobile!='' limit 1"
        mobile_indb = self.cf_presetvar.get('login','cust_mobile_bind_third')    #取预设值

        params_dict['mobile'] = mobile_indb


        status_error_code = ThirdRegisterBindStatusEnum.MOBILEPHONE_IS_BIND.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def register_success(self):
        '''有验证码，未绑定过，注册成功'''
        params_dict = dict(self.initparams)

        vcode= params_dict['vcode']
        mobile= params_dict['mobile']                          #一个不在库的手机号，
        # params_dict['mobile'] = mobile

        PyMySQL().mysqlupdate('customer_verify_sms', {'verify_code':vcode},{'verify_mobile':mobile})


        status_error_code = ThirdRegisterBindStatusEnum.SUCCESS.value

        return params_dict, status_error_code

        pass


def setup_module():

    #初始化，向customer_verify_sms插入一条数据，
    mobile=Third_Register_Bind.initparams['mobile']
    vcode = Third_Register_Bind.initparams['vcode']

    s_date = datetime.datetime.now()
    e_date=s_date+datetime.timedelta(days = 1)

    insert_data = {
        'cust_id': 0,
        'verify_mobile':Third_Register_Bind.cf_presetvar.get('login','cust_mobile_bind_third'),
        'verify_type': '9',
        'verify_code': vcode,
        'verify_send_date': str(s_date),
        'verify_timeout_date': str(e_date),
        'verify_status': 0,
        'verify_ip':'127.0.0.1',
        'creation_date': str(s_date)
    }

    PyMySQL().mysqlinsert('customer_verify_sms',insert_data)


def teardown_module():
    '''用例结果数据销毁'''
    mysql_cursor=PyMySQL()
    # 1.清除customer
    mysql_cursor.mysqldel('customer', {'cust_mobile': Third_Register_Bind.initparams['mobile']})
    #2、清除customer_third
    mysql_cursor.mysqldel('customer_third', {'cust_third_id': Third_Register_Bind.initparams['cust_third_id']})
    #3、清除customer_verify_sms
    mysql_cursor.mysqldel('customer_verify_sms', {'verify_code': Third_Register_Bind.initparams['vcode']})

    pass

@pytest.fixture(params=Third_Register_Bind.casedata(Third_Register_Bind.case_list))
def myfixture(request):
    return request.param

@pytest.mark.third_register_bind
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_Third_Register_Bind(myfixture):

    #请求
    url=Third_Register_Bind.url
    data=myfixture[0]
    # print(data)
    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #注册成功的话，检查其他字段




