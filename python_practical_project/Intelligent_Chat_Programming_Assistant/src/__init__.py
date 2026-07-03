"""DeepSeek AI 聊天助手核心模块

提供配置管理、API 客户端、会话管理和流式响应处理功能。

模块结构（对应教学单元）：
- config:          环境变量与 API 配置管理
- deepseek_client: DeepSeek API 客户端封装（流式调用）
- chat_manager:    多轮对话会话管理（上下文裁剪、Token 估算）
- stream_handler:  流式响应处理（UI 渐进更新）
"""

from .config import (
    get_api_key,
    set_api_key,
    validate_config,
    get_model_label,
    supports_thinking,
)
from .deepseek_client import chat_stream
from .chat_manager import (
    init_messages,
    add_user_message,
    add_assistant_message,
    clear_history,
    get_message_count,
    get_all_messages,
    build_api_messages,
    estimate_token_count,
    should_warn_token_limit,
)
from .stream_handler import process_stream

__all__ = [
    # config
    "get_api_key",
    "set_api_key",
    "validate_config",
    "get_model_label",
    "supports_thinking",
    # deepseek_client
    "chat_stream",
    # chat_manager
    "init_messages",
    "add_user_message",
    "add_assistant_message",
    "clear_history",
    "get_message_count",
    "get_all_messages",
    "build_api_messages",
    "estimate_token_count",
    "should_warn_token_limit",
    # stream_handler
    "process_stream",
]
