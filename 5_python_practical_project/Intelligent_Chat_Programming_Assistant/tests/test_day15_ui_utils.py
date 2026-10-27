"""Day 15 测试：ui/utils.py — CSS 样式注入 + ui/__init__.py

验证点：
1. inject_custom_css() 输出包含关键 CSS 规则
2. ui/__init__.py 正确导出所有公共函数
3. CSS 规则格式正确

运行方式：
    cd Intelligent_Chat_Programming_Assistant
    python tests/test_day15_ui_utils.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_css_contains_critical_rules():
    """测试：inject_custom_css 输出包含所有必需 CSS 规则"""
    from src.ui.utils import inject_custom_css

    # inject_custom_css 调用 st.markdown，这里我们验证 CSS 字符串内容
    import inspect
    source = inspect.getsource(inject_custom_css)

    # 验证所有关键 CSS 规则都在源码中
    required_rules = [
        ("footer", "隐藏 Streamlit 页脚"),
        (".block-container", "主内容区域边距"),
        (".streamlit-expanderHeader", "思维链面板样式"),
        ("monospace", "API Key 等宽字体"),
        (".stChatMessage", "聊天消息间距"),
        ("cursor: pointer", "建议卡片 hover 效果"),
        ("border-color: #4a9eff", "hover 时蓝色边框"),
        ("transition: border-color 0.3s", "过渡动画"),
    ]

    for rule, description in required_rules:
        assert rule in source, f"缺少 CSS 规则: {rule} ({description})"

    # 验证 unsafe_allow_html=True（必须启用才能渲染 HTML <style> 标签）
    assert "unsafe_allow_html=True" in source, "缺少 unsafe_allow_html=True"


def test_ui_package_exports():
    """测试：ui/__init__.py 正确导出所有公共 API"""
    import src.ui as ui_pkg

    # 验证 __all__ 导出列表
    expected_exports = [
        "inject_custom_css",
        "render_sidebar",
        "render_all_message",
        "render_welcome",
    ]

    for name in expected_exports:
        assert hasattr(ui_pkg, name), f"ui 包缺少导出: {name}"
        assert name in ui_pkg.__all__, f"__all__ 中缺少: {name}"


def test_css_syntax():
    """测试：CSS 规则语法正确（花括号匹配）"""
    import inspect
    from src.ui.utils import inject_custom_css

    source = inspect.getsource(inject_custom_css)
    # 提取 <style> 标签内的 CSS
    style_start = source.find("<style>")
    style_end = source.find("</style>")
    assert style_start != -1 and style_end != -1, "找不到 <style> 标签"
    css_content = source[style_start:style_end]

    # 花括号配对检查
    open_braces = css_content.count("{")
    close_braces = css_content.count("}")
    assert open_braces == close_braces, (
        f"CSS 花括号不匹配: {open_braces} 个 {{ vs {close_braces} 个 }}"
    )


if __name__ == "__main__":
    print("=" * 60)
    print("Day 15 测试：ui/utils.py + ui/__init__.py")
    print("=" * 60)

    tests = [
        ("CSS 包含所有关键规则", test_css_contains_critical_rules),
        ("ui 包公共 API 导出", test_ui_package_exports),
        ("CSS 语法正确性", test_css_syntax),
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
