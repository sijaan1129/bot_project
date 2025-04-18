from flask import Flask, render_template, redirect, url_for, request, session
import discord
from discord.ext import commands
import os
import pymongo

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")  # Keep this secret key safe

# MongoDB setup
client = pymongo.MongoClient(os.environ.get("MONGODB_URI"))
db = client['discord_bot_db']

# Discord bot setup (Make sure to run your bot on a separate thread for the web dashboard)
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/settings')
def settings():
    # Fetch any saved settings from MongoDB (e.g., anti-spam, auto roles)
    anti_spam = db["settings"].find_one({"setting": "anti_spam"})["value"]
    return render_template("settings.html", anti_spam=anti_spam)

@app.route('/update_anti_spam', methods=["POST"])
def update_anti_spam():
    if request.method == "POST":
        new_value = request.form.get("anti_spam_value")
        db["settings"].update_one({"setting": "anti_spam"}, {"$set": {"value": new_value}}, upsert=True)
        return redirect(url_for('settings'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
