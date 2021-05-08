import pytest
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from data.weixin_register_returncode_enum import WeixinRegistrReturnCodeEnum


@LoadEnvData(host="test_loginapi",path="weixin_register_path",data="weixin_register.yml")
class WeixinRegister():

    '''
    father_path = os.path.dirname(os.path.dirname(__file__))
    yamlfilepath = os.path.join(father_path, "data", "weixin_register.yml")
    initparams = readyml(yamlfilepath)
    presetvarinifilepath = os.path.join(father_path, "config", "presetvar.ini")
    testenvinifilepath = os.path.join(father_path, "config", "testenv.ini")
    cf_presetvar = readini(presetvarinifilepath)
    cf_testenv = readini(testenvinifilepath)
    url = cf_testenv.get('test_loginapi', 'host') + cf_testenv.get('test_loginapi', 'weixin_register_path')
    '''

    def __init__(self):
        pass


    def email_indb(self):
        '''email值已在库'''

        params_dict = dict(self.initparams)

        # email 替换为已在库的email
        email_exist = self.cf_presetvar.get('login', 'cust_email')

        params_dict['email'] = email_exist
        status_error_code = WeixinRegistrReturnCodeEnum.EMAIL_EXISTS.value

        return params_dict, status_error_code


    def nickname_indb(self):
        '''nickname已在库'''

        params_dict = dict(self.initparams)

        # email 替换为已在库的email
        nickname_exist = self.cf_presetvar.get('login', 'cust_nickname')

        params_dict['nickname'] = nickname_exist
        status_error_code = WeixinRegistrReturnCodeEnum.NICKNAME_EXISTS.value

        return params_dict, status_error_code

    def union_already_bind(self):
        '''union_id已经绑定过'''

        params_dict = dict(self.initparams)

        #
        unionid_exist = self.cf_presetvar.get('login', 'cust_unionid')

        params_dict['union_id'] = unionid_exist
        status_error_code = WeixinRegistrReturnCodeEnum.WEIXIN_REGISTER_IS_BIND.value

        return params_dict, status_error_code

    def email_empty(self):
        '''email 值为空'''
        pass

    def union_id_empty(self):
        '''union_id为空'''
        params_dict = dict(self.initparams)

        params_dict['union_id'] = ''
        status_error_code=WeixinRegistrReturnCodeEnum.FORMATTER_ERROR.value

        return params_dict,status_error_code

    def appkey_not_exist(self):
        '''appkey未传值或传的值不是申请分配的'''
        params_dict = dict(self.initparams)

        params_dict['appkey'] = '199999'
        status_error_code = WeixinRegistrReturnCodeEnum.APPKEY_ERROR.value

        return params_dict, status_error_code


    def weixinregister_success(self):
        '''参数正确，往customer库的Customers表里插入用户注册数据操作成功'''

        params_dict = dict(self.initparams)

        status_error_code=WeixinRegistrReturnCodeEnum.SUCCESS.value

        return params_dict,status_error_code

        pass


def data_list():

    data_driven_list=[]
    weixinregister = WeixinRegister()

    data_driven_list+=[weixinregister.email_indb(), \
                       weixinregister.nickname_indb(),\
                       weixinregister.union_id_empty(), \
                       weixinregister.appkey_not_exist(),\
                       weixinregister.union_already_bind(),\
                       weixinregister.weixinregister_success()
                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''

    #删除customer表
    PyMySQL().mysqldel('customer','cust_mobile',WeixinRegister.initparams['mobilephone'])

    #删除customer_third_wechat表
    PyMySQL().mysqldel('customer_third_wechat', 'wx_union_id', WeixinRegister.initparams['union_id'])

    #to do,其他表


@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.weixin_register
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_WeixinRegister(pyfixture):

    #请求
    url=WeixinRegister.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['statusCode']==pyfixture[1][0]

    return res


