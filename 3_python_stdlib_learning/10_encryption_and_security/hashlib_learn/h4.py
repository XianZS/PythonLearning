# 基础-4：大文件HASH值计算
import hashlib
import os


def cal_big_file_hash(file_path, alg="sha256", chunk_size=1024):
    # 计算大文件的hash值
    hash_obj = hashlib.new(alg)
    with open(file_path, "rb") as f:
        while chunk := f.read(chunk_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()


# 测试
if __name__ == "__main__":
    file_path = "../../word/10.1-hashlib标准库学习.md"
    file_size = os.path.getsize(file_path)
    print(f"[当前文件的大小为]:{file_size}")
    sha256_res = cal_big_file_hash(file_path, "sha256")
    print(f"[sha256]:{sha256_res}")
    md5_res = cal_big_file_hash(file_path, "md5")
    print(f"[md5]:{md5_res}")
