from enum import Enum

class WeixinBindListReturnCodeEnum(Enum):
    SUCCESS=('0', "SUCCESS")
    FAIL=('1', "FAIL")
    NOT_EXIST=('-1','当前账号不存在')