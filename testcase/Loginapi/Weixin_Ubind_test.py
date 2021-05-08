from . import pytest,allure,CASE,LoadEnvData,loadcase,request,PyMySQL
from data.weixin_ubind_returncode_enum import EnumStatusCode

@LoadEnvData(host="test_loginapi",path="weixin_unbind_path",data="weixin_unbind.yml")
class Weixin_Ubind(CASE):

    case_list=[]

    def __init__(self):

        sql="select wx_union_id from customer_third_wechat " \
            " where cust_status=1 and cust_id !="+str(self.initparams['custid'])

        self.unionid=PyMySQL().mysqlget(sql)

        #绑定类型 1-当当账号；2-union_id（微信注册)
        sql="select cust_id,wx_union_id from customer_third_wechat" \
            " where cust_bind_type=2 and cust_status=1 limit 1"

        self.bind_custid,self.bind_unionid=PyMySQL().mysqlget(sql)


    @loadcase(case_list)
    def custid_or_unionid_empty(self):
        '''custid或uniond_id为空'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = ''
        status_error_code =EnumStatusCode.PARAM_ILLEGAL.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def custid_mismath_unionid(self):
        '''custid和union_id不匹配'''
        params_dict = dict(self.initparams)
        params_dict['union_id'] = self.unionid
        status_error_code = EnumStatusCode.UNIONID_QUERY_FAILED.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def custid_or_unionid_not_exist(self):
        '''custid或unionid不存在'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = 43211234
        params_dict['union_id']='xxxyyyyzzzzz'
        status_error_code = EnumStatusCode.UNIONID_QUERY_FAILED.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def combine_deny(self):
        '''账号合并的不允许解绑'''
        params_dict = dict(self.initparams)
        params_dict['custid'] = self.bind_custid
        params_dict['union_id'] = self.bind_unionid

        status_error_code = EnumStatusCode.COMBINE_DENY.value
        return params_dict, status_error_code

    @loadcase(case_list)
    def unbind_success(self):
        '''解绑成功'''
        params_dict = dict(self.initparams)

        status_error_code = EnumStatusCode.SUCCESS.value
        return params_dict, status_error_code


def teardown_module():
    #解绑成功后，需要恢复数据
    data={
        'cust_id':Weixin_Ubind.initparams['custid'],
        'wx_union_id':Weixin_Ubind.initparams['union_id'],
        'cust_bind_type':1,
        'wx_use_status':1,
        'cust_status':1,
        'creation_date':'2019-07-17 10:27:37',
        'last_changed_date':'2020-05-26 15:10:31'
    }

    PyMySQL().mysqlinsert('customer_third_wechat',data)
    pass


@pytest.fixture(params=Weixin_Ubind.casedata(Weixin_Ubind.case_list))
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.weixin_unbind
@pytest.mark.flaky(reruns=2,reruns_delay=5)
def test_Weixin_Get_Openid(pyfixture):

    #请求
    url=Weixin_Ubind.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode'] == pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True