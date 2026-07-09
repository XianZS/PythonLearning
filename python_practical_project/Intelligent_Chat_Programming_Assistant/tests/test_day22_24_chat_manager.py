"""Day 22-24 测试：chat_manager.py — 会话管理

Day 22: init_message, add_user_message, add_assistant_message
Day 23: get_message_count, get_all_message, clear_history, build_api_message
Day 24: estimate_token_count, should_warn_token_limit

因为 chat_manager 依赖 st.session_state，测试使用一个模拟类替代。

运行方式：
    cd Intelligent_Chat_Programming_Assistant
    python tests/test_day22_24_chat_manager.py
"""

import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---- Mock Streamlit session_state ----

class MockSessionState:
    """模拟 Streamlit 的 st.session_state，同时支持属性访问和 'in' 检查"""

    def __init__(self):
        self._data = {}

    def __contains__(self, key):
        return key in self._data

    def __getattr__(self, key):
        if key == "_data" or key.startswith("_"):
            return object.__getattribute__(self, key)
        if key in self._data:
            return self._data[key]
        raise AttributeError(f"MockSessionState has no attribute '{key}'")

    def __setattr__(self, key, value):
        if key == "_data" or key.startswith("_"):
            object.__setattr__(self, key, value)
        else:
            self._data[key] = value


class MockSt:
    """模拟 Streamlit 的 st 模块"""

    def __init__(self, initial_message=None):
        self.session_state = MockSessionState()
        if initial_message is not None:
            self.session_state.message = initial_message


# ---- Day 22 Tests ----

def test_init_message_creates_empty_list():
    """Day 22: 首次调用时创建空列表"""
    from src.chat_manager import init_message

    mock_st = MockSt()
    with patch("src.chat_manager.st", mock_st):
        init_message()

    assert mock_st.session_state.message == []


def test_init_message_idempotent():
    """Day 22: 多次调用不覆盖已有数据"""
    from src.chat_manager import init_message

    existing = [{"role": "user", "content": "nihao"}]
    mock_st = MockSt(initial_message=existing)
    with patch("src.chat_manager.st", mock_st):
        init_message()

    assert mock_st.session_state.message == existing
    assert len(mock_st.session_state.message) == 1


def test_add_user_message():
    """Day 22: 正确添加用户消息"""
    from src.chat_manager import add_user_message

    mock_st = MockSt()
    with patch("src.chat_manager.st", mock_st):
        add_user_message("nihao AI!")

    msg = mock_st.session_state.message
    assert len(msg) == 1
    assert msg[0]["role"] == "user"
    assert msg[0]["content"] == "nihao AI!"
    assert "reasoning_content" not in msg[0]


def test_add_assistant_message():
    """Day 22: 含 reasoning_content"""
    from src.chat_manager import add_assistant_message

    mock_st = MockSt()
    with patch("src.chat_manager.st", mock_st):
        add_assistant_message("answer is 42", reasoning_content="let me think...")

    msg = mock_st.session_state.message
    assert len(msg) == 1
    assert msg[0]["role"] == "assistant"
    assert msg[0]["content"] == "answer is 42"
    assert msg[0]["reasoning_content"] == "let me think..."


def test_add_assistant_message_without_reasoning():
    """Day 22: 无思维链时 reasoning_content 为 None"""
    from src.chat_manager import add_assistant_message

    mock_st = MockSt()
    with patch("src.chat_manager.st", mock_st):
        add_assistant_message("hello!")

    assert mock_st.session_state.message[0]["reasoning_content"] is None


# ---- Day 23 Tests ----

def test_get_message_count():
    """Day 23: 返回正确的消息数"""
    from src.chat_manager import get_message_count

    mock_st = MockSt(initial_message=[{"role": "user"}, {"role": "assistant"}])
    with patch("src.chat_manager.st", mock_st):
        assert get_message_count() == 2

    mock_st = MockSt()
    with patch("src.chat_manager.st", mock_st):
        assert get_message_count() == 0


