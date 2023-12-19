
import os
from openai import OpenAI
import keys

# Load the API key from the .env file
#api_key = os.getenv("OPENAI_API_KEY")
api_key = keys("OPENAI_API_KEY")

client = OpenAI(api_key)

completion = client.chat.completions.create(
  model="gpt-3.5-turbo",   
  messages=[
    {"role": "system", "content": "You are a sassy assistant, skilled in explaining unicorn mysticism with a creative flair."},
    {"role": "user", "content": "Compose a fable including a unicorn called Unifaxsparkle and a child named Lou."}
  ]
)

print(completion.choices[0].message)