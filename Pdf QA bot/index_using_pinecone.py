# Run only when needed for embedding the pdf and indexing into Pinecone when changed

from langchain_community.document_loaders import PyPDFLoader
from pinecone import Pinecone
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
from dotenv import load_dotenv

load_dotenv()

docs = PyPDFLoader("langchain.pdf").load()

print(len(docs))

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=0
)

embeddings = CohereEmbeddings(
    model="embed-english-v3.0"
)

chunks = splitter.split_documents(docs)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

vector_store.add_documents(chunks)