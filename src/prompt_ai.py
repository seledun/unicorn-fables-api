from openai import OpenAI
import os
import json
from store.Unicorn import Unicorn 


def get_fable_from_openai(unicorn: json, mood : str) -> json:
  # Load the API key from the .env file
  api_key = os.getenv("OPENAI_API_KEY")

  # Attach the API key directly to the OpenAI object / module
  OpenAI.api_key = api_key

  client = OpenAI()

  # Extract the useful unicorn parts 
  unicorn_name = unicorn.json().get("name"), 
  location = unicorn.json().get("spottedWhere").get("name"),  
  unicorn_description = unicorn.json().get("description"), 
  name_of_person = unicorn.json().get("reportedBy"), # Antingen upptäckaren av enhörningen, eller användaren som matar in sitt namn
  
  story_theme = mood   # Lösa denna på något sätt
  


  completion = client.chat.completions.create(
    model="gpt-3.5-turbo", 
    messages=[
      {"role": "system", "content": "You are a magical assistant, skilled in telling whimsical and captivating unicorn fables with a mystic flair." + 
      " Your answer needs to be in Swedish."},
      {"role": "user", "content": "Compose a fable including a unicorn called " + unicorn_name + " and a person named " + name_of_person + "." +
      "The location for their encounter:" + location + " , " + 
      "this is the description of the unicorn:" + unicorn_description + "and the theme of the story should be " + story_theme + "."}
    ], 
    temperature=0.4
    
  )



  # Get the response content as a str
  response = completion.choices[0].message.content

  return response

# Print the response JSON object
# print(response)
# print(type(response))