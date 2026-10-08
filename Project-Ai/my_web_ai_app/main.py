from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles  # <-- Must be imported
from fastapi.requests import Request
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import os
from dotenv import load_dotenv
import traceback

load_dotenv()

app = FastAPI()

# 👇 THIS LINE MUST BE HERE (Right after app = FastAPI())
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# Rest of your code continues below...
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY", "AIzaSyBC4MBgLIZHttYY6-iFDDK2mVe9w7nPIVk"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class ScrapeRequest(BaseModel):
    url: str
    question: str

def fetch_website_text(url: str) -> str:
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    }
    try:
        response = requests.get(url, headers=headers, timeout=12)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        for element in soup(["script", "style", "nav", "footer", "header"]):
            element.decompose()
            
        return soup.get_text(separator=' ', strip=True)
    except Exception as e:
        raise Exception(f"Failed to fetch website: {str(e)}")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    # Fixed for modern Starlette template rendering
    return templates.TemplateResponse(request, "index.html")

@app.post("/api/ask-website")
def ask_website(data: ScrapeRequest):
    try:
        web_content = fetch_website_text(data.url)
        
        system_prompt = (
            "You are an expert AI assistant that reads webpage content and "
            "provides clear, accurate answers strictly based on the provided text."
        )
        user_prompt = f"Website Content:\n{web_content[:15000]}\n\nQuestion: {data.question}"
        
        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )
        answer = response.choices[0].message.content
        return {"status": "success", "answer": answer}
        
    except Exception as e:
        print("--- ERROR OCCURRED ---")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))