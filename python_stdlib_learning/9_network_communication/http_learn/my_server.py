# === 服务端 ===
# 我们将使用http标准库实现一个完成的文件传输系统
# 包括：
# - 服务端
# - 客户端
# 支持：
# - 文件上传
# - 文件下载
# - 查看文件列表
# - 删除文件
from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
import http
import urllib.parse


# 自定义文件服务器请求处理器
class FileServerHandler(BaseHTTPRequestHandler):
    # 配置文件存储的文件夹名称
    STORGAE_DIR = "file_storage"

    def __init__(self, *args, **kwargs):
        os.makedirs(self.STORGAE_DIR, exist_ok=True)
        super().__init__(*args, **kwargs)

    def send_json(self, data, status_code=http.HTTPStatus.OK):
        # 向客户端返回json格式数据
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        # 发送数据
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def do_GET(self):
        # 查询和下载文件
        # self.path
        # {dha9iijdwughij*,qhduhqo,127.0.0.1/files/some/quit}
        parsed_path = urllib.parse.urlparse(self.path)
        # /files/some/quit
        # /delete/some/quit
        path = parsed_path.path
        if path == "/files":
            files = []
            # 遍历STORGAE_DIR下面的所有文件
            for filename in os.listdir(self.STORGAE_DIR):
                # 子目录下面的文件和文件夹：main.py main2.py some q.txt
                # /storage_dir/filename
                file_path = os.path.join(self.STORGAE_DIR, filename)
                if os.path.isfile(file_path):
                    files.append(
                        {
                            "name": filename,
                            "size": os.path.getsize(file_path),
                            "modified_time": os.path.getmtime(file_path),
                        }
                    )
            self.send_json({"files": files})
            return
        # path object: /some1/some2
        # startswith("some3")
        elif path.startswith("/download/"):
            filename = urllib.parse.unquote(path[len("/download/") :])
            file_path = os.path.join(self.STORGAE_DIR, filename)
            if not os.path.isfile(file_path):
                self.send_json({"error": "文件不存在"}, http.HTTPStatus.NOT_FOUND)
                return
            # 发送文件流
            self.send_response(http.HTTPStatus.OK)
            self.send_header("Content-Type", "application/octet-stream")
            self.send_header(
                "Content-Disposition",
                f"attachment filename:{urllib.parse.quote(filename)}",
            )
            self.send_header("Content-Length", str(os.path.getsize(file_path)))
            self.end_headers()
            with open(file_path, "rb") as f:
                self.wfile.write(f.read())
        else:
            self.send_json({"error": "路径错误"}, http.HTTPStatus.NOT_FOUND)

    def do_POST(self):
        if self.path == "/upload":
            filename = self.headers.get("X-Filename")
            if not filename:
                self.send_json({"error": "缺少必要信息"}, http.HTTPStatus.BAD_REQUEST)
                return
            filename = urllib.parse.unquote(filename)
            file_path = os.path.join(self.STORGAE_DIR, filename)
            # 读取文件内容
            content_length = int(self.headers.get("Content-Length", 0))
            file_content = self.rfile.read(content_length)
            # 将文件保存到本地之中
            with open(file_path, mode="wb") as f:
                f.write(file_content)
            # 返回上传成功的信息
            self.send_json(
                {
                    "message": "文件上传成功",
                    "filename": filename,
                    "size": len(file_content),
                }
            )
        else:
            self.send_json({"error": "路径错误"}, http.HTTPStatus.NOT_FOUND)

    def do_DELETE(self):
        parsed_path = urllib.parse.urlparse(self.path)
        if parsed_path.path.startswith("/delete/"):
            filename = urllib.parse.unquote(parsed_path.path[len("/delete/") :])
            file_path = os.path.join(self.STORGAE_DIR, filename)
            if not os.path.isfile(file_path):
                self.send_json({"error": "文件不存在"}, http.HTTPStatus.NOT_FOUND)
                return
            # 删除文件
            os.remove(file_path)
            self.send_json({"message": f"文件{file_path}删除成功"})
        else:
            self.send_json({"error": "路径不存在"}, http.HTTPStatus.NOT_FOUND)


def run_server(host="0.0.0.0", port=8000):
    # 启动文件服务器
    server = HTTPServer((host, port), FileServerHandler)
    print(f"文件服务器已经成功启动:http://localhost:{port}")
    print("""
    GET     /files              文件列表
    GET     /download/文件名    下载文件
    POST    /upload/文件名      上传文件
    DELETE  /delete/文件名      删除文件
          """)
    server.serve_forever()


if __name__ == "__main__":
    run_server()
