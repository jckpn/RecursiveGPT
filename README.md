# RecursiveGPT

Process large text files and documents with ChatGPT. Requires an [OpenAI API key](https://platform.openai.com/account/api-keys).

This works by splitting the file into chunks within the context window of ChatGPT (currently limited to 4096 tokens).
You simply specify a prompt, and it'll get prepended to the start of each chunk.
The ChatGPT outputs are recursively added to an output text file.

Example prompts:
- _"Summarise the following lecture notes."_
- _"Proofread the following, providing your response in the form 'original text' -> 'revised text'."_
- _"Rewrite the following in the style of a pirate."_
- _"Convert the following scientific paper into a child-friendly overview."_
- _"Task: For each mention of a dog breed, state the breed and describe where in the text it occurs."_
