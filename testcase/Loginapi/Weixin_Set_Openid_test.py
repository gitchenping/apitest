from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.weixin_set_openid_returncode_enum import EnumStatusCode

@LoadEnvData(host="test_loginapi",path="weixin_set_openid_path",data="weixin_set_openid.yml")
class Weixin_Set_Openid(CASE):

    case_list=[]

    def __init__(self):
        #从focus表中获取一个openid
        # 关注状态:0取消关注  1已关注
        sql=" select focus_open_id from customer_wechat_focus where focus_status=1" \
            " and focus_union_id!='' limit 1"

        self.openid=PyMySQL().mysqlget(sql)


    @loadcase(case_list)
    def openid_empty(self):
        '''openid为空'''
        params_dict = dict(self.initparams)
        params_dict['openid'] = ''
        status_error_code =EnumStatusCode.PARAM_ILLEGAL.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def openid_not_exist(self):
        '''根据openid查询unionid失败'''
        params_dict = dict(self.initparams)
        params_dict['openid'] = '1298712'
        status_error_code = EnumStatusCode.UNIONID_QUERY_FAILED.value
        return params_dict, status_error_code


    @loadcase(case_list)
    def openid_not_find(self):
        '''当cancel=1时，focus表未查到openid'''
        params_dict = dict(self.initparams)
        params_dict['cancel']=1

        status_error_code = EnumStatusCode.OPENID_NOT_INIT.value
        return params_dict, status_error_code


    @loadcase(case_list)
    def upeate_focus_status_success(self):
        '''当cancel=1时，更新focus表状态成功'''
        params_dict = dict(self.initparams)
        params_dict['cancel'] = 1
        params_dict['openid']=self.openid

        status_error_code = EnumStatusCode.SUCCESS.value
        return params_dict, status_error_code



@pytest.fixture(params=Weixin_Set_Openid.casedata(Weixin_Set_Openid.case_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.weixin_set_openid
@pytest.mark.flaky(reruns=2,reruns_delay=5)
def test_Weixin_Set_Openid(pyfixture):

    #请求
    url=Weixin_Set_Openid.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode'] == pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True