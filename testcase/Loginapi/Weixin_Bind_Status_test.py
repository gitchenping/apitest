from data.weixin_bind_status_returncode_enum import WeixinBindStatusReturnCodeEnum,EnumWeixinBindFlag
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="weixin_bind_status_path",data="weixin_bind_status.yml")
class Weixin_Bind_Staus(CASE):
    '''微信账号绑定状态判断'''

    case_list = []  # 存放各实例方法


    def __init__(self):
        self.flg={
            'combine_flg':None,
            'assoc_flg':None,
            'mobile_flg':None,
            'statusCode':'0',
            'errorCode': "0",
            'errorMsg': None
        }



    @loadcase(case_list)
    def params_invalid(self):
        '''参数错误'''
        params_dict = dict(self.initparams)
        params_dict['union_id']=''

        status_error_code = WeixinBindStatusReturnCodeEnum.PARAM_ILLEGAL.value


        return params_dict,status_error_code

    @loadcase(case_list)
    def unionid_not_exist(self):
        '''账号不存在'''
        params_dict = dict(self.initparams)
        params_dict['unionid'] = 'xxxxyyyyuuuu1234'

        status_error_code = WeixinBindStatusReturnCodeEnum.CUSTID_NOT_FIND.value


        return params_dict, status_error_code

    @loadcase(case_list)
    def combine(self):
        '''发生过合并、关联过当当账号、有手机号'''
        params_dict = dict(self.initparams)
        params_dict['unionid'] =self.cf_presetvar.get('login', 'cust_unionid')

        status_error_code = WeixinBindStatusReturnCodeEnum.SUCCESS.value

        # 赋值
        flg=dict(self.flg)
        flg['combine_flg'] = '1'
        flg['assoc_flg'] = '1'
        flg['mobile_flg'] = '1'

        return params_dict, status_error_code,flg


    @loadcase(case_list)
    def combine_no_mobile(self):
        '''合并过，但没有手机号'''
        params_dict = dict(self.initparams)

        sql="select   b.wx_union_id from customer a, " \
            "(select cust_id, wx_union_id, cust_status from customer_third_wechat where  cust_bind_type=1) b" \
            " where a.cust_mobile = '' and b.cust_status != -1 and a.cust_id = b.cust_id and b.wx_union_id " \
            " like 'oci%' group by b.wx_union_id limit 1"

        unionid=PyMySQL().mysqlget(sql)


        params_dict['unionid'] = unionid

        status_error_code = WeixinBindStatusReturnCodeEnum.SUCCESS.value
        # 赋值
        flg = dict(self.flg)
        flg['combine_flg'] = '1'
        flg['assoc_flg'] = '1'
        flg['mobile_flg'] = None


        return params_dict, status_error_code, flg

    @loadcase(case_list)
    def nocombine_nomobile(self):
        '''没合并过，没有手机号'''
        params_dict = dict(self.initparams)

        sql = "select   b.wx_union_id from customer a, " \
              "(select cust_id, wx_union_id, cust_status from customer_third_wechat where  cust_bind_type=2) b" \
              " where a.cust_mobile = '' and b.cust_status != -1 and a.cust_id = b.cust_id and b.wx_union_id " \
              " like 'oci%' group by b.wx_union_id limit 1"

        unionid = PyMySQL().mysqlget(sql)

        params_dict['unionid'] = unionid

        status_error_code = WeixinBindStatusReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code, self.flg




@pytest.fixture(params=Weixin_Bind_Staus.casedata(Weixin_Bind_Staus.case_list))
def myfixture(request):
    return request.param

@pytest.mark.weixin_bind_status
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Weixin_Get_Bind_List(myfixture):

    #请求
    url=Weixin_Bind_Staus.url
    data=myfixture[0]

    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    if res['statusCode']=='0':
        assert res==myfixture[2]
