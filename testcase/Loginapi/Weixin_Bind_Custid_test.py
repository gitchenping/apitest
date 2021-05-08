import pytest
import allure
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from data.weixin_bind_custid_returncode_enum import WeixinBindCustidReturnCodeEnum
from utils.requesttool import loadcase

weixinbindcustidlist=[]

@LoadEnvData(host="test_loginapi",path="weixin_bind_custid_path",data="weixin_bind_custid.yml")
class Weixin_Bind_Custid():


    def __init__(self):
        pass

    @loadcase(weixinbindcustidlist)
    def custid_notindb(self):
        '''custid不存在'''

        params_dict = dict(self.initparams)

        status_error_code =WeixinBindCustidReturnCodeEnum.CUSTID_NOT_FIND.value

        return params_dict, status_error_code

    @loadcase(weixinbindcustidlist)
    def custid_binded(self):
        '''当前custid已绑定过其它微信'''
        params_dict = dict(self.initparams)

        #custid替换为库里已绑定过微信的custid
        params_dict['custid'] = self.cf_presetvar.get('login', 'cust_bind_weixin')

        status_error_code = WeixinBindCustidReturnCodeEnum.CUSTID_BINDED.value

        return params_dict, status_error_code

    @loadcase(weixinbindcustidlist)
    def weixin_binded(self):
        '''当前微信曾绑定过其它custid'''
        params_dict = dict(self.initparams)

        #1.从库里选择一个未绑定过微信的custid
        sql='select cust_id from customer where cust_id not in (select cust_id from customer_third_wechat) and cust_id>0 limit 1;'
        custid=PyMySQL().mysqlget(sql)

        #2.从库里选择一个微信union_id(该union_id必被绑定过）
        sql='select wx_union_id from customer_third_wechat where cust_bind_type=2 limit 1; '
        unionid = PyMySQL().mysqlget(sql)

        #3.更新组合参数
        params_dict['custid']=custid
        params_dict['union_id']=unionid

        status_error_code = WeixinBindCustidReturnCodeEnum.WEIXIN_BINDED.value

        return params_dict, status_error_code

    @loadcase(weixinbindcustidlist)
    def weixin_binc_custid_success(self):
        '''绑定成功'''
        params_dict = dict(self.initparams)

        # 1.从库里选择一个未绑定过微信的custid
        sql = 'select cust_id from customer where cust_id not in (select cust_id from customer_third_wechat)  and cust_id>0 limit 1 ;'
        custid = PyMySQL().mysqlget(sql)

        # 2.更新组合参数
        params_dict['custid'] = custid

        status_error_code = WeixinBindCustidReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

def teardown_module():
    '''用例结果数据销毁'''

    #删除customer_third_wechat表
    PyMySQL().mysqldel('customer_third_wechat', 'wx_union_id', Weixin_Bind_Custid.initparams['union_id'])

    #to do,其他表
    pass

weixinbainccustid=Weixin_Bind_Custid()
datalist=[ele(weixinbainccustid) for ele in weixinbindcustidlist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param


@allure.title('{pyfixture[1][1]}')
@pytest.mark.weixin_bind_custid
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_WeixinBindCustid(pyfixture):

    #请求
    url=Weixin_Bind_Custid.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['statusCode']==pyfixture[1][0]

    if res['statusCode']==WeixinBindCustidReturnCodeEnum.SUCCESS.value[0]:
        assert PyMySQL().checkdbok('customer_third_wechat','wx_union_id',Weixin_Bind_Custid.initparams['union_id']),'''未写入数据库'''
        #assert PyMySQL().checkdbok('customer_third_wechat', 'wx_union_id',"232412134"), '''未写入数据库'''
    #return res0.
