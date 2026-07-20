from langchain_anthropic import ChatAnthropic
from langchain_cohere import CohereEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from dotenv import load_dotenv
import os
load_dotenv()

embeddings = CohereEmbeddings(
    model="embed-multilingual-v3.0"
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

retriever = vector_store.as_retriever(search_kwargs={'k':3})

# LLM
model = ChatAnthropic(
    model="claude-sonnet-4-6",  # or "claude-2.0"
    base_url='https://capi.aerolink.lat/'
)

prompt = ChatPromptTemplate.from_template("""
You are a helpful AI assistant.

The retrieved context may be written in any language.

Instructions:
1. Detect the language of the retrieved context.
2. If the context is not in English, translate it internally into English before reasoning.
3. Answer every question in fluent English unless the user explicitly requests another language.
4. Use only the information provided in the context.
5. If the answer cannot be found in the context, reply with:
   "I don't know based on the provided context."

Context:
{context}

Question:
{input}

Answer:
""")

query = "Give me the summary of the video"

def format_docs(docs):
    context = "\n\n".join([doc.page_content for doc in docs])

    return context

parser = StrOutputParser()

document_chain = create_stuff_documents_chain(
    llm=model,
    prompt=prompt
)

retriever_chain = create_retrieval_chain(
    retriever,
    document_chain
)

response = retrieval_chain.invoke({
    "input": "Give me the summary of the video"
})

print(response)