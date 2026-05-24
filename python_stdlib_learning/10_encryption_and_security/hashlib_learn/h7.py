# 进阶-3：并行计算多个hash值
import hashlib


def cal_mul_hashes(data, algs):
    print("===")
    # 为同一个数据计算多个不同算法的hash值
    hash_objs = {alg: hashlib.new(alg) for alg in algs}
    for hash_obj in hash_objs.values():
        hash_obj.update(data)
    results = {alg: hash_obj.hexdigest() for alg, hash_obj in hash_objs.items()}
    return results


if __name__ == "__main__":
    data = "并行计算多个哈希数值".encode("utf-8")
    algs = ["md5", "sha1", "sha256", "sha512"]
    results = cal_mul_hashes(data, algs)
    print("多个算法的hash结果:")
    for alg, hash_value in results.items():
        print(f"[{alg}]:{hash_value}")
