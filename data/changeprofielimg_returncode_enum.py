from enum import Enum

class ChangeProfileImgReturnCodeEnum(Enum):
    SUCCESS=(0, "upload user image succeed")
    INFO_NULL=(1, "post info is null")
    USER_NOT_EXIST=(2, "this user is not exist")
    EMPTYINFO=(3,'查询数据为空')