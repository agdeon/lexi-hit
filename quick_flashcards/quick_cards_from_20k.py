import os
from openai import OpenAI
from dotenv import load_dotenv
import re
import time

def ask_gpt(msg, retry_delay=5):
    load_dotenv()
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    while True:
        try:
            response = client.responses.create(
                model="gpt-4o-mini",
                input=msg
            )
            return response.output_text
        except Exception as e:
            print(f'>>> Error: {e}')
            print(f'>>> Retrying in {retry_delay} seconds...')
            time.sleep(retry_delay)

def correct_response(text):
    pattern = re.compile(r'^[a-zA-Z]+;\s*[^,]+,\s*.+$')
    lines = text.strip().split('\n')
    filtered_lines = [line.strip() for line in lines if pattern.match(line.strip())]
    result = '\n'.join(filtered_lines)
    result = re.sub(r'\n{2,}', '\n', result)
    return result

PROMPT = "Give me the same list strictly in the following format: English word, then a semicolon, then its two most popular translations into Russian separated by a comma, then a new line, and so on. Do not use spaces in the response. Provide only the list of such words and do not write anything else in the answer. Only the transformed list in the specified format without any other text. Also, change the word if it requires capital letters, for example, proper names, and so on"

with open("20k_frequency_words.txt", "r", encoding="utf-8") as f:
    lines = [line.strip() for line in f]
print(f'>>> {len(lines)} lines extracted from the file')

batch_size = 90
batch_counter = 1

for i in range(0, len(lines), batch_size):
    batch = lines[i:i + batch_size]
    response_text = ask_gpt(f'{PROMPT}\n\n{",".join(batch)}')

    processed_batch = correct_response(response_text)

    with open("flashcards1.txt", "a", encoding="utf-8") as f:
        f.write(processed_batch)
        f.write("\n")

    print(f'>>> Batch number {batch_counter} completed. Words processed: {batch_counter * batch_size}')
    batch_counter += 1
    time.sleep(0.5)
