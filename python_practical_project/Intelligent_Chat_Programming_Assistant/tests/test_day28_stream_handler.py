"""Day 28 测试：stream_handler.py — 流式响应处理

验证点：
1. _render_reasoning_html 在 streaming=True 时展开面板
2. _render_reasoning_html 在 streaming=False 时折叠面板
3. process_stream 正确处理 reasoning/content/done/error 四种 chunk
4. process_stream 在无内容时显示友好提示
5. HTML 模板字符串完整

运行方式：
    cd Intelligent_Chat_Programming_Assistant
    python tests/test_day28_stream_handler.py
"""

import sys
import os
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_render_reasoning_html_streaming_true():
    """测试：流式进行中时面板展开 + 显示"思考中" """
    from src.stream_handler import _render_reasoning_html

    html = _render_reasoning_html("让我想想...", streaming=True)

    # streaming=True → <details open> (展开状态)
    assert "<details open>" in html, "streaming=True 时面板应展开"
    assert "🧠 思考中..." in html, "streaming=True 时应显示'思考中'"
    assert "让我想想..." in html, "推理文本应出现在 HTML 中"


def test_render_reasoning_html_streaming_false():
    """测试：流式结束后面板折叠 + 显示"查看思考过程" """
    from src.stream_handler import _render_reasoning_html

    html = _render_reasoning_html("最终推理结果", streaming=False)

    # streaming=False → <details> (折叠状态，无 open 属性)
    assert "<details>" in html, "streaming=False 时面板应折叠"
    assert "open" not in html.split("<details>")[1].split(">")[0], (
        "streaming=False 时不应有 open 属性"
    )
    assert "🧠 查看思考过程" in html, "streaming=False 时应显示'查看思考过程'"
    assert "最终推理结果" in html


def test_render_reasoning_html_styles():
    """测试：HTML 模板包含所有必需的 CSS 样式"""
    from src.stream_handler import _render_reasoning_html

    html = _render_reasoning_html("test", streaming=True)

    required_styles = [
        "color: #888",        # 标题灰色
        "cursor: pointer",    # 标题可点击
        "font-size: 0.9em",   # 标题字号
        "color: #aaa",        # 内容区灰色
        "font-size: 0.85em",  # 内容区字号
        "line-height: 1.6",   # 行间距
        "border-left: 3px solid #555",  # 左边框
    ]

    for style in required_styles:
        assert style in html, f"缺少 CSS 样式: {style}"


def test_process_stream_handles_content():
    """测试：process_stream 正确处理 content chunk"""
    from src.stream_handler import process_stream

    # 模拟 chat_stream 产生 2 个 content chunk，然后 done
    mock_chunks = [
        {"type": "content", "text": "你好"},
        {"type": "content", "text": "世界"},
        {"type": "done", "usage": None},
    ]

    mock_reasoning_placeholder = MagicMock()
    mock_content_placeholder = MagicMock()

    with patch("src.stream_handler.chat_stream", return_value=mock_chunks):
        reasoning_text, content_text, has_error = process_stream(
            api_key="sk-test",
            api_message=[{"role": "user", "content": "hi"}],
            settings={"model": "deepseek-v4-flash", "temperature": 0.7,
                      "max_tokens": 4096, "enable_thinking": False},
            reasoning_placeholder=mock_reasoning_placeholder,
            content_placeholder=mock_content_placeholder,
        )

    assert content_text == "你好世界", f"content 应累积，实际: {content_text}"
    assert reasoning_text == "", "无 reasoning 时应为空字符串"
    assert has_error is False

    # 验证最终渲染：去除光标
    final_call_arg = mock_content_placeholder.markdown.call_args_list[-1][0][0]
    assert "▌" not in final_call_arg, "最终渲染不应包含光标"


