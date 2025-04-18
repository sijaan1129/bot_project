from pymongo import MongoClient
import os

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")  # Use environment variable for MongoDB URI
client = MongoClient(mongo_uri)
db = client.get_database()  # Access the database
