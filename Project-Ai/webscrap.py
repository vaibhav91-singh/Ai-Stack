from dotenv import load_dotenv
from openai import OpenAI
import requests
from bs4 import BeautifulSoup

load_dotenv()

client = OpenAI(
    api_key="AIzaSyBC4MBgLIZHttYY6-iFDDK2mVe9w7nPIVk",
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

def fetch_website_text(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for script in soup(["script", "style"]):
            script.decompose()
            
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        return f"Error fetching website: {e}"

def main():
    url = input("<< Enter Website URL :: ")
    user_question = input("<< What do you want to know from this website? :: ")
    
    # 1. Fetch content from the website
    print("Fetching website content...")
    web_content = fetch_website_text(url)
    
    # 2. Construct the prompt with the scraped text
    system_prompt = "You are an AI assistant that reads webpage content and answers questions based strictly on the provided text."
    user_prompt = f"Website Content:\n{web_content}\n\nUser Question: {user_question}"
    
    # 3. Call Gemini
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    
    print("\n--- Response ---")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()

