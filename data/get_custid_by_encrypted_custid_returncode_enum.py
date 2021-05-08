from enum import Enum

class EnumCommonCode(Enum):

    ERROR_CODE_SUCCESS=('0', "请求成功")
    STATUS_CODE_PARAM_ERRO=('1', "参数校验错误")
    STATUS_CODE_USER_NOT_EXIST=('-1', "根据解密出的custid表读取的用户信息为空")