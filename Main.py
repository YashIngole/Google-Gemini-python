import google.generativeai as genai
from google.cloud import firestore
import Constants
import re

# Configure Gemini API key
genai.configure(api_key=Constants.gemini_api)

# Initialize Firestore client
firebase_credentials_path = 'firebasecreds.json'
db = firestore.Client.from_service_account_json(firebase_credentials_path)

# Fetch the latest Flutter news using Gemini
model = genai.GenerativeModel('gemini-pro') 
response = model.generate_content('Provide a summary of Flutter news under 60 words with a publicly accessible image URL. Include the image URL after **Image URL:** and the summary after **Summary:**')


# Print the plain response on the CLI
print("Plain Response:")
print(response.text)
print()

# Extract relevant information using regular expressions
image_url_match = re.search(r'\*\*Image URL:\*\* (.+)', response.text)
news_summary_match = re.search(r'\*\*Summary:\*\* (.+)', response.text)

image_url = image_url_match.group(1).strip() if image_url_match else "Unable to extract image URL"
news_summary = news_summary_match.group(1).strip() if news_summary_match else "Unable to extract summary"

# Push the news data to Firestore
news_collection = db.collection('News')  # Replace 'News' with your Firestore collection name
news_document = news_collection.add({
    'Summary': news_summary,
    'ImageUrl': image_url,
    'Date': firestore.SERVER_TIMESTAMP
})

print(f"News pushed to Firestore ")
