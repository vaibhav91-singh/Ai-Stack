import json
from openai import OpenAI

# Access the Gemini API via the OpenAI compatibility layer
client = OpenAI(
    api_key="AIzaSyBC4MBgLIZHttYY6-iFDDK2mVe9w7nPIVk",  # Note: Keep your API keys secure!
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

SYSTEM_PROMPT = """  
You are an expert AI Assistant that resolves user queries using a strict Chain of Thought (CoT) process.
You break down your thinking into sequential steps: START -> PLAN -> OUTPUT.

Rules:
- You must ONLY run one step per API call. 
- The sequence MUST start with PLAN steps to think through the problem, and end with an OUTPUT step.
- Never output anything other than the raw JSON object. Do not include prefixes like "PLAN:" or "OUTPUT:".

Output JSON format:
{
  "steps": "PLAN", 
#   "content": "Your reasoning or plan for this specific step"
}
or when completely finished:
{
  "steps": "OUTPUT", 
  "content": "The final answer to display to the user"
}
"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("👉 ")
message_history.append({"role": "user", "content": user_query})

print("\n--- Starting Chain of Thought ---")

while True:
    response = client.chat.completions.create(
        model="gemini-2.5-flash", # Use a stable current model version
        response_format={"type": "json_object"},
        messages=message_history
    )
    
    raw_result = response.choices[0].message.content
    
    # Save the assistant's step to the history so it remembers its progress
    message_history.append({"role": "assistant", "content": raw_result})
    
    try:
        parsed_result = json.loads(raw_result)
    except json.JSONDecodeError:
        print("❌ LLM returned invalid JSON:", raw_result)
        break

    # Extract step type and clean up any accidental whitespace
    steps = str(parsed_result.get("steps", "")).strip().upper()
    content = parsed_result.get("content", "")

    if steps == "PLAN":
        print(f"🧠 [PLAN]: {content}")
        # Crucial: Tell the LLM to continue to its next thought step
        message_history.append({"role": "user", "content": "Continue to the next step of your plan or output the final answer."})
        continue
    elif steps == "OUTPUT":
        print(f"\n🤖 [FINAL OUTPUT]: {content}")
        break
        
    else:
        # Fallback if it gives something unexpected
        print(f"❓ [UNKNOWN STEP '{steps}']: {content}")
        break

