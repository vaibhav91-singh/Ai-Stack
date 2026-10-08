from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

API_KEY = "YOUR_API_KEY_HERE"

def process_query(query:str):
    print("Searching Chunks", query)
    search_result = vector_db.similarity_search(query=user_query)

    context= "\n\n\n".join([f"page content : {result.page_content}\n Page number : { result.metadata['page_lable']}\n Fole locate "])
    SYSTEM_PROMPT = """
You are a helpful AI assistant who answers user queries based strictly on the available context retrieved from PDF files. 
Always include relevant details, page contents, and page numbers when available in the context.
If the answer cannot be found in the context, politely state that you don't know based on the provided documents.
"""

response = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    message=[
        {"role": "system","content":SYSTEAM_PROMPT},
        {"role":"user","content":query},
    ]
    temperature=0.2,
    google_api_key=API_KEY,
    print(f"{response.choices[0].message.content}")
    return response.choices[0].message.content
)
