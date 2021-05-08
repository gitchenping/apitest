from enum import Enum

class GetuserinfobymobilephoneReturnCodeEnum(Enum):
    FORMATTER_ERROR=('1', "参数错误")
    USER_NOT_EXISTS=('-1', "从customer库的Customers表读取的用户信息为空")
    SUCCESS=('0', "success")