from data.find_bind_third_user_returncode_enum import EnumCommonCode
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="find_bind_third_user_path",data="find_bind_third_user.yml")
class Find_Bind_Third_User(CASE):
    '''根据custid取得用户信息(读库) '''
    case_list = []                  # 存放各实例方法

    def __init__(self):

        pass

    @loadcase(case_list)
    def cust_third_id_empty(self):
        '''cust_third_id为空'''
        params_dict = dict(self.initparams)
        params_dict['cust_third_id']=''

        status_error_code = EnumCommonCode.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def appkey_invalid(self):
        '''appkey非法'''
        params_dict = dict(self.initparams)
        # params_dict['cust_third_id']='xxx'
        params_dict['appkey']='0'

        status_error_code = EnumCommonCode.APPKEY_IS_VALID.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def cust_third_id_find(self):
        '''根据cust_third_id和third_id从customer_third(share_sign_link)表中存在'''
        params_dict = dict(self.initparams)

        third_id = params_dict['appkey']
        sql="select cust_third_id from customer_third where cust_status!=-1 and  third_id= '"+str(third_id)+"' limit 1"

        params_dict['cust_third_id'] = PyMySQL().mysqlget(sql)


        status_error_code = EnumCommonCode.STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def success(self):
        '''注册绑定成功'''
        params_dict = dict(self.initparams)


        status_error_code = EnumCommonCode.STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code

def teardown_module():

    #先从customer_third表中找到绑定的cust_id
    sql="select cust_id from customer_third where cust_third_id='"+Find_Bind_Third_User.initparams['cust_third_id']+"'"

    custid=PyMySQL().mysqlget(sql)

    #删数据
    data={'cust_id':custid}
    mysql_cursor=PyMySQL()
    mysql_cursor.mysqldel('customer_third',data)
    mysql_cursor.mysqldel('customer',data)


@pytest.fixture(params=Find_Bind_Third_User.casedata(Find_Bind_Third_User.case_list))
def myfixture(request):
    return request.param

@pytest.mark.find_bind_third_user
@pytest.mark.flaky(reruns=1,reruns_delay=5)
def test_Find_Bind_Third_User(myfixture):

    #请求
    url=Find_Bind_Third_User.url
    data=myfixture[0]

    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #返回用户信息成功的话，检查字段信息