
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

USERS = set()

FAKE_GIFTS = [
    {'title': '🌟 Новый подарок', 'supply': '1000', 'price': '10 TON'},
    {'title': '🔥 Секретный подарок', 'supply': '500', 'price': '25 TON'}
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    USERS.add(user_id)
    await update.message.reply_text("🎁 Я начну присылать тебе новые Telegram Gifts, как только они появятся!")

async def notify_users(application):
    sent_gifts = set()
    while True:
        for gift in FAKE_GIFTS:
            gift_id = gift['title']
            if gift_id not in sent_gifts:
                for user_id in USERS:
                    try:
                        text = f"🎁 Новый подарок!\nНазвание: {gift['title']}\nSupply: {gift['supply']}\nЦена: {gift['price']}"
                        await application.bot.send_message(chat_id=user_id, text=text)
                    except Exception as e:
                        print(f"Ошибка при отправке пользователю {user_id}: {e}")
                sent_gifts.add(gift_id)
        await asyncio.sleep(5)

async def main():
    application = ApplicationBuilder().token(os.environ["TELEGRAM_BOT_TOKEN"]).build()
    application.add_handler(CommandHandler("start", start))
    application.job_queue.run_once(lambda ctx: asyncio.create_task(notify_users(application)), 1)
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
