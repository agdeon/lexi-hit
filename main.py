import os
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.responses.create(
    model="gpt-4o-mini",
    input="Привет привет мой свет"
)

print(response.output_text)

