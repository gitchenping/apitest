import pytest
import allure
import hashlib
from utils.requesttool import request
from utils.loaddata import LoadEnvData
from data.change_viptype_returncode_enum import ChangeVipTypeReturnCodeEnum
from utils.requesttool import loadcase

changeviptypelist=[]

@LoadEnvData(host="test_loginapi",path="change_viptype_path",data="change_viptype.yml")
class Change_VipType():

    def __init__(self):
        pass

    @loadcase(changeviptypelist)
    def custid_empty(self):
        '''custid为空'''
        params_dict = dict(self.initparams)

        params_dict['custid'] = ''
        status_error_code = ChangeVipTypeReturnCodeEnum.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(changeviptypelist)
    def clientip_invalid(self):
        '''客户端ip错误'''
        params_dict = dict(self.initparams)

        params_dict['clientIP'] = '192.168.1.890'
        status_error_code =ChangeVipTypeReturnCodeEnum.STATUS_CODE_PARAM_ERROR.value

        return params_dict, status_error_code

    @loadcase(changeviptypelist)
    def vip_startdate_lt_enddate(self):
        '''vip_start_date>vip_end_date'''
        params_dict = dict(self.initparams)
        params_dict['vip_start_date'],params_dict['vip_end_date']=params_dict['vip_end_date'],params_dict['vip_start_date']

        status_error_code = ChangeVipTypeReturnCodeEnum.STATUS_CODE_PARAM_ERROR.value
        return params_dict, status_error_code

    @loadcase(changeviptypelist)
    def custid_not_exist(self):
        '''custid不存在'''
        params_dict = dict(self.initparams)
        params_dict['custid']=104401903883

        status_error_code=ChangeVipTypeReturnCodeEnum.STATUS_CODE_CUST_GET_NOT_EXISTS.value

        return params_dict,status_error_code

    @loadcase(changeviptypelist)
    def authkey_invalid(self):
        '''authkey 不合法'''
        params_dict = dict(self.initparams)

        status_error_code = ChangeVipTypeReturnCodeEnum.STATUS_CODE_CUST_AUTHON_KEY_FAIL.value

        return params_dict, status_error_code

    @loadcase(changeviptypelist)
    def success(self):
        '''viptype 更新成功'''
        params_dict = dict(self.initparams)

        #计算authkey
        md5 = hashlib.md5()
        rawstring=params_dict['authKey']+str(params_dict['custid'])
        md5.update(rawstring.encode('utf-8'))
        params_dict['authKey']=md5.hexdigest()

        status_error_code = ChangeVipTypeReturnCodeEnum.STATUS_CODE_SUCCESS.value

        return params_dict, status_error_code

def teardown_module():
    '''用例结果数据销毁'''

    #改回原来数据库的值
    # PyMySQL().mysqlupdate('customer',{'cust_id':Change_MobilePhone.initparams['custid']},{'cust_mobile':Change_MobilePhone.initparams['mobile_phone']})

    #to do,其他表
    pass

changeviptype=Change_VipType()
datalist=[ele(changeviptype) for ele in changeviptypelist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@allure.title('{pyfixture[1][1]}')
@pytest.mark.change_viptype
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_ChangeMobilePhone(pyfixture):

    #请求
    url=Change_VipType.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)

    #返回码检查
    assert res['statusCode']==pyfixture[1][0]
    #数据库检查
    # assert dbcheckok(res['statusCode']) is True