from data.register_returncode_enum import EnumRegisterStatus
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="register_path",data="register.yml")
class Register(CASE):
    '''邮箱或手机号注册'''

    case_list=[]        #存放各实例方法

    @loadcase(case_list)
    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)
        params_dict['appkey'] = '199999'
        status_error_code = EnumRegisterStatus.APPKEY_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def email_invalid(self):
        '''格式错误-registion_type的值为0时email格式不正确'''

        params_dict = dict(self.initparams)
        params_dict['registion_type'] = 0
        params_dict['email'] = '123@'
        status_error_code = EnumRegisterStatus.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def mobile_invalid(self):
        '''格式错误-registion_type的值为1时mobile格式不正确'''

        params_dict = dict(self.initparams)
        params_dict['registion_type'] = 1
        params_dict['mobilephone'] = 1881134925
        status_error_code = EnumRegisterStatus.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def registiontype_not_0_1(self):
        '''注册类型非0 非1'''

        params_dict = dict(self.initparams)
        params_dict['registion_type'] = 10
        status_error_code = EnumRegisterStatus.REGISTER_TYPE_BEYOND_0_1.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def email_already_indb(self):
        '''邮箱地址注册 已在库'''
        params_dict = dict(self.initparams)
        params_dict['registion_type'] = 0

        # email 替换为已在库的email
        sql="select cust_email from customer where cust_status!=-1 " \
            " and cust_email REGEXP '^[_A-Za-z0-9]+@([_A-Za-z0-9]+.)+[A-Za-z0-9]{2,3}$' limit 1"

        params_dict['email'] = PyMySQL().mysqlget(sql)
        status_error_code = EnumRegisterStatus.EMAIL_EXISTS.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def mobile_already_indb(self):
        '''手机号注册 已在库'''
        params_dict = dict(self.initparams)
        params_dict['registion_type'] = 1

        # email 替换为已在库的email
        sql = "select cust_mobile from customer where cust_status!=-1 " \
              " and length(cust_mobile)=11 limit 1"

        params_dict['mobilephone'] = PyMySQL().mysqlget(sql)
        status_error_code = EnumRegisterStatus.MOBILE_PHONE_EXISTS.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def register_success(self):
        '''参数正确，往customer库的Customers表里插入用户注册数据操作成功'''
        params_dict = dict(self.initparams)
        status_error_code = EnumRegisterStatus.SUCCESS.value

        return params_dict, status_error_code


        pass


def teardown_module():
    '''用例结果数据销毁'''
    mysql_cursor = PyMySQL()

    #手机号注册
    if Register.initparams['registion_type']==1:


        sql="select cust_id from customer where cust_mobile='"+str(Register.initparams['mobilephone'])+"'"

        column='cust_mobile'
        column_='mobilephone'

    else:   #邮箱注册
        sql = "select cust_id from customer where cust_email='" + Register.initparams['email']+"'"

        column = 'cust_email'
        column_ = 'email'

    custid = mysql_cursor.mysqlget(sql)
    mysql_cursor.mysqldel('customer', {column: str(Register.initparams[column_])})
    mysql_cursor.mysqldel('customer_detail', {'cust_id': custid})

    pass

@pytest.fixture(params=Register.casedata(Register.case_list))
def myfixture(request):
    return request.param

@pytest.mark.register
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Register(myfixture):

    #请求
    url=Register.url
    data=myfixture[0]
    # print(data)
    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #注册成功的话，检查其他字段




