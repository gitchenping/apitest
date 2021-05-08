from enum import Enum

class EnumCommonCode(Enum):

    ERROR_CODE_SUCCESS=('0', "请求成功")
    ERROR_CODE_FAIL=('1', "请求失败")
    STATUS_CODE_SUCCESS=('0', "请求成功")
    STATUS_CODE_PARAM_ERROR=('1', "参数校验错误")
    STATUS_CODE_APPKEY_NOT_PATCH=('-1', "Appkey不匹配")
    STATUS_CODE_CUST_GET_NOT_EXISTS=('-1', "数据库中查不到用户")
    APPKEY_IS_VALID=('-3', "appkey的值不是申请分配的")