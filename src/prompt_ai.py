from openai import OpenAI
from keys import OPENAI_API_KEY
import os

# Load the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

OpenAI.api_key = api_key

client = OpenAI()


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",   
  messages=[
    {"role": "system", "content": "You are a sassy assistant, skilled in explaining unicorn mysticism with a creative flair."},
    {"role": "user", "content": "Compose a fable including a unicorn called Unifaxsparkle and a child named Lou."}
  ]
)

print(completion.choices[0].message)