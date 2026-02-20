"""Message bus module for decoupled channel-agent communication."""

from rodbot.bus.events import InboundMessage, OutboundMessage
from rodbot.bus.queue import MessageBus

__all__ = ["MessageBus", "InboundMessage", "OutboundMessage"]
