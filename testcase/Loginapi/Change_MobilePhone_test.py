from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.change_mobilephone_returncode_enum import ChangeMobilePhoneReturnCodeEnum

@LoadEnvData(host="test_loginapi",path="change_mobilephone_path",data="change_mobilephone.yml")
class Change_MobilePhone(CASE):
    data_driven_list = []

    @loadcase(data_driven_list)
    def custid_empty(self):
        '''custid为空'''
        params_dict = dict(self.initparams)

        params_dict['custid'] = ''
        status_error_code = ChangeMobilePhoneReturnCodeEnum.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(data_driven_list)
    def mobilephone_invalid(self):
        '''手机号不合法'''
        params_dict = dict(self.initparams)

        params_dict['mobile_phone'] = '111222233333'
        status_error_code = ChangeMobilePhoneReturnCodeEnum.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(data_driven_list)
    def clientip_invalid(self):
        '''客户端ip错误'''
        params_dict = dict(self.initparams)

        params_dict['clientIP'] = '192.168.1.890'
        status_error_code = ChangeMobilePhoneReturnCodeEnum.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(data_driven_list)
    def operatorname_no(self):
        '''isFrontendCall为no时 operatorName参数为空'''
        params_dict = dict(self.initparams)
        params_dict['isFrontendCall']='no'

        params_dict['operatorName'] =''

        status_error_code = ChangeMobilePhoneReturnCodeEnum.STATUS_CODE_PARAM_ERROR.value
        return params_dict, status_error_code

    @loadcase(data_driven_list)
    def mobilephone_exist(self):
        '''新手机号已经存在'''
        params_dict = dict(self.initparams)
        status_error_code = ChangeMobilePhoneReturnCodeEnum.STATUS_CODE_CUST_MOBILE_EXISTS.value

        return params_dict, status_error_code

    @loadcase(data_driven_list)
    def custid_not_exist(self):
        '''custid不存在'''
        params_dict = dict(self.initparams)
        params_dict['mobile_phone']=18888118881      #保证手机号不存在
        params_dict['custid']=104401903883

        status_error_code=ChangeMobilePhoneReturnCodeEnum.STATUS_CODE_CUST_GET_NOT_EXISTS.value

        return params_dict,status_error_code

    @loadcase(data_driven_list)
    def success(self):
        '''新手机号修改成功'''
        params_dict = dict(self.initparams)
        params_dict['mobile_phone']=18811451515

        status_error_code = ChangeMobilePhoneReturnCodeEnum.STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code

def teardown_module():
    '''用例结果数据销毁'''

    #改回原来数据库的值
    PyMySQL().mysqlupdate('customer',{'cust_id':Change_MobilePhone.initparams['custid']},{'cust_mobile':Change_MobilePhone.initparams['mobile_phone']})

    #to do,其他表
    pass

@pytest.fixture(params=Change_MobilePhone.casedata(Change_MobilePhone.data_driven_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.change_mobilephone
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_ChangeMobilePhone(pyfixture):

    #请求
    url=Change_MobilePhone.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True









