import pytest
import allure
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.mobile_bind_status_returncode_enum import EnumMobileBindFlag,MobileBindStatusReturnCodeEnum
from utils.requesttool import loadcase
from utils.pysql import  PyMySQL

mobilebindstatuslist=[]

@LoadEnvData(host="test_loginapi",path="mobile_bind_status_path",data="mobile_bind_status.yml")
class Mobile_Bind_Status():

    def __init__(self):
        pass

    @loadcase(mobilebindstatuslist)
    def mobile_empty(self):
        '''mobile 为空'''
        params_dict = dict(self.initparams)

        params_dict['mobile'] = ''
        status_error_code =MobileBindStatusReturnCodeEnum.FAIL.value

        return params_dict, status_error_code

    @loadcase(mobilebindstatuslist)
    def mobile_not_exist(self):
        '''mobile不存在 ,视为未绑定'''
        params_dict = dict(self.initparams)
        params_dict['mobile']='18818818888'

        status_error_code=EnumMobileBindFlag.UNBIND.value

        return params_dict,status_error_code

    @loadcase(mobilebindstatuslist)
    def moible_bind_dangdang(self):
        '''mobile 未绑定'''
        params_dict = dict(self.initparams)

        #找一个mobile在customer表但不在customer_third_wechat表中
        sql=" select cust_mobile from customer where cust_id not in (select cust_id from customer_third_wechat ) " \
            " and cust_status!=-1 and length(cust_mobile)=11 limit 1"

        mobile=PyMySQL().mysqlget(sql)

        params_dict['mobile']=mobile

        status_error_code = EnumMobileBindFlag.CUST_BIND.value

        return params_dict, status_error_code

    @loadcase(mobilebindstatuslist)
    def moible_bind_weixin(self):
        '''mobile 绑定了微信'''
        params_dict = dict(self.initparams)

        status_error_code = EnumMobileBindFlag.COMBINE_OR_WEIXIN_BIND.value

        return params_dict, status_error_code


mobilebindstatus=Mobile_Bind_Status()
datalist=[ele(mobilebindstatus) for ele in mobilebindstatuslist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.mobile_bind_status
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Mobile_Bind_Status(pyfixture):

    #请求
    url=Mobile_Bind_Status.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    if data['mobile'] !='':
         assert res['bind_flg']==pyfixture[1][0]
    else:
         assert res['statusCode'] == pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True