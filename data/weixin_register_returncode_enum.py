from enum import Enum

class WeixinRegistrReturnCodeEnum(Enum):
    FORMATTER_ERROR=("1", "参数格式不正确")
    EMAIL_EXISTS=("-1", "邮箱已经存在库里")
    NICKNAME_EXISTS=("-2", "昵称已经存在库里")
    MOBILE_PHONE_EXISTS=("-3", "手机号已经存在库里")
    WEIXIN_REGISTER_IS_BIND=("-4", "当前微信曾绑定过其它custid,无需重复绑定")
    SESSION_ERROR=(-7, "调用写session接口失败"),
    WEIXIN_REGISTER_DB_ERROR=(-8, "微信注册数据库异常")
    APPKEY_ERROR=("-10", "参数appkey未传值或传的值不是申请分配的")
    SUCCESS=("0", "往customer库的Customers表里插入用户注册数据操作成功")

