"""Day 25-27 测试：ui/sidebar.py — 侧边栏控件

Day 25: API 密钥输入 + 状态指示
Day 26: 模型选择 + Temperature/Max Tokens 滑块
Day 27: 思维链开关 + 会话管理（消息计数 get_message_count、Token 估算、清除按钮）

sidebar.py 依赖 Streamlit 运行时，大部分逻辑无法在无 Streamlit 环境下测试。
本测试文件验证代码结构。
"""

import sys
import os
import inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_render_returns_dict_with_all_keys():
    """Day 25-27: render() 返回字典包含所有 5 个必需字段"""
    import src.ui.sidebar as sb

    source = inspect.getsource(sb.render)

    # 返回字典必须包含的 5 个字段
    required_keys = ["api_key", "model", "temperature", "max_tokens", "enable_thinking"]
    for key in required_keys:
        assert f'"{key}"' in source or f"'{key}'" in source, f"返回字典缺少字段: {key}"


def test_sidebar_imports():
    """验证所有必需的导入"""
    import src.ui.sidebar as sb

    source = inspect.getsource(sb)

    required_imports = [
        "streamlit as st",
        "MODELS",
        "DEFAULT_MODEL",
        "DEFAULT_TEMPERATURE",
        "DEFAULT_MAX_TOKENS",
        "MIN_MAX_TOKENS",
        "MAX_MAX_TOKENS",
        "TOKEN_STEP",
        "supports_thinking",
        "get_model_label",
        "get_api_key",
        "set_api_key",
        "validate_config",
        "get_message_count",
        "clear_history",
        "should_warn_token_limit",
        "estimate_token_count",
    ]

    for imp in required_imports:
        assert imp in source, f"缺少导入: {imp}"


def test_api_key_input_secure():
    """Day 25: API Key 输入框为密码模式"""
    source = inspect.getsource(__import__("src.ui.sidebar", fromlist=["render"]).render)
    assert 'type="password"' in source or "type='password'" in source, (
        "API Key 输入框应为密码模式"
    )
    assert '"sk-..."' in source or "'sk-...'" in source, "缺少 placeholder"


def test_temperature_disabled_in_thinking_mode():
    """Day 26-27: Temperature 滑块在思维链模式下禁用"""
    import src.ui.sidebar as sb

    source = inspect.getsource(sb.render)
    assert "disabled=thinking_mode" in source, (
        "Temperature 滑块缺少 disabled=thinking_mode"
    )
    assert "thinking_mode" in source, "缺少 thinking_mode 变量"


def test_thinking_checkbox_conditional_disable():
    """Day 27: 思维链复选框在 V4 Flash 下禁用"""
    import src.ui.sidebar as sb

    source = inspect.getsource(sb.render)
    assert "checkbox" in source, "缺少思维链复选框"
    assert "disabled=not model_supports_thinking" in source, (
        "思维链复选框缺少条件禁用逻辑"
    )


def test_info_message_when_thinking_disabled():
    """Day 27: 切换到不支持模型时显示 info 提示"""
    import src.ui.sidebar as sb

    source = inspect.getsource(sb.render)
    assert '思维链模式仅在 deepseek-v4-pro 模型中可用' in source, (
        "缺少思维链不可用时的 info 提示"
    )


def test_token_warning_message():
    """Day 27: Token 超限警告信息完整"""
    import src.ui.sidebar as sb

    source = inspect.getsource(sb.render)
    assert "建议清除历史避免上下文溢出" in source, (
        "Token 警告消息不完整（缺少'避免上下文溢出'）"
    )


def test_clear_history_button():
    """Day 27: 清除按钮调用 clear_history + st.rerun()"""
    import src.ui.sidebar as sb

    source = inspect.getsource(sb.render)
    assert "clear_history()" in source, "清除按钮未调用 clear_history()"
    assert "st.rerun()" in source, "清除按钮未调用 st.rerun()"


if __name__ == "__main__":
    print("=" * 60)
    print("Day 25-27 测试：ui/sidebar.py")
    print("=" * 60)

    tests = [
        ("返回字典包含全部 5 个字段", test_render_returns_dict_with_all_keys),
        ("所有必需导入", test_sidebar_imports),
        ("API Key 密码模式", test_api_key_input_secure),
        ("Temperature 思维链禁用", test_temperature_disabled_in_thinking_mode),
        ("思维链复选框条件禁用", test_thinking_checkbox_conditional_disable),
        ("思维链不可用时 info 提示", test_info_message_when_thinking_disabled),
        ("Token 警告消息完整", test_token_warning_message),
        ("清除按钮逻辑", test_clear_history_button),
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
    print("\n--- 手动验证步骤（需启动 Streamlit）---")
    print("  1. streamlit run app.py")
    print("  2. Day 25: 在侧边栏输入密钥 → 验证状态变为 [PASS]")
    print("  3. Day 26: 切换模型 → 验证描述文字变化")
    print("  4. Day 26: 拖动 Temperature → 验证值实时更新")
    print("  5. Day 27: V4 Pro → 勾选思维链 → Temperature 变灰禁用")
    print("  6. Day 27: 切换到 V4 Flash → 思维链自动关闭 + info 提示")
    print("  7. Day 27: 发多条消息 → Token 估算增长 → 警告出现")
    print("  8. Day 27: 点击清除 → 回到欢迎页")
    if passed < len(tests):
        sys.exit(1)
