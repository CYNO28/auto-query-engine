	
import openai
import os
from dotenv import load_dotenv
import pinecone


load_dotenv(".env")

apiKey :str =os.getenv("OPEN_API_KEY")

apiKey1 :str =os.getenv("PINECONE_API_KEY")


pinecone.init(api_key=apiKey1, environment="gcp-starter")
pinecone_index = pinecone.Index("test")

os.environ["OPENAI_API_KEY"] = apiKey

openai.api_key = os.environ["OPENAI_API_KEY"]

from llama_index import (
 VectorStoreIndex,
    SimpleDirectoryReader,
    ServiceContext,
    StorageContext,
    SQLDatabase,
    WikipediaReader

)



from llama_index.node_parser.simple import SimpleNodeParser
from llama_index import ServiceContext, LLMPredictor
from llama_index.storage import StorageContext
from llama_index.vector_stores import PineconeVectorStore
from llama_index.text_splitter import TokenTextSplitter
from llama_index.llms import OpenAI



chunk_size = 1024
llm = OpenAI(temperature=0, model="gpt-4", streaming=True)
service_context = ServiceContext.from_defaults(chunk_size=chunk_size, llm=llm)
text_splitter = TokenTextSplitter(chunk_size=chunk_size)
node_parser = SimpleNodeParser.from_defaults(text_splitter=text_splitter)


#  vector store
vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index, namespace="wiki_cities"
)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
vector_index = VectorStoreIndex([], storage_context=storage_context)
print(vector_index,"vector index")

from sqlalchemy import create_engine


db_url :str=os.getenv('SQL_DB_URL')

engine = create_engine(db_url)


with engine.connect() as connection:
    print('connection works')



sql_database = SQLDatabase(engine, include_tables=["city_stats"])   

from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine

sql_query_engine = NLSQLTableQueryEngine(sql_database,tables=["city_stats"],)

res=sql_query_engine.query("what is the country for tokyo")

print(str(res))


# cities = ["Toronto", "Berlin", "Tokyo"]
# wiki_docs = WikipediaReader().load_data(pages=cities)

# print('done fetch wiki_docs')

# for city, wiki_doc in zip(cities, wiki_docs):
#     nodes = node_parser.get_nodes_from_documents([wiki_doc])
    
#     for node in nodes:
#         node.metadata = {"title": city}
#     vector_store.insert_nodes(nodes)
# print('done till here')



# from llama_index.query_engine import SQLAutoVectorQueryEngine, RetrieverQueryEngine
# from llama_index.tools.query_engine import QueryEngineTool
# from llama_index.indices.vector_store import VectorIndexAutoRetriever
# from llama_index.indices.vector_store.retrievers import VectorIndexAutoRetriever
# from llama_index.vector_stores.types import MetadataInfo, VectorStoreInfo
# from llama_index.query_engine.retriever_query_engine import RetrieverQueryEngine


# vector_store_info = VectorStoreInfo(
#     content_info="articles about different cities",
#     metadata_info=[
#         MetadataInfo(name="title", type="str", description="The name of the city"),
#     ],
# )
# vector_auto_retriever = VectorIndexAutoRetriever(
#     vector_index, vector_store_info=vector_store_info
# )

# retriever_query_engine = RetrieverQueryEngine.from_args(
#     vector_auto_retriever, service_context=service_context
# )
# sql_tool = QueryEngineTool.from_defaults(
#     query_engine=sql_query_engine,
#     description=(
#         "Useful for translating a natural language query into a SQL query over a table containing: "
#         "city_stats, containing the population/country of each city"
#     ),
# )
# vector_tool = QueryEngineTool.from_defaults(
#     query_engine=retriever_query_engine,
#     description=f"Useful for answering semantic questions about different cities",
# )


# query_engine = SQLAutoVectorQueryEngine(
#     sql_tool, vector_tool, service_context=service_context
# )


# response = query_engine.query(
#     "Tell me about the arts and culture of the city with the highest population"
# )
# print(str(response))