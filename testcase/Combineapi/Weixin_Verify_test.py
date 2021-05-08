import pytest
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from data.weixin_verify_returncode_enum import WeixinVerifyReturnCodeEnum

@LoadEnvData(host="test_combineapi",path="weixin_verify_path",data="weixin_verify.yml")
class WeixinVerify():

    def __init__(self):

        pass

    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符
        params_dict['custid'] = "123xxx"
        status_error_code = WeixinVerifyReturnCodeEnum.PARAM_ILLEGAL.value

        return params_dict, status_error_code


    def verify_ok(self):
        '''账号合规'''
        params_dict = dict(self.initparams)

        #从库里选一个微信注册用户
        sql='select cust_id from customer_third_wechat where cust_id in (select cust_id from customer where  cust_mobile="" and ' \
            ' cust_email like "%ddmobile_user.com") ' \
            'and cust_bind_type=2 limit 1;'

        custid=PyMySQL().mysqlget(sql)
        params_dict['custid']=custid

        status_error_code = WeixinVerifyReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

    def verify_fail(self):
        '''账号不合规'''
        params_dict = dict(self.initparams)
        params_dict['custid']=self.cf_presetvar.get('combine','cust_bind_weixin')

        status_error_code = WeixinVerifyReturnCodeEnum.VERIFY_FAIL.value

        return params_dict, status_error_code


def data_list():

    data_driven_list=[]
    weixinverify = WeixinVerify()

    data_driven_list+=[weixinverify.params_invalid(), \
                       weixinverify.verify_ok(), \
                       weixinverify.verify_fail()

                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.weixinverify
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_WeixinVerify(pyfixture):
    #请求
    url=WeixinVerify.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]




