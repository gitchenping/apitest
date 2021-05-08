from enum import Enum

class WeixinBindCustidReturnCodeEnum(Enum):
    PARAM_ILLEGAL=(1, "参数错误")
    CUSTID_NOT_FIND=("-1", "根据custid读取信息为空")
    CUSTID_BINDED=("-2", "当前custid已绑定过其它微信")
    WEIXIN_BINDED=("-3", "当前微信曾绑定过其它custid")
    WRITE_SESSION_FAILED=(-7, "调用写session信息接口失败")
    DB_ERROR=(-8, "数据库系统异常")
    APPKEY_ILLEGAL=("-10", "参数appkey未传值或传的值不是申请分配的")
    SUCCESS=("0", "成功")
