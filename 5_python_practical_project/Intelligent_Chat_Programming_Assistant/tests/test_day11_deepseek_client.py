"""Day 11 测试：deepseek_client.py — chat_stream 流式对话生成器

验证点：
1. chat_stream 正确传递参数给 OpenAI 客户端
2. reasoning chunk (思维链) 被正确 yield
3. content chunk (普通回复) 被正确 yield
4. done chunk 在流结束时被 yield
5. AuthenticationError → 友好的中文错误消息
6. RateLimitError → 友好的中文错误消息
7. HTTP 400/500 → 友好的中文错误消息
8. 思维链模式下 temperature 参数不传递

运行方式：
    cd Intelligent_Chat_Programming_Assistant
    python tests/test_day11_deepseek_client.py
"""

import sys
import os
from unittest.mock import patch, MagicMock

# 确保项目根目录在 sys.path 中
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.deepseek_client import chat_stream


def mock_chunk(content=None, reasoning_content=None):
    """构造一个模拟的 OpenAI stream chunk"""
    chunk = MagicMock()
    chunk.choices = [MagicMock()]
    delta = MagicMock()
    delta.content = content
    # 使用 getattr 能正常获取 reasoning_content
    if reasoning_content:
        delta.reasoning_content = reasoning_content
    else:
        delattr(delta, "reasoning_content")  # 模拟属性不存在
    chunk.choices[0].delta = delta
    return chunk


