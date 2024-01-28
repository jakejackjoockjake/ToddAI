from openai import OpenAI
from pathlib import Path
from dotenv import load_dotenv
import requests
from gtts import gTTS
import os



def generateStory(classes): 

  client = OpenAI(API_KEY=API_KEY)

  response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
      {"role": "system", "content": "Write a 200 word fairytale story about a " + classes + ". The primary audience of this story is for children."},
    ]
  )

  aiResponse = response.choices[0].message.content

  return
def generateTextToSpeech(prompt):
  myText = prompt
  language = 'en'

  myobj = gTTS(text=myText, lang=language, slow=False)

  myobj.save("audio/output.mp3")
