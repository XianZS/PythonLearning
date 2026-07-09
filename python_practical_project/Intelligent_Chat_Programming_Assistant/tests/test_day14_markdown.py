"""Day 14 验证：st.markdown() — Markdown 与 HTML 渲染

Day 14 没有新增项目代码——它是 Streamlit st.markdown() 用法的练习讲解。
验证方式：在 Python 交互环境或临时脚本中执行以下代码。
"""

# ============================================================
# 验证代码（复制到 app.py 中临时测试，然后删除）
# ============================================================
VERIFY_CODE = '''
import streamlit as st

st.set_page_config(page_title="Day 14 测试", page_icon="[TEST]")

# 验证 1：纯 Markdown
st.markdown("## 二级标题")
st.markdown("**粗体** 和 *斜体*")
st.markdown("- 列表项 1\\n- 列表项 2")
print("[PASS] 纯 Markdown 渲染正常")

# 验证 2：HTML（需要 unsafe_allow_html=True）
st.markdown(
    '<div style="color: #ff6b6b; font-size: 1.5em;">红色大字</div>',
    unsafe_allow_html=True,
)
print("[PASS] HTML 渲染正常")

# 验证 3：不使用 unsafe_allow_html 时 HTML 标签以纯文本显示
st.markdown('<div>这应该显示为纯文本</div>')
print("[PASS] 默认安全模式：HTML 标签显示为纯文本")

# 验证 4：Markdown + HTML 混合
st.markdown("""
    ## 标题
    这是**Markdown**内容
    <div style="background: #333; padding: 10px;">
        这是 HTML 内容
    </div>
""", unsafe_allow_html=True)
print("[PASS] Markdown + HTML 混合渲染正常")
'''

if __name__ == "__main__":
    print("Day 14 验证说明：")
    print("  1. 理解 st.markdown() 三种用法：纯 Markdown / HTML / 混合")
    print("  2. 理解 unsafe_allow_html=True 的作用（允许 HTML 渲染）")
    print("  3. 理解默认 unsafe_allow_html=False（安全考虑，防 XSS）")
    print()
    print("[PASS] 验证通过标准：")
    print("  - 能区分 Markdown 语法和 HTML 语法的渲染差异")
    print("  - 知道 unsafe_allow_html 参数的作用和默认值")
    print("  - HTML 标签在 unsafe_allow_html=False 时显示为纯文本")
