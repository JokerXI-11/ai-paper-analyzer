"""
大模型调用模块：统一封装 GPT、Claude、DeepSeek 的 API 调用
"""

from openai import OpenAI
from anthropic import Anthropic
from config import MODEL_CONFIGS


class LLMClient:
    """多模型统一调用客户端"""

    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model_name = model_name
        self.config = MODEL_CONFIGS.get(model_name)
        if not self.config:
            raise ValueError(f"不支持的模型: {model_name}。可选: {list(MODEL_CONFIGS.keys())}")

        self.provider = self.config["provider"]
        self._init_client()

    def _init_client(self):
        """初始化对应厂商的客户端"""
        if self.provider == "openai":
            self.client = OpenAI(api_key=self.config["api_key"])
        elif self.provider == "deepseek":
            self.client = OpenAI(
                api_key=self.config["api_key"],
                base_url=self.config.get("base_url", "https://api.deepseek.com"),
            )
        elif self.provider == "claude":
            self.client = Anthropic(api_key=self.config["api_key"])

    def chat(self, system_prompt: str, user_prompt: str, temperature: float = 0.3) -> str:
        """统一对话接口"""
        if self.provider in ("openai", "deepseek"):
            return self._chat_openai_compatible(system_prompt, user_prompt, temperature)
        elif self.provider == "claude":
            return self._chat_claude(system_prompt, user_prompt, temperature)

    def _chat_openai_compatible(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """OpenAI 兼容接口（GPT 和 DeepSeek 通用）"""
        response = self.client.chat.completions.create(
            model=self.config["model"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content

    def _chat_claude(self, system_prompt: str, user_prompt: str, temperature: float) -> str:
        """Claude API 接口"""
        response = self.client.messages.create(
            model=self.config["model"],
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            temperature=temperature,
        )
        return response.content[0].text

    def compare_models(self, system_prompt: str, user_prompt: str, models: list[str] = None) -> dict:
        """
        用多个模型分析同一内容，比较结果
        """
        if models is None:
            models = [m for m in MODEL_CONFIGS if MODEL_CONFIGS[m]["api_key"]]

        results = {}
        for model in models:
            try:
                temp_client = LLMClient(model)
                results[model] = temp_client.chat(system_prompt, user_prompt)
            except Exception as e:
                results[model] = f"[错误] {model}: {str(e)}"

        return results
