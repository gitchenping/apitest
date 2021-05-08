from enum import Enum

class EnumSendAndCheckEmailVcode(Enum):
    FORMAT_ERROR=('1', "custid，email，verify_type有一个为空或email格式不正确或verify_type、max_send_time、effective_time不是一个数字")
    VERIFY_TYPE_NOT_IN_CONF=('-1', "输入的verify_type不是config文件里配置的verify_type取值中的一个")
    READ_TIME_QT_MAX_SEND_TIME=('-2', "读取的次数大于等于 max_send_time")
    INSERT_DB_ERROR=('-3', "往email_verify表插入一条数据失败")
    INSERT_QUEUEDB_ERROR_FAIL_DELETE_EMAIL_DB=('-4', "往instant_message_queue表里插入数据失败后删除之前插入email_verify表里的数据失败")
    INSERT_QUEUEDB_ERROR_SUCCESS_DELETE_EMAIL_DB=('-5', "往instant_message_queue表里插入数据失败且删除之前插入email_verify表里的数据成功")
    SUCCESS=('0', "往email_verify表和instant_message_queue表或msg_cs_queue表里插入数据都成功")