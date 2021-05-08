from enum import Enum

class GetUserProfileReturnCodeEnum(Enum):
    SUCCESS=(0, "success")
    CUSTID_WRONG=(1, "custid不正确")
    KEWWORDWRONG=(2, "keyword不正确")
    EMPTYINFO=(3,'查询数据为空')
