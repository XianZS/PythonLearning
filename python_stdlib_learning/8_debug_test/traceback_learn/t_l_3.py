import traceback


# 进阶-3：异常组
# 3.11 以上版本:
# ExceptionGroup
# 3.14 以上版本:
# 改进了异常组的traceback显示
def val_user(user):
    errors = []
    if not user.get("name"):
        errors.append(ValueError("用户名不能为空"))
    if not user.get("email"):
        errors.append(ValueError("邮箱不能为空"))
    if not user.get("password") or len(user["password"]) < 6:
        errors.append(ValueError("密码不能为空 或 密码的字符长度必须大于等于6"))
    if errors:
        raise ExceptionGroup("用户验证失败", errors)  # type:ignore


try:
    val_user({"name": "", "email": "test@example.com", "password": "123"})
except ExceptionGroup as eg:
    traceback.print_exc()
