from openai import OpenAI
import os


client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
# client = OpenAI()

response=client.responses.create(
    model="gpt-5-mini",
    input="start"
)

print(response.output_text)