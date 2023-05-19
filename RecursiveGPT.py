import openai
import os
from tqdm import tqdm
from time import strftime

# use current time to create output filename
time_str = strftime('%Y%m%d_%H%M%S')
output_name = f'output_{time_str}.txt'
openai.api_key = 'YOUR-API-KEY'

input_path = 'input.txt'
output_path = output_name
chunk_size = 3000
prompt = 'The following are automated captions from a lecture. Use the captions to make brief and concise notes in bullet point form, as if you were a student watching this lecture.\n\n'

def process_chunk(chunk):
    with open(output_path, 'a') as output_file:
        messages = [{'role': 'system', 'content': 'I am a helpful assistant.'},
                {'role': 'user', 'content': (prompt + ' '.join(chunk))}]
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages)
        response = response['choices'][0]['message']['content']
        output_file.write(response + '\n\n')

def split_file_to_chunks(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        words = content.split()

        num_chunks = round(len(words)/chunk_size)
        cost_per_token = 0.0002/1000
        est_cost = len(words)/0.75*cost_per_token

        print(f'Estimated prompts required: {num_chunks:.1f} prompts ({chunk_size} words each)')
        print(f'Estimated cost: between ${est_cost:.2f}-${est_cost*2:.2f}')
        print(f'Press RETURN to continue or exit (Ctrl+Z) to cancel.')
        input()

        print(f'Writing full output to file {output_name}...')

        for i in tqdm(range(0, len(words), chunk_size)):
            chunk = words[i:i+chunk_size]
            process_chunk(chunk)

if __name__ == '__main__':
    split_file_to_chunks(input_path)