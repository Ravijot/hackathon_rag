from src.llm import model
from langchain_core.prompts import PromptTemplate

class Augmentator:
    
    def generate_response(self, retrieved_data, query):
        
        try:
            combined_data = ""
            for data in retrieved_data:
                combined_data += str(data["page_content"])
                
                combined_data += "\n"
            
            context = combined_data
            
            prompt = PromptTemplate(
                        input_variables=["context","query"],
                        template="You are an assistant that helps people find information.Use the following pieces of context to answer the question at the end. If you don'thave the context, just say that you don't know, don't try to make up an answer.\n{context}\nQuestion: {query}\nAnswer:",
                    )
            
            
            # response_chain = {"context": lambda x: x, "query": lambda x: x} | model
            response_chain = prompt | model
            
            response = response_chain.invoke({"context": context, "query": query})
            return response.content
        except Exception as e:
            print(f"Error in Generating Response : {str(e)}")
            return "Error in generating Response"