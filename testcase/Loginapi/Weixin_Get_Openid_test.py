from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.weixin_get_openid_returncode_enum import EnumStatusCode

@LoadEnvData(host="test_loginapi",path="weixin_get_openid_path",data="weixin_get_openid.yml")
class Weixin_Get_Openid(CASE):

    case_list=[]

    @loadcase(case_list)
    def custid_empty(self):
        '''custid为空'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = ''
        status_error_code =EnumStatusCode.PARAM_ILLEGAL.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def custid_not_exist(self):
        '''custid为空'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = '1298712'
        status_error_code = EnumStatusCode.CUSTID_NOT_FIND.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def openid_not_exist(self):
        '''custid 存在unionid 但在focus表中没有找到openid'''
        params_dict = dict(self.initparams)

        status_error_code = EnumStatusCode.OPENID_NOT_FIND.value
        return params_dict, status_error_code


    @loadcase(case_list)
    def open_id_find_success(self):
        '''custid存在对应的openid'''
        params_dict = dict(self.initparams)

        sql="select cust_id from customer_wechat_focus where cust_id in " \
            "(select cust_id from customer_third_wechat where wx_union_id!='' and cust_status!=-1) " \
            " and focus_status=1 and focus_open_id!='' limit 1"
        custid=PyMySQL().mysqlget(sql)

        params_dict['custid']=custid

        status_error_code = EnumStatusCode.SUCCESS.value
        return params_dict, status_error_code



@pytest.fixture(params=Weixin_Get_Openid.casedata(Weixin_Get_Openid.case_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.weixin_get_openid
@pytest.mark.flaky(reruns=2,reruns_delay=5)
def test_Weixin_Get_Openid(pyfixture):

    #请求
    url=Weixin_Get_Openid.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode'] == pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True