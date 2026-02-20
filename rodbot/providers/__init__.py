"""LLM provider abstraction module."""

from rodbot.providers.base import LLMProvider, LLMResponse
from rodbot.providers.litellm_provider import LiteLLMProvider
from rodbot.providers.openai_codex_provider import OpenAICodexProvider

__all__ = ["LLMProvider", "LLMResponse", "LiteLLMProvider", "OpenAICodexProvider", "make_provider"]


def make_provider(config: "Config", model: str | None = None) -> LLMProvider:
    """Create the appropriate LLM provider for a given model.

    Used at startup and when /model switches across providers.
    """
    from rodbot.providers.custom_provider import CustomProvider
    from rodbot.providers.registry import find_by_name

    model = model or config.agents.defaults.model
    provider_name = config.get_provider_name(model)
    p = config.get_provider(model)

    if provider_name == "openai_codex" or model.startswith("openai-codex/"):
        return OpenAICodexProvider(default_model=model)

    if provider_name == "custom":
        return CustomProvider(
            api_key=p.api_key if p else "no-key",
            api_base=config.get_api_base(model) or "http://localhost:8000/v1",
            default_model=model,
        )

    spec = find_by_name(provider_name)
    if not model.startswith("bedrock/") and not (p and p.api_key) and not (spec and spec.is_oauth):
        raise ValueError(f"No API key configured for provider '{provider_name}'")

    return LiteLLMProvider(
        api_key=p.api_key if p else None,
        api_base=config.get_api_base(model),
        default_model=model,
        extra_headers=p.extra_headers if p else None,
        provider_name=provider_name,
    )
