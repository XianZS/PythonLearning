# 进阶-1：大文件HMAC计算
import hashlib
import hmac
import os


def cal_file_hmac(file_path, secret_key, alg="sha256", chunk_size=65536):
    hmac_obj = hmac.new(secret_key, digestmod=alg)
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            hmac_obj.update(chunk)
    return hmac_obj.hexdigest()


if __name__ == "__main__":
    file_path = "../../word/10.2-hmac标准库学习.md"
    secret_key = "my_file_key".encode("utf-8")
    file_size = os.path.getsize(file_path)
    print(f"[file size]:{file_size}")
    file_hmac = cal_file_hmac(file_path, secret_key, "sha256")
    print(f"文件的hmac值:{file_hmac}")
    make_hmac_obj = hmac.new(secret_key, digestmod="sha256")
    with open(file_path, "rb") as f:
        make_hmac_obj.update(f.read())
    val_hmac = make_hmac_obj.hexdigest()
    print(f"本地存储的hmac值:{val_hmac}")
    judge = hmac.compare_digest(val_hmac, file_hmac)
    print(f"[judge]:{judge}")
