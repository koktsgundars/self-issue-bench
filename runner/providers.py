"""Shared API provider abstractions for Anthropic and OpenAI."""

MAX_TOKENS = 4096


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
    def __init__(self):
        import openai
        self.client = openai.OpenAI()

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
    key_var = "OPENAI_API_KEY" if provider_name == "openai" else "ANTHROPIC_API_KEY"
    if not os.environ.get(key_var):
        print(f"Error: {key_var} environment variable not set")
        sys.exit(1)


def create_provider(provider_name: str):
    """Factory function to create a provider by name."""
    if provider_name == "openai":
        return OpenAIProvider()
    elif provider_name == "anthropic":
        return AnthropicProvider()
    else:
        raise ValueError(f"Unknown provider: {provider_name!r}. Use 'anthropic' or 'openai'.")
