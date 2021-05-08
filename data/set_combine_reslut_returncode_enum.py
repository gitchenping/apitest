from enum import Enum

class SetCombineResultReturnCodeEnum(Enum):
    SUCCESS=("0", "success")
    PARAM_ERROR_PREFIX=("1001", "The wrong parameter:({%s}:{%s})")
    CUSTID_NOT_EXIST=('1002','custid %s not exist')
