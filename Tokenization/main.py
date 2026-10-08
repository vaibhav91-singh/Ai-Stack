# first we create virtual environment
# to create virtual environment 
# python -m venv venv
# activate the virtual environment
# venv\Scripts\Activate.ps1 

import tiktoken 
enc = tiktoken.encoding_for_model("gpt-4o")

text="Hey, My name is vaibhav singh"
tokens = enc.encode(text)

print("Tokens",tokens)
# output Tokens [25216, 11, 3673, 1308, 382, 3423, 31685, 407, 6211, 71]

# decode
decoded=enc.decode([25216, 11, 3673, 1308, 382, 3423, 31685, 407, 6211, 71])
print(decoded)
