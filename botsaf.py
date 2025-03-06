from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler

# توكن البوت
bot_token = '7789926752:AAHhETbgMZuweYc7N2ZmmCrAIhX4WJGAtjk'

# دالة للاستجابة لأمر /start
def start(update, context):
    # إعداد الأزرار التي تحتوي على الروابط
    keyboard = [
        [InlineKeyboardButton("قناتي على تيليجرام", url="https://t.me/V_Y_I_2")],
        [InlineKeyboardButton("بوت فحص يوزرات إنستا و تيليجرام", url="https://t.me/user_temo_bot")],
        [InlineKeyboardButton("حساب المطور", url="https://t.me/V_Y_I_1")]
    ]
    
    # إنشاء لوحة المفاتيح
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # إرسال رسالة ترحيبية للمستخدم مع الأزرار
    update.message.reply_text(
        text="مرحباً بك في بوتنا! 👋\n\n"
             "اختَر من الخيارات أدناه للانتقال إلى القنوات أو البوتات.\n"
             "نحن هنا لمساعدتك في فحص يوزرات إنستا وتيليجرام وغير ذلك.\n\n"
             "اختر الرابط التالي:",
        reply_markup=reply_markup
    )

# إعداد البوت
updater = Updater(bot_token)  # تأكد من استخدام الطريقة الصحيحة للنسخة القديمة
dispatcher = updater.dispatcher

# إضافة الكوماند handler
dispatcher.add_handler(CommandHandler('start', start))

# بدء البوت
updater.start_polling()
updater.idle()
