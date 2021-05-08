import pytest
import time
from utils.requesttool import request
from utils.pysql import PyMySQL
from utils.loaddata import LoadEnvData
from data.weixin_unbind_delete_returncode_enum import WeixinUnbindDeleteReturnCodeEnum

@LoadEnvData(host="test_loginapi",path="weixin_unbind_delete_path",data="weixin_unbind_delete.yml")
class WeixinUnbindDelete():

    def __init__(self):
        pass

    def custid_invalid(self):
        '''参数错误'''
        params_dict = dict(self.initparams)

        # custid替换为非法字符

        params_dict['custid'] = "123xxx"
        status_error_code = WeixinUnbindDeleteReturnCodeEnum.PARAM_ILLEGAL.value

        return params_dict, status_error_code

    def custid_notexist(self):
        '''custid找不到'''
        params_dict = dict(self.initparams)

        # custid替换为不存在的

        params_dict['custid'] = "99999999"
        status_error_code = WeixinUnbindDeleteReturnCodeEnum.CUST_NOT_FOUND.value

        return params_dict, status_error_code


    def custid_already_combine(self):
        '''账号合并的不允许删除'''

        #1、从customer_combine和customer_third_wechat中找一个custid传参
        sql = 'select combine_cust_id from customer_combine where combine_cust_id in (select cust_id from customer_third_wechat) limit 1;'

        custid_combinded=PyMySQL().mysqlget(sql)


        params_dict = dict(self.initparams)

        params_dict['custid'] = custid_combinded
        status_error_code = WeixinUnbindDeleteReturnCodeEnum.COMBINE_DENY.value

        return params_dict, status_error_code


    def weixin_unbind_success(self):
        '''解绑成功'''

        params_dict = dict(self.initparams)
        #1、先向插入customer_third_wechat
        #1.1获取一个未绑定的custid
        sql = 'select cust_id from customer where cust_id not in (select cust_id from customer_third_wechat) and cust_id>0 limit 1;'

        custid=PyMySQL().mysqlget(sql)

        #1.2插入数据

        localtime=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        sql = 'insert into customer_third_wechat(cust_id,wx_union_id,cust_bind_type,wx_use_status,cust_status,creation_date,last_changed_date) ' \
              'values({},{},{},{},{},{},{});'.format(int(custid),'"fake1230900000000"',1,1,1,\
                                                                                  '"'+localtime+'"','"'+localtime+'"')

        PyMySQL().mysqlinsert(sql)

        params_dict['custid']=custid
        status_error_code = WeixinUnbindDeleteReturnCodeEnum.SUCCESS.value

        return params_dict, status_error_code

        pass



def data_list():

    data_driven_list=[]
    weixinunbinddelete = WeixinUnbindDelete()

    data_driven_list+=[weixinunbinddelete.custid_invalid(), \
                       weixinunbinddelete.custid_notexist(),\
                       weixinunbinddelete.custid_already_combine(),\
                       # weixinunbinddelete.weixin_unbind_success()
                       ]

    return data_driven_list


def teardown_module():
    '''用例结果数据销毁'''
    pass

    #to do,其他表



@pytest.fixture(params=data_list())
def pyfixture(request):
    return request.param


@pytest.mark.weixin_unbind_delete
@pytest.mark.flaky(reruns=1,reruns_delay=10)
def test_WeixinUnbindDelete(pyfixture):

    #请求
    url=WeixinUnbindDelete.url
    data=pyfixture[0]
    res=request(url=url,data=data)
    #print(data)
    assert res['statusCode']==pyfixture[1][0]




