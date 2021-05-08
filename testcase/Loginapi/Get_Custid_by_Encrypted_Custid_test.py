from data.get_custid_by_encrypted_custid_returncode_enum import EnumCommonCode
from . import pytest, CASE, LoadEnvData, loadcase, request, PyMySQL


@LoadEnvData(host="test_loginapi", path="get_custid_by_encrypted_custid_path", data="get_custid_by_encrypted_custid.yml")
class Get_Custid_by_Encrypted_Custid(CASE):
    '''根据邮箱或手机取得加密的custid'''

    case_list = []  # 存放各实例方法

    @loadcase(case_list)
    def encrypted_custid_empty(self):
        '''encrypted_custid'''
        params_dict = dict(self.initparams)
        params_dict['encrypted_custid']=''

        status_error_code = EnumCommonCode.STATUS_CODE_PARAM_ERRO.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def username_not_exist(self):
        '''根据解密出的custid表读取的用户信息为空'''
        params_dict = dict(self.initparams)
        params_dict['encrypted_custid'] = 'eIF89z+j3t8Ig7Vdb74CCw=='

        status_error_code = EnumCommonCode.STATUS_CODE_USER_NOT_EXIST.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def success(self):

        params_dict = dict(self.initparams)
        params_dict['encrypted_custid'] = 'IVjiFeqzktsBG3obEt3P5w=='

        status_error_code = EnumCommonCode.ERROR_CODE_SUCCESS.value

        return params_dict, status_error_code



@pytest.fixture(params=Get_Custid_by_Encrypted_Custid.casedata(Get_Custid_by_Encrypted_Custid.case_list))
def myfixture(request):
    return request.param


@pytest.mark.get_encrypted_custid
@pytest.mark.flaky(reruns=1, reruns_delay=10)
def test_Get_Encrypted_Custid(myfixture):
    # 请求
    url = Get_Custid_by_Encrypted_Custid.url

    # for each_myfixture in myfixture:
    data = myfixture[0]
    # print(data)
    res = request(url=url, data=data)
    assert res['statusCode'] == myfixture[1][0]
    # 返回用户信息成功的话，检查字段信息




