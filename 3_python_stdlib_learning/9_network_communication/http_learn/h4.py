import http.server
import json
import http


# 进阶-3：服务端高级用法
# 处理多种HTTP方法
class APIServerHandler(http.server.BaseHTTPRequestHandler):
    # 辅助方法：发送json响应
    def send_json(self, data, status_code=http.HTTPStatus.OK):
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    # 辅助方法：请求JSON数据
    def get_json_body(self):
        content_length = int(self.headers.get("Content_Length", 0))
        if content_length == 0:
            return None
        body = self.rfile.read(content_length)
        return json.loads(body.decode("utf-8"))

    # 辅助方法：GET method
    def do_GET(self):
        if self.path == "/":
            self.send_json(
                {
                    "message": "welcome to my website!",
                    "endpoints": ["/api/users", "/api/info"],
                }
            )
        elif self.path == "/api/info":
            self.send_json({"server": "Python http server", "version": "3.14"})
        else:
            self.send_json(
                {"message": "Error", "version": "3.14"}, http.HTTPStatus.NOT_FOUND
            )

    # 辅助方法：POST method
    def do_POST(self):
        if self.path == "/api/users":
            try:
                user_data = self.get_json_body()
                if not user_data or "name" not in user_data:
                    self.send_json(
                        {"error": "无效的数据响应"}, http.HTTPStatus.BAD_REQUEST
                    )
                    return
                user_id = 1
                new_user = {
                    "id": user_id,
                    "user_name": user_data["name"],
                    "email": user_data["email"],
                }
                self.send_json(
                    {"message": "用户创建成功", "user": new_user},
                    http.HTTPStatus.CREATED,
                )
            except Exception as e:
                print("e")


if __name__ == "__main__":
    server = http.server.HTTPServer(("", 8000), APIServerHandler)
    print("HTTP Server Start!")
    server.serve_forever()
