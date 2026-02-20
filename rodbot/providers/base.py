"""Base LLM provider interface."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

import json_repair
from loguru import logger


@dataclass
class ToolCallRequest:
    """A tool call request from the LLM."""

    id: str
    name: str
    arguments: dict[str, Any]


@dataclass
class LLMResponse:
    """Response from an LLM provider."""

    content: str | None
    tool_calls: list[ToolCallRequest] = field(default_factory=list)
    finish_reason: str = "stop"
    usage: dict[str, int] = field(default_factory=dict)
    reasoning_content: str | None = None  # Kimi, DeepSeek-R1 etc.

    @property
    def has_tool_calls(self) -> bool:
        """Check if response contains tool calls."""
        return len(self.tool_calls) > 0


def normalize_tool_calls(message: Any) -> list[ToolCallRequest]:
    """Extract tool calls from any LLM response format (OpenAI/Legacy/Anthropic)."""
    tool_calls: list[ToolCallRequest] = []

    if hasattr(message, "tool_calls") and message.tool_calls:
        for tc in message.tool_calls:
            args = tc.function.arguments
            if isinstance(args, str):
                try:
                    parsed = json_repair.loads(args)
                    args = parsed if isinstance(parsed, dict) else {}
                except Exception:
                    args = {}
            if not isinstance(args, dict):
                args = {}
            tool_calls.append(ToolCallRequest(id=tc.id, name=tc.function.name, arguments=args))
        return tool_calls

    if hasattr(message, "function_call") and message.function_call:
        fc = message.function_call
        args = fc.arguments
        if isinstance(args, str):
            try:
                parsed = json_repair.loads(args)
                args = parsed if isinstance(parsed, dict) else {}
            except Exception:
                args = {}
        if not isinstance(args, dict):
            args = {}
        tool_calls.append(ToolCallRequest(id="fc_0", name=fc.name, arguments=args))
        return tool_calls

    content = getattr(message, "content", None)
    if content and isinstance(content, list):
        for i, block in enumerate(content):
            if isinstance(block, dict) and block.get("type") == "tool_use":
                input_args = block.get("input", {})
                if not isinstance(input_args, dict):
                    input_args = {}
                tool_calls.append(
                    ToolCallRequest(
                        id=block.get("id", f"tu_{i}"),
                        name=block.get("name", "unknown"),
                        arguments=input_args,
                    )
                )

    return tool_calls


class LLMProvider(ABC):
    def __init__(self, api_key: str | None = None, api_base: str | None = None):
        self.api_key = api_key
        self.api_base = api_base

    @abstractmethod
    async def chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None = None,
        model: str | None = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> LLMResponse:
        pass

    @abstractmethod
    def get_default_model(self) -> str:
        pass
