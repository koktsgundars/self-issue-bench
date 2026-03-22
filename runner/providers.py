"""Shared API provider abstractions for Anthropic, OpenAI, and OpenAI-compatible APIs."""

MAX_TOKENS = 4096

# Registry of OpenAI-compatible providers.
# Each entry maps a provider name to (base_url, api_key_env_var).
# Models are passed through as-is to the API.
OPENAI_COMPATIBLE_PROVIDERS = {
    "deepseek": (
        "https://api.deepseek.com/v1",
        "DEEPSEEK_API_KEY",
    ),
    "gemini": (
        "https://generativelanguage.googleapis.com/v1beta/openai/",
        "GEMINI_API_KEY",
    ),
    "qwen": (
        "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "DASHSCOPE_API_KEY",
    ),
    "moonshot": (
        "https://api.moonshot.cn/v1",
        "MOONSHOT_API_KEY",
    ),
    "zhipu": (
        "https://open.bigmodel.cn/api/paas/v4/",
        "ZHIPU_API_KEY",
    ),
    "minimax": (
        "https://api.minimax.chat/v1",
        "MINIMAX_API_KEY",
    ),
}

ALL_PROVIDER_NAMES = ["anthropic", "openai"] + sorted(OPENAI_COMPATIBLE_PROVIDERS)


class AnthropicProvider:
    def __init__(self):
        import anthropic
        self.client = anthropic.Anthropic()

    def chat(self, model: str, messages: list[dict]) -> tuple[str, dict]:
        response = self.client.messages.create(
            model=model,
            max_tokens=MAX_TOKENS,
            messages=messages,
        )
        text = response.content[0].text
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }
        return text, usage


class OpenAIProvider:
    def __init__(self, base_url=None, api_key=None):
        import openai
        kwargs = {}
        if base_url:
            kwargs["base_url"] = base_url
        if api_key:
            kwargs["api_key"] = api_key
        self.client = openai.OpenAI(**kwargs)

    def chat(self, model: str, messages: list[dict]) -> tuple[str, dict]:
        # o-series reasoning models (o1, o3, o4, etc.) require max_completion_tokens
        import re
        is_o_series = bool(re.match(r"^o\d", model))
        token_param = "max_completion_tokens" if is_o_series else "max_tokens"
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            **{token_param: MAX_TOKENS},
        )
        text = response.choices[0].message.content
        usage = {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
        }
        return text, usage


def check_api_key(provider_name: str) -> None:
    """Check that the required API key environment variable is set."""
    import os
    import sys
    if provider_name == "openai":
        key_var = "OPENAI_API_KEY"
    elif provider_name == "anthropic":
        key_var = "ANTHROPIC_API_KEY"
    elif provider_name in OPENAI_COMPATIBLE_PROVIDERS:
        _, key_var = OPENAI_COMPATIBLE_PROVIDERS[provider_name]
    else:
        print(f"Error: unknown provider {provider_name!r}")
        sys.exit(1)
    if not os.environ.get(key_var):
        print(f"Error: {key_var} environment variable not set")
        sys.exit(1)


def create_provider(provider_name: str):
    """Factory function to create a provider by name."""
    import os
    if provider_name == "anthropic":
        return AnthropicProvider()
    elif provider_name == "openai":
        return OpenAIProvider()
    elif provider_name in OPENAI_COMPATIBLE_PROVIDERS:
        base_url, key_var = OPENAI_COMPATIBLE_PROVIDERS[provider_name]
        return OpenAIProvider(base_url=base_url, api_key=os.environ.get(key_var))
    else:
        raise ValueError(
            f"Unknown provider: {provider_name!r}. "
            f"Available: {', '.join(ALL_PROVIDER_NAMES)}"
        )
