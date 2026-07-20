# PDF Q&A Bot

# Load a PDF.
# Split into chunks.
# Create embeddings.
# Store in FAISS.
# Answer questions with citations.

from langchain_anthropic import ChatAnthropic
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence

import os

os.environ["HF_HOME"] = "E:/Projects/huggingface_cache"

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vector_store = Chroma(
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

retriver = vector_store.as_retriever(search_kwargs={"k": 3})

# LLM
model = ChatAnthropic(
    model="claude-sonnet-4-6",  # or "claude-2.0"
    base_url='https://capi.aerolink.lat/'
)

prompt = ChatPromptTemplate.from_template(
    template="You are a helpful assistant. Use the following context to answer the question. If you don't know the answer, just say that you don't know, don't try to make up an answer.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:",
    # input_variables=["context", "question"]
)


query = "Give me the summary of the document"

retrive = retriver.invoke(query)

context = "\n\n".join([doc.page_content for doc in retrive])

# messages = prompt.invoke({
#     "context": context,
#     "question": query
# })

parser = StrOutputParser()

chain = RunnableSequence(prompt, model, parser)

response = chain.invoke({
    "context": context,
    "question": query
})

print(response)
