import time
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_qdrant import QdrantVectorStore

# Define API key and configuration constants
API_KEY = "YOUR_API_KEY_HERE"
COLLECTION_NAME = "Learning_RAG"
QDRANT_URL = "http://localhost:6333"

# Define PDF path
pdf_path = Path(__file__).parent / "nodeJs.pdf"

# 1. Loader: Load the PDF document
print("Loading PDF document...")
loader = PyPDFLoader(file_path=str(pdf_path))
docs = loader.load()

# 2. Chunking: Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

chunks = text_splitter.split_documents(documents=docs)
print(f"Total chunks created: {len(chunks)}")

# 3. Embedding Model: Dedicated model for converting text to vectors
embedding_model = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-2-preview",
    google_api_key='YOUR_API_KEY_HERE'
)

# 4. Vector Store: Index chunks in safe batches to bypass Free Tier 429 limits
print("Starting safe batch indexing into Qdrant...")
vector_store = None
batch_size = 5  # Small batch size to strictly respect free tier rate limits

for i in range(0, len(chunks), batch_size):
    batch_chunks = chunks[i:i + batch_size]
    if vector_store is None:
        # Initialize collection with the first batch
        vector_store = QdrantVectorStore.from_documents(
            documents=batch_chunks,
            embedding=embedding_model,
            url=QDRANT_URL,
            collection_name=COLLECTION_NAME
        )
    else:
        # Append subsequent batches to the existing collection
        vector_store.add_documents(batch_chunks)
    print(f"Successfully indexed batch {i // batch_size + 1} of {(len(chunks) + batch_size - 1) // batch_size}")
    
    # Pause for 4 seconds between batches to avoid hitting API rate limits
    time.sleep(4)

print("Indexing of documents complete successfully!")

# 5. Generation Model: Use Gemini Flash for text generation and Q&A
llm = ChatGoogleGenerativeAI(
    model="gemini-3.6-flash",
    temperature=0.2,
    google_api_key='YOUR_API_KEY_HERE'
)