from enum import Enum

class CombineStatusReturnCodeEnum(Enum):
    SUCCESS=("0", "success")
    PARAM_ERROR_PREFIX=("1001", "The wrong parameter:({%s}:{%s})")
    NOT_COMBINED=("1002", "not combined")
    COMBINE_DOING=("1003", "combine doing")
    NOT_WEIXIN=("1004", "not weixin")