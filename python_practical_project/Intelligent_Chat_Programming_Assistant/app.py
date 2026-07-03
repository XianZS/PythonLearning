"""Streamlit 主程序入口：编排 UI 和业务逻辑，实现 DeepSeek AI 聊天助手

本模块是整个应用的编排层——它负责：
1. 初始化配置、会话和样式
2. 渲染侧边栏和主聊天区域
3. 接收用户输入并驱动流式对话
4. 将流式响应持久化到会话历史

教学要点：
- Streamlit 的 rerun 循环模型（每次交互从头执行脚本）
- 如何将各独立模块组装为完整应用
- 关注点分离：编排层不应包含 UI 渲染细节或流处理细节
"""

import streamlit as st

# ⚠️ set_page_config 必须是第一个 Streamlit 调用
st.set_page_config(
    page_title="DeepSeek AI 助手",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

from src.ui.utils import inject_custom_css
from src.ui.sidebar import render as render_sidebar
from src.ui.chat_area import render_all_messages, render_welcome
from src.config import get_api_key, validate_config
from src.chat_manager import (
    init_messages,
    add_user_message,
    add_assistant_message,
    get_message_count,
    build_api_messages,
)
from src.stream_handler import process_stream


def main() -> None:
    """主程序入口：编排应用生命周期"""

    inject_custom_css()
    init_messages()

    # ---- 侧边栏 ----
    settings = render_sidebar()

    api_key = settings["api_key"] or get_api_key()
    valid, _ = validate_config()

    # ---- 主聊天区域 ----
    if get_message_count() == 0:
        render_welcome()
    else:
        render_all_messages()

    # ---- 聊天输入 ----
    chat_disabled = not valid

    if prompt := st.chat_input(
        "输入你的问题..." if not chat_disabled else "请先在侧边栏配置 API 密钥",
        disabled=chat_disabled,
    ):
        # 1. 记录用户消息
        add_user_message(prompt)
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # 2. 构建 API 消息（不含历史 reasoning_content）
        api_messages = build_api_messages()

        # 3. 流式处理 LLM 响应
        with st.chat_message("assistant", avatar="🤖"):
            reasoning_placeholder = st.empty()
            content_placeholder = st.empty()

            reasoning_text, content_text, _ = process_stream(
                api_key=api_key,
                api_messages=api_messages,
                settings=settings,
                reasoning_placeholder=reasoning_placeholder,
                content_placeholder=content_placeholder,
            )

        # 4. 持久化助手消息（含推理内容）
        if content_text or reasoning_text:
            add_assistant_message(
                content=content_text if content_text else "（模型未返回文本内容）",
                reasoning_content=reasoning_text if reasoning_text else None,
            )

        # 5. 触发 rerun 以刷新历史消息展示
        st.rerun()


if __name__ == "__main__":
    main()
