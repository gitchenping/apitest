from enum import Enum

class EnumSendAndCheckSmsVcode(Enum):
    FORMAT_ERROR=('1', "custid，mobile_phone，verify_type有一个为空或格式不正确")
    VERIFY_TYPE_NOT_IN_CONF=('-1', "输入的verify_type不是config文件里配置的verify_type取值中的一个")
    READ_FAIL=('-2', "有效短信验证码失败")
    INSERT_DB_ERROR=('-3', "修改status失败")
    SUCCESS=('0', "成功")