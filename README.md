# Discord TTS bot

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Black](https://github.com/Electronic-Mango/discord-tts-bot/actions/workflows/black.yml/badge.svg)](https://github.com/Electronic-Mango/discord-tts-bot/actions/workflows/black.yml)
[![Flake8](https://github.com/Electronic-Mango/discord-tts-bot/actions/workflows/flake8.yml/badge.svg)](https://github.com/Electronic-Mango/discord-tts-bot/actions/workflows/flake8.yml)
[![CodeQL](https://github.com/Electronic-Mango/discord-tts-bot/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/Electronic-Mango/discord-tts-bot/actions/workflows/codeql-analysis.yml)

A simple bot allowing reading out messages in a Discord voice channel.
Built using [`disnake`](https://docs.disnake.dev/en/stable/) and [`gTTS`](https://gtts.readthedocs.io/en/latest/).

Set TTS language, select a voice channel as for TTS output, select however many channels to read out all messages, or use `/read` command.
That's it!



## Table of contents

- [Requirements](#requirements)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Commands](#commands)
  - [Slash commands](#slash-commands)
  - [Message context command](#message-context-command)
  - [Source channels](#source-channels)
  - [Target channel](#target-channel)



## Requirements

Bot was built using `Python 3.10`. Full list of requirements is in `requirements.txt` file.



## Configuration

Bot needs a few environment variables to work.
You can provide them directly, via `.env` file, or via `docker-compose.yml`.

|Variable name|Optional|Description|
|-------------|--------|-----------|
|`DISCORD_BOT_TOKEN`|**No**|Token of your Discord bot.|
|`TEXT_LANGUAGE`|**No**|Language used for TTS.|
|`SOURCE_CHANNELS_FILE`|Yes|Path to file storing source channels, by default `source`.|
|`TARGET_CHANNEL_FILE`|Yes|Path to file storing target channel, by default `target`.|
|`VOICE_FILE_PATH`|Yes|Path to file storing converted audio files, by default `voice_file.mp3`.|

To get specific values for `TEXT_LANGUAGE` you can check [`gTTS` documentation](https://gtts.readthedocs.io/en/latest/module.html#languages-gtts-lang).

When deploying the bot via Docker I'd recommend setting `SOURCE_CHANNELS_FILE` and `TARGET_CHANNEL_FILE` to point to location in a mounted volume.
Otherwise data won't survive container being recreated.
This is already configured in default `docker-compose.yml`.

`VOICE_FILE_PATH` can mostly be ignored, it's just a temporary files where `gTTS` output is stored, before it's read out in a configured voice channel.



## Deployment

The easiest way of deploying the bot is via Docker Compose.
There's `docker-compose.yml` file in the project.

You just need to add to it value of `DISCORD_BOT_TOKEN`, configure `TEXT_LANGUAGE` if you want to use different language than english and run in project root:

```console
docker compose up -d --build
```

You can skip `--build` if you're recreating the container after just configuration changes.

To run the bot manually you have to:
 1. Install all dependencies in `requirements.txt`
 1. Provide all required environment variables (e.g. via `.env` file)
 1. Execute `src/main.py`



## Commands

### Slash commands

These commands are available when you start typing `/` in the chat.

 * `/help` - print help message
 * `/source` - add source channel
 * `/target` - add target **voice** channel
 * `/read <text>` - read out given string in channel configured via `target` command
 * `/list` - list all configured channels, source and target


### Message context command

This command is available from the context menu of selected message.

`read` - read out given string in channel configured via `target` command


### Source channels

There can be multiple source channels configured.
All messages (except slash commands output) will be read out in configured target channel.

You can deconfigure current channel from sources by running `source` command again.


### Target channel

There can be only one configured target **voice** channel.
All messages are read out in selected channel.

You can swith to a new channel by just executing `target` command in it.
You can deconfigure current channel by running `target` command in it again.
