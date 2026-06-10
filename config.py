"""
配置文件：管理各模型 API Key 和基础设置
使用 .env 文件或环境变量配置
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY", "")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# 模型配置
MODEL_CONFIGS = {
    "gpt-4o": {
        "provider": "openai",
        "model": "gpt-4o",
        "api_key": OPENAI_API_KEY,
    },
    "gpt-4o-mini": {
        "provider": "openai",
        "model": "gpt-4o-mini",
        "api_key": OPENAI_API_KEY,
    },
    "claude-sonnet": {
        "provider": "claude",
        "model": "claude-sonnet-4-20250514",
        "api_key": CLAUDE_API_KEY,
    },
    "deepseek": {
        "provider": "deepseek",
        "model": "deepseek-chat",
        "api_key": DEEPSEEK_API_KEY,
        "base_url": DEEPSEEK_BASE_URL,
    },
}

# PDF 分块设置
MAX_CHUNK_CHARS = 8000
CHUNK_OVERLAP = 200

# 输出设置
OUTPUT_DIR = "output"
