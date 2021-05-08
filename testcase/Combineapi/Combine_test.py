import pytest
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from utils.requesttool import loadcase
from utils.log import callback_log,combinelogger
from data.combine_returncode_enum import CombineReturnCodeEnum

combinelist=[]

@LoadEnvData(host="test_combineapi",path="combine_path",data="combine.yml")
class Combine():
    def __init__(self):
        #从数据库选取一个有手机的custid作为父账号
        self.custid=self.cf_presetvar.get('combine','cust_unbind')

        # 从数据库选取一个没有手机的账户，作为子账号
        self.custid_no_phone=self.cf_presetvar.get('combine','cust_unbind_weixin')

    @loadcase(combinelist)
    def params_invalid(self):
        '''参数校验-必填字段为空'''
        #custid_parent为空

        request_data=self.initparams
        request_data['custid_parent']=''

        status_error_code = CombineReturnCodeEnum.PARAM_ERROR_PREFIX.value

        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_notexist(self):
        '''父账号或子账号cust_id不存在'''
        request_data = dict(self.initparams)

        request_data['custid_parent']= '123123123'
        request_data['custid_child'] = '321321321'
        status_error_code = CombineReturnCodeEnum.CUSTID_IS_NOT_EXIST.value

        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_parent_nophone(self):
        '''父账号未绑定手机'''
        request_data = dict(self.initparams)

        sql = "select cust_id from customer where cust_id>0 and cust_mobile='' limit 1"
        request_data['custid_parent']=PyMySQL().mysqlget(sql)
        status_error_code=CombineReturnCodeEnum.CUSTID_NOT_BIND_MOBILE.value

        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_child_bindphone(self):
        '''子账号已绑定手机'''
        request_data = dict(self.initparams)

        sql = "select cust_id from customer where cust_id>0 and cust_mobile<>'' limit 5,1"
        request_data['custid_child'] = PyMySQL().mysqlget(sql)
        request_data['custid_parent'] = self.custid

        status_error_code = CombineReturnCodeEnum.CUSTID_ALREADY_BIND_MOBILE.value

        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_parent_already_bind_wechat(self):
        '''父账号已绑定微信'''
        request_data = dict(self.initparams)
        #从customer_combine中选择一个cust_id
        sql = "select cust_id from customer where cust_id in (" \
              " select cust_id from customer_third_wechat where cust_bind_type=2) and cust_mobile<>'' limit 1"
        request_data['custid_parent'] = PyMySQL().mysqlget(sql)

        #未绑定微信的cust_id
        sql="select cust_id from customer where cust_id in (select cust_id from " \
            "customer_third_wechat where cust_bind_type=1)  and cust_mobile='' limit 1"
        request_data['custid_child'] = PyMySQL().mysqlget(sql)

        status_error_code = CombineReturnCodeEnum.CUSTID_ALREADY_BIND_WEIXIN.value

        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_parent_already_bind_qq(self):
        '''父账号已绑定qq'''
        request_data = dict(self.initparams)
        thirdid=6       #qq
        sql = "select cust_id from customer where cust_id in (" \
              " select cust_id from customer_third where third_id=6) and cust_mobile<>'' limit 1"
        request_data['custid_parent'] = PyMySQL().mysqlget(sql)

        sql = "select cust_id from customer where cust_id in (" \
              " select cust_id from customer_third where third_id=6) and cust_mobile='' limit 1"
        request_data['custid_child'] = PyMySQL().mysqlget(sql)

        status_error_code = CombineReturnCodeEnum.CUSTID_ALREADY_BIND_WEIXIN.value

        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_child_already_combine(self):
        '''子账号发生过绑定'''
        request_data = dict(self.initparams)

        request_data['custid_parent'] = self.custid
        # 发生过绑定的cust_id
        sql = "select cust_id from customer where cust_id in (select cust_id from " \
              "customer_combine )  and cust_mobile='' limit 1"
        request_data['custid_child'] = PyMySQL().mysqlget(sql)

        status_error_code = CombineReturnCodeEnum.CUSTID_COMBINE_REPEAT_VERIFY_FAIL.value

        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_apply_cancel_deny(self):
        '''提交注销申请的账户不能合并'''
        request_data = dict(self.initparams)

        # 注销申请的cust_id
        sql = "select cust_id from customer where cust_id in (select cust_id from " \
              "customer_cancel_apply where cust_mobile<>'' ) and cust_status!=-1 limit 1"
        request_data['custid_parent'] = PyMySQL().mysqlget(sql)

        request_data['custid_child'] = self.custid_no_phone

        status_error_code = CombineReturnCodeEnum.CUSTID_ALREADY_APPLY_CANCEL.value
        return request_data, status_error_code

    @loadcase(combinelist)
    def custid_enterprise_deny(self):
        '''企业账号不能合并'''
        request_data = dict(self.initparams)

        #父账号为企业账号
        custid=self.cf_presetvar.get('combine','enterprise_cust_id')     #预定义变量中获取企业账号
        request_data['custid_parent'] = custid

        request_data['custid_child'] = self.custid_no_phone

        status_error_code = CombineReturnCodeEnum.CUSTID_ENTERPRISE_VERIFY_FAIL.value
        return request_data, status_error_code

    @loadcase(combinelist)
    def combine_success(self):
        '''合并微信账号成功'''
        request_data = dict(self.initparams)

        request_data['custid_parent'] = self.custid
        request_data['custid_child'] = self.custid_no_phone

        status_error_code = CombineReturnCodeEnum.SUCCESS.value
        return request_data, status_error_code


def teardown_module():
    '''用例结果数据销毁'''
    combine=Combine()
    custidlist=[combine.custid,combine.custid_no_phone]
    for custid in custidlist:
        data={'cust_id':custid}
        PyMySQL().mysqldel('customer_combine',data)

combine = Combine()
datalist = [ele(combine) for ele in combinelist]

@pytest.fixture(params=datalist)
def pyfixture(request):
    return request.param

@pytest.mark.combine
@pytest.mark.flaky(reruns=1, reruns_delay=5)
def test_Combine(pyfixture,hook=callback_log):
    # 请求
    url = Combine.url
    data = pyfixture[0]
    res = request(url=url, data=data)
    # print(data)
    if hook:  # 写日志,写在assert断言之前
        callback_log(url, data, res, combinelogger,return_msg=pyfixture[1][1])

    assert res['return_code'] == pyfixture[1][0]