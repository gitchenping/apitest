from enum import Enum

class EnumRegisterStatus(Enum):
    FORMATTER_ERROR=('1', "参数格式不正确")
    EMAIL_EXISTS=('-1', "邮箱已经存在库里")
    NICKNAME_EXISTS=('-2', "昵称已经存在库里")
    MOBILE_PHONE_EXISTS=('-3', "手机号已经存在库里")
    REGISTER_TYPE_BEYOND_0_1=('-4', "用户输入的registion_type为0，1以外的值")
    DB_INSERT_ERROR=('-5', "往customer库的Customers表里插入用户注册数据操作失败")
    IP_O300_ERROR=('-7', "当watchdog_flg=1时用阈值300去检测ip是否恶意，如果是恶意返回错误码")
    IP_MALICIOUS_ERROR=('-6', "恶意ip")
    TOKEN_ID_CHECK_ERROR=('-8', "token_id校验失败")
    SESSION_API_ERROR=('-9', "调用写session接口失败")
    APPKEY_ERROR=('-10', "参数appkey未传值或传的值不是申请分配的")
    IP_COUNT_ERROR=('-11', "同一ip在24小时内注册数量超过限制")
    APPLEID_BIND_EXISTS=('-11', "appleId已经绑定了一个用户")
    SUCCESS=('0', "往customer库的Customers表里插入用户注册数据操作成功")