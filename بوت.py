import os
import requests
import random
import threading
from telebot import TeleBot, types

# توكن البوت
TOKEN = "7296062133:AAELuVqY7cV-C-uF-ZOiy_oJpPfsbUlfxNA"
bot = TeleBot(TOKEN, parse_mode="Markdown")  # تمكين تنسيق Markdown

# متغيرات التحكم في الفحص
is_instagram_scanning = False
is_telegram_scanning = False

# دالة فحص يوزرات إنستغرام
def instaa(user, tok, iD):
    url = requests.post(
        'https://www.instagram.com/accounts/web_create_ajax/attempt/',
        headers={
            'Host': 'www.instagram.com',
            'content-type': 'application/x-www-form-urlencoded',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Safari/537.36'
        },
        data=f'email=test@gmail.com&username={user}&first_name=&opt_into_one_tap=false'
    )

    if '"code": "username_is_taken"' in url.text:
        print(f"❌ يوزر مأخوذ ➯ {user}")
    else:
        print(f"✅ يوزر متاح ➯ {user}")
        message = f"يوزر متاح{user}"
        requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", params={"chat_id": iD, "text": message})

# دالة إنشاء يوزرات عشوائية إنستغرام
def users(tok, iD):
    global is_instagram_scanning
    insta = "1234567890qwertyuiopasdfghjklzxcvbnm"
    all_chars = "_"

    while is_instagram_scanning:
        user = "".join(random.choice(insta) for _ in range(3)) + random.choice(all_chars) + "".join(random.choice(insta) for _ in range(3))
        instaa(user, tok, iD)

# دالة فحص يوزرات تيليجرام
def temo(tok, iD):
    global is_telegram_scanning
    tt = 'qwertyuiopasdfghjklzxcvbnm'
    gh = 'QWERTYUIOPASDFGHJKLZXCVBNM_-.1234567890'

    while is_telegram_scanning:
        user = ''.join(random.choice(tt) for _ in range(1)) + ''.join(random.choice(tt) for _ in range(1)) + "_" + ''.join(random.choice(gh) for _ in range(2))
        re = requests.get(f'https://t.me/{user}')

        if "tgme_username_link" in re.text:  
            print(f"✅ يوزر تيليجرام متاح ➯ @{user}")
            message = f"🎉 *يوزر تيليجرام متاح{user}"
            requests.post(f"https://api.telegram.org/bot{tok}/sendMessage", params={"chat_id": iD, "text": message})
        else:
            print(f"❌ يوزر مأخوذ ➯ {user}")

# عند استقبال /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    chat_id = message.chat.id

    # رسالة الترحيب بتنسيق جميل
    welcome_text = """✨ *مرحبًا بك في بوت فحص اليوزرات* ✨  
🚀 *يمكنك استخدام الأزرار أدناه لبدء الفحص:*"""

    # إنشاء الأزرار بشكل أجمل
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_start = types.InlineKeyboardButton("🔍 فحص إنستغرام", callback_data="start_scan")
    btn_help = types.InlineKeyboardButton("📱 فحص تيليجرام", callback_data="help_scan")
    btn_dev = types.InlineKeyboardButton("👤 المطور", callback_data="developer_info")
    btn_stop = types.InlineKeyboardButton("🛑 إيقاف الفحص", callback_data="stop_scan")
    markup.add(btn_start, btn_help, btn_dev, btn_stop)

    # إرسال الرسالة مع الأزرار
    bot.send_message(chat_id, welcome_text, reply_markup=markup)

# التعامل مع الضغط على الأزرار
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global is_instagram_scanning, is_telegram_scanning

    if call.data == "start_scan":
        if not is_instagram_scanning:
            is_instagram_scanning = True
            bot.send_message(call.message.chat.id, "🔍 *جاري فحص يوزرات إنستغرام...*")
            threading.Thread(target=users, args=(TOKEN, call.message.chat.id)).start()
        else:
            bot.send_message(call.message.chat.id, "⚠️ *الفحص قيد التشغيل بالفعل!*")

    elif call.data == "help_scan":
        if not is_telegram_scanning:
            is_telegram_scanning = True
            bot.send_message(call.message.chat.id, "📱 *جاري فحص يوزرات تيليجرام...*")
            threading.Thread(target=temo, args=(TOKEN, call.message.chat.id)).start()
        else:
            bot.send_message(call.message.chat.id, "⚠️ *الفحص قيد التشغيل بالفعل!*")

    elif call.data == "developer_info":
        # أزرار المطور بتنسيق جميل
        dev_markup = types.InlineKeyboardMarkup()
        btn_channel = types.InlineKeyboardButton("📢 قناة المطور", url="https://t.me/V_Y_I_2")
        btn_profile = types.InlineKeyboardButton("👤 حساب المطور", url="https://t.me/V_Y_I_1")
        dev_markup.add(btn_channel, btn_profile)

        bot.send_message(call.message.chat.id, "🔧 *معلومات المطور:*", reply_markup=dev_markup)

    elif call.data == "stop_scan":
        if is_instagram_scanning or is_telegram_scanning:
            is_instagram_scanning = False
            is_telegram_scanning = False
            bot.send_message(call.message.chat.id, "🛑 *تم إيقاف الفحص بنجاح!*")
        else:
            bot.send_message(call.message.chat.id, "⚠️ *لا يوجد فحص قيد التشغيل حاليًا!*")

bot.polling()