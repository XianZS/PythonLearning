"""Day 12 验证：异常处理理论与实践

Day 12 没有新增代码——它是对 Day 11 中 chat_stream() 异常处理逻辑的讲解。
验证方式如下。
"""

# ============================================================
# 验证方式 1：运行 Day 11 的测试
# ============================================================
# test_day11_deepseek_client.py 中的以下测试覆盖了异常处理：
#   test_authentication_error  → 验证 AuthenticationError (HTTP 401)
#   test_rate_limit_error      → 验证 RateLimitError (HTTP 429)
#   test_http_400_error        → 验证 HTTP 400 参数错误
#   test_http_500_error        → 验证 HTTP 500 服务器错误
#
# 运行：
#   python tests/test_day11_deepseek_client.py
#
# 预期输出：全部 9 个测试通过，含 4 个异常处理测试。

# ============================================================
# 验证方式 2：手动触发错误（终端交互）
# ============================================================
"""
在 Python 交互环境中执行以下操作：

>>> from src.deepseek_client import chat_stream

# 1. 用假密钥触发 AuthenticationError
>>> for chunk in chat_stream(api_key="sk-fake-key-12345", message=[{"role": "user", "content": "hi"}]):
...     if chunk["type"] == "error":
...         print(chunk["message"])
🔑 API 密钥无效，请检查后重试。可以前往 platform.deepseek.com/api_keys 获取密钥。

# 2. 用错误的 base_url 触发 APIConnectionError
>>> import src.deepseek_client as dc
>>> dc.DEEPSEEK_BASE_URL = "https://invalid-host.example.com"
>>> for chunk in chat_stream(api_key="sk-test", message=[{"role": "user", "content": "hi"}]):
...     if chunk["type"] == "error":
...         print(chunk["message"])
🌐 无法连接到 DeepSeek 服务器，请检查网络连接。

# 3. 验证异常捕获顺序（具体 → 宽泛）
# AuthenticationError 继承自 Exception，
# 但因为我们把它放在前面，它会被优先匹配。
# 如果调换顺序（先 except Exception），AuthenticationError 永远不会被触发。
"""

if __name__ == "__main__":
    print("Day 12 验证说明：")
    print("  1. 运行 test_day11_deepseek_client.py 中的 4 个异常测试")
    print("  2. 验证所有 6 种异常类型（401/429/超时/连接/400/500）都有中文提示")
    print("  3. 确认异常不 raise 而是 yield（防止 for 循环崩溃）")
    print("  4. 确认每个错误消息包含：emoji + 中文描述 + 解决建议")
    print()
    print("Verification criteria:")
    print("  - All error messages start with emoji")
    print("  - Messages in Chinese")
    print("  - AuthenticationError includes platform.deepseek.com URL")
    print("  - 400/500 checks 'status_code' before status code number")
    print("  - 消息为中文（方便国内用户）")
    print("  - AuthenticationError 包含获取密钥的 URL")
    print("  - 400/500 错误先检查 'status_code' 再检查状态码数字")
