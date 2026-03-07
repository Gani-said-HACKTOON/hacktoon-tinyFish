from dotenv import load_dotenv
load_dotenv()
from tinyfish import TinyFish
import os

print(os.getenv("TINYFISH_API_KEY"))  


#dari dokumentasi 
clien =  TinyFish() # Reads TINYFISH_API_KEY from environment


with clien.agent.stream(
    url="https://scrapeme.live/shop",  # Target website to automate
    goal="Extract the first 2 product names and prices",  # Natural language instruction
)as stream:
    for event in stream:
         if event.type.name == "STARTED":
            print("Agent started")

         elif event.type.name == "STREAMING_URL":
            print("Live view:", event.streaming_url)

         elif event.type.name == "PROGRESS":
            print("Progress:", event.purpose)

         elif event.type.name == "COMPLETE":
            print("Result:", event.result_json)