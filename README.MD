# Кото-бот 🐱
Простой Telegram-бот, который присылает фото и описание породы кота по запросу. Также умеет показывать случайное космическое фото с NASA.

## Установка
1. Склонируй репозиторий:
```bash
git clone https://github.com/CHEPURNOV-S-S/TG05.git
cd TG05
```
2. Установи зависимости:
```bash
pip install -r requirements.txt
```

3. Создай файл .env в корне проекта и добавь в него следующие переменные:
```env
TG_BOT_API_KEY=ваш_telegram_bot_api_key
CAT_API_KEY=ваш_api_key_для_TheCatAPI
NASA_API_KEY=ваш_api_key_для_NASA_APOD
```
## Как запустить
```bash
python bot_aiogram.py
```

Команды бота
/start — начать общение с ботом
/cats — перейти в режим поиска котиков по породе
/exit — выйти из режима котиков
/random_apod — получить случайное фото с NASA
