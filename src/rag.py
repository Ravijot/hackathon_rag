

import faiss
from uuid import uuid4
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document

class RAG:
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

        self.index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello world")))
        
        

        self.vector_store = FAISS(
            embedding_function=self.embeddings,
            index=self.index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )

    def add_data_to_vector_store(self, source, texts, filename, metadata=None):
        try:
            print(f"Vector Store : Source : {source} , Filename : {filename}")
            docs = [Document(page_content=t, metadata={"source": source, "filename": filename}) for t in texts]
            uuids = [str(uuid4()) for _ in range(len(docs))]
            self.vector_store.add_documents(documents=docs, ids=uuids)
            return self.vector_store
        except Exception as e:
            print("Error Occured in Add Data to Vector Store")
            return None
    
    def retrieve_data(self, query, k=2):
        try:
            retriever = self.vector_store.as_retriever(search_type="mmr", search_kwargs={"k": k})
            docs = retriever.invoke(query)
            # print("Docs Retrieved :",docs)
            context = []
            
            for doc in docs:
                dt = {}
                dt["id"] = doc.id
                dt['page_content'] = doc.page_content
                dt['metadata'] = doc.metadata
                context.append(dt)
            # print(context)
            return context
        except Exception as e:
            print("Error Occured in Retrieve Data")
            return []