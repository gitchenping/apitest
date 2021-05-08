from enum import Enum

class WeixinBindStatusReturnCodeEnum(Enum):
    SUCCESS=('0', "SUCCESS")
    PARAM_ILLEGAL=('1', "FAIL")
    CUSTID_NOT_FIND=('-1','当前账号不存在')

class EnumWeixinBindFlag(Enum):
    COMBINE_FLG=('1', "合并过")
    ASSOC_FLG=('1', "关联过当当主账号")
    MOBILE_FLG=('1', "有手机")