from openai import OpenAI
import os
import json
from store.Unicorn import Unicorn 
import keys


def get_fable_from_openai(unicorn: json, mood : str) -> json:
  # Load the API key from the .env file
  # api_key = os.environ['OPENAI_API_KEY']
  api_key = keys.OPENAI_API_KEY

  # Attach the API key directly to the OpenAI object / module
  #OpenAI.api_key = api_key

  client = OpenAI(api_key=api_key)

  # Extract the useful unicorn parts - EV TA BORT .json !!!!!!!!!
  unicorn_name = unicorn.get("name") 
  location = unicorn.get("spottedWhere").get("name") 
  unicorn_description = unicorn.get("description")
  name_of_person = unicorn.get("reportedBy") # Antingen upptäckaren av enhörningen, eller användaren som matar in sitt namn
  
  if (mood == "happy"):
    story_theme = "light and happy"
  elif (mood == "night"):
    story_theme = "dark, thrilling and a bit scary"

  


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

