import pinecone
import os
from dotenv import load_dotenv

load_dotenv(".env")

apiKey :str =os.getenv("PINECONE_API_KEY")


pinecone.init(api_key=apiKey, environment="gcp-starter")
pinecone_index = pinecone.Index("test")
