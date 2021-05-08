from data.get_user_info_returncode_enum import GetuserinfoReturnCodeEnum
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="get_user_info_path",data="get_user_info.yml")
class Get_USER_INFO(CASE):
    '''根据custid取得用户信息(读库) '''
    case_list = []                  # 存放各实例方法

    @loadcase(case_list)
    def custid_not_exist(self):
        '''custid不存在'''
        params_dict = dict(self.initparams)
        params_dict['custid']=12333321

        status_error_code = GetuserinfoReturnCodeEnum.USER_NOT_EXISTS.value


        return params_dict,status_error_code

    @loadcase(case_list)
    def custid_empty(self):
        '''custid为空'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = ''

        status_error_code = GetuserinfoReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def success(self):
        '''参数正确，返回用户信息'''
        params_dict = dict(self.initparams)
        params_dict['custid']=self.cf_presetvar.get('login', 'cust_id')

        status_error_code = GetuserinfoReturnCodeEnum.SUCCESS.value

        return params_dict,status_error_code


@pytest.fixture(params=Get_USER_INFO.casedata(Get_USER_INFO.case_list))
def myfixture(request):
    return request.param

@pytest.mark.get_user_info
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Get_USER_INFO(myfixture):

    #请求
    url=Get_USER_INFO.url
    data=myfixture[0]

    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #返回用户信息成功的话，检查字段信息