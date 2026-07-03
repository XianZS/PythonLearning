"""流式响应处理器：处理 LLM 流式输出并更新 Streamlit UI

教学要点：
- 如何处理流式 API 响应的不同 chunk 类型（reasoning/content/done/error）
- 如何使用 st.empty() 占位符实现渐进式 UI 更新
- 如何将 UI 渲染逻辑从业务编排中分离
- 如何抽象重复的 HTML 模板为可复用函数
"""

import streamlit as st

from .deepseek_client import chat_stream


def _render_reasoning_html(text: str, *, streaming: bool) -> str:
    """生成思维链折叠面板 HTML

    Args:
        text: 推理文本内容（已累积的全部 reasoning text）
        streaming: True=展开面板显示"思考中"，False=折叠面板显示"查看思考过程"

    Returns:
        HTML 字符串，由 st.markdown(..., unsafe_allow_html=True) 渲染
    """
    return (
        f'<details{" open" if streaming else ""}>'
        f'<summary style="color: #888; cursor: pointer; font-size: 0.9em;">'
        f'{"🧠 思考中..." if streaming else "🧠 查看思考过程"}</summary>'
        f'<div style="color: #aaa; font-size: 0.85em; line-height: 1.6; '
        f'padding: 8px; border-left: 3px solid #555; margin-top: 4px;">'
        f'{text}</div></details>'
    )


def process_stream(
    api_key: str,
    api_messages: list[dict[str, str]],
    settings: dict,
    reasoning_placeholder,
    content_placeholder,
) -> tuple[str, str, bool]:
    """处理流式 LLM 响应并更新 UI 占位符

    调用方应在 with st.chat_message("assistant"): 上下文内调用此函数，
    并在函数返回后根据 content_text / reasoning_text 决定是否持久化消息。

    Args:
        api_key: DeepSeek API 密钥
        api_messages: 发送给 API 的消息列表（不含 reasoning_content）
        settings: 用户设置字典，包含 model / temperature / max_tokens / enable_thinking
        reasoning_placeholder: 思维链展示区的 st.empty() 占位符
        content_placeholder: 回复内容的 st.empty() 占位符

    Returns:
        (reasoning_text, content_text, has_error)
        - reasoning_text: 累积的思维链推理文本（空字符串表示无推理内容）
        - content_text: 累积的回复文本（空字符串表示无文本输出）
        - has_error: 是否发生了错误
    """
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
            # 累积推理文本，实时更新展开的折叠面板
            reasoning_text += chunk["text"]
            reasoning_placeholder.markdown(
                _render_reasoning_html(reasoning_text, streaming=True),
                unsafe_allow_html=True,
            )

        elif chunk_type == "content":
            # 累积回复文本，实时更新带光标动画的内容
            content_text += chunk["text"]
            content_placeholder.markdown(content_text + "▌")

        elif chunk_type == "done":
            # 流结束：推理面板折叠，内容去除光标
            if reasoning_text:
                reasoning_placeholder.markdown(
                    _render_reasoning_html(reasoning_text, streaming=False),
                    unsafe_allow_html=True,
                )
            else:
                reasoning_placeholder.empty()
            content_placeholder.markdown(content_text)

        elif chunk_type == "error":
            # 发生错误：清除推理面板，在内容区显示错误信息
            if reasoning_text:
                reasoning_placeholder.empty()
            content_placeholder.error(chunk["message"])
            has_error = True
            break

    # 边界情况：模型未返回任何内容
    if not content_text and not has_error and not reasoning_text:
        content_placeholder.info("模型未返回任何内容，请重试。")

    return reasoning_text, content_text, has_error
