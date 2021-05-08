from enum import Enum

class CheckMobilePhoneReturnCodeEnum(Enum):
    FORMAT_ERROR=('1', "格式错误")
    NOT_EXISTS=('false', "不存在")
    EXISTS=('true', "SUCCESS")