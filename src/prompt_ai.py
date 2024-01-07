from openai import OpenAI
import json
from store.Unicorn import Unicorn 
import keys

# Get a fable from OpenAI
# Using the OpenAI API, we can generate a fable based on the unicorn and the mood
# The fable is returned as a JSON object
def get_fable_from_openai(unicorn: json, mood : str) -> json:

  api_key = keys.OPENAI_API_KEY
  client = OpenAI(api_key=api_key)

  unicorn_name = unicorn.get("name") 
  location = unicorn.get("spottedWhere").get("name") 
  unicorn_description = unicorn.get("description")
  name_of_person = unicorn.get("reportedBy") 
  
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

  response = completion.choices[0].message.content

  return response


