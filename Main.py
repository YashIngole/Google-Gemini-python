import re
from googlesearch import search
from bs4 import BeautifulSoup
from google.cloud import firestore
import google.generativeai as genai
import requests
import Constants

# Configure Gemini API key
genai.configure(api_key=Constants.gemini_api)

# Initialize Firestore client
firebase_credentials_path = 'firebasecreds.json'
db = firestore.Client.from_service_account_json(firebase_credentials_path)

# Function to visit the link and extract the image URL
def visit_link_and_extract_image(link):
    response = requests.get(link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the image URL from the article page
    image_element = soup.find('img')  # You might need a more specific selector here
    news_image_url = image_element['src'] if image_element and 'src' in image_element.attrs else "No image URL found"

    return news_image_url

# Function to search for the latest Technology news and extract content
def search_and_extract_technology_news():
    search_query = 'flutter news site:news.google.com'
    news_link = None

    # Search for the latest news and extract the first link
    for result in search(search_query, num_results=1):
        news_link = result
        break

    if not news_link:
        print("No news link found")
        return None, None, None

    response = requests.get(news_link)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the relevant information from the news page
    title_element = soup.find('h1')
    news_title = title_element.text if title_element else "No news title found"

    description_element = soup.find('meta', attrs={'name': 'description'})
    news_description = description_element['content'] if description_element and 'content' in description_element.attrs else "No news description found"

    # Use the improved method to extract the image URL
    news_image_url = visit_link_and_extract_image(news_link) if news_link else "No image URL found"

    return news_title, news_description, news_image_url

# Fetch the latest Technology news
news_title, news_description, news_image_url = search_and_extract_technology_news()

# Print the plain output
print(f"News Title: {news_title}")
print(f"News Description: {news_description}")
print(f"Image URL: {news_image_url}")
print()

# Use the Google Gemini API to summarize the news content under 60 words
model = genai.GenerativeModel('gemini-pro')
summary_query = f'Summarize this news in 50-60 words: {news_description}'
response = model.generate_content(summary_query)
print(response.text)

# Extract relevant information using regular expressions
news_summary_match = re.search(r'\*\*Summary:\*\* (.+)', response.text)
news_summary = news_summary_match.group(1).strip() if news_summary_match else "Unable to extract summary"

# Push the news data to Firestore
news_collection = db.collection('News')  # Replace 'News' with your Firestore collection name
news_document = news_collection.add({
    'Title': news_title,
    'Summary': news_summary,
    'ImageUrl': news_image_url,
    'Date': firestore.SERVER_TIMESTAMP
})

print(f"News pushed to Firestore")
