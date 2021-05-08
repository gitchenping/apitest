from enum import Enum

class CombineReturnCodeEnum(Enum):
    SUCCESS=('0', "success")
    PARAM_ERROR_PREFIX=("1001", "The wrong parameter:({%s}:{%s})")
    CUSTID_IS_NOT_EXIST=("1002", "custid xxx not exist")
    CUSTID_IS_NOT_WEIXIN=("1003", "custid xxx is not weixin")
    CUSTID_COMBINE_REPEAT_VERIFY_FAIL=("1004", "custid xxx combine repeat verify fail")
    CUSTID_ENTERPRISE_VERIFY_FAIL=('1005', "custid %s enterprise verify fail")
    CUSTID_SHOP_VERIFY_FAIL=(1006, "custid %s shop verify fail")
    CUSTID_ORDER_VERIFY_FAIL=(1007, "custid %s order verify fail")
    CUSTID_PAY_VERIFY_FAIL=(1008, "custid %s pay verify fail")
    CUSTID_COMBINE_DOING=(1010, "custid %s combine doing")
    CUSTID_IS_ONE_PARENT_MORE_CHILD=(1011, "custid %s is not allowed one parent more child")
    CUSTID_ACTION_VERIFY_FAIL=(1012, "custid %s auction verify fail")
    CUSTID_NO_CASH_VERIFY_FAIL=(1013, "custid %s no cash verify fail")
    CUSTID_OYUAN_LED_FAIL=(1015, "Participating in zero buy events verify fail")
    CUSTID_ALREADY_APPLY_CANCEL=('1016', "custid %s already apply cancel")
    CUSTID_ALREADY_BIND_MOBILE=("1017", "custid %s already bind mobile")
    CUSTID_ALREADY_BIND_WEIXIN=('1018', "custid %s already bind same type third")
    CUSTID_NOT_BIND_MOBILE=("1019", "custid %s is not bind mobile")
    CUSTID_PINQUAN_VERIFY_FAIL=(1020, "custid %s pinquan verify fail")
    CUSTID_WEIMENG_VERIFY_FAIL=(1021, "custid %s weimeng verify fail")
    CUSTID_SHUZI_VERIFY_FAIL=(1022, "custid %s shuzi verify fail")
    CUSTID_YIYUANKANJIA_VERIFY_FAIL=(1023, "custid %s yiyuankanjia verify fail")

    CUSTID_BACKUP_FAIL=(2001, "%s backup fail"),
    DATABASE_FAIL=(2002, "database fail"),

    CUSTID_THIRD_API_ERROR=(4001, "custid %s %s third api error"),
