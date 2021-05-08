from data.register_third_returncode_enum import EnumRegisterStatus
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL
from utils.log import register_third_logger,callback_log

@LoadEnvData(host="test_loginapi",path="register_third_path",data="register_third.yml")
class Register_Third(CASE):
    '''第三方注册（仅供第三方注册调用）'''

    case_list=[]        #存放各实例方法

    @loadcase(case_list)
    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)
        params_dict['appkey'] = '199999'
        status_error_code = EnumRegisterStatus.APPKEY_ERROR.value

        return params_dict, status_error_code

    # @loadcase(case_list)
    def must_fill_field_empty(self):
        '''必填字段有一个为空'''

        params_dict = dict(self.initparams)
        params_dict['cust_third_id'] = ''
        params_dict['third_id'] = ''
        status_error_code = EnumRegisterStatus.FORMATTER_ERROR.value

        return params_dict, status_error_code

    # @loadcase(case_list)
    def email_exist(self):
        '''邮箱已经在库里'''

        params_dict = dict(self.initparams)
        params_dict['email'] = self.cf_presetvar.get('login', 'cust_email')
        status_error_code = EnumRegisterStatus.EMAIL_EXISTS.value

        return params_dict, status_error_code

    # @loadcase(case_list)
    def mobile_exist(self):
        '''手机号已经在库里'''

        params_dict = dict(self.initparams)
        params_dict['mobilephone'] = self.cf_presetvar.get('login','cust_mobile')
        status_error_code = EnumRegisterStatus.MOBILE_PHONE_EXISTS.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def cust_third_id_indb(self):
        '''cust_third_id 在customer_third_wechat表中存在'''
        params_dict = dict(self.initparams)
        params_dict['third_id'] = 200

        # cust_third_id 替换为已在库的union_id
        sql="select wx_union_id from customer_third_wechat where cust_status=1 limit 1"

        params_dict['cust_third_id'] = PyMySQL().mysqlget(sql)
        status_error_code = EnumRegisterStatus.DB_INSERT_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def qq_union_id_indb(self):
        '''qq_union_id 在customer_third_qq_openid表中存在'''
        params_dict = dict(self.initparams)
        params_dict['third_id'] = 6

        # cust_third_id 替换为已在库的qq_union_id
        sql = "select qq_union_id from customer_third_qq_openid where is_valid=1 limit 1"

        params_dict['qq_union_id'] = PyMySQL().mysqlget(sql)
        status_error_code = EnumRegisterStatus.DB_INSERT_ERROR.value

        return params_dict, status_error_code


    # @loadcase(case_list)
    def cust_third_id_already_bind(self):
        '''账号已经绑定过，重复绑定失败'''
        params_dict = dict(self.initparams)

        #
        sql = "select cust_third_id,third_id from customer_third where cust_status=1 limit 1"

        params_dict['cust_third_id'],params_dict['third_id'] = PyMySQL().mysqlget(sql)

        status_error_code = EnumRegisterStatus.DB_INSERT_ERROR.value

        return params_dict, status_error_code


    # @loadcase(case_list)
    def register_third_success(self):
        '''参数正确，普通第三方注册并绑定到third表成功'''
        params_dict = dict(self.initparams)
        status_error_code = EnumRegisterStatus.SUCCESS.value

        return params_dict, status_error_code

        pass


    # @loadcase(case_list)
    def register_third_bind_success(self):
        '''参数正确，mobile存在，特定第三方绑定成功（不注册）'''

        #特定third_id:CUST_THIRD_ID_IOS = 300;CUST_THIRD_ID_BAIDU = 1201;
        # CUST_THIRD_ID_FASTAPP = 1200
        params_dict = dict(self.initparams)

        params_dict['third_id']=300
        params_dict['mobilephone']=self.cf_presetvar.get('login','cust_mobile')

        status_error_code = EnumRegisterStatus.SUCCESS.value

        return params_dict, status_error_code

        pass


    # @loadcase(case_list)
    def register_third_success(self):
        '''参数正确，mobile不存在，特定第三方注册成功'''

        # 特定third_id:CUST_THIRD_ID_IOS = 300;CUST_THIRD_ID_BAIDU = 1201;
        # CUST_THIRD_ID_FASTAPP = 1200
        params_dict = dict(self.initparams)

        params_dict['third_id'] = 300
        # params_dict['mobilephone'] = self.cf_presetvar.get('login', 'cust_mobile')

        status_error_code = EnumRegisterStatus.SUCCESS.value

        return params_dict, status_error_code

        pass



def teardown_module():
    '''用例结果数据销毁'''
    mysql_cursor = PyMySQL()

    #删customer_third表
    mysql_cursor.mysqldel('customer_third',{'cust_third_id':Register_Third.initparams['cust_third_id']})

    #删customer表
    mysql_cursor.mysqldel('customer',{'cust_mobile':Register_Third.initparams['mobilephone']})

    pass

@pytest.fixture(params=Register_Third.casedata(Register_Third.case_list))
def myfixture(request):
    return request.param

@pytest.mark.register_third
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Register(myfixture,hook=callback_log):

    #请求
    url=Register_Third.url
    data=myfixture[0]
    # print(data)
    res=request(url=url,data=data)
    if hook:  # 写日志,写在assert断言之前
        callback_log(url, data, res, register_third_logger,return_msg=myfixture[1][1])
    assert res['statusCode']==myfixture[1][0]
    #注册成功的话，检查其他字段