class TestChatStream:
    """测试 chat_stream 生成器的各个场景"""

    def test_yields_content_chunks(self):
        """测试：普通对话正常返回 content chunk"""
        mock_chunks = [
            mock_chunk(content="你好"),
            mock_chunk(content="，世界"),
            mock_chunk(content="！"),
        ]

        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_response = MagicMock()
            mock_response.__iter__.return_value = mock_chunks
            mock_client.chat.completions.create.return_value = mock_response

            chunks = list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "你好"}],
                model="deepseek-v4-flash",
                temperature=0.7,
            ))

        content_chunks = [c for c in chunks if c["type"] == "content"]
        done_chunks = [c for c in chunks if c["type"] == "done"]

        assert len(content_chunks) == 3, f"应该有 3 个 content chunk，实际: {len(content_chunks)}"
        assert len(done_chunks) == 1, "流结束时应有 done chunk"
        assert "".join(c["text"] for c in content_chunks) == "你好，世界！"

    def test_yields_reasoning_chunks(self):
        """测试：V4 Pro 思维链模式返回 reasoning chunk"""
        mock_chunks = [
            mock_chunk(reasoning_content="让我"),
            mock_chunk(reasoning_content="思考一下"),
            mock_chunk(content="答案是 42"),
        ]

        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_response = MagicMock()
            mock_response.__iter__.return_value = mock_chunks
            mock_client.chat.completions.create.return_value = mock_response

            chunks = list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "1+1=?"}],
                model="deepseek-v4-pro",
                enable_thinking=True,
            ))

        reasoning_chunks = [c for c in chunks if c["type"] == "reasoning"]
        content_chunks = [c for c in chunks if c["type"] == "content"]

        assert len(reasoning_chunks) == 2
        assert len(content_chunks) == 1
        assert "".join(c["text"] for c in reasoning_chunks) == "让我思考一下"

    def test_thinking_mode_sets_extra_body(self):
        """测试：思维链模式传递 extra_body，不传 temperature"""
        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_response = MagicMock()
            mock_response.__iter__.return_value = []
            mock_client.chat.completions.create.return_value = mock_response

            list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "test"}],
                model="deepseek-v4-pro",
                temperature=0.7,
                enable_thinking=True,
            ))

            call_kwargs = mock_client.chat.completions.create.call_args.kwargs
            assert "extra_body" in call_kwargs, "思维链模式应传递 extra_body"
            assert call_kwargs["extra_body"] == {"thinking": {"type": "enabled"}}
            assert "temperature" not in call_kwargs, "思维链模式下不应传递 temperature"

    def test_normal_mode_passes_temperature(self):
        """测试：普通模式传递 temperature，不传 extra_body"""
        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_response = MagicMock()
            mock_response.__iter__.return_value = []
            mock_client.chat.completions.create.return_value = mock_response

            list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "test"}],
                model="deepseek-v4-flash",
                temperature=1.5,
            ))

            call_kwargs = mock_client.chat.completions.create.call_args.kwargs
            assert "extra_body" not in call_kwargs
            assert call_kwargs["temperature"] == 1.5

    def test_authentication_error(self):
        """测试：认证失败返回友好中文提示"""
        from openai import AuthenticationError

        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.side_effect = AuthenticationError(
                "Invalid API key",
                response=MagicMock(),
                body=None,
            )

            chunks = list(chat_stream(
                api_key="sk-wrong-key",
                message=[{"role": "user", "content": "test"}],
            ))

        error_chunks = [c for c in chunks if c["type"] == "error"]
        assert len(error_chunks) == 1
        assert "API 密钥无效" in error_chunks[0]["message"]
        assert "platform.deepseek.com" in error_chunks[0]["message"]

    def test_rate_limit_error(self):
        """测试：频率限制返回友好中文提示"""
        from openai import RateLimitError

        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.side_effect = RateLimitError(
                "Rate limit exceeded",
                response=MagicMock(),
                body=None,
            )

            chunks = list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "test"}],
            ))

        error_chunks = [c for c in chunks if c["type"] == "error"]
        assert len(error_chunks) == 1
        assert "频率超限" in error_chunks[0]["message"]

    def test_http_400_error(self):
        """测试：HTTP 400 返回参数错误提示"""
        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            # 模拟 OpenAI SDK 抛出的异常，消息中包含 status_code 400
            mock_client.chat.completions.create.side_effect = Exception(
                "Error code: 400 - status_code 400 - Bad Request"
            )

            chunks = list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "test"}],
            ))

        error_chunks = [c for c in chunks if c["type"] == "error"]
        assert len(error_chunks) == 1
        assert "请求参数错误" in error_chunks[0]["message"]

    def test_http_500_error(self):
        """测试：HTTP 500 返回服务器错误提示"""
        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_client.chat.completions.create.side_effect = Exception(
                "status_code 500 - Internal Server Error"
            )

            chunks = list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "test"}],
            ))

        error_chunks = [c for c in chunks if c["type"] == "error"]
        assert len(error_chunks) == 1
        assert "服务器内部错误" in error_chunks[0]["message"]

    def test_default_model_is_flash(self):
        """测试：默认使用 MODEL_FLASH"""
        with patch("src.deepseek_client.OpenAI") as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            mock_response = MagicMock()
            mock_response.__iter__.return_value = []
            mock_client.chat.completions.create.return_value = mock_response

            list(chat_stream(
                api_key="sk-test-key",
                message=[{"role": "user", "content": "test"}],
            ))

            call_kwargs = mock_client.chat.completions.create.call_args.kwargs
            assert call_kwargs["model"] == "deepseek-v4-flash"

    def test_uses_model_constant(self):
        """测试：使用 MODEL_FLASH/MODEL_PRO 常量而非硬编码字符串"""
        import src.deepseek_client as dc
        assert dc.MODEL_FLASH == "deepseek-v4-flash"
        assert dc.MODEL_PRO == "deepseek-v4-pro"


if __name__ == "__main__":
    print("=" * 60)
    print("Day 11 测试：deepseek_client.py")
    print("=" * 60)

    tests = TestChatStream()
    passed = 0
    failed = 0

    test_methods = [m for m in dir(tests) if m.startswith("test_")]
    for method_name in test_methods:
        method = getattr(tests, method_name)
        try:
            method()
            print(f"  [PASS] {method_name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {method_name}: {e}")
            failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败, {len(test_methods)} 总计")
    if failed > 0:
        sys.exit(1)
