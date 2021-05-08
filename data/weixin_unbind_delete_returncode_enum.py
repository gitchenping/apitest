from enum import Enum

class WeixinUnbindDeleteReturnCodeEnum(Enum):
    PARAM_ILLEGAL=("1", "参数错误")
    CUST_NOT_FOUND=("-1", "当前账号不存在")
    UNBIND_FORBIDDEN=("-2", "30天内绑定的账号不允许解绑")
    COMBINE_DENY=("-3", "账号合并的不支持解绑")
    DB_ERROR=(-8, "数据库异常")
    SUCCESS=("0", "成功")


