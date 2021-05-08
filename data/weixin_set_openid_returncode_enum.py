from enum import Enum

class EnumStatusCode(Enum):
    PARAM_ILLEGAL=('1', "参数错误")
    UNIONID_QUERY_FAILED=('-1', "用openid在微信查询unionid失败")
    OPENID_NOT_INIT=('-2', "数据库未查到openid")
    DB_ERROR=('-8', "数据库系统异常")
    SUCCESS=('0', "成功")