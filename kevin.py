import asyncio
from telethon import TelegramClient, events

# 🔹 अपने टेलीग्राम क्रेडेंशियल्स डालें
API_ID = "25057606"
API_HASH = "bb37f3b7d70879d8e650f20d2beb09f6"
BOT_TOKEN = "7668887729:AAFn_5E6V24iIEpqlqT0_n36tP4"

# 🔹 बॉट को इनिशियलाइज़ करें
bot = TelegramClient("reply_forward_bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# 🔹 टेलीग्राम यूज़रनेम जहाँ मैसेज फॉरवर्ड होंगे (आपका अकाउंट)
ADMIN_USERNAME = "@KevinfantasyteamKft"

# 🔹 एक डिक्शनरी (dict) जहाँ यूज़र्स के मैसेज स्टोर होंगे
user_messages = {}

# 🔹 सभी नए मैसेज हैंडलर (चैनल के मैसेज को रोकें)
@bot.on(events.NewMessage)
async def handle_message(event):
    if event.is_channel:  # अगर मैसेज चैनल से आया है, तो इसे स्किप करें
        return
    
    sender = await event.get_sender()
    user_id = sender.id  # यूज़र का Telegram ID
    
    if user_id != ADMIN_USERNAME:  # अगर मैसेज यूज़र से आया है
        # मैसेज को फॉरवर्ड करें और स्टोर करें
        user_messages[user_id] = event  # यूज़र का मैसेज स्टोर करें
        await event.forward_to(ADMIN_USERNAME)
        print(f"Message received from {user_id} and forwarded to {ADMIN_USERNAME}")

@bot.on(events.NewMessage(from_users=ADMIN_USERNAME))
async def reply_to_user(event):
    # चेक करें कि रिप्लाई किसी स्टोर किए गए यूज़र मैसेज का जवाब है या नहीं
    if event.reply_to and event.reply_to.reply_markup is None:
        original_msg = await event.get_reply_message()
        sender_id = None

        # खोजें कि यह किस यूज़र के मैसेज का जवाब है
        for user_id, user_msg in user_messages.items():
            if user_msg.id == original_msg.id:
                sender_id = user_id
                break

        if sender_id:
            # यूज़र को रिप्लाई भेजें
            await bot.send_message(sender_id, event.text)
            print(f"Replied to {sender_id}: {event.text}")

# 🔹 बॉट को 24/7 चलाने के लिए
async def main():
    print("Bot is running 24/7...")
    await bot.run_until_disconnected()

# 🔹 बॉट शुरू करें
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
