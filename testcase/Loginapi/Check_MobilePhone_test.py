import pytest
import allure
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.check_mobilephone_returncode_enum import CheckMobilePhoneReturnCodeEnum
from utils.requesttool import loadcase

checkmobilephonelist=[]

@LoadEnvData(host="test_loginapi",path="check_mobilephone_path",data="check_mobilephone.yml")
class Check_MobilePhone():

    def __init__(self):
        pass

    @loadcase(checkmobilephonelist)
    def mobilephone_empty(self):
        '''mobile_phone'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = ''
        status_error_code =CheckMobilePhoneReturnCodeEnum.FORMAT_ERROR.value

        return params_dict, status_error_code


    @loadcase(checkmobilephonelist)
    def mobilephone_not_exist(self):
        '''mobile_phone不存在'''
        params_dict = dict(self.initparams)
        params_dict['mobile_phone']=18811888811

        status_error_code=CheckMobilePhoneReturnCodeEnum.NOT_EXISTS.value

        return params_dict,status_error_code

    @loadcase(checkmobilephonelist)
    def mobilephone_exist(self):
        '''mobile_phone存在'''
        params_dict = dict(self.initparams)

        status_error_code = CheckMobilePhoneReturnCodeEnum.EXISTS.value

        return params_dict, status_error_code


checkmobilephone=Check_MobilePhone()
datalist=[ele(checkmobilephone) for ele in checkmobilephonelist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.check_mobilephone
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_CheckMobilePhone(pyfixture):

    #请求
    url=Check_MobilePhone.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    if data['mobile_phone'] !='':
         assert res['if_exist']==pyfixture[1][0]
    else:
         assert res['statusCode'] == pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True