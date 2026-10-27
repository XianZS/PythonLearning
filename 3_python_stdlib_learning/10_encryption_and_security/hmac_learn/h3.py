# 进阶-2：基于HMAC的API签名生成
import hmac
import hashlib
from nt import times
import time
import uuid
import urllib.parse


def generate_api_sign(secret_key, params, timestamp=None, nonce=None):
    timestamp = timestamp or int(time.time())
    nonce = nonce or str(uuid.uuid4())
    # 将时间戳和随机数添加到参数之中
    params_with_auth = params.copy()
    params_with_auth["timestamp"] = str(timestamp)
    params_with_auth["nonce"] = nonce
    sorted_params = sorted(params_with_auth.items(), key=lambda x: x[0])
    # 拼接成字符串格式
    strs = urllib.parse.urlencode(sorted_params).encode("utf-8")
    sign = hmac.new(secret_key, strs, hashlib.sha256).hexdigest()
    return sign, timestamp, nonce


if __name__ == "__main__":
    client_secret = "client_secret_123".encode("utf-8")
    request_params = {
        "user_id": "12345",
        "action": "get_user_info",
        "page": "1",
        "page_size": "10",
    }
    sign, timestamp, nonce = generate_api_sign(client_secret, request_params)
    print("API请求签名的生成结果:")
    print(f"时间戳:{timestamp}")
    print(f"随机数:{nonce}")
    print(f"签名:{sign}")
    request_params["timestamp"] = str(timestamp)
    request_params["nonce"] = nonce
    request_params["sign"] = sign
    print(f"添加之后的请求体为:{request_params}")
