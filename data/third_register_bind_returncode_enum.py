from enum import Enum

class  ThirdRegisterBindStatusEnum(Enum):
    FORMATTER_ERROR=('1', "参数格式不正确")
    SMS_VERIFY_FAIL=('-1', "当当线上新用户短信验证码校验失败")
    CUST_THIRD_ID_IS_BIND=('-2', "cust_third_id已经绑定过，无需重复绑定")
    MOBILEPHONE_IS_BIND=('-3', "当前手机号已被其它实体书店用户绑定")
    REGISTER_FAIL=('-4', "账号注册失败")
    BIND_ERROR=('-5', "账号绑定失败")
    VCODE_EXISTS_MOBILE_EXISTS=('-6', "vcode参数有值时，手机号在当当线上库存在")
    VCODE_NOT_EXISTS_MOBILE_NOT_EXISTS=('-7', "vcode参数没有值时，手机号在当当线上库不存在")
    SUCCESS=('0', "往customer库的Customers表里插入用户注册数据操作成功")