from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import os
import requests

API_KEY = os.getenv("API_KEY")
XI_API_KEY = os.getenv("XI_API_KEY")

def generateStory(classes): 

  client = OpenAI(api_key=API_KEY)

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Write a 200 word fairytale story about a " + classes + ". The primary audience of this story is for children."},
    ]
  )

  aiResponse = response.choices[0].message.content

  return aiResponse

def generateTextToSpeech(prompt):
  CHUNK_SIZE = 1024
  url = "https://api.elevenlabs.io/v1/text-to-speech/oWAxZDx7w5VEj9dCyTzz"

  headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": XI_API_KEY
  }

  data = {
    "text": prompt,
    "model_id": "eleven_monolingual_v1",
    "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
    }
  }

  response = requests.post(url, json=data, headers=headers)
  with open('audio/speechoutput.mp3', 'wb') as f:
      for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
          if chunk:
              f.write(chunk)