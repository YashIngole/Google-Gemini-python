import google.generativeai as genai
import os
import Constants
genai.configure(api_key = Constants.gemini_api)

model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('hey')

print(response.text)