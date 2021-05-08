import os
import pytest
import time
import base64
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.changeprofielimg_returncode_enum import ChangeProfileImgReturnCodeEnum

@LoadEnvData(host="test_profileapi",path="set_user_profile_path",data="changeprofileimg.yml")
class ChangeProfileImg():

    father_path=os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    changeprofileimgpath=father_path + "\\resource\\changeprofileimg.png"

    def __init__(self):

        #加载图像
        with open(self.changeprofileimgpath,'rb') as f:
            self.bf=base64.b64encode(f.read())


        pass

    def custid_notexist(self):
        '''custid不存在'''
        params_dict = dict(self.initparams)

        # custid替换

        params_dict['custid'] = "123456789"
        params_dict['img_data']=self.bf
        status_error_code = ChangeProfileImgReturnCodeEnum.USER_NOT_EXIST.value

        return params_dict, status_error_code


    def postinfo_null(self):
        '''info is null'''
        params_dict = dict(self.initparams)

        params_dict['img_data'] = ''

        status_error_code = ChangeProfileImgReturnCodeEnum.INFO_NULL.value

        return params_dict, status_error_code


    def postinfo_seccess(self):
        '''success'''
        params_dict = dict(self.initparams)

        params_dict['img_data']=self.bf

        status_error_code = ChangeProfileImgReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code



def data_list():

    data_driven_list=[]
    changeprofileimg = ChangeProfileImg()

    data_driven_list+=[changeprofileimg.custid_notexist(),\
                       changeprofileimg.postinfo_null(),\
                       changeprofileimg.postinfo_seccess()

                    ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.changeprofileimg
@pytest.mark.flaky(reruns=1,reruns_delay=60)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=ChangeProfileImg.url
    data=pyfixture[0]
    res=request('post',url=url,data=data)
    #print(data)
    assert res['statusCode']==pyfixture[1][0]




