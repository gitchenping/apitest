from enum import Enum

class MobileBindStatusReturnCodeEnum(Enum):
    SUCCESS=('0', "SUCCESS")
    FAIL=('1', "FAIL")

class EnumMobileBindFlag(Enum):
    UNBIND=('0', "未绑定")
    CUST_BIND=('1', "绑定当当账号")
    COMBINE_OR_WEIXIN_BIND=('2', "绑定/合并微信")