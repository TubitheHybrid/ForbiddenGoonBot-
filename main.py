import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== BOT TOKEN ==================
TOKEN = "8299621003:AAHZeb7dOeXxY40luliNic-1kd7o9c5gD4I"

# ================== WALLETS ==================
WALLET_SOL = "4QzwVoyLShABRUvgtCZuJBiVyD9VNZ1VwSZopRTyjLZ6"
WALLET_BTC = "1H76dFg9325Y4ZcHftFWqhMqR4qaSYxZx9"
WALLET_ETH = "0x3d2e5e082095854a782c478f91803f4464ef83f8"

# ================== GROUP LINK ==================
GROUP_LINK = "https://t.me/+2dg4TwR0xCBiNGU0"

# ================== FLASK APP ==================
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is alive!"

@app.route("/webhook", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok"

# ================== HANDLERS ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Hi Goonbot", callback_data="hi_goonbot")]]
    await update.message.reply_text("Tap below to begin 👇", reply_markup=InlineKeyboardMarkup(keyboard))

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "hi_goonbot":
        keyboard = [
            [InlineKeyboardButton("Yes", callback_data="yes_ready"),
             InlineKeyboardButton("No", callback_data="no_ready")]
        ]
        await query.edit_message_text(
            "Hey there gooner, ready to explore dark desires?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "no_ready":
        await query.edit_message_text("Ohh bye twinkle toes, see you when you want to get naughty.")

    elif query.data == "yes_ready":
        keyboard = [
            [InlineKeyboardButton("Videos", callback_data="videos")],
            [InlineKeyboardButton("Live anon personnel", callback_data="live_anon")],
            [InlineKeyboardButton("Back", callback_data="hi_goonbot")]
        ]
        await query.edit_message_text(
            "Welcome gooner, please be sure you're sensitive and stimulated by dark desires.\n\nChoose an option 👇",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "videos":
        keyboard = [
            [InlineKeyboardButton("$250", callback_data="price_250")],
            [InlineKeyboardButton("Back", callback_data="yes_ready")]
        ]
        await query.edit_message_text("You chose Videos 🎥", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "live_anon":
        keyboard = [
            [InlineKeyboardButton("$750", callback_data="price_750")],
            [InlineKeyboardButton("Back", callback_data="yes_ready")]
        ]
        await query.edit_message_text("You chose Live Anonymous Personnel 🔥", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "price_250":
        keyboard = [
            [InlineKeyboardButton("Solana", callback_data="crypto_sol")],
            [InlineKeyboardButton("Bitcoin", callback_data="crypto_btc")],
            [InlineKeyboardButton("ETH (ERC20)", callback_data="crypto_eth")],
            [InlineKeyboardButton("Back", callback_data="videos")]
        ]
        await query.edit_message_text("You selected $250 (Videos) 💰\nNow choose your payment method 👇",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "price_750":
        keyboard = [
            [InlineKeyboardButton("Solana", callback_data="crypto_sol")],
            [InlineKeyboardButton("Bitcoin", callback_data="crypto_btc")],
            [InlineKeyboardButton("ETH (ERC20)", callback_data="crypto_eth")],
            [InlineKeyboardButton("Back", callback_data="live_anon")]
        ]
        await query.edit_message_text("You selected $750 (Live Anon Personnel) 💰\nNow choose your payment method 👇",
                                      reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "crypto_sol":
        await send_wallet(query, "Solana", WALLET_SOL)

    elif query.data == "crypto_btc":
        await send_wallet(query, "Bitcoin", WALLET_BTC)

    elif query.data == "crypto_eth":
        await send_wallet(query, "ETH (ERC20)", WALLET_ETH)

    elif query.data == "payment_sent":
        keyboard = [[InlineKeyboardButton("Start Over", callback_data="hi_goonbot")]]
        await query.edit_message_text(
            f"🚪 Door is being unlocked to your goon-geon...\n\n📸 Send a screenshot of your transaction to our group:\n👉 {GROUP_LINK}",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

async def send_wallet(query, label, wallet):
    keyboard = [
        [InlineKeyboardButton("I have sent payment", callback_data="payment_sent")],
        [InlineKeyboardButton("Back", callback_data="yes_ready")]
    ]
    msg = await query.edit_message_text(
        text=f"💎 Send your payment in {label} to this address:\n\n{wallet}\n\n⚠️ This address will self-destruct in 5 minutes.",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    await asyncio.sleep(300)
    try:
        await query.message.delete()
    except:
        pass

# ================== MAIN ==================
application = Application.builder().token(TOKEN).build()
application.add_handler(CommandHandler("start", start))
application.add_handler(CallbackQueryHandler(callbacks))

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        url_path="webhook",
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/webhook"
    )).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
