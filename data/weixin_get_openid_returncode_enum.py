from enum import Enum

class EnumStatusCode(Enum):
        PARAM_ILLEGAL=('1',"参数错误")
        CUSTID_NOT_FIND=('-1',"custid不存在微信unionid绑定关系")
        OPENID_NOT_FIND=('-2',"未查到对应的openid")
        DB_ERROR=('-8',"数据库系统异常")
        SUCCESS=('0',"成功")