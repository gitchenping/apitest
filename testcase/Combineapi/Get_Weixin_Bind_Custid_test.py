import pytest
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from data.get_weixin_bind_custid_returncode_enum import GetWeixinBindCustidReturnCodeEnum
from utils.requesttool import loadcase

getweixinbindcustidlist=[]

@LoadEnvData(host="test_combineapi",path="get_weixin_bind_custid_path",data="get_weixin_bind_custid.yml")
class GetWeixinBindCustid():
    def __init__(self):

        pass

    @loadcase(getweixinbindcustidlist)
    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # unionid替换为非法字符
        params_dict['unionid'] = ""
        status_error_code = GetWeixinBindCustidReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code

    @loadcase(getweixinbindcustidlist)
    def weixin_notbind_custid(self):
        '''未绑定'''
        params_dict = dict(self.initparams)

        #从库里获取一个未绑定的账户
        sql='select wx_union_id from customer_third_wechat where cust_bind_type=2 limit 1; '

        unionid=PyMySQL().mysqlget(sql)
        params_dict['unionid'] = unionid

        status_error_code = GetWeixinBindCustidReturnCodeEnum.NOT_COMBINED.value

        return params_dict, status_error_code

    @loadcase(getweixinbindcustidlist)
    def weixin_bind_custid(self):
        '''已绑定'''
        params_dict = dict(self.initparams)
        params_dict['unionid'] = self.cf_presetvar.get('combine','cust_bind_weixin_unionid')

        status_error_code = GetWeixinBindCustidReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表

getweixinbindcustid = GetWeixinBindCustid()
datalist=[ele(getweixinbindcustid) for ele in getweixinbindcustidlist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param


@pytest.mark.getweixinbindcustid
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_GetWeixinBindCustid(pyfixture):

    #请求
    url=GetWeixinBindCustid.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]




