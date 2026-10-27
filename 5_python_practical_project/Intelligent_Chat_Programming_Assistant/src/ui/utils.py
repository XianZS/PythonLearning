"""UI 工具函数：CSS 样式注入"""

import streamlit as st


def inject_custom_css() -> None:
    """注入自定义 CSS 样式"""
    st.markdown(
        """
        <style>
            /* 隐藏 Streamlit 默认页脚 "Made with Streamlit" */
            footer { display: none; }

            /* 主内容区域上边距 */
            .block-container {
                padding-top: 2rem;
            }

            /* 思维链展开面板样式 */
            .streamlit-expanderHeader {
                font-size: 0.9em;
                color: #888;
            }

            /* 侧边栏 API Key 输入框使用等宽字体 */
            [data-testid="stSidebar"] [data-testid="stTextInput"] input {
                font-family: monospace;
            }

            /* 聊天消息间距优化 */
            .stChatMessage {
                padding: 0.5rem 1rem;
            }

            /* 建议卡片 hover 效果 */
            [data-testid="stMarkdownContainer"] div[style*="cursor: pointer"]:hover {
                border-color: #4a9eff !important;
                transition: border-color 0.3s;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
