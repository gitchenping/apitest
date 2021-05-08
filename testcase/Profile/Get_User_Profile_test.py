import os
import pytest
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.get_user_profile_returncode_enum import GetUserProfileReturnCodeEnum

from utils.requesttool import loadcase

GetUserProfilecaselist=[]

@LoadEnvData(host="test_profileapi",path="get_user_profile_path",data="get_user_profile.yml")
class GetUserProfile():

    def __init__(self):

        pass

    # @loadcase(GetUserProfilecaselist)
    def custid_invalid(self):
        '''custid不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符

        params_dict['cust_id'] = "123xxx"
        status_error_code = GetUserProfileReturnCodeEnum.CUSTID_WRONG.value

        return params_dict, status_error_code

    # @loadcase(GetUserProfilecaselist)
    def keyword_invalid(self):
        '''keyword不正确'''
        params_dict = dict(self.initparams)

        params_dict['cust_id'] = self.cf_presetvar.get('profile','cust_id')
        # keyword替换为非法字符

        params_dict['keyword'] = "xxxxxx"
        status_error_code = GetUserProfileReturnCodeEnum.KEWWORDWRONG.value

        return params_dict, status_error_code

    # @loadcase(GetUserProfilecaselist)
    def empty_search(self):
        params_dict = dict(self.initparams)

        params_dict['cust_id'] = '12345678'     #custid不存在
        params_dict['keyword']=''
        status_error_code = GetUserProfileReturnCodeEnum.EMPTYINFO.value

        return params_dict, status_error_code

    @loadcase(GetUserProfilecaselist)
    def getuserprofile_success(self):
        '''获取用户档案信息成功'''

        params_dict = dict(self.initparams)

        params_dict['cust_id'] = self.cf_presetvar.get('profile', 'cust_id')

        status_error_code = GetUserProfileReturnCodeEnum.SUCCESS.value

        params_dict_list = []
        # keyword展开
        for ele in params_dict['keyword']:

            params_dict['keyword']=ele

            params_dict_list.append((params_dict,status_error_code))

        return params_dict_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表

getuserprofile = GetUserProfile()
datalist=[ele(getuserprofile) for ele in GetUserProfilecaselist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param


@pytest.mark.getuserprofile
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_GetUserProfile(pyfixture):

    #请求
    url=GetUserProfile.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['errorCode']==pyfixture[1][0]




