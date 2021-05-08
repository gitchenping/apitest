from enum import Enum

class EnumStatusCode(Enum):
        SUCCESS=('0', "send success")  #往customer_verify_sms 表成功
        PARAM_ILLEGAL=('1', "param illegal") #custid，mobile_phone，verify_type有一个为空或mobile_phone格式不正确或verify_type、max_send_time、effective_time不是一个数字、time_unit不正确
        VERIFY_TYPE=('-1', "verify_type illegal") #输入的verify_type不是config文件里配置的verify_type取值中的一个，见本页面上的手机验证短信的type说明
        MAX_TIMES=('-2', "send max times") #一天之内同一手机号同一类型的验证码发送次数大于max_send_time
        DB_FAILED_MOBILE_VERIFY=('-3', "write db failed")
        SMS_QUEUE=('-4', "sms_queue failed") #往sms_queue表里插入数据失败后删除之前插入customer_verify_sms 表里的数据失败
        API_FAIL=('-5', "invoke send message api failed")
        CUST_NOT_FIND=('-6', "cust not found")    #除新用户注册以外的情况时根据custid读取用户信息为空
        TIME_INTERVAL=('-7', "less than min time interval 120s") #同一个手机短信验证码发送间隔小于120秒
        IP_LIMIT=('-8', "ip limit 10 min more than 5 times") #同一ip在最近10分钟发送超过5次短信验证码
        BOOKSTORE_MAX_TIMES=('-10', "book store send max times") #线下实体书店短信发送量超过限制（每24小时1000条）

