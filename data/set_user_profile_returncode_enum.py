from enum import Enum

class SetUserProfileReturnCodeEnum(Enum):
    SUCCESS=(0, "success")
    CUSTID_WRONG=(1, "custid不正确")
    KEYWORD_EMPTY=(2,"keyword 为空")
    KEWWORD_WRONG=(3, "keyword不正确")
    CONTENT_EMPTY=(4,"设置内容为空")
    ADDRESS_FAIL=(5,"new_address设置不成功（区域id不存在）")
    SEX_FAIL=(6,"new_sex 设置不成功 内容只能为0 或者1")
    BIRTHDAY_FAIL=(7,"new_birthday 日期格式不正确")
    STATION_FAIL=(8,"station 长度超限 40")







