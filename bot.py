import telebot
import os
import google.generativeai as genai
import time
from datetime import datetime

# ===== AMBIK TOKEN DARI ENVIRONMENT =====
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = "AIzaSyCiQbgCZqskSKJOUs5p1tTMBegtK9npVDc"

# Init bot
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Setup Gemini
genai.configure(api_key=GEMINI_KEY)

# Configuration untuk natural conversation
generation_config = {
    "temperature": 1.0,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 200,
}

model = genai.GenerativeModel(
    'gemini-pro',
    generation_config=generation_config
)

# ===== FUNGSI AI CHAT =====
def ai_chat(user_message, user_name):
    """AI akan reply secara natural"""
    try:
        # Context ringkas
        prompt = f"""Kamu adalah {bot.get_me().first_name}, anak muda Malaysia yang sedang chat.

CARA CAKAP:
- Gaya macam muda-mudi Malaysia (guna: weh, wei, geng, bro, aku, kau)
- Ada emoji sikit
- Respons pendek je (1-3 ayat)
- Jangan formal sangat

Yang chat: {user_name}
Dia cakap: {user_message}

Balas macam kawan chat:"""

        response = model.generate_content(prompt)
        return response.text.strip()
        
    except Exception as e:
        print(f"AI Error: {e}")
        return f"Ha ah, betul tu {user_name} 😊"

# ===== WELCOME =====
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            continue
        bot.send_message(message.chat.id, 
            f"🌺 Welcome {member.first_name}! Jom aktif 🔥")

# ===== GOODBYE =====
@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):
    left = message.left_chat_member
    if left.id == bot.get_me().id:
        return
    bot.send_message(message.chat.id, 
        f"👋 Bye {left.first_name}! 😢")

# ===== SEMUA MESEJ =====
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    if message.text.startswith('/'):
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    time.sleep(1)
    
    response = ai_chat(message.text, message.from_user.first_name)
    bot.reply_to(message, response)

# ===== COMMANDS =====
@bot.message_handler(commands=['start', 'help'])
def start(message):
    bot.reply_to(message, f"👋 Hai {message.from_user.first_name}! Jom sembang!")

@bot.message_handler(commands=['about'])
def about(message):
    bot.reply_to(message, "🤖 Bot Gemini AI - Sembang macam kawan!")

# ===== MAIN =====
if __name__ == "__main__":
    print("🤖 BOT GEMINI - READY!")
    print(f"Bot: @{bot.get_me().username}")
    
    # Remove webhook
    bot.remove_webhook()
    time.sleep(1)
    
    # Start bot
    bot.infinity_polling()