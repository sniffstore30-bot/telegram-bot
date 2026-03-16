import telebot
import os
import google.generativeai as genai
import random
from datetime import datetime

# ===== TOKEN DARI ENVIRONMENT =====
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
GEMINI_KEY = "AIzaSyCiQbgCZqskSKJOUs5p1tTMBegtK9npVDc"

# Init bot dan Gemini
bot = telebot.TeleBot(TELEGRAM_TOKEN)
genai.configure(api_key=GEMINI_KEY)

# Setup model Gemini dengan temperature tinggi (lagi random)
generation_config = {
    "temperature": 1.2,        # Tinggi sangat random!
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 150,
}

model = genai.GenerativeModel(
    'gemini-pro',
    generation_config=generation_config
)

# ===== FUNGSI DAPAT RESPON RANDOM DARI GEMINI =====
def gemini_chat(user_message, user_name):
    try:
        # Random personality setiap kali!
        personalities = [
            "gila lawak", "sengal", "friendly", "kawaii", "cool", 
            "caring", "excited", "chill", "hyper", "laid back"
        ]
        personality = random.choice(personalities)
        
        # Random slang variation
        slang = random.choice(["biasa", "pekat", "rojak", "street"])
        
        prompt = f"""Kamu adalah {bot.get_me().first_name}, BOT MALAYSIA SEBENAR!

IDENTITI KAMU HARI INI:
- Personaliti: {personality}
- Gaya slang: {slang}
- Mood: {random.choice(['baik', 'excited', 'chill', 'rikuh', 'gembira'])}

PERATURAN WAJIB:
1. GUNA SLANG MALAYSIA PEKAT! 
   - Wajib guna: weh, wei, geng, bang, bro, sis, korang, aku, kau, depa, kat, gi, mai
   - Campur: lah, bah, kot, je, pun, tah

2. SETIAP AYAT MESTI ADA EMOJI BERBEZA! 😎🔥👌😂🤙✨🥺💀🤣😭😘🥳🤪

3. RESPONS RANDOM - JANGAN SAMA SETIAP KALI!
   - Hari ni lain, esok lain
   - Kalau tanya benda sama, jawab lain sikit

4. PANJANG: 1-3 AYAT JE (macam orang malas taip panjang)

5. RELEVAN TAPI KREATIF - jangan jawab template

CONTOH RESPONS ORG MALAYSIA BEBAN:

Bila orang tanya "hai":
- "Wahh weh! Lama tak nampak! Pi mana kau? 👋"
- "Yo bro! Lemmeh sangat pagi ni haha 😂"
- "Hai geng! Aku baru lepas makan. Kenapa? 😋"
- "Ohh kau rupanya! Kiut kau pagi-pagi dah tegur aku 🤭"

Bila orang tanya "apa khabar":
- "Alhamdulillah geng! Tadi baru gi mamak, perut kenyang skrang 🤤"
- "Hidup laa... Biasalah kita orang susah, rezeki ada je 😎"
- "Wahh kau tanya aku? Aku sihat gila weh! Korang macam mana?"
- "Kenyang? Ngantuk? Rasa macam nak tido je sekarang ni 😴"

Bila orang tanya "tengah buat apa":
- "Lepak je la bro. Boring gila tengok dinding rumah 😂"
- "Baru lepas scroll tiktok sejam. Tak ingat dah dunia 🤪"
- "Ni tengah layan korang je. Aku online 24/7 geng!"
- "Makan maggi. Lapar weh. Kau dah makan? 🍜"

Bila orang cakap "lawak":
- "Haha lawak ke? Aku pun tak sangka aku boleh lawak 😂"
- "Ko ni geli hati la. Tapi aku layan je 🤣"
- "Seriously? Aku ingat lawak tadi tak funny hahaha"
- "Memang aku power bab lawak! Kau nak lagi? 🤪"

Bila orang cakap "sedih":
- "Aduhai... kenapa la pulak? Cerita kat aku, aku dengaq je 🥺"
- "Jangan sedih-sedih la weh. Mai sini aku peluk 🤗"
- "Sedih ke? Nak aku mai teman? 🫂"
- "Hidup ni keras bro. Tapi kau kena kuat! Aku support kau 💪"

Bila orang tanya random:
- "Ha ah, betul tu! Aku paham maksud kau 😎"
- "Eh kejap, aku pikir dulu... okay teruskan! 😅"
- "Wahh berat gak topik ni. Tapi aku layan je!"
- "Kau ni bijak gila! Aku kagom weh 🤩"
- "Aku rasa macam... hmm... apa-apa la yang kau setuju 😂"

SEKARANG user '{user_name}' cakap: "{user_message}"

BALAS MACAM ORG MALAYSIA BEBAN (RANDOM, JANGAN SAMA):"""

        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        print(f"Gemini Error: {e}")
        # Fallback super random
        fallbacks = [
            f"Haha {user_name} lawak gila weh! 😂",
            f"Wahh {user_name}, bestnya cakap kau tu 😎",
            f"Aku blur jap. Cakap lagi eh? 😅",
            f"Betul gila! Aku setuju 100% 🤙",
            f"Kau ni pandai weh! Kagom aku 🤩",
            f"Menarik tu... cerita lagi dong 🔥",
            f"Aku rasa... hmm... aku suka apa kau cakap! 👍",
            f"Eh same lah kita! Aku pun selalu macam tu 😂"
        ]
        return random.choice(fallbacks)

