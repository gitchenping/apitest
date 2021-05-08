from data.get_user_viptype_returncode_enum import EnumCommonCode
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="get_user_viptype_path",data="get_user_viptype.yml")
class Get_USER_Viptype(CASE):
    '''根据custid取得用户信息(读库) '''
    case_list = []                  # 存放各实例方法


    @loadcase(case_list)
    def custid_empty(self):
        '''custid为空'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = ''

        status_error_code = EnumCommonCode.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def custid_not_exist(self):
        '''custid不存在'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = 12333321

        status_error_code = EnumCommonCode.STATUS_CODE_CUST_GET_NOT_EXISTS.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def success(self):
        '''参数正确，返回用户信息'''
        params_dict = dict(self.initparams)

        status_error_code = EnumCommonCode.STATUS_CODE_SUCCESS.value

        return params_dict,status_error_code


@pytest.fixture(params=Get_USER_Viptype.casedata(Get_USER_Viptype.case_list))
def myfixture(request):
    return request.param

@pytest.mark.get_user_viptype
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Get_USER_Viptype(myfixture):

    #请求
    url=Get_USER_Viptype.url
    data=myfixture[0]

    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #返回用户信息成功的话，检查字段信息