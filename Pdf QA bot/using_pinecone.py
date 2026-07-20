# This uses no space in RAM
# PDF Q&A Bot

# Load a PDF.
# Split into chunks.
# Create embeddings.
# Store in FAISS.
# Answer questions with citations.

from langchain_anthropic import ChatAnthropic
from langchain_cohere import CohereEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
load_dotenv()

embeddings = CohereEmbeddings(
    model="embed-english-v3.0"
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
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

result = retriver.invoke(query)

context = "\n\n".join([doc.page_content for doc in result])

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
