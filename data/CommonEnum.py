from enum import Enum

class EnumCommonCode(Enum):
    ERROR_CODE_SUCCESS=('0', "请求成功")
    ERROR_CODE_FAIL=('1', "请求失败")
    STATUS_CODE_SUCCESS=('0', "请求成功")
    STATUS_CODE_PARAM_ERROR=('1', "参数校验错误")
    STATUS_CODE_EMAIL_HAS_EXISTS=('-1', "邮箱已存在")
    STATUS_CODE_APPKEY_NOT_PATCH=('-1', "Appkey不匹配")
    STATUS_CODE_CUSTID_LENGTH_MAX=('-1', "custId数量超限")
    STATUS_CODE_EMAIL_IS_THIRD=(-1, "是第三方邮箱")
    STATUS_CODE_CUST_GET_NOT_EXISTS=('-1', "数据库中查不到用户")
    STATUS_CODE_CUST_DECUSTID_CUSTID_NOT_EQUAL=(-1, "加密custId与传入custId不一致")
    STATUS_CODE_CUST_NOT_EXISTS=(-2, "用户不存在"),
    STATUS_CODE_CUST_AUTHON_KEY_FAIL=(-2, "修改vip的AUTHKEY不正确")
    STATUS_CODE_CUST_DB_SMS_VERIFY_NULL=(-2, "DB验证码为空")
    STATUS_CODE_CUST_PASSWORD_EQUAL=(-2, "新设置密码与支付密码相同")
    STATUS_CODE_CUST_PASSWORD_FAIL=('-2', "登录密码错误")
    STATUS_CODE_CUST_NOT_TYPE=(2, "插入日志没有type值")
    STATUS_CODE_EMAIL_EXISTS=('-2', "邮箱已存在")
    STATUS_CODE_UPDATE_SESSION_FAIL=(-4, "更新session失败")
    STATUS_CODE_UPDATE_DB_FAIL=(-3, "修改DB错误")
    STATUS_CODE_CUST_MOBILE_EXISTS=(-3, "新手机号已存在")
    APPKEY_IS_VALID=(-3, "appkey的值不是申请分配的")
    STATUS_CODE_CUST_DB_UPDATE_FAIL=(-4, "查询DB无该用户")
    STATUS_CODE_CUST_SMS_VERIFYTYPE_FAIL=(-4, "sms验证状态错误")
    STATUS_CODE_CUST_PASSWORD=(-4, "新设置密码与支付密码相同")
    STATUS_CODE_CUST_DB_NOT_EXISTS=(-3, "查询DB无该用户")
    STATUS_CODE_CUST_MOBILE_FAIL=(-5, "更新手机号失败")
    STATUS_CODE_CUST_UPDATE_SMSVERIFY_FAIL=(-5, "更新验证码结果失败")
    STATUS_CODE_CUST_UPDATE_MOBILE_FAIL=(-5, "更新手机号失败")