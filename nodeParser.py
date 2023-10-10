# from llama_index import (
#     VectorStoreIndex,
#     ServiceContext,
#     StorageContext,
# )
# import pineconeIndex as pineIndex
# from llama_index.node_parser.simple import SimpleNodeParser
# from llama_index import ServiceContext, LLMPredictor
# from llama_index.storage import StorageContext
# from llama_index.vector_stores import PineconeVectorStore
# from llama_index.text_splitter import TokenTextSplitter
# from llama_index.llms import OpenAI


# chunk_size = 1024
# llm = OpenAI(temperature=0, model="gpt-4", streaming=True)
# service_context = ServiceContext.from_defaults(chunk_size=chunk_size, llm=llm)
# text_splitter = TokenTextSplitter(chunk_size=chunk_size)
# node_parser = SimpleNodeParser.from_defaults(text_splitter=text_splitter)


# vector_store = PineconeVectorStore(
#     pinecone_index=pineIndex.pinecone_index, namespace="wiki_cities"
# )
# storage_context = StorageContext.from_defaults(vector_store=vector_store)
# vector_index = VectorStoreIndex([], storage_context=storage_context)



vector_store = PineconeVectorStore(
    pinecone_index=pinecone_index, namespace="wiki_cities"
)
vector_index = VectorStoreIndex([], storage_context=storage_context)
vector_auto_retriever = VectorIndexAutoRetriever(
    vector_index, vector_store_info=vector_store_info
)

# create retriever query engine
retriever_query_engine = RetrieverQueryEngine(
    vector_auto_retriever,
    llm=llm,
    chunk_size=chunk_size,
    node_parser=node_parser,
)
