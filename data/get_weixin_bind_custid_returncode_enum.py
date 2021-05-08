from enum import Enum

class GetWeixinBindCustidReturnCodeEnum(Enum):
    SUCCESS=("0", "success")
    PARAM_ERROR_PREFIX=("1001", "The wrong parameter:({%s}:{%s})")
    NOT_COMBINED=("1002", "not combined")
