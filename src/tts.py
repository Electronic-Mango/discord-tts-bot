from os import environ

from dotenv import load_dotenv
from gtts import gTTS
from loguru import logger

load_dotenv()
TEXT_LANGUAGE = environ["TEXT_LANGUAGE"]
VOICE_FILE_PATH = environ.get("VOICE_FILE_PATH", "voice_file.mp3")


def convert_text_to_speech_file(text: str) -> str:
    """Converts given string into audio file and returns path to it"""
    logger.info("Starting TTS...")
    speech = gTTS(text, lang=TEXT_LANGUAGE)
    speech.save(VOICE_FILE_PATH)
    logger.info("TTS finished")
    return VOICE_FILE_PATH
