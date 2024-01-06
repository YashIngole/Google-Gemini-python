import requests
from google.cloud import firestore

# Initialize Firestore client
firebase_credentials_path = 'firebasecreds.json'
db = firestore.Client.from_service_account_json(firebase_credentials_path)

# Replace 'YOUR_BRAVE_SEARCH_API_KEY' with your actual Brave Search API key
brave_search_api_key = 'BSAXxqbn4ethV26K9AJM2z2IHoNBLj3'
brave_search_api_url = 'https://api.search.brave.com/res/v1/web/search'

# Specify the query parameters for the Brave Search API
params = {
    'q': 'brave search',  # Search term (you can adjust it based on your needs)
}

# Set up headers with the Brave Search API key
headers = {
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'X-Subscription-Token': brave_search_api_key,
}

# Make the Brave Search API request
response = requests.get(brave_search_api_url, params=params, headers=headers)
search_data = response.json()

# Print the full API response for inspection
print("Full API Response:", search_data)

# Extract relevant information from the Brave Search API response
title = snippet = url = "No results found"

if 'data' in search_data and 'results' in search_data['data']:
    results = search_data['data']['results']
    if results:
        result = results[0]
        title = result.get('title', title)
        snippet = result.get('description', snippet)
        url = result.get('url', url)

# Print the extracted information in the terminal
print("Title:", title)
print("Snippet:", snippet)
print("URL:", url)

# Push the search data to Firestore
search_collection = db.collection('SearchResults')  # Replace 'SearchResults' with your Firestore collection name
search_document = search_collection.add({
    'Title': title,
    'Snippet': snippet,
    'URL': url,
    'Date': firestore.SERVER_TIMESTAMP
})

print(f"Search results pushed to Firestore")
