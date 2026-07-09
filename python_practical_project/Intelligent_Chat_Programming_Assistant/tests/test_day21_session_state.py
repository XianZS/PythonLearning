"""Day 21 验证：st.session_state — Streamlit 的"记忆"

Day 21 没有新增项目代码——它是 st.session_state 原理的讲解。
验证方式：编写一个独立的 Streamlit 演示脚本来对比普通变量与 session_state。

运行方式（临时演示，不纳入项目）：
    streamlit run tests/test_day21_session_state.py
"""

# ============================================================
# 验证：session_state 跨 Rerun 持久化
# ============================================================
# 以下是完整的 Streamlit 演示脚本（临时运行后删除或保留作为参考）。
# 将以下代码保存为临时文件并运行，观察点击按钮后两个变量的差异。

STREAMLIT_DEMO = '''
"""st.session_state 演示：普通变量 vs 持久变量"""
import streamlit as st

st.set_page_config(page_title="Session State 演示", page_icon="[TEST]")

st.markdown("## 🔬 Session State 对比实验")

# 普通 Python 变量——每次 Rerun 都重置
count_normal = 0

# Session State 持久变量——跨 Rerun 保持
if "count_persistent" not in st.session_state:
    st.session_state.count_persistent = 0

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    st.metric("普通变量", count_normal)
with col2:
    st.metric("持久变量 (session_state)", st.session_state.count_persistent)

if st.button("➕ 两个变量各 +1", use_container_width=True):
    count_normal += 1                           # 每次 Rerun 重置为 0
    st.session_state.count_persistent += 1       # 持续累加

st.markdown("---")
st.caption("💡 多次点击按钮：普通变量始终为 1，持久变量持续增长。")
st.caption("原因：每次按钮点击触发 Rerun，整个脚本重新执行。")
st.caption("普通变量被重新赋值为 0，session_state 的值保留在内存中。")
'''

if __name__ == "__main__":
    print("Day 21 验证说明：")
    print("  将上述 STREAMLIT_DEMO 内容保存为临时 .py 文件")
    print("  运行: streamlit run <临时文件>.py")
    print()
    print("[PASS] 验证通过标准：")
    print("  - 首次点击按钮：普通变量显示 1，持久变量显示 1")
    print("  - 第 2 次点击：普通变量显示 1（被重置），持久变量显示 2")
    print("  - 第 10 次点击：普通变量始终为 1，持久变量为 10")
    print("  - 刷新浏览器：持久变量重置为 0（新会话）")
    print()
    print("Key takeaway:")
    print("  Streamlit 的 Rerun 模型导致所有普通变量每次重置")
    print("  st.session_state 是 Streamlit 提供的跨 Rerun 存储机制")
    print("  懒初始化模式 if 'key' not in st.session_state 是标准写法")
