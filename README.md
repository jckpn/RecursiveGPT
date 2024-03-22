RecursiveGPT

Process large text files and documents with ChatGPT (more APIs coming soon\*). Requires [Python 3](https://www.python.org/downloads/) and an [OpenAI API key](https://platform.openai.com/account/api-keys).

## Use:

Currently command-line only.

```bash
git clone https://github.com/jckpn/RecursiveGPT.git
cd RecursiveGPT
pip install -r requirements.txt
python RecursiveGPT.py
```
Then just follow the prompts as given in the termimal.

## How it works

This script works by splitting the file into chunks within the context window of ChatGPT (currently limited to 4096 tokens).
You simply specify a prompt, and it'll get prepended to the start of each chunk.
The ChatGPT outputs are recursively added to an output text file.

## Examples

Your prompts could be anything like:
- _"Summarise the following lecture notes."_
- _"Proofread the following, providing your response in the form \[original text -> revised text\]."_
- _"Rewrite the following in the style of a pirate."_
- _"Convert the following scientific paper into a child-friendly overview."_
- _"Task: For each mention of a dog breed, state the breed and describe where in the text it occurs."_

The prompt below was _"Convert these lecture captions to concise revision notes."_
<img width="1033" alt="Screenshot 2023-05-20 at 16 09 06" src="https://github.com/jckpn/RecursiveGPT/assets/14837124/8b1a2fde-f11b-4ef7-9e27-fde418ee1418">

I made this to help me with tasks like proofreading and lecture summaries, but it works well for a range of tasks.

\**I have very little free time at the moment due to my MSc and other jobs – pull requests would be appreciated!*

(Privacy note: No data is sent anywhere except for interacting with the ChatGPT API.)
