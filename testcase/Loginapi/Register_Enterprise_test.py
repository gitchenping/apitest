from data.register_enterprise_returncode_enum import RegisterEnterpriseEnum
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="register_enterprise_path",data="register_enterprise.yml")
class Register_Enterprise(CASE):
    '''企业注册'''

    case_list=[]        #存放各实例方法

    @loadcase(case_list)
    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)
        params_dict['appkey'] = '199999'
        status_error_code = RegisterEnterpriseEnum.APPKEY_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def email_invalid(self):
        '''邮箱注册时，email格式不正确'''
        params_dict = dict(self.initparams)
        params_dict['registion_type']=0
        params_dict['email'] = '123@'

        status_error_code = RegisterEnterpriseEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def mobile_invalid(self):
        '''格式错误-registion_type的值为1时mobile格式不正确'''

        params_dict = dict(self.initparams)
        params_dict['registion_type'] = 1
        params_dict['mobilephone'] = 1881134925

        status_error_code = RegisterEnterpriseEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def country_province_town_quarter_id_empty(self):
        '''地址代码为空'''

        params_dict = dict(self.initparams)
        params_dict['city_id'] = ''

        status_error_code = RegisterEnterpriseEnum.FORMATTER_ERROR.value

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
        status_error_code = RegisterEnterpriseEnum.EMAIL_EXISTS.value

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

        status_error_code = RegisterEnterpriseEnum.MOBILE_PHONE_EXISTS.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def nickname_already_indb(self):
        '''昵称 已在库'''
        params_dict = dict(self.initparams)

        # nickname 替换为已在库的nickname

        params_dict['nickname'] =self.cf_presetvar.get('login', 'cust_nickname_enterprise')

        status_error_code = RegisterEnterpriseEnum.NICKNAME_EXISTS.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def success(self):
        '''参数正确，往customer库的Customers表里插入用户注册数据操作成功'''
        params_dict = dict(self.initparams)
        status_error_code = RegisterEnterpriseEnum.SUCCESS.value

        return params_dict, status_error_code


        pass


def teardown_module():
    '''用例结果数据销毁'''
    mysql_cursor = PyMySQL()

    #删除customer\customer_detail_enterprise

    customer_data={'cust_email':Register_Enterprise.initparams['email'],
                   'cust_mobile':Register_Enterprise.initparams['mobilephone']}

    PyMySQL().mysqldel('customer',customer_data)
    mysql_cursor.mysqldel('customer_detail_enterprise', {'cust_company': Register_Enterprise.initparams['company']})

    pass

@pytest.fixture(params=Register_Enterprise.casedata(Register_Enterprise.case_list))
def myfixture(request):
    return request.param

@pytest.mark.register_enterprise
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Register_Enterprise(myfixture):

    #请求
    url=Register_Enterprise.url
    data=myfixture[0]
    # print(data)
    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #注册成功的话，检查其他字段




