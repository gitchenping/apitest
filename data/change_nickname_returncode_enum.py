from enum import Enum

class ChangeNicknameReturnCodeEnum(Enum):
    FORMATTER_ERROR=('1', "参数错误")
    NICKNAME_EXISTS=('-1', "新昵称已经在库")
    USER_NOT_EXISTS=('-2', "用户不存在")
    DB_ERROR=('-3', "修改Customers表用户信息操作失败")
    UPDATE_CACHE_ERROR=('-4', "将新昵称更新到redis操作失败")
    SUCCESS=('0', "所有操作都成功")