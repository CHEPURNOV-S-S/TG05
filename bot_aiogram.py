import os
import random
import asyncio
from datetime import datetime, timedelta

import requests
from dotenv import load_dotenv

# Загружаем .env в первую очередь
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '.env')
print(f"Start load_dotenv Path to .env {dotenv_path}")
result = load_dotenv(dotenv_path, encoding='utf-8-sig')
print(f"Load result: {result}")

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, FSInputFile

TG_BOT_API_KEY = os.environ.get('TG_BOT_API_KEY')
CAT_API_KEY = os.getenv('CAT_API_KEY')
NASA_API_KEY = os.getenv('NASA_API_KEY')


bot = Bot(token=TG_BOT_API_KEY)
dp = Dispatcher()

async def main():
    print("Bot starting")
    await dp.start_polling(bot)

user_states = {}  # Например: {user_id: "cats_mode"}

def get_cat_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": CAT_API_KEY}
    response = requests.get(url, headers=headers)
    data = response.json()
    return data[0]['url']


def get_breed_info(breed_name):
    breeds = get_cat_breeds()
    for breed in breeds:
        if breed['name'].lower() == breed_name.lower():
            return breed
    return None

def get_random_apod():
   end_date = datetime.now()
   start_date = end_date - timedelta(days=365)
   random_date = start_date + (end_date - start_date) * random.random()
   date_str = random_date.strftime("%Y-%m-%d")

   url = f'https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}&date={date_str}'
   response = requests.get(url)
   return response.json()

@dp.message(Command("random_apod"))
async def random_apod(message: Message):
   apod = get_random_apod()
   photo_url = apod['url']
   title = apod['title']

   await message.answer_photo(photo=photo_url, caption=f"{title}")

# Новая команда для входа в режим котиков
@dp.message(Command("cats"))
async def cats_mode_on(message: Message):
    user_id = message.from_user.id
    user_states[user_id] = "cats_mode"
    await message.answer("Вы вошли в режим поиска котиков. Введите название породы или /exit чтобы выйти.")

# Новая команда для выхода из режима котиков
@dp.message(Command("exit"))
async def exit_cats_mode(message: Message):
    user_id = message.from_user.id
    if user_states.get(user_id) == "cats_mode":
        del user_states[user_id]
        await message.answer("Вы вышли из режима поиска котиков.")
    else:
        await message.answer("Вы не в режиме поиска котиков.")

@dp.message(Command("start"))
async def start_command(message: Message):
    await message.answer("Привет! Напиши /cats, чтобы начать искать котиков по породам. Или /random_apod для случайного фото с NASA.")


# Обновлённая функция send_cat_info
@dp.message()
async def send_cat_info(message: Message):
    user_id = message.from_user.id
    current_state = user_states.get(user_id)

    if current_state == "cats_mode":
        breed_name = message.text
        breed_info = get_breed_info(breed_name)
        if breed_info:
            cat_image_url = get_cat_image_by_breed(breed_info['id'])
            info = (
                f"Порода - {breed_info['name']}\n"
                f"Описание - {breed_info['description']}\n"
                f"Продолжительность жизни - {breed_info['life_span']} лет"
            )
            await message.answer_photo(photo=cat_image_url, caption=info)
        else:
            cat_breeds = get_cat_breeds()
            cat_breeds_names = [breed['name'] for breed in cat_breeds]
            await message.answer(f"Порода не найдена. Попробуйте еще раз. Возможные варианты:\n{cat_breeds_names}")
    else:
        await message.answer("Введите /cats, чтобы начать поиск котиков, или /random_apod для случайного фото с NASA.")

if __name__ == "__main__":
    asyncio.run(main())
