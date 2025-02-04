from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext
import requests
from bs4 import BeautifulSoup

# Replace with your bot token
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Sample Playing XI for England and India
playing_xi = {
    "England": ["Ben Duckett", "Philip Salt", "Jos Buttler", "Harry Brook", "Liam Livingstone", "Jacob Bethell", 
                "Jamie Overton", "Jofra Archer", "Brydon Carse", "Adil Rashid", "Mark Wood"],
    "India": ["Sanju Samson", "Abhishek Sharma", "Tilak Varma", "Suryakumar Yadav", "Hardik Pandya", 
              "Rinku Singh", "Shivam Dube", "Axar Patel", "Ravi Bishnoi", "Mohammed Shami", "Varun Chakaravarthy"]
}

# Function to fetch player stats from CricMetric
def fetch_player_stats(player_name, stat_type):
    url = f"https://www.cricmetric.com/index.py"
    params = {"search": player_name}
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract relevant data (Customize based on page structure)
    stats = []
    table = soup.find("table", {"class": "stat-table"})
    if table:
        rows = table.find_all("tr")[1:]  # Skip header
        for row in rows:
            cols = row.find_all("td")
            stats.append([col.text.strip() for col in cols])
    
    if not stats:
        return f"No {stat_type} records found for {player_name}."

    return f"Stats for {player_name} ({stat_type}):\n" + "\n".join([" | ".join(stat) for stat in stats])

# Start Command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Send a player name to get their records.")

# Player Name Handler
def player_handler(update: Update, context: CallbackContext) -> None:
    player_name = update.message.text

    # Check if the player is in any team's Playing XI
    team = None
    for t, players in playing_xi.items():
        if player_name in players:
            team = t
            break

    if not team:
        update.message.reply_text("Player not found in today's Playing XI.")
        return

    # Show options to user
    keyboard = [
        [InlineKeyboardButton("Twenty20 Stats", callback_data=f"t20|{player_name}")],
        [InlineKeyboardButton("T20I Stats", callback_data=f"t20i|{player_name}")],
        [InlineKeyboardButton("Venue Record", callback_data=f"venue|{player_name}")],
        [InlineKeyboardButton("Head-to-Head", callback_data=f"h2h|{player_name}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"Select a record type for {player_name}:", reply_markup=reply_markup)

# Callback Query Handler
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    
    stat_type, player_name = query.data.split("|")
    records = fetch_player_stats(player_name, stat_type)
    
    query.edit_message_text(text=records)

# Main Function
def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, player_handler))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
