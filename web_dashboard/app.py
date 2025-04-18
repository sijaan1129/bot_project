from flask import Flask, render_template, request, redirect, url_for, session
import os
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Use the environment variable for MongoDB URI
client = MongoClient(mongo_uri)
db = client.get_database()  # Connect to your database

# Route for homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route for settings page
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        anti_spam_value = request.form.get('anti_spam_value')
        db.settings.update_one({"setting": "anti_spam"}, {"$set": {"value": anti_spam_value}}, upsert=True)
        return redirect(url_for('settings'))

    # Retrieve current anti-spam setting
    anti_spam = db.settings.find_one({"setting": "anti_spam"})
    anti_spam_value = anti_spam['value'] if anti_spam else 'False'
    
    return render_template('settings.html', anti_spam=anti_spam_value)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
