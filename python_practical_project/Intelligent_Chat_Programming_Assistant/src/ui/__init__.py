"""DeepSeek AI 聊天助手 UI 模块

提供 Streamlit UI 组件：侧边栏控件、聊天区域渲染和自定义样式。

模块结构（对应教学单元）：
- utils:     自定义 CSS 样式注入
- sidebar:   侧边栏设置面板（模型选择、参数调节、会话管理）
- chat_area: 聊天区域消息渲染（Markdown、思维链折叠面板）
"""

from .utils import inject_custom_css
from .sidebar import render as render_sidebar
from .chat_area import render_all_messages, render_welcome

__all__ = [
    "inject_custom_css",
    "render_sidebar",
    "render_all_messages",
    "render_welcome",
]
