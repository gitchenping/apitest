from enum import Enum

class ChangeEmailorPasswordReturnCodeEnum(Enum):
    FORMATTER_ERROR=('1', "参数格式不正确")
    CUST_NOT_EXISTS=('-1', "用户不存在")
    EMAIL_EXISTS=('-2', "邮箱不为空时其值在库中已经存在 ")
    DB_INSERT_ERROR=('-3', "写数据库操作失败 ")
    NEW_PASS_IS_SAME=('-4', "新设置的密码与支付密码相同 ")
    SUCCESS=('0', "成功修改邮箱或者密码 ")