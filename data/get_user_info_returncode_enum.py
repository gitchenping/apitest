from enum import Enum

class GetuserinfoReturnCodeEnum(Enum):
    FORMATTER_ERROR=('1', "用户输入的custid为空")
    USER_NOT_EXISTS=('-1', "从customer库的Customers表读取的用户信息为空")
    SUCCESS=('0', "success")