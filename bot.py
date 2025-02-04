from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
from telegram import Bot
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Your token
TOKEN = '"8159859015:AAEk2mrnuWVfq79oSXQ0QkMyrJtxGjmOx9M'

# Command to start the bot
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Hello! I am your Cricket Bot.')

# Command to show player stats
def player_stats(update: Update, context: CallbackContext):
    # This should be updated with your actual logic to fetch player stats
    update.message.reply_text('Fetching player stats...')

# Command to show head-to-head stats
def head_to_head(update: Update, context: CallbackContext):
    # This should be updated with your actual logic to fetch head-to-head stats
    update.message.reply_text('Fetching head-to-head stats...')

# Function to handle messages
def handle_message(update: Update, context: CallbackContext):
    text = update.message.text.lower()
    if 'player' in text:
        player_stats(update, context)
    elif 'head-to-head' in text:
        head_to_head(update, context)
    else:
        update.message.reply_text("Sorry, I didn't understand that.")

def main():
    # Set up the Updater with the bot token
    updater = Updater(token=TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
