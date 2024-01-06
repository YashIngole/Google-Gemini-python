import google.generativeai as genai
import os
import Constants
from google.cloud import firestore

# Configure Gemini API key
genai.configure(api_key=Constants.gemini_api)

# Initialize Firestore client
firebase_credentials_path = 'path/to/your/firebase/credentials.json'
db = firestore.Client.from_service_account_json(firebase_credentials_path)

# Fetch the latest Flutter news using Gemini
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Flutter news')

# Extract relevant information from the response
news_data = response.text
news_data = " ".join(news_data.split()[:60])  # Limit to 60 words

# Push the news data to Firestore
news_collection = db.collection('news')  # Replace 'news' with your Firestore collection name
news_document = news_collection.add({
    'content': news_data,
    'timestamp': firestore.SERVER_TIMESTAMP
})

print(f"News pushed to Firestore with document ID: {news_document.id}")
