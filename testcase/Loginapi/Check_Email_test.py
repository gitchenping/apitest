from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.check_email_returncode_enum import CheckEmailReturnCodeEnum

@LoadEnvData(host="test_loginapi",path="check_email_path",data="check_email.yml")
class Check_Email(CASE):

    data_driven_list = []

    @loadcase(data_driven_list)
    def email_empty(self):
        '''邮箱为空'''
        params_dict = dict(self.initparams)
        params_dict['email'] = ''
        status_error_code =CheckEmailReturnCodeEnum.FORMAT_ERROR.value
        return params_dict, status_error_code

    @loadcase(data_driven_list)
    def email_not_exist(self):
        '''email不存在'''
        params_dict = dict(self.initparams)
        params_dict['email']='188881@188.com'
        status_error_code=CheckEmailReturnCodeEnum.NOT_EXISTS.value

        return params_dict,status_error_code

    @loadcase(data_driven_list)
    def email_exist(self):
        '''email存在'''
        params_dict = dict(self.initparams)

        status_error_code = CheckEmailReturnCodeEnum.EXISTS.value

        return params_dict, status_error_code

@pytest.fixture(params=Check_Email.casedata(Check_Email.data_driven_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.check_email
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_CheckEmail(pyfixture):

    #请求
    url=Check_Email.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    if data['email'] !='':
         assert res['if_exist']==pyfixture[1][0]
    else:
         assert res['statusCode'] == pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True