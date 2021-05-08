from enum import Enum

class  RegisterEnterpriseEnum(Enum):
    FORMATTER_ERROR=('1', "参数格式不正确")
    EMAIL_EXISTS=('-1', "邮箱已经存在库里")
    NICKNAME_EXISTS=('-2', "昵称已经存在库里")
    MOBILE_PHONE_EXISTS=('-3', "手机号已经存在库里")
    DB_INSERT_ERROR=('-4', "往customer库的Customers表里插入用户注册数据操作失败")
    ENTERPRISE_NAME_EXISTS=('-5', "公司名已经在库里")
    SESSION_API_ERROR=('-9', "调用写session接口失败")
    APPKEY_ERROR=('-10', "参数appkey未传值或传的值不是申请分配的")
    SUCCESS=('0', "往customer库的Customers表里插入用户注册数据操作成功")