def test_get_all_message():
    """Day 23: 返回完整消息列表（含 reasoning_content）"""
    from src.chat_manager import get_all_message

    expected = [
        {"role": "user", "content": "hello"},
        {"role": "assistant", "content": "hi!", "reasoning_content": "thinking..."},
    ]
    mock_st = MockSt(initial_message=expected)
    with patch("src.chat_manager.st", mock_st):
        result = get_all_message()

    assert result == expected
    assert result[1]["reasoning_content"] == "thinking..."


def test_clear_history():
    """Day 23: 清空消息列表"""
    from src.chat_manager import clear_history

    mock_st = MockSt(initial_message=[{"role": "user"}, {"role": "assistant"}])
    with patch("src.chat_manager.st", mock_st):
        clear_history()

    assert mock_st.session_state.message == []


def test_build_api_message_strips_reasoning():
    """Day 23: 移除 reasoning_content 字段

    关键规则：历史 assistant 消息含 reasoning_content 时，
    DeepSeek API 会返回 400 错误。
    """
    from src.chat_manager import build_api_message

    mock_st = MockSt(initial_message=[
        {"role": "user", "content": "1+1=?"},
        {"role": "assistant", "content": "equals 2", "reasoning_content": "simple math"},
        {"role": "user", "content": "thanks"},
    ])
    with patch("src.chat_manager.st", mock_st):
        api_message = build_api_message()

    assert len(api_message) == 3
    for msg in api_message:
        assert set(msg.keys()) == {"role", "content"}, (
            f"message should not contain reasoning_content: {msg.keys()}"
        )
        assert "reasoning_content" not in msg
    assert api_message[1]["content"] == "equals 2"


# ---- Day 24 Tests ----

def test_estimate_token_count():
    """Day 24: 正确估算 token 数 (CHARS_PER_TOKEN=2)"""
    from src.chat_manager import estimate_token_count

    # "Hello World" = 11 chars, "Hi" = 2 chars, "think" = 5 chars
    # Total = 11 + 2 + 5 = 18 chars, 18 // 2 = 9 tokens
    mock_st = MockSt(initial_message=[
        {"role": "user", "content": "Hello World"},
        {"role": "assistant", "content": "Hi", "reasoning_content": "think"},
    ])
    with patch("src.chat_manager.st", mock_st):
        estimated = estimate_token_count()

    assert estimated == 9, f"expected 9 tokens, got {estimated}"


def test_should_warn_below_threshold():
    """Day 24: 低于阈值时返回 False"""
    from src.chat_manager import should_warn_token_limit

    mock_st = MockSt(initial_message=[{"role": "user", "content": "hi"}])
    with patch("src.chat_manager.st", mock_st):
        assert should_warn_token_limit() is False


def test_should_warn_above_threshold():
    """Day 24: 超过阈值时返回 True"""
    from src.chat_manager import should_warn_token_limit

    mock_st = MockSt(initial_message=[{"role": "user", "content": "A" * 120000}])
    with patch("src.chat_manager.st", mock_st):
        assert should_warn_token_limit() is True


if __name__ == "__main__":
    print("=" * 60)
    print("Day 22-24 Tests: chat_manager.py")
    print("=" * 60)

    tests = [
        ("Day 22: init_message creates empty list", test_init_message_creates_empty_list),
        ("Day 22: init_message idempotent", test_init_message_idempotent),
        ("Day 22: add_user_message", test_add_user_message),
        ("Day 22: add_assistant_message with reasoning", test_add_assistant_message),
        ("Day 22: add_assistant_message without reasoning", test_add_assistant_message_without_reasoning),
        ("Day 23: get_message_count", test_get_message_count),
        ("Day 23: get_all_message", test_get_all_message),
        ("Day 23: clear_history", test_clear_history),
        ("Day 23: build_api_message strips reasoning", test_build_api_message_strips_reasoning),
        ("Day 24: estimate_token_count", test_estimate_token_count),
        ("Day 24: should_warn below threshold", test_should_warn_below_threshold),
        ("Day 24: should_warn above threshold", test_should_warn_above_threshold),
    ]

    passed = 0
    for name, test_fn in tests:
        try:
            test_fn()
            print(f"  [PASS] {name}")
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")

    print(f"\nResult: {passed}/{len(tests)} passed")
    if passed < len(tests):
        sys.exit(1)
