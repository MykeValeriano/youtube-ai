import os
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from utils.text_splitter import split_text
from utils.youtube_agent import get_transcript_from_youtube
load_dotenv()


def load_vector_db(transcript):
    # Step 1: Split transcript
    documents = split_text(transcript)

    # Step 2: Create Gemini embeddings using Google API key
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key="AIzaSyBcRtLFcwuHt2cMN_1Qf9G0xn48w1usn4Y"  # ✅ updated key name
    )

    # Step 3: Create FAISS vector DB
    vectorstore = FAISS.from_documents(documents, embeddings)

    return vectorstore