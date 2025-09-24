import logging
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Replace with your bot token
TOKEN = "8299621003:AAHZeb7dOeXxY40luliNic-1kd7o9c5gD4I"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
    filename="log.txt"
)
logger = logging.getLogger(__name__)

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("Yes", callback_data="age_yes"),
                 InlineKeyboardButton("No", callback_data="age_no")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Are you 18+?", reply_markup=reply_markup)

# Handle button presses
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "age_yes":
        keyboard = [
            [InlineKeyboardButton("Videos", callback_data="videos"),
             InlineKeyboardButton("Live anon personnel", callback_data="live")],
            [InlineKeyboardButton("Back", callback_data="start_over")]
        ]
        await query.edit_message_text("Choose an option:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "age_no":
        await query.edit_message_text("You must be 18+. Please /start again.")

    elif query.data == "videos":
        keyboard = [
            [InlineKeyboardButton("$250", callback_data="pay_videos")],
            [InlineKeyboardButton("Back", callback_data="age_yes")]
        ]
        await query.edit_message_text("Videos\n\nPrice: $250", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == "live":
        keyboard = [
            [InlineKeyboardButton("$750", callback_data="pay_live")],
            [InlineKeyboardButton("Back", callback_data="age_yes")]
        ]
        await query.edit_message_text("Live anon personnel\n\nPrice: $750", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data in ["pay_videos", "pay_live"]:
        crypto_keyboard = [
            [InlineKeyboardButton("BTC", callback_data="btc"),
             InlineKeyboardButton("ETH", callback_data="eth")],
            [InlineKeyboardButton("USDT", callback_data="usdt")],
            [InlineKeyboardButton("Back", callback_data="videos" if query.data == "pay_videos" else "live")]
        ]
        await query.edit_message_text(
            "Select your payment method:",
            reply_markup=InlineKeyboardMarkup(crypto_keyboard)
        )

    elif query.data in ["btc", "eth", "usdt"]:
        addresses = {
            "btc": "your_btc_wallet_address",
            "eth": "your_eth_wallet_address",
            "usdt": "your_usdt_wallet_address"
        }
        wallet = addresses[query.data]

        msg = await query.edit_message_text(
    text=f"💎 Send your payment in {chosen} to this address:\n\n{wallet}\n\n⚠️ This address will self-destruct in 5 minutes.",
    reply_markup=InlineKeyboardMarkup(keyboard)
)

        # Auto delete after 5 mins
        await asyncio.sleep(300)
        try:
            await query.delete_message()
        except Exception as e:
            logger.error(f"Failed to delete message: {e}")

        # After deletion, show "I have sent payment" button
        sent_keyboard = [[InlineKeyboardButton("I have sent payment", callback_data="sent")]]
        await query.message.reply_text("Did you send the payment?", reply_markup=InlineKeyboardMarkup(sent_keyboard))

    elif query.data == "sent":
        await query.edit_message_text(
            "🚪 Door is being unlocked to your goon-geon.\n\n📸 Send a screenshot of your transaction to the group."
        )

    elif query.data == "start_over":
        await start(update, context)

# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f"Update {update} caused error {context.error}")

# Main function
def main():
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_error_handler(error)
    application.run_polling()

if __name__ == "__main__":
    main()