# ===== WELCOME AHLI BARU (RANDOM) =====
@bot.message_handler(content_types=['new_chat_members'])
def welcome(message):
    for member in message.new_chat_members:
        if member.id == bot.get_me().id:
            continue
        
        welcomes = [
            f"🌺 **HAI {member.first_name.upper()}!** 🌺\n\nWahh ada member baru! Korang sambut la dia elok-elok. Jangan buli eh! 😂",
            f"👋 **YO {member.first_name}!**\n\nAkhirnya kau join! Dah lama kami tunggu. Jom aktif jangan malu-malu! 🔥",
            f"🎉 **WELCOME ABANG {member.first_name}!** 🎉\n\nGroup ni makin happening dengan kehadiran kau. Jom sembang! 🤙",
            f"✨ **FRESH MEAT!** ✨\n\n{member.first_name} baru masuk. Kau orang lama layan la dia baik-baik. Jangan cancel culture plak 😂"
        ]
        
        bot.send_message(message.chat.id, random.choice(welcomes))

# ===== GOODBYE AHLI KELUAR (RANDOM) =====
@bot.message_handler(content_types=['left_chat_member'])
def goodbye(message):
    left = message.left_chat_member
    if left.id == bot.get_me().id:
        return
    
    goodbyes = [
        f"👋 **DAAAH {left.first_name.upper()}!**\n\nSedih weh kau tinggal kami. Jangan lupa mai mai lagi eh! 🥺",
        f"😢 **BYE {left.first_name}**\n\nKau akan dirindukan geng! Aku still ada sini kalau kau nak sembang. PM je! ✨",
        f"💔 **SAD MOMENT**\n\n{left.first_name} keluar. Rasa macam kehilangan kawan baik. Take care weh! 🌟",
        f"🕊️ **UNTIL WE MEET AGAIN**\n\nSelamat jalan {left.first_name}! Jauh di mata, dekat di hati. Jangan delete contact aku eh! 💕"
    ]
    
    bot.send_message(message.chat.id, random.choice(goodbyes))

# ===== AI CHAT =====
@bot.message_handler(func=lambda message: True)
def chat(message):
    if message.text.startswith('/'):
        return
    
    bot.send_chat_action(message.chat.id, 'typing')
    
    response = gemini_chat(message.text, message.from_user.first_name)
    bot.reply_to(message, response)

# ===== COMMANDS =====
@bot.message_handler(commands=['start', 'help'])
def start(message):
    msg = f"""👋 **YO {message.from_user.first_name}!**

Aku **{bot.get_me().first_name}** - BOT MALAYSIA SEBENAR!

**🔥 Apa aku boleh buat?**
✅ Sembang slang Malaysia pekat
✅ Setiap kali jawab lain (random!)
✅ Ada emoji setiap ayat
✅ Personaliti berubah-ubah

**📌 Cara guna:**
- Tanya apa je kat aku
- Cakap "hai", "apa khabar", "tengah buat apa"
- Cerita pasal hari kau
- Share lawak, sedih, apa-apa!

**Jom kita lepak sembang geng!** 🔥😎🤙"""
    
    bot.reply_to(message, msg)

@bot.message_handler(commands=['about'])
def about(message):
    msg = f"""🤖 **ABOUT AKU**

📌 **Nama:** {bot.get_me().first_name}
📌 **AI Model:** Gemini Pro + Personality Randomizer
📌 **Slang:** Malaysia pekat (berubah-ubah)
📌 **Personaliti:** Random setiap chat!
📌 **Emoji:** Wajib ada, random gak!
📌 **Harga:** PERCUMA (gemini free tier)

**Aku bukan template, aku natural!** 😎"""
    
    bot.reply_to(message, msg)

# ===== MAIN =====
if __name__ == "__main__":
    print("=" * 50)
    print("🤖 BOT MALAYSIA RANDOM - READY!")
    print("=" * 50)
    print("✅ Slang Malaysia pekat (random)")
    print("✅ Personaliti berubah-ubah")
    print("✅ Emoji random setiap kali")
    print("✅ Bukan template! Natural macam org sembang")
    print("=" * 50)
    
    bot.infinity_polling()