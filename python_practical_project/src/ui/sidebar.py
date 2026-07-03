"""Streamlit 侧边栏组件：模型选择、参数调节、会话管理"""

import streamlit as st

from ..config import (
    MODELS,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    MIN_MAX_TOKENS,
    MAX_MAX_TOKENS,
    TOKEN_STEP,
    supports_thinking,
    get_model_label,
    get_api_key,
    set_api_key,
    validate_config,
)
from ..chat_manager import get_message_count, clear_history, should_warn_token_limit, estimate_token_count


def render() -> dict:
    """渲染侧边栏，返回当前用户设置

    Returns:
        {
            "api_key": str,
            "model": str,
            "temperature": float,
            "max_tokens": int,
            "enable_thinking": bool,
        }
    """
    st.sidebar.markdown("## ⚙️ 设置")

    # ---- API Key ----
    st.sidebar.markdown("### 🔑 API 密钥")
    env_key = get_api_key()
    valid, status_msg = validate_config()

    if valid:
        st.sidebar.success(status_msg)
    else:
        st.sidebar.warning(status_msg)

    # 手动输入 API Key
    api_key_input = st.sidebar.text_input(
        "DeepSeek API Key",
        type="password",
        value=env_key or "",
        placeholder="sk-...",
        help="输入你的 DeepSeek API 密钥。可在 platform.deepseek.com/api_keys 获取。",
    )
    if api_key_input and api_key_input != env_key:
        set_api_key(api_key_input)

    st.sidebar.markdown("---")

    # ---- 模型选择 ----
    st.sidebar.markdown("### 🤖 模型选择")

    model_options = list(MODELS.keys())
    default_index = model_options.index(DEFAULT_MODEL) if DEFAULT_MODEL in model_options else 0

    if "selected_model" not in st.session_state:
        st.session_state.selected_model = model_options[default_index]

    selected_model = st.sidebar.selectbox(
        "选择模型",
        options=model_options,
        format_func=get_model_label,
        index=model_options.index(st.session_state.selected_model),
        key="model_selector",
    )
    st.session_state.selected_model = selected_model

    model_info = MODELS.get(selected_model, {})
    st.sidebar.caption(model_info.get("description", ""))

    st.sidebar.markdown("---")

    # ---- 对话参数 ----
    st.sidebar.markdown("### 🎛️ 对话参数")

    model_supports_thinking = supports_thinking(selected_model)

    if "enable_thinking" not in st.session_state:
        st.session_state.enable_thinking = False

    if not model_supports_thinking and st.session_state.enable_thinking:
        st.session_state.enable_thinking = False
        st.sidebar.info("💡 思维链模式仅在 deepseek-v4-pro 模型中可用")

    enable_thinking = st.sidebar.checkbox(
        "🧠 思维链推理",
        value=st.session_state.enable_thinking,
        disabled=not model_supports_thinking,
        help="启用后模型会展示推理过程。仅 deepseek-v4-pro 支持。",
    )
    st.session_state.enable_thinking = enable_thinking

    thinking_mode = enable_thinking and model_supports_thinking
    temperature = st.sidebar.slider(
        "🌡️ Temperature",
        min_value=0.0,
        max_value=2.0,
        value=DEFAULT_TEMPERATURE,
        step=0.1,
        disabled=thinking_mode,
        help="控制回复的随机性。越高越有创意。思维链模式下此参数无效。" if thinking_mode else "控制回复的随机性。越高越有创意，越低越确定。",
    )
    if thinking_mode:
        st.sidebar.caption("💡 思维链模式下 Temperature 参数无效")

    max_tokens = st.sidebar.slider(
        "📏 最大输出长度",
        min_value=MIN_MAX_TOKENS,
        max_value=MAX_MAX_TOKENS,
        value=DEFAULT_MAX_TOKENS,
        step=TOKEN_STEP,
        help="单次回复的最大 token 数量。越大回复越长。",
    )

    st.sidebar.markdown("---")

    # ---- 会话管理 ----
    st.sidebar.markdown("### 💬 会话管理")

    col1, col2 = st.sidebar.columns(2)
    with col1:
        msg_count = get_message_count()
        st.metric("消息数", msg_count)

    with col2:
        est_tokens = estimate_token_count()
        st.metric("估 Token", f"{est_tokens}")

    if should_warn_token_limit():
        st.sidebar.warning("⚠️ 对话已较长，建议清除历史避免上下文溢出")

    if st.sidebar.button("🗑️ 清除对话历史", use_container_width=True):
        clear_history()
        st.rerun()

    st.sidebar.markdown("---")

    # ---- 关于 ----
    st.sidebar.markdown("### 📖 关于")
    st.sidebar.markdown(
        """
        **DeepSeek AI 聊天助手**
        基于 Streamlit + DeepSeek API 构建

        🎬 Bilibili 教程：[XianZS](https://space.bilibili.com/3690991649294439)
        """
    )

    return {
        "api_key": api_key_input,
        "model": selected_model,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "enable_thinking": enable_thinking,
    }
