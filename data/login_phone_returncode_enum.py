from enum import Enum

class LoginPhoneReturnCodeEnum(Enum):
    LOGIN_STATUS_CODE_PARAM_FORMAT=("1", "必须输入的字段为空或者输入的参数格式不正确")
    LOGIN_STATUS_CODE_CUST_NOT_EXISTS=("-1", "用户不存在")
    LOGIN_STATUS_CODE_TOKEN_FAIL=(-3, "token_id校验失败")
    LOGIN_STATUS_CODE_PASSWORD_FAIL=("-4", "密码错误")
    LOGIN_STATUS_CODE_ANTIFRAUD_IP=(-5, "watchdog检测为恶意ip")
    LOGIN_STATUS_CODE_CLIENT_FAIL=(-6, "客户端登录信息验证失败")
    LOGIN_STATUS_CODE_WRITE_SESSION_FAIL=(-7, "调用写session信息接口失败")
    LOGIN_STATUS_CODE_SMS_FAIL=("-8", "是短信登录时，短信验证码验证失败")
    LOGIN_STATUS_CODE_QRCODEID_FAIL=(-9, "qrcodeId非法")
    LOGIN_STATUS_CODE_ONETOUCH_WRITESESSION_FAIL=(-9, "一键登录写Session失败")
    LOGIN_STATUS_CODE_APPKEY_NOT_ALLOW=("-10", "参数appkey未传值或传的值不是申请分配的")
    LOGIN_STATUS_CODE_SUCCESS=('0', "用户名和密码都正确")