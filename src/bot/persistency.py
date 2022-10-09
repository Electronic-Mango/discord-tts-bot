"""
Module handling storing configuration persistently, between bot reboots.
"""

from os import environ
from os.path import exists
from pickle import dump, load

SOURCE_CHANNELS_FILE = environ.get("SOURCE_CHANNELS_FILE", "sources")
TARGET_CHANNEL_FILE = environ.get("TARGET_CHANNEL_FILE", "target")


def save_source_channels(channels: set[int]) -> None:
    """Save given source channels to file"""
    with open(SOURCE_CHANNELS_FILE, "wb") as file:
        return dump(channels, file)


def load_source_channels() -> set[int]:
    """Read all stored source channels, or return and emtpy set"""
    if not exists(SOURCE_CHANNELS_FILE):
        return set()
    with open(SOURCE_CHANNELS_FILE, "rb") as file:
        return load(file)


def save_target_channel(channel: int | None) -> None:
    """Save given target channel to file"""
    with open(TARGET_CHANNEL_FILE, "wb") as file:
        return dump(channel, file)


def load_target_channel() -> int | None:
    """Read stored target channel, or return None"""
    if not exists(TARGET_CHANNEL_FILE):
        return None
    with open(TARGET_CHANNEL_FILE, "rb") as file:
        return load(file)
