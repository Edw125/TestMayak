import logging
import os

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from dotenv import load_dotenv

from handlers import start, from_button, instance, catch_other_message, user_answer, UserInput, cancel

load_dotenv()

BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.getLogger("aiogram").setLevel(logging.INFO)


def init_bot():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    return bot, dp


bot, dp = init_bot()


def main():
    logging.warning("Starting connection")
    dp.register_message_handler(start, commands="start")
    dp.register_callback_query_handler(
        from_button,
        instance.filter(action=["add_site"]), state="*")
    dp.register_message_handler(user_answer, state=UserInput.file, content_types=["document"])
    dp.register_message_handler(cancel, Text(equals="/cancel", ignore_case=True), state="*")
    dp.register_message_handler(
        catch_other_message,
        state=UserInput.file,
        content_types=["text", "sticker", "pinned_message", "photo", "audio"]
    )
    dp.register_message_handler(
        catch_other_message,
        content_types=["text", "sticker", "pinned_message", "photo", "audio"]
    )
    executor.start_polling(dp, skip_updates=True)


if __name__ == '__main__':
    main()
