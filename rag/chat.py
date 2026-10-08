from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore

# Define API key and configuration constants (matching your index.py)
API_KEY = "YOUR_API_KEY_HERE"
COLLECTION_NAME = "Learning_RAG"
QDRANT_URL = "http://localhost:6333"

print("Connecting to embedding model and Qdrant database...")

# 1. Embedding Model (Must match the one used during indexing)
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    google_api_key=API_KEY
)

# 2. Connect to the existing Qdrant vector store collection
vector_db = QdrantVectorStore.from_existing_collection(
    url=QDRANT_URL,
    collection_name=COLLECTION_NAME,
    embedding=embedding_model
)

# 3. Initialize Generation Model (Gemini Flash)
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.2,
    google_api_key=API_KEY
)

# Define the system prompt
SYSTEM_PROMPT = """
You are a helpful AI assistant who answers user queries based strictly on the available context retrieved from PDF files. 
Always include relevant details, page contents, and page numbers when available in the context.
If the answer cannot be found in the context, politely state that you don't know based on the provided documents.
"""

# 4. Interactive Chat Loop
print("\n--- RAG Chatbot Ready ---")
while True:
    user_query = input("\nAsk Something (type 'exit' to quit): ").strip()
    
    if user_query.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break
        
    if not user_query:
        continue

    print("Searching documents...")
    # Perform similarity search to fetch relevant chunks
    search_results = vector_db.similarity_search(query=user_query, k=3)

    # Format the retrieved context cleanly
    context_blocks = []
    for doc in search_results:
        page_num = doc.metadata.get("page", "Unknown")
        context_blocks.append(f"[Page {page_num}]: {doc.page_content}")
    
    combined_context = "\n\n".join(context_blocks)

    # Build the final prompt for the LLM
    final_prompt = f"""
{SYSTEM_PROMPT}

Retrieved Context:
{combined_context}

User Query: {user_query}
"""

    print("Generating answer...")
    # Invoke the LLM
    response = llm.invoke(final_prompt)
    
    # Safely extract text whether response.content is a string or a list of blocks
    if isinstance(response.content, list):
        answer_text = "".join([block.get("text", "") for block in response.content if isinstance(block, dict)])
    else:
        answer_text = str(response.content)
    print("\n--- Answer ---")
    print(answer_text)
    print("-" * 40)