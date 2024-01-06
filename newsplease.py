from google.cloud import firestore
from newsplease import NewsPlease
import Constants

# Initialize Firestore client
firebase_credentials_path = 'firebasecreds.json'
db = firestore.Client.from_service_account_json(firebase_credentials_path)

# Specify the URL you want to extract news from
url_to_extract = 'https://example.com'  # Replace with your desired URL

# Use news-please to extract information from the URL
article = NewsPlease.from_url(url_to_extract)

# Extract relevant information
image_url = article.image_url if hasattr(article, 'image_url') else "Unable to extract image URL"
news_summary = article.description if hasattr(article, 'description') else "Unable to extract summary"

# Push the news data to Firestore
news_collection = db.collection('News')  # Replace 'News' with your Firestore collection name
news_document = news_collection.add({
    'Summary': news_summary,
    'ImageUrl': image_url,
    'Date': firestore.SERVER_TIMESTAMP
})

print(f"News pushed to Firestore")
