import telebot
import requests
import os

# --- ТВОЙ TELEGRAM ТОКЕН ---
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7740685981:AAHhWvD4xRswFUCtWe8v6hS9mdVSgFOT2QY")  # замени ТВОЙ_ТОКЕН_СЮДА на настоящий

# --- URL до LLM-сервера (например, HuggingFace или Render API) ---
LLM_API_URL = os.getenv("LLM_API_URL", "https://example.com/api/chat")  # сюда вставим позже

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
user_histories = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id
    user_message = message.text

    if user_id not in user_histories:
        user_histories[user_id] = []

    user_histories[user_id].append({"role": "user", "content": user_message})

    try:
        payload = {
            "model": "llama3",  # название модели
            "messages": user_histories[user_id]
        }

        response = requests.post(LLM_API_URL, json=payload)
        response.raise_for_status()

        reply = response.json().get('message', {}).get('content', '⚠️ Пустой ответ от модели')
        user_histories[user_id].append({"role": "assistant", "content": reply})
        bot.send_message(user_id, reply)

    except Exception as e:
        bot.send_message(user_id, f"Ошибка: {str(e)}")

bot.polling(non_stop=True)
