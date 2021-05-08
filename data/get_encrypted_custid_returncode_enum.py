from enum import Enum

class EnumCommonCode(Enum):

    ERROR_CODE_SUCCESS=('0', "请求成功")
    STATUS_CODE_PARAM_ERRO=('1', "参数校验错误")
    STATUS_CODE_EMAIL_IS_THIRD=('-1', "是第三方邮箱")
    STATUS_CODE_CUST_NOT_EXISTS=('-2', "用户不存在")