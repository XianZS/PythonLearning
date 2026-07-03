"""DeepSeek API 客户端封装：基于 OpenAI SDK，支持流式对话和思维链模式"""

from collections.abc import Generator
from openai import OpenAI, AuthenticationError, RateLimitError, APITimeoutError, APIConnectionError

from .config import DEEPSEEK_BASE_URL, MODEL_FLASH, MODEL_PRO


def _create_client(api_key: str) -> OpenAI:
    """创建 DeepSeek API 客户端（兼容 OpenAI SDK）"""
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def chat_stream(
    api_key: str,
    messages: list[dict[str, str]],
    model: str = MODEL_FLASH,
    temperature: float = 0.7,
    max_tokens: int = 4096,
    enable_thinking: bool = False,
) -> Generator[dict, None, None]:
    """流式对话生成器

    Args:
        api_key: DeepSeek API 密钥
        messages: 对话消息列表 [{"role": "user"/"assistant", "content": "..."}]
        model: 模型标识 (deepseek-v4-flash / deepseek-v4-pro)
        temperature: 采样温度 (0.0 ~ 2.0)，对话模式有效，思维链模式被忽略
        max_tokens: 最大输出 token 数
        enable_thinking: 是否启用思维链推理（仅 V4 Pro 支持）

    Yields:
        {"type": "reasoning", "text": "..."}    — 思维链推理内容
        {"type": "content", "text": "..."}      — 普通回复内容
        {"type": "done", "usage": {...}}        — 流结束，携带 token 用量
        {"type": "error", "message": "..."}     — 发生错误
    """
    try:
        client = _create_client(api_key)

        # 构建 API 请求参数
        kwargs: dict = {
            "model": model,
            "messages": messages,
            "stream": True,
            "max_tokens": max_tokens,
        }

        # 思维链模式：仅 deepseek-v4-pro 支持
        if enable_thinking and model == MODEL_PRO:
            kwargs["extra_body"] = {"thinking": {"type": "enabled"}}
        else:
            kwargs["temperature"] = temperature

        response = client.chat.completions.create(**kwargs)

        # 逐块读取流式响应
        for chunk in response:
            delta = chunk.choices[0].delta if chunk.choices else None
            if delta is None:
                continue

            # 思维链推理内容
            reasoning = getattr(delta, "reasoning_content", None) or ""
            if reasoning:
                yield {"type": "reasoning", "text": reasoning}

            # 普通回复内容
            if delta.content:
                yield {"type": "content", "text": delta.content}

        # 流结束，尝试获取 usage 信息
        # 在流式模式下，最后一个 chunk 可能包含 usage
        yield {"type": "done", "usage": None}

    except AuthenticationError:
        yield {"type": "error", "message": "🔑 API 密钥无效，请检查后重试。可以前往 platform.deepseek.com/api_keys 获取密钥。"}
    except RateLimitError:
        yield {"type": "error", "message": "⏳ API 请求频率超限，请稍等片刻后重试。"}
    except APITimeoutError:
        yield {"type": "error", "message": "⏰ 请求超时，请检查网络连接后重试。"}
    except APIConnectionError:
        yield {"type": "error", "message": "🌐 无法连接到 DeepSeek 服务器，请检查网络连接。"}
    except Exception as e:
        error_msg = str(e)
        # 处理一些 OpenAI SDK 可能抛出的其他异常
        if "status_code" in error_msg and "400" in error_msg:
            yield {"type": "error", "message": "⚠️ 请求参数错误，请尝试清除对话历史后重试。"}
        elif "status_code" in error_msg and "500" in error_msg:
            yield {"type": "error", "message": "⚠️ DeepSeek 服务器内部错误，请稍后重试。"}
        else:
            yield {"type": "error", "message": f"❌ 发生未知错误：{error_msg}"}


