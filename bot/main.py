import discord
from discord.ext import commands
import os
import threading
from web_dashboard.app import app  # Import Flask app

# Discord bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Run Flask app on a separate thread
def run_flask():
    app.run(debug=True, host="0.0.0.0", port=5000)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

if __name__ == "__main__":
    # Start Flask in a separate thread
    threading.Thread(target=run_flask).start()

    # Run bot
    bot.run(os.environ.get("DISCORD_TOKEN"))
