import os
import pytest
import time
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.set_user_profile_all_info_returncode_enum import SetUserProfileAllInfoReturnCodeEnum

@LoadEnvData(host="test_profileapi",path="set_user_profile_all_info_path",data="set_user_profile_all_info.yml")
class SetUserProfileAllInfo():

    def __init__(self):

        pass

    def custid_invalid(self):
        '''custid不正确'''
        params_dict = dict(self.initparams)

        # custid替换为空
        params_dict['cust_id'] = ""
        status_error_code = SetUserProfileAllInfoReturnCodeEnum.CUSTID_WRONG.value

        return params_dict, status_error_code


    def job_long(self):
        '''cust_job的长度大于40'''
        params_dict = dict(self.initparams)

        params_dict['cust_id']=self.cf_presetvar.get('profile','cust_id')
        params_dict['cust_job']=''.join('a' for i in range(42))

        status_error_code = SetUserProfileAllInfoReturnCodeEnum.JOB_LONG.value

        return params_dict, status_error_code




    def setcompanyallinfo_success(self):
        '''修改完毕'''
        params_dict = dict(self.initparams)

        params_dict['cust_id'] = self.cf_presetvar.get('profile', 'enterprise_cust_id')

        status_error_code = SetUserProfileAllInfoReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code



def data_list():

    data_driven_list=[]
    setuserprofileallinfo = SetUserProfileAllInfo()

    data_driven_list+=[setuserprofileallinfo.custid_invalid(), \
                        setuserprofileallinfo.job_long(),\
                       setuserprofileallinfo.setcompanyallinfo_success()

                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.setuserprofileallinfo
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=SetUserProfileAllInfo.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['errorCode']==pyfixture[1][0]
