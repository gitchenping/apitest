from data.get_user_info_by_mobilephone_returncode_enum import GetuserinfobymobilephoneReturnCodeEnum
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="get_user_info_by_mobilephone_path",data="get_user_info_by_mobilephone.yml")
class Get_USERINFO_by_Mobilephone(CASE):
    '''根据手机号取得用户信息'''
    case_list = []  # 存放各实例方法

    @loadcase(case_list)
    def mobile_not_exist(self):
        '''username不存在'''
        params_dict = dict(self.initparams)
        params_dict['mobilephone']=18888099999

        status_error_code = GetuserinfobymobilephoneReturnCodeEnum.USER_NOT_EXISTS.value


        return params_dict,status_error_code

    @loadcase(case_list)
    def success(self):
        '''参数正确，返回用户信息'''
        params_dict = dict(self.initparams)
        status_error_code = GetuserinfobymobilephoneReturnCodeEnum.SUCCESS.value

        return params_dict,status_error_code

@pytest.fixture(params=Get_USERINFO_by_Mobilephone.casedata(Get_USERINFO_by_Mobilephone.case_list))
def myfixture(request):
    return request.param

@pytest.mark.get_user_info_by_mobilephone
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Get_USERINFO_by_EmailNICKNAME(myfixture):

    #请求
    url=Get_USERINFO_by_Mobilephone.url
    data=myfixture[0]

    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #返回用户信息成功的话，检查字段信息