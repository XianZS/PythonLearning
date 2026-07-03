"""Streamlit 主程序入口：编排 UI 和业务逻辑，实现 DeepSeek AI 聊天助手"""

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
from src.deepseek_client import chat_stream


def main() -> None:
    """主程序入口"""

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
        add_user_message(prompt)

        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        api_messages = build_api_messages()

        with st.chat_message("assistant", avatar="🤖"):
            reasoning_placeholder = st.empty()
            content_placeholder = st.empty()

            reasoning_text = ""
            content_text = ""
            has_error = False

            for chunk in chat_stream(
                api_key=api_key,
                messages=api_messages,
                model=settings["model"],
                temperature=settings["temperature"],
                max_tokens=settings["max_tokens"],
                enable_thinking=settings["enable_thinking"],
            ):
                chunk_type = chunk["type"]

                if chunk_type == "reasoning":
                    reasoning_text += chunk["text"]
                    reasoning_html = (
                        f'<details open>'
                        f'<summary style="color: #888; cursor: pointer; font-size: 0.9em;">'
                        f'🧠 思考中...</summary>'
                        f'<div style="color: #aaa; font-size: 0.85em; line-height: 1.6; '
                        f'padding: 8px; border-left: 3px solid #555; margin-top: 4px;">'
                        f'{reasoning_text}</div></details>'
                    )
                    reasoning_placeholder.markdown(reasoning_html, unsafe_allow_html=True)

                elif chunk_type == "content":
                    content_text += chunk["text"]
                    content_placeholder.markdown(content_text + "▌")

                elif chunk_type == "done":
                    if reasoning_text:
                        reasoning_html = (
                            f'<details>'
                            f'<summary style="color: #888; cursor: pointer; font-size: 0.9em;">'
                            f'🧠 查看思考过程</summary>'
                            f'<div style="color: #aaa; font-size: 0.85em; line-height: 1.6; '
                            f'padding: 8px; border-left: 3px solid #555; margin-top: 4px;">'
                            f'{reasoning_text}</div></details>'
                        )
                        reasoning_placeholder.markdown(reasoning_html, unsafe_allow_html=True)
                    else:
                        reasoning_placeholder.empty()
                    content_placeholder.markdown(content_text)

                elif chunk_type == "error":
                    if reasoning_text:
                        reasoning_placeholder.empty()
                    content_placeholder.error(chunk["message"])
                    has_error = True
                    break

            if not content_text and not has_error and not reasoning_text:
                content_placeholder.info("模型未返回任何内容，请重试。")

        if content_text or reasoning_text:
            add_assistant_message(
                content=content_text if content_text else "（模型未返回文本内容）",
                reasoning_content=reasoning_text if reasoning_text else None,
            )

        st.rerun()


if __name__ == "__main__":
    main()
