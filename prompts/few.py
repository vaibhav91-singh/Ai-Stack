# Few shot prompting
from openai import OpenAI
# acces the open api threw the gimini
client = OpenAI(
    api_key="AIzaSyBC4MBgLIZHttYY6-iFDDK2mVe9w7nPIVk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT="""  # Rules for Agent
# In this field all rules are writing here
Q:who is the father of zero
A:Brahmagupta

Q: what is the formula of a+b whole square
A: a^2+b^2=2*a*b

Q: provide all answer at current time period

"""


response = client.chat.completions.create(
    model="gemini-3-flash-preview",
    
    messages=[
        {   "role": "system",
            "content":SYSTEM_PROMPT  # define rules in content 
            },
        {
            "role": "user",
            "content":"who is the President of America"
            
            
        }
    ]
)
print(response.choices[0].message)
