from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore
import warnings

# Suppress annoying warning logs
warnings.filterwarnings("ignore", category=UserWarning)

app = FastAPI(title="DocuMind AI - PDF Chatbot")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration Constants
API_KEY = "YOUR_API_KEY_HERE"
COLLECTION_NAME = "Learning_RAG"
QDRANT_URL = "http://localhost:6333"
print("Initializing Embedding Model & Qdrant Connection...")
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    google_api_key=API_KEY
)

# Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    url=QDRANT_URL,
    collection_name=COLLECTION_NAME,
    embedding=embedding_model
)

# Initialize Gemini Flash LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.2,
    google_api_key=API_KEY
)

SYSTEM_PROMPT = """
You are a helpful AI assistant who answers user queries based strictly on the available context retrieved from PDF files. 
Always include relevant details, page contents, and page numbers when available in the context.
If the answer cannot be found in the context, politely state that you don't know based on the provided documents.
"""

class QueryRequest(BaseModel):
    query: str
# API endpoint for processing queries
@app.post("/ask")
async def ask_question(request: QueryRequest):
    user_query = request.query.strip()
    if not user_query:
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        # Similarity search in Qdrant
        search_results = vector_db.similarity_search(query=user_query, k=3)

        context_blocks = []
        for doc in search_results:
            page_num = doc.metadata.get("page", "Unknown")
            context_blocks.append(f"[Page {page_num}]: {doc.page_content}")
        
        combined_context = "\n\n".join(context_blocks)

        final_prompt = f"""
{SYSTEM_PROMPT}

Retrieved Context:
{combined_context}

User Query: {user_query}
"""

        response = llm.invoke(final_prompt)
        
        # Safely extract text from response
        if isinstance(response.content, list):
            answer_text = "".join([block.get("text", "") for block in response.content if isinstance(block, dict)])
        else:
            answer_text = str(response.content)

        return {"answer": answer_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Embedded HTML/CSS/JS Chatbot Frontend UI
@app.get("/", response_class=HTMLResponse)
async def get_frontend():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>DocuMind AI - PDF Chatbot</title>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
        <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: 'Inter', sans-serif; 
                background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                margin: 0; padding: 0; display: flex; justify-content: center; align-items: center; height: 100vh; 
            }
            .chat-container { 
                width: 600px; height: 750px; background: rgba(255, 255, 255, 0.9); 
                border-radius: 16px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); 
                display: flex; flex-direction: column; overflow: hidden; backdrop-filter: blur(10px); border: 1px solid rgba(255,255,255,0.5);
            }
            .chat-header { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 20px; text-align: center; font-size: 1.4rem; font-weight: 600; letter-spacing: 0.5px; 
            }
            .chat-messages { 
                flex: 1; padding: 25px; overflow-y: auto; display: flex; flex-direction: column; gap: 15px; 
            }
            .message { 
                max-width: 85%; padding: 14px 18px; border-radius: 12px; line-height: 1.6; word-wrap: break-word; font-size: 0.95rem; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            }
            .user-message { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; align-self: flex-end; border-bottom-right-radius: 4px; 
            }
            .bot-message { 
                background: white; color: #333; align-self: flex-start; border-bottom-left-radius: 4px; border: 1px solid #eee;
            }
            /* Markdown styles inside bot message */
            .bot-message p { margin-top: 0; margin-bottom: 10px; }
            .bot-message p:last-child { margin-bottom: 0; }
            .bot-message pre { background: #2d2d2d; color: #f8f8f2; padding: 10px; border-radius: 6px; overflow-x: auto; font-size: 0.9rem; }
            .bot-message code { font-family: Consolas, Monaco, monospace; background: rgba(0,0,0,0.05); padding: 2px 4px; border-radius: 4px; color: #d63384; }
            .bot-message pre code { background: none; padding: 0; color: inherit; }
            .bot-message table { border-collapse: collapse; width: 100%; margin-bottom: 10px; font-size: 0.9rem; }
            .bot-message th, .bot-message td { border: 1px solid #ddd; padding: 8px; }
            .bot-message th { background-color: #f8f9fa; }
            .bot-message ul, .bot-message ol { margin-top: 0; padding-left: 20px; }
            .bot-message blockquote { border-left: 4px solid #667eea; margin: 0; padding-left: 10px; color: #555; font-style: italic; }
            
            .chat-input-area { 
                display: flex; padding: 20px; background: white; border-top: 1px solid #eaeaea; 
            }
            .chat-input-area input { 
                flex: 1; padding: 14px 18px; border: 1px solid #ccc; border-radius: 25px; outline: none; font-size: 1rem; 
                transition: border-color 0.3s;
            }
            .chat-input-area input:focus { border-color: #667eea; }
            .chat-input-area button { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; border: none; padding: 14px 24px; margin-left: 12px; border-radius: 25px; cursor: pointer; 
                font-weight: 600; font-size: 1rem; transition: transform 0.2s, box-shadow 0.2s;
            }
            .chat-input-area button:hover { 
                transform: translateY(-2px); box-shadow: 0 4px 10px rgba(118, 75, 162, 0.3); 
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <div class="chat-header">📚 DocuMind AI</div>
            <div class="chat-messages" id="chatMessages">
                <div class="message bot-message">Hello! Ask me anything about your PDF document.</div>
            </div>
            <div class="chat-input-area">
                <input type="text" id="queryInput" placeholder="Ask a question..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">Send</button>
            </div>
        </div>
        <script>
            async function sendMessage() {
                const inputField = document.getElementById('queryInput');
                const messagesContainer = document.getElementById('chatMessages');
                const query = inputField.value.trim();
                if (!query) return;
                
                messagesContainer.innerHTML += `<div class="message user-message">${escapeHtml(query)}</div>`;
                inputField.value = '';
                messagesContainer.scrollTop = messagesContainer.scrollHeight;

                const loadingId = 'loading-' + Date.now();
                messagesContainer.innerHTML += `<div id="${loadingId}" class="message bot-message" style="color: #777;">Searching documents & thinking...</div>`;
                messagesContainer.scrollTop = messagesContainer.scrollHeight;

                try {
                    const response = await fetch('/ask', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ query: query })
                    });
                    const data = await response.json();
                    
                    document.getElementById(loadingId).remove();
                    
                    if (response.ok) {
                        // Use marked.parse to render Markdown properly to HTML
                        const parsedHtml = marked.parse(data.answer);
                        messagesContainer.innerHTML += `<div class="message bot-message">${parsedHtml}</div>`;
                    } else {
                        messagesContainer.innerHTML += `<div class="message bot-message" style="color: red;">Error: ${escapeHtml(data.detail || 'Something went wrong')}</div>`;
                    }
                } catch (err) {
                    document.getElementById(loadingId).remove();
                    messagesContainer.innerHTML += `<div class="message bot-message" style="color: red;">Network error connecting to backend server.</div>`;
                }
                messagesContainer.scrollTop = messagesContainer.scrollHeight;
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            function escapeHtml(text) {
                return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
            }
        </script>
    </body>
    </html>
    """

# RUN uvicorn main:app --reload
# server http://127.0.0.1:8000
