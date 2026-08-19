# config.py
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")  # берём из переменных Railway

OFFER_URL = "https://telegra.ph/PUBLICHNAYA-OFERTA-08-18-27"
POLICY_URL = "https://telegra.ph/Politika-v-otnoshenii-obrabotki-personalnyh-dannyh-08-18-11"

COURSES = {
    "buy1": {"name": "Курс 1", "duration": "14 дней", "price": 1500, "description": "Йога для начинающих"},
    "buy2": {"name": "Курс 2", "duration": "21 день", "price": 2000, "description": "Йога для гибкости"},
    "buy3": {"name": "Курс 3", "duration": "14 дней", "price": 1700, "description": "Утренняя йога"},
    "buy4": {"name": "Курс 4", "duration": "21 день", "price": 2200, "description": "Вечерняя йога"},
    "buy5": {"name": "Курс 5", "duration": "14 дней", "price": 1800, "description": "Йога для спины"},
    "buy6": {"name": "Курс 6", "duration": "21 день", "price": 2500, "description": "Продвинутая йога"},
}