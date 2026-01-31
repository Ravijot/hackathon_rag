from src.llm import model
from langchain.prompts import ChatPromptTemplate
from langchain.schema import StrOutputParser

class SummarizeData:
    
    def create_summaries_of_tables(self, tables):
        try:
            # Prompt
            prompt_text = """You are an assistant tasked with summarizing tables. \
            Give a concise summary of the table. Table chunk: {element} """
            prompt = ChatPromptTemplate.from_template(prompt_text)

            # Summary chain
            summarize_chain = {"element": lambda x: x} | prompt | model | StrOutputParser()

            table_summaries = summarize_chain.batch(tables, {"max_concurrency": 5})
            return table_summaries
        except Exception as e:
            print("Error in Table Summary Creation : ",str(e))
            return []
    
    def create_summaries_of_images(self, images):
        try:
            print("Creating summaries for images")
            
            prompt_template = """You are an assistant tasked with summarizing images for retrieval.
                    Remember these images could potentially contain graphs, charts or 
                    tables also.
                    These summaries will be embedded and used to retrieve the raw image 
                    for question answering.
                    Give a detailed summary of the image that is well optimized for 
                    retrieval.
                    Do not add additional words like Summary: etc.
                """
            messages = [
                (
                    "user",
                    [
                        {"type": "text", "text": prompt_template},
                        {
                            "type": "image_url",
                            "image_url": {"url": "data:image/jpeg;base64,{image}"},
                        },
                    ],
                )
            ]

            prompt = ChatPromptTemplate.from_messages(messages)

            chain = prompt | model | StrOutputParser()

            image_summaries = chain.batch(images)
            print("Image Summaries : ",image_summaries)
            return image_summaries
        except Exception as e:
            print("Error in Image Summary Creation : ",str(e))
            return []