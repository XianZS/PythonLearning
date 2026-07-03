"""聊天区域渲染：消息展示、思考内容折叠、流式输出"""

import streamlit as st
from typing import Optional


def render_message(role: str, content: str, reasoning_content: Optional[str] = None) -> None:
    """渲染单条消息气泡

    Args:
        role: 角色 ("user" / "assistant")
        content: 消息正文（Markdown 格式）
        reasoning_content: 思维链推理内容（如有），以折叠面板展示
    """
    avatar = "🧑‍💻" if role == "user" else "🤖"

    with st.chat_message(role, avatar=avatar):
        # 如果有思维链内容，在可折叠面板中展示
        if reasoning_content and role == "assistant":
            with st.expander("🧠 查看思考过程", expanded=False):
                st.markdown(
                    f'<div style="color: #888; font-size: 0.9em; line-height: 1.6;">{reasoning_content}</div>',
                    unsafe_allow_html=True,
                )

        # 渲染消息正文
        st.markdown(content)


def render_all_messages() -> None:
    """渲染所有历史消息"""
    from ..chat_manager import get_all_messages

    messages = get_all_messages()
    for msg in messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        reasoning = msg.get("reasoning_content")
        render_message(role, content, reasoning)


def render_welcome() -> None:
    """渲染欢迎屏幕（无对话历史时显示）"""
    st.markdown(
        """
        <div style="text-align: center; padding: 40px 20px;">
            <h1 style="font-size: 2.5em; margin-bottom: 10px;">🤖 DeepSeek AI 聊天助手</h1>
            <p style="color: #888; font-size: 1.1em; margin-bottom: 30px;">
                基于 DeepSeek V4 大模型，支持流式对话与思维链推理
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 示例提示词
    st.markdown("#### 💡 试试这些：")
    cols = st.columns(3)
    suggestions = [
        ("📝", "帮我写一段Python代码", "用 Python 实现一个简单的 HTTP 服务器"),
        ("🔍", "解释概念", "请通俗易懂地解释什么是机器学习"),
        ("💡", "头脑风暴", "我想做一个个人博客网站，给我一些技术选型建议"),
    ]
    for i, (icon, title, desc) in enumerate(suggestions):
        with cols[i]:
            st.markdown(
                f"""
                <div style="
                    border: 1px solid #333;
                    border-radius: 10px;
                    padding: 15px;
                    height: 100%;
                    cursor: pointer;
                ">
                    <div style="font-size: 1.5em;">{icon}</div>
                    <div style="font-weight: bold; margin: 8px 0;">{title}</div>
                    <div style="color: #888; font-size: 0.85em;">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
