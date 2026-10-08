from openai import OpenAI
# acces the open api threw the gimini
client = OpenAI(
    api_key="AIzaSyBC4MBgLIZHttYY6-iFDDK2mVe9w7nPIVk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    
    messages=[
        {   "role": "system",
            "content": "You are expert in maths adn only answer related question that if the query is not ralted to amth then dont answer  "
        },
        {
            "role": "user",
            "content": "255+100 "
        }
    ]
)

print(response.choices[0].message)