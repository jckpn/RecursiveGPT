import openai
import os
from tqdm import tqdm
import sys
import nltk
nltk.download('punkt')

def count_tokens(string: str, encoding_name: str) -> int:
    num_tokens = len(string) // 4  # Divide the length of the text by 4
    return num_tokens

def split_file_to_chunks(prompt, input_path, output_path, model):
    with open(input_path, 'r') as file:
        content = file.read()
        paragraphs = content.split("\n")
        chunks = []

        def split_paragraph(paragraph):
            sentences = nltk.sent_tokenize(paragraph)
            half = len(sentences) // 2
            return ' '.join(sentences[:half]).strip(), ' '.join(sentences[half:]).strip()

        with tqdm(total=len(paragraphs), desc="Processing paragraphs") as pbar:
            current_chunk = []
            current_chunk_length = 0

            for paragraph in paragraphs:
                paragraph_length = count_tokens(paragraph, 'cl100k_base')

                if current_chunk_length + paragraph_length <= 3500:
                    current_chunk.append(paragraph)
                    current_chunk_length += paragraph_length
                else:
                    if paragraph_length > 3500:
                        first_half, second_half = split_paragraph(paragraph)
                        chunks.append('\n'.join(current_chunk))
                        chunks.append(first_half.strip())
                        chunks.append(second_half.strip())
                        current_chunk = []
                        current_chunk_length = 0
                    else:
                        chunks.append('\n'.join(current_chunk))
                        current_chunk = [paragraph]
                        current_chunk_length = paragraph_length

                pbar.update(1)

            if current_chunk:
                chunks.append('\n'.join(current_chunk))

        with tqdm(total=len(chunks), desc="Processing chunks") as pbar:
            for i, chunk in enumerate(chunks):
                full_prompt = prompt + f'\n(Note: the following is an extract, chunk {i + 1} of {len(chunks)})\n\n'
                print(count_tokens(chunk, 'cl100k_base'))
                print (full_prompt + ": " + chunk)
                process_chunk(full_prompt, chunk, output_path, model)
                pbar.update(1)

        print(f'Finished writing to {output_path}.')

def process_chunk(prompt, chunk, output_path, model):
    with open(output_path, 'a') as output_file:
        messages = [{'role': 'system', 'content': 'I am a helpful assistant.'},
                {'role': 'user', 'content': (prompt + chunk)}]
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages)
        response = response['choices'][0]['message']['content']
        output_file.write(response + '\n\n')

if __name__ == '__main__':
    api_key = input('Enter your OpenAI API key: ')
    openai.api_key = api_key
    # TODO: add checks for key validity

    model = input('Enter the model to be used (default: gpt-3.5-turbo, available: gpt-4): ')
    if model == '':
        model = 'gpt-3.5-turbo'

    input_path = input('Enter the input path to the text file to process: ')
    if os.path.exists(input_path) == False:
        print(f'`{input_path}` can\'t be found.')
        exit()

    prompt = input('Enter the prompt to be prepended to each chunk of text: ')
    if prompt == '':
        print('A prompt is required to use this script.')
        exit()

    output_path = input('Enter the output path to the text file to write to (default: output.txt): ')
    if output_path == '':
        output_path = 'output.txt'
        
    split_file_to_chunks(prompt, input_path, output_path, model)
