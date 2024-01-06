import re
from google.cloud import firestore
import google.generativeai as genai
import Constants
import requests
from bs4 import BeautifulSoup

# Configure Gemini API key
genai.configure(api_key=Constants.gemini_api)

# Initialize Firestore client
firebase_credentials_path = 'firebasecreds.json'
db = firestore.Client.from_service_account_json(firebase_credentials_path)

# Function to search for the latest Flutter news and extract content
def search_and_extract_flutter_news():
    # Implement your code to search for the latest Flutter news and extract content
    # Sample code using requests and BeautifulSoup (modify as per your requirements)
    search_query = 'java news of past 1 week'
    search_url = f'https://www.google.com/search?q={search_query}&tbm=nws'
    response = requests.get(search_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract relevant information such as news content and image URL
    news_content_elements = soup.find_all('div', class_='BNeawe vvjwJb AP7Wnd')
    image_url_elements = soup.find_all('img')

    # Assuming the first result for simplicity, adjust as needed
    news_title = news_content_elements[0].text.strip() if news_content_elements else "No news title found"
    news_summary = news_content_elements[0].text.strip() if news_content_elements else "No news content found"
    news_image_url = image_url_elements[0]['src'] if image_url_elements else "No image URL found"

    return news_title, news_summary, news_image_url

# Fetch the latest Flutter news
news_title, news_summary, news_image_url = search_and_extract_flutter_news()

# Print the plain output
print(f"News Title: {news_title}")
print(f"News Summary: {news_summary}")
print(f"Image URL: {news_image_url}")
print()

# Use the Google Gemini API to summarize the news content under 60 words
model = genai.GenerativeModel('gemini-pro')
summary_query = f'Summarize the latest Flutter news under 60 words: {news_summary}'
response = model.generate_content(summary_query)
print(response.text)

# Extract relevant information using regular expressions
image_url_match = re.search(r'\*\*Image URL:\*\* (.+)', response.text)
news_summary_match = re.search(r'\*\*Summary:\*\* (.+)', response.text)

image_url = image_url_match.group(1).strip() if image_url_match else "Unable to extract image URL"
news_summary = news_summary_match.group(1).strip() if news_summary_match else "Unable to extract summary"

# Push the news data to Firestore
news_collection = db.collection('News')  # Replace 'News' with your Firestore collection name
news_document = news_collection.add({
    'Title': news_title,
    'Summary': news_summary,
    'ImageUrl': image_url,
    'Date': firestore.SERVER_TIMESTAMP
})

print(f"News pushed to Firestore")
