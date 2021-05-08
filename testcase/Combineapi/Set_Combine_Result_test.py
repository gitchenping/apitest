import pytest
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from utils.requesttool import loadcase
from data.set_combine_reslut_returncode_enum import SetCombineResultReturnCodeEnum

setcombineresultlist=[]

@LoadEnvData(host="test_combineapi",path="set_combine_result_path",data="set_combine_result.yml")
class SetCombineResult():

    def __init__(self):

        #custid
        sql="select cust_id,combine_cust_id from customer_combine where cust_id in (" \
            "select combine_cust_id from customer_combine) and combine_relation_type=1"

        custid,custid_child = PyMySQL().mysqlget(sql)

        self.initparams['custid'] = custid
        self.initparams['custid_child'] = custid_child

        #没有绑定的cust_id
        sql="select cust_id,combine_cust_id from customer_combine where cust_id not in (" \
            "select combine_cust_id from customer_combine) and combine_relation_type=1"

        self.custid_unbind,self.custid_child_inbind = PyMySQL().mysqlget(sql)

    @loadcase(setcombineresultlist)
    def params_invalid(self):
        '''参数不正确-custid不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符
        params_dict['custid'] = ""
        status_error_code = SetCombineResultReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code

    @loadcase(setcombineresultlist)
    def params_invalid_type(self):
        '''type类型不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符
        params_dict['type'] = "100"
        status_error_code = SetCombineResultReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code

    @loadcase(setcombineresultlist)
    def custid_child_nobind_relation(self):
        '''子账号没有绑定关系'''
        params_dict = dict(self.initparams)

        params_dict['custid'] = self.custid_unbind
        params_dict['custid_child'] = self.custid_child_inbind

        status_error_code = SetCombineResultReturnCodeEnum.CUSTID_NOT_EXIST.value
        return params_dict, status_error_code

    @loadcase(setcombineresultlist)
    def setresult_ok(self):
        '''合并结果写入OK'''
        params_dict = dict(self.initparams)

        status_error_code = SetCombineResultReturnCodeEnum.SUCCESS.value
        return params_dict, status_error_code

setcombineresult = SetCombineResult()
datalist = [ele(setcombineresult) for ele in setcombineresultlist]


def teardown_module():
    '''用例结果数据销毁'''
    data = {'cust_id': SetCombineResult.initparams['custid'],
            'combine_cust_id': SetCombineResult.initparams['custid_child']
            }
    # print(data)
    PyMySQL().mysqldel('customer_combine_process',data)


@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param


@pytest.mark.setcombineresult
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_SetCombineResult(pyfixture):

    #请求
    url=SetCombineResult.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]
    if res['return_code']==SetCombineResultReturnCodeEnum.SUCCESS.value[0]:
        #检查数据库日志
        data={'cust_id':SetCombineResult.initparams['custid'],
              'combine_cust_id': SetCombineResult.initparams['custid_child']
        }
        assert PyMySQL().checkdbok('customer_combine_process',data),'''写入数据库失败'''




