"""Day 29 测试：app.py — 完整编排 + 端到端测试

验证点：
1. app.py 的 5 步数据流正确编排
2. set_page_config 是第一个 Streamlit 调用
3. 所有模块正确导入和调用
4. st.rerun() 在消息持久化后被调用
"""

import sys
import os
import inspect
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# 切换到项目根目录，确保无论从哪里运行都能找到 app.py
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_set_page_config_is_first():
    """验证 set_page_config 是文件中第一个 st.xxx() 调用"""
    with open("app.py", "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 找到第一个 st.xxx() 调用
    first_st_call = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("st.") and not stripped.startswith("#"):
            first_st_call = (i + 1, stripped)
            break

    assert first_st_call is not None, "找不到 st.xxx() 调用"
    assert "set_page_config" in first_st_call[1], (
        f"第一个 st 调用应为 set_page_config，实际: {first_st_call[1]}"
    )


def test_all_imports_present():
    """验证 app.py 导入了所有必需的模块"""
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()

    required_imports = [
        "from src.ui.utils import inject_custom_css",
        "from src.ui.sidebar import render as render_sidebar",
        "from src.ui.chat_area import render_all_message, render_welcome",
        "from src.config import get_api_key, validate_config",
        "from src.chat_manager import",
        "init_message",
        "add_user_message",
        "add_assistant_message",
        "get_message_count",
        "build_api_message",
        "from src.stream_handler import process_stream",
    ]

    for imp in required_imports:
        assert imp in source, f"缺少导入: {imp}"


def test_five_step_flow():
    """验证 5 步数据流的关键调用顺序"""
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()

    # 所有 5 个步骤的调用必须存在
    steps = [
        "add_user_message(prompt)",            # 步骤 1: 记录用户消息
        "render_message(\"user\", prompt)",    # 步骤 1: 用统一函数渲染用户消息
        "build_api_message()",                # 步骤 2: 构建 API 消息
        "process_stream(",                     # 步骤 3: 流式处理
        "add_assistant_message(",              # 步骤 4: 持久化助手消息
        "st.rerun()",                          # 步骤 5: 触发 rerun
    ]

    for step in steps:
        assert step in source, f"5 步数据流缺少: {step}"


def test_chat_disabled_logic():
    """验证密钥未配置时输入框禁用"""
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()

    assert "chat_disabled = not valid" in source, "缺少 chat_disabled 逻辑"
    assert 'disabled=chat_disabled' in source, "chat_input 缺少 disabled 参数"


def test_rerun_after_persist():
    """验证 st.rerun() 在 add_assistant_message 之后调用"""
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()

    # st.rerun() 必须出现在 add_assistant_message 之后
    rerun_pos = source.find("st.rerun()")
    add_msg_pos = source.find("add_assistant_message(")

    assert rerun_pos > add_msg_pos, (
        "st.rerun() 应在 add_assistant_message() 之后（先持久化再 rerun）"
    )


def test_page_config_values():
    """验证页面配置参数正确"""
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()

    config_checks = [
        'page_title="DeepSeek AI 助手"',
        'page_icon="🤖"',
        'layout="wide"',
        'initial_sidebar_state="expanded"',
    ]

    for check in config_checks:
        assert check in source, f"页面配置缺少: {check}"


if __name__ == "__main__":
    print("=" * 60)
    print("Day 29 测试：app.py 完整编排")
    print("=" * 60)

    tests = [
        ("set_page_config 是第一个 st 调用", test_set_page_config_is_first),
        ("所有必需导入", test_all_imports_present),
        ("5 步数据流", test_five_step_flow),
        ("输入框禁用逻辑", test_chat_disabled_logic),
        ("先持久化再 rerun", test_rerun_after_persist),
        ("页面配置参数", test_page_config_values),
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
    print("\n--- 端到端手动验证（需启动 Streamlit + 有效 API Key）---")
    print("  1. streamlit run app.py")
    print("  2. 配置有效的 DeepSeek API Key")
    print("  3. 发送 '你好' → 验证 AI 流式回复")
    print("  4. 发送 '用 Python 写一个快速排序' → 验证代码高亮")
    print("  5. V4 Pro + 思维链 → 验证思考过程折叠面板")
    print("  6. 清除历史 → 验证回到欢迎页")
    print("  7. 删除 API Key → 验证输入框禁用")
    if passed < len(tests):
        sys.exit(1)
