"""配置管理：从环境变量读取 DeepSeek API 密钥和默认设置"""

import os
from typing import Any, Optional
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

# ---- API 配置 ----
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

# ---- 模型标识 ----
MODEL_FLASH = "deepseek-v4-flash"
MODEL_PRO = "deepseek-v4-pro"

# ---- 模型元数据 ----
MODELS: dict[str, dict[str, Any]] = {
    MODEL_FLASH: {
        "name": "DeepSeek V4 Flash",
        "description": "快速、经济实惠的通用模型，适合日常对话",
        "supports_thinking": False,
    },
    MODEL_PRO: {
        "name": "DeepSeek V4 Pro",
        "description": "高性能模型，支持思维链推理，适合复杂任务",
        "supports_thinking": True,
    },
}

# ---- 默认参数 ----
DEFAULT_MODEL = MODEL_FLASH
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 4096
MIN_MAX_TOKENS = 256
MAX_MAX_TOKENS = 8192
TOKEN_STEP = 256

# ---- Token 估算阈值 ----
TOKEN_WARNING_THRESHOLD = 50000  # 估计超过此值时发出警告
CHARS_PER_TOKEN = 2  # 中文约 1.5-2 字符/token，英文约 4 字符/token，取保守值


def get_api_key() -> Optional[str]:
    """获取 DeepSeek API 密钥（优先环境变量，其次 .env 文件）"""
    return os.environ.get("DEEPSEEK_API_KEY")


def set_api_key(api_key: str) -> None:
    """运行时设置 API 密钥到环境变量"""
    os.environ["DEEPSEEK_API_KEY"] = api_key


def validate_config() -> tuple[bool, str]:
    """校验配置是否就绪

    Returns:
        (is_valid, message): 校验是否通过及说明信息
    """
    api_key = get_api_key()
    if not api_key:
        return False, "⚠️ 请设置 DEEPSEEK_API_KEY（通过 .env 文件或侧边栏输入）"
    if api_key == "your_api_key_here":
        return False, "⚠️ 请将 .env 中的 DEEPSEEK_API_KEY 替换为你的真实密钥"
    if not api_key.startswith("sk-"):
        return False, "⚠️ API 密钥格式不正确，DeepSeek 密钥应以 'sk-' 开头"
    return True, "✅ 配置就绪"


def get_model_label(model_id: str) -> str:
    """获取模型显示名称"""
    return MODELS.get(model_id, {}).get("name", model_id)


def supports_thinking(model_id: str) -> bool:
    """判断模型是否支持思维链模式"""
    return MODELS.get(model_id, {}).get("supports_thinking", False)
