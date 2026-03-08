# from ollama import chat
# from ollama import ChatResponse

# response: ChatResponse = chat(model='qwen2.5-coder:latest', messages=[
#   {
#     'role': 'user',
#     'content': 'Why is the sky blue?',
#   },
# ])
# print(response['message']['content'])
# print(response.message.content)

# # test with ollama library
from dotenv import load_dotenv
load_dotenv()

from tinyfish import TinyFish
from fastapi import FastAPI

app = FastAPI()
client = TinyFish()

@app.get("/")
def hello():
    return {"message": "hello"}

@app.get("/scrape")
def scrape(url: str):

    result = None

    with client.agent.stream(
        url=url,
        goal="Summarize this website"
    ) as stream:

        for event in stream:
            if event.type.value == "COMPLETE":
                result = event.result_json

    return {"result": result}

#ngetes fastapi di gabung sama tinyfish