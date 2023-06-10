import openai
import os
from tqdm import tqdm
import sys
import nltk
nltk.download('punkt')

def count_tokens(string: str) -> int:
    num_tokens = len(string) // 4  # Divide the length of the text by 4
    return num_tokens

def split_file_to_chunks(prompt, input_path, output_path, model, token_max):
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
                paragraph_length = count_tokens(paragraph)

                if current_chunk_length + paragraph_length <= token_max:
                    current_chunk.append(paragraph)
                    current_chunk_length += paragraph_length
                else:
                    if paragraph_length > token_max:
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

        confirm_proceed(content, len(chunks))

        with tqdm(total=len(chunks), desc="Processing chunks") as pbar:
            for i, chunk in enumerate(chunks):
                full_prompt = prompt + f'\n(Note: the following is an extract, chunk {i + 1} of {len(chunks)})\n\n'
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
        output_file.write(response + '\n\n' + '++++++++++++++++++++++' + '\n\n')

def confirm_proceed(content, chunk_count):
    est_tokens = count_tokens(content)
    cost_per_token = 0.0002/1000
    est_cost = est_tokens*cost_per_token
    est_time = est_tokens/4000*1.5 # around 1.5 mins per 4000 tokens

    print(f'\nEstimated tokens required: {est_tokens:.1f} ({chunk_count} prompts)')
    print(f'Estimated cost: between ${est_cost:.2f}-${est_cost*2:.2f}')
    print(f'Estimated time: {est_time:.1f} minutes')
    print(f'Press RETURN to continue or exit (Ctrl+Z) to cancel.')
    input()

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

    token_max = 4098 - int(input('Enter the number of tokens you want the response to be (out of 4k total tokens): '))
    if token_max == '':
        print('A token count is required to use this script.')
        exit()

    output_path = input('Enter the output path to the text file to write to (default: output.txt): ')
    if output_path == '':
        output_path = 'output.txt'
        
    split_file_to_chunks(prompt, input_path, output_path, model, token_max)
