from data.weixin_get_bind_list_returncode_enum import WeixinBindListReturnCodeEnum
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="weixin_get_bind_list_path",data="weixin_get_bind_list.yml")
class Weixin_Get_Bind_List(CASE):
    '''通过union_id获取绑定账号列表'''

    case_list = []  # 存放各实例方法

    @loadcase(case_list)
    def params_invalid(self):
        '''参数错误'''
        params_dict = dict(self.initparams)
        params_dict['union_id']=''

        status_error_code = WeixinBindListReturnCodeEnum.FAIL.value


        return params_dict,status_error_code

    @loadcase(case_list)
    def unionid_not_exist(self):
        '''账号不存在'''
        params_dict = dict(self.initparams)
        params_dict['union_id'] = 'xxxxyyyyuuuu1234'

        status_error_code =WeixinBindListReturnCodeEnum.NOT_EXIST.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def success(self):
        '''账号存在'''
        params_dict = dict(self.initparams)
        params_dict['union_id'] = self.cf_presetvar.get('login', 'cust_unionid')

        status_error_code = WeixinBindListReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code




@pytest.fixture(params=Weixin_Get_Bind_List.casedata(Weixin_Get_Bind_List.case_list))
def myfixture(request):
    return request.param

@pytest.mark.weixin_get_bind_list
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Weixin_Get_Bind_List(myfixture):

    #请求
    url=Weixin_Get_Bind_List.url
    data=myfixture[0]

    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]

    #返回用户信息成功的话，检查字段信息