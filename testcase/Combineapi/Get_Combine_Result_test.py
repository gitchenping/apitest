import os
import pytest
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.get_combine_result_returncode_enum import GetCombineResultReturnCodeEnum


@LoadEnvData(host="test_combineapi",path="get_combine_result_path",data="get_combine_result.yml")
class GetCombineResult():

    def __init__(self):

        pass

    def params_invalid(self):
        '''参数不正确-必填字段非法'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符
        params_dict['custid'] = "123xxx"
        status_error_code = GetCombineResultReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code

    def result_empty(self):
        '''参数不正确-必填字段为空'''
        params_dict = dict(self.initparams)

        # custid替换为不存在
        params_dict['custid'] = "1234567889"
        status_error_code = GetCombineResultReturnCodeEnum.RESULT_EMPTY.value

        return params_dict, status_error_code

    def getresult_ok(self):
        '''获取结果OK'''
        params_dict = dict(self.initparams)

        params_dict['custid'] = self.cf_presetvar.get('combine','combine_cust_id')
        status_error_code = GetCombineResultReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code



def data_list():

    data_driven_list=[]
    combineresult = GetCombineResult()

    data_driven_list+=[combineresult.params_invalid(), \
                       combineresult.result_empty(),\
                       combineresult.getresult_ok()

                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.getcombineresult
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_GetCombineResult(pyfixture):

    #请求
    url=GetCombineResult.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]




