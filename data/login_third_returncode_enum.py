from enum import Enum

class LoginThirdReturnCodeEnum(Enum):
    LOGIN_STATUS_CODE_PARAM_FORMAT=("1", "必须输入的字段为空或者输入的参数格式不正确")
    LOGIN_STATUS_CODE_CUST_NOT_EXISTS=("-1", "根据cust_third_id和third_id从share_sign_link表读取custid失败")
    LOGIN_STATUS_CODE_CUST_INFO_FAIL=("-2","根据custid从Customers表读取用户信息失败")
    LOGIN_STATUS_CODE_WRITE_SESSION_FAIL=(-7, "调用写session信息接口失败")
    LOGIN_STATUS_CODE_SMS_FAIL=("-8", "是短信登录时，短信验证码验证失败")
    LOGIN_STATUS_CODE_APPKEY_NOT_ALLOW=("-10", "参数appkey未传值或传的值不是申请分配的")
    LOGIN_STATUS_CODE_SUCCESS=("0", "用户名和密码都正确")