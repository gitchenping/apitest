from enum import Enum

class EnumStatusCode(Enum):
        PARAM_ILLEGAL=('1', "参数错误")
        UNIONID_QUERY_FAILED=('-1', "当前绑定关系不存在，无需解绑")
        COMBINE_DENY=('-3', "账号合并的不支持解绑")
        DB_ERROR=('-8', "数据库系统异常")
        SUCCESS=('0', "成功")
