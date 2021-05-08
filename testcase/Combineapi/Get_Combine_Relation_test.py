import pytest
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.get_combine_relation_returncode_enum import GetCombineRelationReturnCodeEnum
from utils.requesttool import loadcase

combinerelationlist=[]

@LoadEnvData(host="test_combineapi",path="get_combine_relation_path",data="get_combine_relation.yml")
class GetCombineRelation():

    def __init__(self):
        pass

    @loadcase(combinerelationlist)
    def params_invalid(self):
        '''参数不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符
        params_dict['custid'] = "123xxx"
        status_error_code = GetCombineRelationReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return params_dict, status_error_code

    @loadcase(combinerelationlist)
    def get_combine_relation_success(self):
        '''获取账户主子关系成功'''
        params_dict = dict(self.initparams)
        params_dict['custid']=self.cf_presetvar.get('combine','combine_cust_id')

        status_error_code = GetCombineRelationReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

combinerelation = GetCombineRelation()
datalist=[ele(combinerelation) for ele in combinerelationlist]


def teardown_module():
    '''用例结果数据销毁'''
    pass




@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param


@pytest.mark.get_combine_relation
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=GetCombineRelation.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['return_code']==pyfixture[1][0]




