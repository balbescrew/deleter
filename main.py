import asyncio
import json
import logging
from logging import getLogger

from aiogram import Bot
from aiokafka import AIOKafkaConsumer

from config import BOT_TOKEN, KAFKA_BROKER

logging.basicConfig(level=logging.INFO)
logger = getLogger(__name__)
logger.setLevel("DEBUG")

BOT = Bot(token=BOT_TOKEN)


async def process_message(message: dict, bot: Bot):
    try:
        logger.info("сообщение удаляется")
        await bot.delete_message(
            chat_id=message["chat_id"],
            message_id=message["message_id"],
        )
        logger.info("сообщение удалилось")
    except Exception as e:
        logger.error(f"Failed to delete message: {e}", exc_info=True)


async def consume_messages(bot: Bot, topic: str = "spam_messages"):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id="delete_bot",
        value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        enable_auto_commit=True,
        auto_offset_reset="latest",
    )

    await consumer.start()
    logger.info(f"Subscribed to Kafka topic: {topic}")
    try:
        async for msg in consumer:
            message = msg.value
            logger.info(f"Received message from Kafka: {message}")
            asyncio.create_task(process_message(message, bot))
    except Exception as e:
        logger.error("Kafka consumer loop error", exc_info=e)
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped cleanly.")


async def main():
    logger.info("Starting Kafka consumer...")
    try:
        await consume_messages(bot=BOT)
    except asyncio.CancelledError:
        logger.info("Consumer cancelled.")
    except Exception as e:
        logger.exception("Unexpected error in Kafka consumer", exc_info=e)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Kafka consumer stopped via signal.")
