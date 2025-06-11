import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")

KAFKA_BROKER = os.getenv("KAFKA_BROKER", "")
