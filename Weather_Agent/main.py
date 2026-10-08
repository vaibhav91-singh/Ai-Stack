
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel,Field
from typing import Optional
load_dotenv()
# The client gets the API key from the environment variable `GEMINI_API_KEY`.

# acces the open api threw the gimini
client = OpenAI(
    api_key="AIzaSyBC4MBgLIZHttYY6-iFDDK2mVe9w7nPIVk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
SYSTEM_PROMPT = """
YOU ARE AI ASSISTANT OF WEATHER INFORMATION
YOU GIVE TEMPTURE OF CURRENT WEATHER IN TERM OF DEGREE 
USER ENTER CITY AME YOU GIVE THEM CURRENT TEMPTURE OF THAT CITY 
IF USER WANT ANYTHING RATHER THAN TEMPRETURE THEN SHOW THEM INVALID PLESE ASK ONLY TEMPTURE 
CRITICAL RULE 
RESPONSE SHOULD BE ONLY IN NUMBER 
if user ansk anything rather than twmpture of city then show them plese enter city 

"""
def run_Command(cmd:str):
    result=os.System(cmd)
    return result

# my op formate 
print("/n/n/n")
class MyOutputFormate(Basemodel):
    step: str = Field(..., description = " The Id Of the step, Example: Plan, Output,Tool,etc")
    content:Optional[str] = Field(None,description ="The optional string content foe the step")
    tool:Optional[str] = Field(None,description="The Id of the tool to call.")
    input:Optional[str] = Field(None,description="The Input params for the tool")

def main():
    user_query = input("<< Enter City ::")
    # LLM calling
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages =[
            {"role": "system", "content": SYSTEM_PROMPT},  # <-- Fixed: Passed as system role
            {"role": "user", "content": user_query}
        ]
    )
    print(f'{response.choices[0].message.content}')
main()
