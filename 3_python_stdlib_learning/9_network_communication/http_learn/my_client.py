# === 客户端 ===
# 我们将使用http标准库实现一个完成的文件传输系统
# 包括：
# - 服务端
# - 客户端
# 支持：
# - 文件上传
# - 文件下载
# - 查看文件列表
# - 删除文件
import http.client
import json
import os
import urllib.parse


class FileClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        # 创建HTTP连接
        self.conn = http.client.HTTPConnection(host, port, timeout=10)

    def list_files(self):
        self.conn.request("GET", "/files")
        response = self.conn.getresponse()
        return json.loads(response.read().decode("utf-8"))

    def upload_files(self, local_path):
        # 校验被上传的文件是否存在
        if not os.path.isfile(local_path):
            raise FileNotFoundError(f"本地文件不存在:{local_path}")
        # 获取文件名
        filename = os.path.basename(local_path)
        # 编码
        encoded_filename = urllib.parse.quote(filename)
        # 读取文件二进制内容
        with open(local_path, mode="rb") as f:
            file_content = f.read()
        # 请求头
        headers = {
            "X-Filename": encoded_filename,
            "Content-Length": str(len(file_content)),
        }
        # 发送上传请求
        self.conn.request("POST", "/upload", body=file_content, headers=headers)
        response = self.conn.getresponse()
        return json.loads(response.read().decode("utf-8"))

    def download_file(self, filename, save_path=None):
        if save_path is None:
            save_path = filename
        encoded_filename = urllib.parse.quote(filename)
        self.conn.request("GET", f"/download/{encoded_filename}")
        response = self.conn.getresponse()
        if response.status != 200:
            return
        # json.loads(response.read().decode("utf-8"))
        # 保存文件到本地之中
        with open(save_path, "wb") as f:
            f.write(response.read())
        return {"message": f"文件下载成功,保存为:{save_path}"}

    def delete_file(self, filename):
        encoded_filename = urllib.parse.quote(filename)
        self.conn.request("DELETE", f"/delete/{encoded_filename}")
        response = self.conn.getresponse()
        return json.loads(response.read().decode("utf-8"))

    def close(self):
        self.conn.close()


def main():
    # 连接本地文件服务器
    client = FileClient("localhost", 8000)
    # 测试文件名
    test_file = "h1.py"
    try:
        print("=== 查看文件列表 ===")
        print(json.dumps(client.list_files(), indent=2, ensure_ascii=False))
        print("=== 测试上传文件 ===")
        print(json.dumps(client.upload_files(test_file), indent=2, ensure_ascii=False))
        print(json.dumps(client.list_files(), indent=2, ensure_ascii=False))
        print("=== 测试下载文件 ===")
        print(
            json.dumps(
                client.download_file("main.py", "下载的文件.py"),
                indent=2,
                ensure_ascii=False,
            )
        )
        print("=== 测试删除文件 ===")
        print(json.dumps(client.delete_file("some.py"), indent=2, ensure_ascii=False))
        print(json.dumps(client.list_files(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[Error]:{e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
