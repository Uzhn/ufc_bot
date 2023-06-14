import os
import datetime
import logging
import json

from aiogram import Bot, Dispatcher, executor, types
from dotenv import load_dotenv

load_dotenv()


TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Привет!\nМеня зовут ufc_bot!\nЯ напоминаю о предстоящих турнирах UFC.")

def check_event_notification(event_data):
    current_time = datetime.datetime.now()
    event_date_time = datetime.datetime.strptime(event_data[0]["date_time"], "%d.%m.%y / %H:%M МСК / Основной кард")
    time_difference = event_date_time - current_time
    if time_difference <= datetime.timedelta(hours=24):
        return 'Не забудьте о турнире! Осталось меньше 24 часов.'
    return 'До турнира больше 24 часов.'


@dp.message_handler(commands=['notification'])
async def send_notification(message: types.Message):
    with open('data/event.json', encoding='utf-8') as file:
        event_data = json.load(file)
    await message.answer(check_event_notification(event_data))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
