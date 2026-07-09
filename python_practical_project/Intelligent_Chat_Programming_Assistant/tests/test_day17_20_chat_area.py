"""Day 17-20 测试：ui/chat_area.py — 聊天区域渲染

Day 17: render_message() 基础版本
Day 18: render_message() 加入思维链折叠面板
Day 19: render_welcome() 欢迎页与建议卡片
Day 20: render_all_message() 历史消息遍历

验证点：
1. render_message 正确区分 user/assistant 角色和头像
2. render_message 在 assistant + reasoning_content 时包含折叠面板
3. render_welcome 包含标题和 3 张建议卡片
4. render_all_message 正确遍历消息列表
5. 所有 HTML 模板字符串正确

运行方式：
    cd Intelligent_Chat_Programming_Assistant
    python tests/test_day17_20_chat_area.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_render_message_user_avatar():
    """Day 17: 用户消息使用 🧑‍💻 头像"""
    import inspect
    from src.ui.chat_area import render_message

    source = inspect.getsource(render_message)
    assert '"🧑‍💻"' in source or "'🧑‍💻'" in source, "用户消息缺少 🧑‍💻 头像"
    assert '"🤖"' in source or "'🤖'" in source, "助手消息缺少 🤖 头像"


def test_render_message_has_expander():
    """Day 18: 助手消息含思维链内容时使用 st.expander"""
    import inspect
    from src.ui.chat_area import render_message

    source = inspect.getsource(render_message)
    assert "st.expander" in source, "缺少 st.expander（思维链折叠面板）"
    assert "🧠 查看思考过程" in source, "折叠面板标题不正确"
    assert "reasoning_content" in source, "未检查 reasoning_content 参数"
    assert "role == \"assistant\"" in source or "role == 'assistant'" in source, (
        "未限制仅 assistant 显示思维链面板"
    )


def test_render_welcome_structure():
    """Day 19: 欢迎页包含标题和 3 张建议卡片"""
    import inspect
    from src.ui.chat_area import render_welcome

    source = inspect.getsource(render_welcome)

    # 标题检查
    assert "DeepSeek AI 聊天助手" in source, "欢迎页缺少标题"
    assert "流式对话与思维链推理" in source, "欢迎页缺少副标题"

    # 建议卡片检查
    assert "st.columns(3)" in source, "应为 3 列布局"
    assert "帮我写一段Python代码" in source, "缺少建议卡片 1"
    assert "解释概念" in source, "缺少建议卡片 2"
    assert "头脑风暴" in source, "缺少建议卡片 3"

    # 卡片样式检查
    assert "cursor: pointer" in source, "建议卡片缺少 pointer 光标"
    assert "border-radius: 10px" in source, "建议卡片缺少圆角"


def test_render_all_message_import():
    """Day 20: render_all_message 正确导入 get_all_message"""
    import inspect
    from src.ui.chat_area import render_all_message

    source = inspect.getsource(render_all_message)

    # 检查从 chat_manager 导入
    import src.ui.chat_area as ca
    chat_area_source = inspect.getsource(ca)
    assert "from ..chat_manager import get_all_message" in chat_area_source, (
        "缺少从 chat_manager 导入 get_all_message"
    )

    # 检查函数体
    assert "get_all_message()" in source, "未调用 get_all_message()"
    assert "render_message" in source, "未调用 render_message()"
    assert "msg.get(" in source, "未使用 .get() 安全取值"


def test_html_strings_complete():
    """验证关键 HTML 字符串完整"""
    import inspect
    from src.ui.chat_area import render_message, render_welcome

    # Day 18: render_message 的 HTML 样式
    msg_source = inspect.getsource(render_message)
    assert "color: #888" in msg_source, "思维链文字颜色缺失"
    assert "font-size: 0.9em" in msg_source, "思维链文字大小缺失"
    assert "line-height: 1.6" in msg_source, "思维链行间距缺失"

    # Day 19: render_welcome 的样式
    welcome_source = inspect.getsource(render_welcome)
    assert "text-align: center" in welcome_source, "标题未居中"
    assert "font-size: 2.5em" in welcome_source, "标题字号缺失"
    assert "border: 1px solid #333" in welcome_source, "卡片边框样式缺失"


if __name__ == "__main__":
    print("=" * 60)
    print("Day 17-20 测试：ui/chat_area.py")
    print("=" * 60)

    tests = [
        ("Day 17: 用户/助手头像区分", test_render_message_user_avatar),
        ("Day 18: 思维链折叠面板", test_render_message_has_expander),
        ("Day 19: 欢迎页标题+建议卡片", test_render_welcome_structure),
        ("Day 20: render_all_message 导入和遍历", test_render_all_message_import),
        ("HTML 字符串完整性", test_html_strings_complete),
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
