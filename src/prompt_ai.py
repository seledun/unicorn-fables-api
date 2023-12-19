from openai import OpenAI
import os

# Load the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# Attach the API key directly to the OpenAI object / module
OpenAI.api_key = api_key

client = OpenAI()

gender = "non-binary person"
name = "Anna"
unicorn_name = "Blobb"


completion = client.chat.completions.create(
  model="gpt-3.5-turbo",   
  messages=[
    {"role": "system", "content": "You are a magical assistant, skilled in telling whimsical and captivating unicorn fables with a mystic flair."},
    {"role": "user", "content": "Compose a fable including a unicorn called " + unicorn_name + " and a " + gender + " named" + name + " ."}
  ]
)

print(completion.choices[0].message)