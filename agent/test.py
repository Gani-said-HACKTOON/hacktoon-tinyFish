from ollama import chat
from ollama import ChatResponse

response: ChatResponse = chat(model='qwen2.5-coder:latest', messages=[
  {
    'role': 'user',
    'content': 'Why is the sky blue?',
  },
])
print(response['message']['content'])
print(response.message.content)

# test with ollama library