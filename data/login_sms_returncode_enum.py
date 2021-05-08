from enum import Enum
from utils.pysql import PyMySQL

class LoginSmsReturnCodeEnum(Enum):
    LOGIN_STATUS_CODE_PARAM_FORMAT=("1", "必须输入的字段为空或者输入的参数格式不正确")
    LOGIN_STATUS_CODE_CUST_NOT_EXISTS=("-1", "根据mobile_phone从customers表中读取的信息为空")
    LOGIN_STATUS_CODE_WRITE_SESSION_FAIL=(-7, "调用写session信息接口失败")
    LOGIN_STATUS_CODE_SMS_FAIL=("-8", "是短信登录时，短信验证码验证失败")
    LOGIN_STATUS_CODE_APPKEY_NOT_ALLOW=("-10", "参数appkey未传值或传的值不是申请分配的")
    LOGIN_STATUS_CODE_SUCCESS=("0", "用户名和密码都正确")


class LoginSmsDbResult():

    def dbcheckok(self,data):

        #成功，检查customer_login_log
        if data[1][0]==LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_SUCCESS.value[0]:

            sql="select count(*) from customer_login_log where login_ip={} ".format('"'+data[0]['ip_address']+'"')

            return PyMySQL().mysqlget(sql)>=1


        #不成功,检查
        if data[1][0] in [LoginSmsReturnCodeEnum.LOGIN_STATUS_CODE_CUST_NOT_EXISTS.value[0]] :

            #登录日志
            sql = "select count(*) from customer_login_log where login_ip={} and cust_id={}".format('"' + data[0]['ip_address'] + '"',-1)

            return PyMySQL().mysqlget(sql) >= 1

            pass

        #其他,不检查
        return True

    def redischekok(self):
        pass