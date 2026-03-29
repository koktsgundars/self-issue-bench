"""Model pricing data ($/1M tokens) as of March 2026."""

# (input_cost_per_1m, output_cost_per_1m)
MODEL_PRICING = {
    # Anthropic (direct)
    "claude-sonnet-4-20250514": (3.0, 15.0),
    "claude-opus-4-20250514": (15.0, 75.0),
    "claude-haiku-4-5-20251001": (0.80, 4.0),
    # OpenAI (direct)
    "gpt-4o": (2.50, 10.0),
    "gpt-4o-mini": (0.15, 0.60),
    "o3-mini": (1.10, 4.40),
    # OpenRouter (upstream pricing)
    "deepseek/deepseek-v3.2": (0.27, 1.10),
    "anthropic/claude-sonnet-4": (3.0, 15.0),
    "anthropic/claude-opus-4": (15.0, 75.0),
    "anthropic/claude-haiku-4-5": (0.80, 4.0),
    "google/gemini-3.1-pro-preview": (1.25, 5.0),
    "nvidia/nemotron-3-super-120b-a12b": (0.12, 0.30),
    "minimax/minimax-m2.5": (0.20, 1.10),
    "moonshotai/kimi-k2.5": (0.20, 0.90),
    "z-ai/glm-5": (0.15, 0.60),
    "qwen/qwen3.5-plus-02-15": (0.30, 1.20),
}


def get_cost(model: str, input_tokens: int, output_tokens: int) -> float | None:
    """Compute cost in dollars for a given model and token count."""
    pricing = MODEL_PRICING.get(model)
    if not pricing:
        return None
    input_rate, output_rate = pricing
    return (input_tokens * input_rate + output_tokens * output_rate) / 1_000_000
