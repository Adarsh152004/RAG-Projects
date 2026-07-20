from langchain_anthropic import ChatAnthropic
from langchain_cohere import CohereEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence,RunnablePassthrough
from pinecone import Pinecone
from langchain_pinecone import PineconeVectorStore
from dotenv import load_dotenv
import os
load_dotenv()

video_id = "HhBhWdoXSdg"

embeddings = CohereEmbeddings(
    model="embed-multilingual-v3.0"
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

vector_store = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

retriever = vector_store.as_retriever(search_kwargs={
    'k':15, 
    'filter': {
        'video_id': video_id
    }
  }
)

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
2. If the context is not in English, mentally translate it into English before reasoning.
3. Answer every question in fluent English unless the user explicitly requests another language.
4. Use only the information provided in the context.
5. If the answer cannot be found in the context, reply with:
   "I don't know based on the provided context."
6. Do not make up facts or use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
""")

query = "What is the main topic discussed?"

result = retriever.invoke(query)

context = "\n\n".join([doc.page_content for doc in result])

parser = StrOutputParser()

chain = prompt | model | parser

response = chain.invoke({
    'context':context,
    'question': query
})

print(response)

def format_docs(docs):
    print("=" * 50)

    for i, doc in enumerate(docs):
        print(f"Chunk {i+1}")
        print(doc.page_content)
        print("-" * 50)

    return "\n\n".join(doc.page_content for doc in docs)

parser = StrOutputParser()

chain = prompt | model | parser

rag_chain = (
    {
    'context': retriever | format_docs,
    'question': RunnablePassthrough()
    }
    |
    chain
)

response = rag_chain.invoke(query)