def test_process_stream_handles_reasoning():
    """测试：process_stream 正确处理 reasoning chunk"""
    from src.stream_handler import process_stream

    mock_chunks = [
        {"type": "reasoning", "text": "让我"},
        {"type": "reasoning", "text": "想想"},
        {"type": "content", "text": "42"},
        {"type": "done", "usage": None},
    ]

    mock_reasoning_placeholder = MagicMock()
    mock_content_placeholder = MagicMock()

    with patch("src.stream_handler.chat_stream", return_value=mock_chunks):
        reasoning_text, content_text, has_error = process_stream(
            api_key="sk-test",
            api_message=[{"role": "user", "content": "?"}],
            settings={"model": "deepseek-v4-pro", "temperature": 0.7,
                      "max_tokens": 4096, "enable_thinking": True},
            reasoning_placeholder=mock_reasoning_placeholder,
            content_placeholder=mock_content_placeholder,
        )

    assert reasoning_text == "让我想想"
    assert content_text == "42"
    assert has_error is False

    # reasoning_placeholder 应该被调用了 3 次（2 次 streaming + 1 次 final）
    assert mock_reasoning_placeholder.markdown.call_count >= 2


def test_process_stream_handles_error():
    """测试：process_stream 正确处理 error chunk"""
    from src.stream_handler import process_stream

    mock_chunks = [
        {"type": "content", "text": "前半段"},
        {"type": "error", "message": "🔑 API 密钥无效，请检查后重试。"},
    ]

    mock_reasoning_placeholder = MagicMock()
    mock_content_placeholder = MagicMock()

    with patch("src.stream_handler.chat_stream", return_value=mock_chunks):
        reasoning_text, content_text, has_error = process_stream(
            api_key="sk-wrong",
            api_message=[{"role": "user", "content": "hi"}],
            settings={"model": "deepseek-v4-flash", "temperature": 0.7,
                      "max_tokens": 4096, "enable_thinking": False},
            reasoning_placeholder=mock_reasoning_placeholder,
            content_placeholder=mock_content_placeholder,
        )

    assert has_error is True
    # 错误时应在 content_placeholder 上显示错误
    mock_content_placeholder.error.assert_called_once()


def test_process_stream_empty_response():
    """测试：模型返回空内容时显示友好提示"""
    from src.stream_handler import process_stream

    mock_chunks = [
        {"type": "done", "usage": None},  # 直接结束，无任何内容
    ]

    mock_reasoning_placeholder = MagicMock()
    mock_content_placeholder = MagicMock()

    with patch("src.stream_handler.chat_stream", return_value=mock_chunks):
        reasoning_text, content_text, has_error = process_stream(
            api_key="sk-test",
            api_message=[{"role": "user", "content": "hi"}],
            settings={"model": "deepseek-v4-flash", "temperature": 0.7,
                      "max_tokens": 4096, "enable_thinking": False},
            reasoning_placeholder=mock_reasoning_placeholder,
            content_placeholder=mock_content_placeholder,
        )

    assert reasoning_text == ""
    assert content_text == ""
    assert has_error is False
    # 应显示 info 提示
    mock_content_placeholder.info.assert_called_once_with("模型未返回任何内容，请重试。")


if __name__ == "__main__":
    print("=" * 60)
    print("Day 28 测试：stream_handler.py")
    print("=" * 60)

    tests = [
        ("_render_reasoning_html streaming=True", test_render_reasoning_html_streaming_true),
        ("_render_reasoning_html streaming=False", test_render_reasoning_html_streaming_false),
        ("HTML 模板 CSS 样式完整", test_render_reasoning_html_styles),
        ("process_stream 处理 content", test_process_stream_handles_content),
        ("process_stream 处理 reasoning", test_process_stream_handles_reasoning),
        ("process_stream 处理 error", test_process_stream_handles_error),
        ("process_stream 处理空响应", test_process_stream_empty_response),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")

    print(f"\n结果: {passed}/{len(tests)} 通过")
    if passed < len(tests):
        sys.exit(1)
