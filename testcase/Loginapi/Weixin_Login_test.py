import pytest
import allure
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from data.weixin_login_returncode_enum import WeixinLoginReturnCodeEnum
from utils.requesttool import loadcase

weixinloginlist=[]

@LoadEnvData(host="test_loginapi",path="weixin_login_path",data="weixin_login.yml")
class Weixin_Login():

    def __init__(self):

        pass

    @loadcase(weixinloginlist)
    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)

        params_dict['appkey'] = '199999'
        status_error_code = WeixinLoginReturnCodeEnum.LOGIN_STATUS_CODE_APPKEY_NOT_ALLOW.value

        return params_dict, status_error_code

    @loadcase(weixinloginlist)
    def unionid_empty(self):
        '''union_id为空'''
        params_dict = dict(self.initparams)

        params_dict['union_id'] = ''
        status_error_code = WeixinLoginReturnCodeEnum.LOGIN_STATUS_CODE_PARAM_FORMAT.value

        return params_dict, status_error_code

    @loadcase(weixinloginlist)
    def unionid_not_exist(self):
        '''union_id不存在'''
        params_dict = dict(self.initparams)

        params_dict['union_id'] = '999999999999888888881'               #该union_id随便造的
        status_error_code = WeixinLoginReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(weixinloginlist)
    def unionid_exist_but_notactive_but_bind(self):
        '''union_id存在,但未激活,但存在绑定关系'''
        params_dict = dict(self.initparams)

        #wx_use_status使用状态 0 休眠 1 激活
        sql="select wx_union_id from customer_third_wechat where " \
            "cust_status = 1 and wx_use_status != 1 and cust_bind_type!='' and wx_union_id !='' limit 1"

        params_dict['union_id'] =PyMySQL().mysqlget(sql)
        status_error_code = WeixinLoginReturnCodeEnum.LOGIN_STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code

    @loadcase(weixinloginlist)
    def unionid_exist_and_active(self):
        '''union_id存在,且已激活'''
        params_dict = dict(self.initparams)
        sql = "select wx_union_id from customer_third_wechat where " \
              "cust_status = 1 and wx_use_status = 1 and cust_bind_type!='' and wx_union_id !='' limit 1"

        params_dict['union_id'] = PyMySQL().mysqlget(sql)
        status_error_code = WeixinLoginReturnCodeEnum.LOGIN_STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code

    @loadcase(weixinloginlist)
    def unionid_custid_cancel(self):
        '''union_id对应的cust_id注销'''
        params_dict = dict(self.initparams)
        sql ="select cust_id from customer where cust_id in(select cust_id from customer_third_wechat" \
             " where cust_status = 1 and cust_bind_type !='' and wx_union_id !='') and cust_status=-1 limit 1"

        params_dict['union_id'] = PyMySQL().mysqlget(sql)
        status_error_code = WeixinLoginReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code



weixinlogin=Weixin_Login()
datalist=[ele(weixinlogin) for ele in weixinloginlist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.weixin_login
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_Weixin_Login(pyfixture):

    #请求
    url=Weixin_Login.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True









