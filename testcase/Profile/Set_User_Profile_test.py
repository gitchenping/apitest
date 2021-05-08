import os
import pytest
from utils.requesttool import request
from utils.readyaml import readyml
from utils.loaddata import LoadEnvData
from data.set_user_profile_returncode_enum import SetUserProfileReturnCodeEnum

@LoadEnvData(host="test_profileapi",path="set_user_profile_path",data="set_user_profile.yml")
class SetUserProfile():


    def __init__(self):

        pass

    def custid_invalid(self):
        '''custid不正确'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符
        params_dict['cust_id'] = "123xxx"
        status_error_code = SetUserProfileReturnCodeEnum.CUSTID_WRONG.value

        return params_dict, status_error_code

    def keyword_invalid(self):
        '''keyword不正确'''
        params_dict = dict(self.initparams)

        # keyword替换为非法字符
        params_dict['keyword'] = "xxxxxx"
        status_error_code = SetUserProfileReturnCodeEnum.KEWWORD_WRONG.value

        return params_dict, status_error_code


    def content_null(self):
        '''设置内容为空'''
        params_dict = dict(self.initparams)

        # keyword替换为非法字符
        params_dict['keyword'] = "new_sex"
        status_error_code = SetUserProfileReturnCodeEnum.CONTENT_EMPTY.value

        return params_dict, status_error_code

    def address_fail(self):
        '''new_address设置不成功'''
        params_dict = dict(self.initparams)

        params_dict['keyword'] = "new_address"
        params_dict['content'] = 9999        #设置一个很大的区域

        status_error_code = SetUserProfileReturnCodeEnum.ADDRESS_FAIL.value

        return params_dict, status_error_code

    def birthday_fail(self):
        '''new_birthday设置不成功'''
        params_dict = dict(self.initparams)

        params_dict['keyword'] = "new_birthday"
        params_dict['content'] = "1990:03:44"

        status_error_code = SetUserProfileReturnCodeEnum.BIRTHDAY_FAIL.value

        return params_dict, status_error_code

    def station_long(self):
        '''station 长度超限 40'''
        params_dict = dict(self.initparams)

        params_dict['keyword'] = "station"
        params_dict['content'] = ''.join('a' for i in range(42))

        status_error_code = SetUserProfileReturnCodeEnum.STATION_FAIL.value

        return params_dict, status_error_code





def data_list():

    data_driven_list=[]
    setuserprofile = SetUserProfile()

    data_driven_list+=[setuserprofile.custid_invalid(), \
                       setuserprofile.keyword_invalid(),\
                       setuserprofile.content_null(),\
                       setuserprofile.address_fail(), \
                       setuserprofile.birthday_fail(),\
                       setuserprofile.station_long()

                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.setuserprofile
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=SetUserProfile.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['errorCode']==pyfixture[1][0]
