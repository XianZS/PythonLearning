"""Day 16 验证：st.chat_input() — 聊天输入框

Day 16 更新 app.py，添加 chat_input 的功能逻辑。
验证方式：启动 Streamlit 并检查输入框的三种状态。

运行：
    streamlit run app.py
"""

# ============================================================
# 自动化结构验证（无需 Streamlit 运行时）
# ============================================================
import sys
import os


def test_app_imports_and_structure():
    """验证 app.py 的结构和关键调用"""
    # 切换到项目根目录，确保无论从哪里运行都能找到 app.py
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    sys.path.insert(0, os.getcwd())

    # 读取 app.py 源码验证关键模式
    with open("app.py", "r", encoding="utf-8") as f:
        source = f.read()

    checks = [
        ("set_page_config", "缺少 st.set_page_config()"),
        ("inject_custom_css()", "缺少 inject_custom_css() 调用"),
        ("validate_config()", "缺少 validate_config() 调用"),
        ("chat_disabled = not valid", "缺少 chat_disabled 逻辑"),
        ("st.chat_input(", "缺少 st.chat_input()"),
        ("disabled=chat_disabled", "chat_input 缺少 disabled 参数"),
        ('"请先在侧边栏配置 API 密钥"', "缺少密钥未配置时的提示文字"),
        ('"输入你的问题..."', "缺少正常状态下的占位符文字"),
        ('st.chat_message("assistant"', "缺少助手消息气泡"),
        ('render_message("user"', "缺少用户消息渲染调用"),
        ('avatar="🤖"', "缺少助手头像"),
    ]

    for pattern, error_msg in checks:
        assert pattern in source, f"{error_msg}\n  搜索: {pattern}"


if __name__ == "__main__":
    print("=" * 60)
    print("Day 16 验证：st.chat_input()")
    print("=" * 60)

    # 结构验证（无需 Streamlit）
    failed = False
    print("\n--- 代码结构验证 ---")
    try:
        test_app_imports_and_structure()
        print("  [PASS] app.py contains all required chat_input patterns")
    except AssertionError as e:
        print(f"  [FAIL] {e}")
        failed = True

    # 手动验证说明
    print("\n--- 手动验证步骤（需启动 Streamlit）---")
    print("  1. 确保 .env 中 DEEPSEEK_API_KEY 未配置或无效")
    print("  2. streamlit run app.py")
    print("  3. 验证：输入框灰色禁用，提示 '请先在侧边栏配置 API 密钥'")
    print("  4. 在侧边栏输入正确的 API Key")
    print("  5. 验证：输入框变为可用，提示 '输入你的问题...'")
    print("  6. 输入消息按 Enter，验证：消息出现在用户气泡中")
    print("  7. 验证：侧边栏显示 [PASS] 或 [WARN] 状态")

    if failed:
        sys.exit(1)
