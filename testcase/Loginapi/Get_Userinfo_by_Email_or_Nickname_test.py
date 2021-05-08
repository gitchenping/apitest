from data.get_user_info_by_eamil_or_nickname import GetuserinfobyemailornicknameReturnCodeEnum
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL
from utils.requesttool import platlist

@LoadEnvData(host="test_loginapi",path="get_user_info_by_email_or_nickname_path",data="get_user_info_by_email_or_nickname.yml")
class Get_USERINFO_by_EmailNICKNAME(CASE):
    '''根据邮箱或昵称取得用户信息'''

    case_list=[]        #存放各实例方法

    @loadcase(case_list)
    def username_not_exist(self):
        '''username不存在'''
        params_dict = dict(self.initparams)

        status_error_code = GetuserinfobyemailornicknameReturnCodeEnum.USER_NOT_EXISTS.value

        params_dict_list = []
        #
        for ele in params_dict['username']:
            params_dict['username'] = ele+"_xxxx"       #username 不存在

            params_dict_list.append((dict(params_dict), status_error_code))

        return params_dict_list



    @loadcase(case_list)
    def success(self):
        '''参数正确，返回用户信息'''
        params_dict = dict(self.initparams) #{'username': ['120666@qq.com', '我是代理'], 'authKey': ''}
        status_error_code = GetuserinfobyemailornicknameReturnCodeEnum.SUCCESS.value

        params_dict_list = []
        #
        for ele in params_dict['username']:
            params_dict['username'] = ele

            params_dict_list.append((dict(params_dict), status_error_code))

        return params_dict_list

#测试数据需要展开
data_list=Get_USERINFO_by_EmailNICKNAME.casedata(Get_USERINFO_by_EmailNICKNAME.case_list)

@pytest.fixture(params=platlist(data_list))
def myfixture(request):
    return request.param

@pytest.mark.get_user_info_by_email_or_nickname
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Get_USERINFO_by_EmailNICKNAME(myfixture):

    #请求
    url=Get_USERINFO_by_EmailNICKNAME.url

    # for each_myfixture in myfixture:
    data=myfixture[0]
    # print(data)
    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #返回用户信息成功的话，检查字段信息




