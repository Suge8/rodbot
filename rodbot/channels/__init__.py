"""Chat channels module with plugin architecture."""

from rodbot.channels.base import BaseChannel
from rodbot.channels.manager import ChannelManager

__all__ = ["BaseChannel", "ChannelManager"]
