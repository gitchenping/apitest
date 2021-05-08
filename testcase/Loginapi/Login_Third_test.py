import pytest
import allure
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from utils.pysql import PyMySQL
from utils.log import loginlogger,callback_log
from data.login_third_returncode_enum import LoginThirdReturnCodeEnum
from utils.requesttool import loadcase

loginthirdlist=[]

@LoadEnvData(host="test_loginapi",path="login_third_path",data="login_third.yml")
class LoingThird():
    '''第三方登录（仅供第三方登录调用）'''

    def __init__(self):
        pass

    @loadcase(loginthirdlist)
    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)

        params_dict['appkey'] = '199999'
        status_error_code = LoginThirdReturnCodeEnum.LOGIN_STATUS_CODE_APPKEY_NOT_ALLOW.value

        return params_dict, status_error_code

    @loadcase(loginthirdlist)
    def thirdid_not_exist(self):
        '''third_id既不是普通第三方id，也不是微信union_id'''
        params_dict = dict(self.initparams)

        params_dict['cust_third_id'] = 556677889900
        status_error_code = LoginThirdReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(loginthirdlist)
    def thirdid_no_customerinfo(self):
        '''third_id对应的cust_id被注销'''
        params_dict = dict(self.initparams)

        sql="select cust_third_id,third_id from customer_third where cust_status=-1 order by cust_third_id desc limit 1"

        custthird=PyMySQL().mysqlget(sql)
        params_dict['cust_third_id']=custthird[0]
        params_dict['third_id']=custthird[1]

        status_error_code = LoginThirdReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(loginthirdlist)
    def thirdid_success(self):
        '''三方登录成功'''
        params_dict = dict(self.initparams)

        sql = "select cust_third_id,third_id from customer_third where cust_status=1 and is_valid=1 order by cust_third_id desc limit 1"

        custthird = PyMySQL().mysqlget(sql)
        params_dict['cust_third_id'] = custthird[0]
        params_dict['third_id'] = custthird[1]

        status_error_code = LoginThirdReturnCodeEnum.LOGIN_STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code

loginthird=LoingThird()
datalist=[ele(loginthird) for ele in loginthirdlist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.login_third
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Loginthird(pyfixture,hook=callback_log):

    #请求
    url=LoingThird.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    if hook:  # 写日志,写在assert断言之前
        callback_log(url, data, res, loginlogger, return_msg=pyfixture[1][1])

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True










