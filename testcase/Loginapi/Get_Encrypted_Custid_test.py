from data.get_encrypted_custid_returncode_enum import EnumCommonCode
from . import pytest,CASE,LoadEnvData,loadcase,request,PyMySQL

@LoadEnvData(host="test_loginapi",path="get_encrypted_custid_path",data="get_encrypted_custid.yml")
class Get_Encrypted_Custid(CASE):
    '''根据邮箱或手机取得加密的custid'''

    case_list=[]        #存放各实例方法

    @loadcase(case_list)
    def username_empty(self):
        '''username为空'''
        params_dict = dict(self.initparams)

        status_error_code = EnumCommonCode.STATUS_CODE_PARAM_ERRO.value

        return params_dict, status_error_code

    @loadcase(case_list)
    def username_not_exist(self):
        '''username是手机号但不在库'''
        params_dict = dict(self.initparams)
        params_dict['username']=18818888188

        status_error_code = EnumCommonCode.STATUS_CODE_CUST_NOT_EXISTS.value

        return params_dict, status_error_code
    
    @loadcase(case_list)
    def username_is_thrid_eamil(self):
        '''username是第三方邮箱'''
        '''
            // 新浪第三方邮箱后缀
            "@sina_user.com",
            // qq第三方邮箱后缀
            "@qq_user.com",
            // 支付宝第三方邮箱后缀
            "@taobao_user.com",
            // 人人第三方邮箱后缀
            "@renren_user.com",
            // 163第三方邮箱后缀
            "@163_user.com",
            // msn第三方邮箱后缀
            "@msn_user.com",
            // 百度第三方邮箱后缀
            "@baidu_user.com",
            // 139第三方邮箱后缀
            "@139_user.com",
            // 飞信第三方邮箱后缀
            "@fetion_user.com",
            // 360第三方邮箱后缀
            "@360_user.com",
            // 江苏移动第三方邮箱后缀
            "@jsmobile_user.com",
            // 湖北移动第三方邮箱后缀
            "@hbcmcc__user.com",
            // 豆瓣第三方邮箱后缀
            "@douban_user.com",
            // 搜狐第三方邮箱后缀
            "@sohu_user.com",
            // 百度微购邮箱后缀
            "@weigou__user.com",
            // BD的免注册结算邮箱后缀
            "@bd_auto_user.com",
            // 1号店第三方用户的邮箱后缀
            "@yhd_user.com",
            // 苏宁第三方用户的邮箱后缀
            "@suning_user.com",
            // 天猫第三方用户的邮箱后缀
            "@tmall_user.com",
            // 51返利第三方用户的邮箱后缀
            "@fanli_user.com",
            // 微信第三方用户的邮箱后缀
            "@weixin_user.com",
            "@fenxiao_user.com",
        
        '''

        params_dict = dict(self.initparams)
        params_dict['username']='tester@qq_user.com'

        status_error_code = EnumCommonCode.STATUS_CODE_EMAIL_IS_THIRD.value

        return params_dict, status_error_code


    @loadcase(case_list)
    def success(self):
        '''参数正确，返回用户信息'''
        params_dict = dict(self.initparams)

        params_dict['username']=18811348250

        status_error_code = EnumCommonCode.ERROR_CODE_SUCCESS.value

        return params_dict, status_error_code

@pytest.fixture(params=Get_Encrypted_Custid.casedata(Get_Encrypted_Custid.case_list))
def myfixture(request):
    return request.param

@pytest.mark.get_encrypted_custid
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_Get_Encrypted_Custid(myfixture):

    #请求
    url=Get_Encrypted_Custid.url

    # for each_myfixture in myfixture:
    data=myfixture[0]
    # print(data)
    res=request(url=url,data=data)
    assert res['statusCode']==myfixture[1][0]
    #返回用户信息成功的话，检查字段信息




