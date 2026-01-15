import google.generativeai as genai
import os

# 1. Setup - Paste your key directly here for this test
# Make sure your key is inside the " " marks
YOUR_API_KEY = "AIzaSyCHbgD2i_8XD0bn4gqry1sUpXoeoan6jso"
genai.configure(api_key=YOUR_API_KEY)

print("Checking available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"✅ Available: {m.name}")
except Exception as e:
    print(f"❌ Error: {e}")