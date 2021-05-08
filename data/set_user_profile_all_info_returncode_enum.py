from enum import Enum

class SetUserProfileAllInfoReturnCodeEnum(Enum):
    SUCCESS=(0, "success")
    CUSTID_WRONG=(1, "custid不正确")
    ADDRESS_WRONG=(5,"cust_address设置不成功（区域id不存在）")
    SEX_WRONG=(6, "cust_sex设置不成功 内容只能为0 或者1")
    BIRTHDAY_LONG=(7,"cust_birthday日期格式不正确")
    JOB_LONG=(8,"cust_job长度超限 40")


