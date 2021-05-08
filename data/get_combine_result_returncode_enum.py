from enum import Enum

class GetCombineResultReturnCodeEnum(Enum):

    SUCCESS=("0", "success")
    PARAM_ERROR_PREFIX=("1001", "The wrong parameter:({%s}:{%s})")
    RESULT_EMPTY=("1002","result empty")
