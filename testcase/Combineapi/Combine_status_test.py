import pytest
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from utils.requesttool import loadcase
from data.combine_status_returncode_enum import CombineStatusReturnCodeEnum

combinestatuslist=[]

@LoadEnvData(host="test_combineapi",path="combine_status_path",data="combine_status.yml")
class CombineStatus():

    def __init__(self):
        pass

    @loadcase(combinestatuslist)
    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符
        params_dict['custid'] = "123xxx"
        status_error_code = CombineStatusReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code

    @loadcase(combinestatuslist)
    def combine_notweixin(self):
        '''非微信账号，即主站账号'''

        params_dict = dict(self.initparams)

        #从库里获取一个主站账户
        sql='select cust_id from customer where cust_id not in (select cust_id from customer_third_wechat union ' \
            ' select cust_id from customer_third) and cust_id>0 limit 1'

        custid=PyMySQL().mysqlget(sql)
        params_dict['custid'] = custid
        status_error_code = CombineStatusReturnCodeEnum.NOT_WEIXIN.value

        return params_dict, status_error_code

    @loadcase(combinestatuslist)
    def combine_done(self):
        '''合并完成'''
        params_dict = dict(self.initparams)

        #在customer_third_wechat表中找到一条cust_bind_type=1（当当账户）的custid 或找一个绑定过微信的custid
        params_dict['custid'] =self.cf_presetvar.get('combine','cust_bind_weixin')
        status_error_code = CombineStatusReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

    @loadcase(combinestatuslist)
    def combine_notdo(self):
        '''未合并'''
        params_dict = dict(self.initparams)

        #从customer_third_wechat表中找到一条cust_bind_type=2（微信注册）的custid，该custid作为子账号在customer_combine表不存在
        sql='select cust_id from customer_third_wechat where ' \
            'cust_bind_type=2 and cust_id not in (select cust_id from customer_combine where combine_relation_type=1 ) limit 1'

        custid = PyMySQL().mysqlget(sql)
        params_dict['custid'] = custid

        status_error_code = CombineStatusReturnCodeEnum.NOT_COMBINED.value

        return params_dict, status_error_code

    @loadcase(combinestatuslist)
    def combine_doing(self):
        '''合并进行中'''
        params_dict = dict(self.initparams)

        #用主账号在customer_combine中combine_status=0的微信账号
        sql="select cust_id from customer_third_wechat where cust_id in (" \
            "select cust_id from customer_combine where combine_status=0) and cust_status!=-1 limit 1"

        #
        params_dict['custid'] = PyMySQL().mysqlget(sql)
        status_error_code = CombineStatusReturnCodeEnum.COMBINE_DOING.value

        return params_dict, status_error_code



combinestatus=CombineStatus()
datalist=[ele(combinestatus) for ele in combinestatuslist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@pytest.mark.combinestatus
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_CombineStatus(pyfixture):

    #请求
    url=CombineStatus.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]




