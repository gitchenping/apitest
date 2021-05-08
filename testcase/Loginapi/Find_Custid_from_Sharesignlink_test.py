from data.find_custid_from_sharesignlink_returncode_enum import EnumCommonCode
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="find_custid_from_sharesignlink_path",data="find_custid_from_sharesignlink.yml")
class Find_Custid_from_Sharesignlink(CASE):
    '''根据custid取得用户信息(读库) '''
    case_list = []                  # 存放各实例方法

    def __init__(self):

        sql="select cust_third_id,third_id from customer_third where cust_status!=-1 limit 1"
        self.cust_third_id,self.third_id=PyMySQL().mysqlget(sql)

        sql="select qq_union_id from customer_third_qq_openid where is_valid=1 limit 1"
        self.qq_unionid = PyMySQL().mysqlget(sql)

    @loadcase(case_list)
    def cust_third_id_empty(self):
        '''cust_third_id为空'''
        params_dict = dict(self.initparams)
        params_dict['third_id'] = '3'

        status_error_code = EnumCommonCode.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def qqunion_id_empty(self):
        '''third_id=6,qqunion_id 为空'''
        params_dict = dict(self.initparams)

        params_dict['cust_third_id']=self.cust_third_id
        params_dict['third_id'] = '6'

        status_error_code = EnumCommonCode.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def cust_id_not_find(self):
        '''根据cust_third_id和third_id从customer_third(share_sign_link)表中查找custid为空'''
        params_dict = dict(self.initparams)

        params_dict['cust_third_id'] = self.cust_third_id
        params_dict['third_id'] = '66'

        status_error_code = EnumCommonCode.STATUS_CODE_CUST_GET_NOT_EXISTS.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def qq_unionid_success(self):
        '''使用qq_unionid 查询成功'''
        params_dict = dict(self.initparams)

        params_dict['cust_third_id'] = self.cust_third_id
        params_dict['third_id'] = '6'
        params_dict['qq_union_id']=self.qq_unionid

        status_error_code = EnumCommonCode.STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def success(self):
        '''查询成功'''
        params_dict = dict(self.initparams)

        params_dict['cust_third_id'] = self.cust_third_id
        params_dict['third_id'] = self.third_id
        # params_dict['qq_union_id'] = self.qq_unionid

        status_error_code = EnumCommonCode.STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code


@pytest.fixture(params=Find_Custid_from_Sharesignlink.casedata(Find_Custid_from_Sharesignlink.case_list))
def myfixture(request):
    return request.param

@pytest.mark.find_custid_from_sharesignlink
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_Find_Custid_from_Sharesignlink(myfixture):

    #请求
    url=Find_Custid_from_Sharesignlink.url
    data=myfixture[0]

    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #返回用户信息成功的话，检查字段信息