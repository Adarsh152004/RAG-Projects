from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pinecone import Pinecone
from langchain_cohere import CohereEmbeddings
from langchain_pinecone import PineconeVectorStore
import os 
from dotenv import load_dotenv
from langchain_core.documents import Document

load_dotenv()

video_id = "HhBhWdoXSdg" # only the ID, not full URL
try:
    # If you don’t care which language, this returns the “best” one
    ytt_api = YouTubeTranscriptApi()
    transcript_list = ytt_api.fetch(video_id)

    transcript = " ".join(chunk.text for chunk in transcript_list)

    documents = [
        Document(
            page_content=transcript,
            metadata={
                "video_id": video_id
            }
        )
    ]

except TranscriptsDisabled:
    print("No caption available for this video. ")

splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

chunks = splitter.split_documents(documents)

embeddings = CohereEmbeddings(
    model="embed-multilingual-v3.0"
)

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
index = pc.Index(os.getenv("PINECONE_INDEX_NAME"))

vectorstore = PineconeVectorStore(
    index=index,
    embedding=embeddings
)

vectorstore.add_documents(chunks)