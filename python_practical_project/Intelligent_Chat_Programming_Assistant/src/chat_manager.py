"""会话管理：处理多轮对话历史、思维链内容裁剪、上下文限制

本模块封装了 Streamlit session_state 的所有读写操作，
让上层调用方无需直接操作 session_state 原始数据结构。

命名约定：全部统一使用 ``message``，不区分单复数。
- ``st.session_state.message`` = 消息列表（数据层）
- ``st.chat_message()`` = Streamlit 内置的 UI 渲染函数，与数据无关

教学要点：
- 如何使用 st.session_state 在 Streamlit 无状态 rerun 循环中持久化数据
- 多轮对话的数据结构设计（role / content / reasoning_content）
- 发送 API 前如何处理历史消息（裁剪 reasoning_content 防止 400 错误）
- 如何使用字符数粗略估算 token 数量
"""

from typing import Optional
import streamlit as st

from .config import CHARS_PER_TOKEN, TOKEN_WARNING_THRESHOLD


# ---- 消息初始化 ----

def init_message() -> None:
    """初始化消息列表（如果不存在）"""
    if "message" not in st.session_state:
        st.session_state.message = []


# ---- 消息操作 ----

def add_user_message(text: str) -> None:
    """添加用户消息到对话历史"""
    init_message()
    st.session_state.message.append({
        "role": "user",
        "content": text,
    })


def add_assistant_message(content: str, reasoning_content: Optional[str] = None) -> None:
    """添加助手回复到对话历史

    Args:
        content: 助手的回复文本
        reasoning_content: 思维链推理内容（如有），仅用于本地展示
    """
    init_message()
    st.session_state.message.append({
        "role": "assistant",
        "content": content,
        "reasoning_content": reasoning_content,
    })


def clear_history() -> None:
    """清空所有对话历史"""
    init_message()
    st.session_state.message = []


def get_message_count() -> int:
    """获取消息列表中的消息总数"""
    init_message()
    return len(st.session_state.message)


def get_all_message() -> list[dict]:
    """获取全部消息列表"""
    init_message()
    return st.session_state.message


# ---- API 消息构建 ----

def build_api_message() -> list[dict[str, str]]:
    """构建发送给 DeepSeek API 的消息列表

    关键规则（来自 DeepSeek API 文档）：
    多轮对话中，必须移除历史 assistant 消息中的 reasoning_content 字段，
    否则 API 会返回 400 错误。仅保留最近一轮当前正在生成的推理内容。
    由于我们只在接收完整个回复后才将消息持久化到 session_state，
    所以所有历史消息中的 reasoning_content 都应该被裁剪。
    """
    init_message()

    api_message = []
    for message in st.session_state.message:
        clean_message = {
            "role": message["role"],
            "content": message["content"],
        }
        api_message.append(clean_message)

    return api_message


# ---- Token 估算 ----

def estimate_token_count() -> int:
    """估算当前对话的总 token 数

    使用粗略的字符/token 比例估算：
    - 中文字符 ~1.5-2 char/token
    - 英文字符 ~4 char/token
    - 取保守值 2 char/token
    """
    init_message()

    total_chars = 0
    for message in st.session_state.message:
        total_chars += len(message.get("content", ""))
        # 如果有思维链内容，也计入
        if message.get("reasoning_content"):
            total_chars += len(message["reasoning_content"])

    return total_chars // CHARS_PER_TOKEN


def should_warn_token_limit() -> bool:
    """判断是否应该发出 token 限制警告"""
    return estimate_token_count() >= TOKEN_WARNING_THRESHOLD
