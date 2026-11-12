
import os
import telebot
from telebot import types

# توكن البوت الرسمي
TOKEN = "9007603023:AAEfVH0npaypVzJhja9v8YNcKMfXhQO0MUg"
bot = telebot.TeleBot(TOKEN)

# (اختياري لاحقاً) معرف مجموعة الإدارة لتلقي الإيصالات
ADMIN_GROUP_ID = None  

# أمر البداية
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_shop = types.InlineKeyboardButton("🛒 قسم الشحن والخدمات", callback_data="shop_menu")
    btn_support = types.InlineKeyboardButton("📞 التواصل والدعم", callback_data="support")
    markup.add(btn_shop, btn_support)
    
    welcome_text = (
        " أهلاً بك في متجر **SKO-Store** للخدمات الرقمية وشحن الألعاب!\n\n"
        "اختر من القائمة أدناه للبدء:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=markup)

# الأزرار التفاعلية
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "shop_menu":
        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_game = types.InlineKeyboardButton("🎮 شحن الألعاب والشدات", callback_data="games_section")
        btn_back = types.InlineKeyboardButton("🔙 القائمة الرئيسية", callback_data="main_menu")
        markup.add(btn_game, btn_back)
        
        bot.edit_message_text(
            "اختر القسم المناسب لطلبك:",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=markup
        )
        
    elif call.data == "games_section":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "لقد اخترت قسم الألعاب.\n"
            "الرجاء إرسال تفاصيل طلبك (الآيدي، الكمية)، ثم حول المبلغ عبر **شام كاش (ChamCash)** وأرسل صورة الإيصال هنا في الشات 📸."
        )
        
    elif call.data == "main_menu":
        send_welcome(call.message)
        
    elif call.data == "support":
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, "للدعم والاستفسار، تواصل مع الإدارة عبر معرف المتجر.")

# استقبال صور إيصالات الدفع
@bot.message_handler(content_types=['photo'])
def handle_receipt(message):
    bot.reply_to(
        message, 
        "✅ تم استلام صورة الإيصال بنجاح!\n"
        "⏳ جاري التحقق من الدفع، سيتم تسليم طلبك فور تأكيد وصول الأموال."
    )
    if ADMIN_GROUP_ID:
        bot.forward_message(ADMIN_GROUP_ID, message.chat.id, message.message_id)
        bot.send_message(ADMIN_GROUP_ID, f"طلب دفع جديد من المستخدم: {message.from_user.first_name}")

if __name__ == "__main__":
    print("Bot is running from scratch...")
    bot.infinity_polling()
