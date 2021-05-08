from enum import Enum

class WeixinVerifyReturnCodeEnum(Enum):
    PARAM_ILLEGAL=("1001", "The wrong parameter:({%s}:{%s})")
    VERIFY_FAIL=("1002","账号不合规")
    SUCCESS=("0", "账号合规")