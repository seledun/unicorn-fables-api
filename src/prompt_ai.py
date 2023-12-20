from openai import OpenAI
import os
import json

# Load the API key from the .env file
api_key = os.getenv("OPENAI_API_KEY")

# Attach the API key directly to the OpenAI object / module
OpenAI.api_key = api_key

client = OpenAI()

name_of_person = "Anna"      # Antingen upptäckaren av enhörningen, eller användaren som matar in sitt namn
unicorn_name = "Blobb"
location = "Malmö"
encounter_date = "2020-01-01"
unicorn_description = "Bladibladiblo"
story_theme = "Romantic mystery"


completion = client.chat.completions.create(
  model="gpt-3.5-turbo", 
  messages=[
    {"role": "system", "content": "You are a magical assistant, skilled in telling whimsical and captivating unicorn fables with a mystic flair." + 
     " Your answer needs to be in Swedish."},
    {"role": "user", "content": "Compose a fable including a unicorn called " + unicorn_name + " and a person named " + name_of_person + "." +
    "The location for their encounter:" + location + " , date of the encounter: " + encounter_date + ", " + 
    "this is the description of the unicorn:" + unicorn_description + "and the theme of the story should be " + story_theme + "."}
  ], 
  temperature=0.4
  
)



# Get the response content as a str
response = completion.choices[0].message.content

# Print the response JSON object
print(response)
print(type(response))


# print(completion.choices[0].message.content)