# Zero shot prompting
from openai import OpenAI
# acces the open api threw the gimini
client = OpenAI(
    api_key="AIzaSyBC4MBgLIZHttYY6-iFDDK2mVe9w7nPIVk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
#Zeroshot prompitng
SYSTEM_PROMPT=" You should only ans only ans  math realted query. do not answer if query is not related math ans say sorry , Your name is Alexa , "
response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    
    messages=[
        {   "role": "system",
            "content":SYSTEM_PROMPT
            },
        {
            "role": "user",
            "content": "(a+b)^2"
        }
    ]
)

print(response.choices[0].message)