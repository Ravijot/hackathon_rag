from src.extraction import ExtractData
from src.summary import SummarizeData
from src.rag import RAG
from src.augmentor import Augmentator
from fastapi.responses import JSONResponse
from src.evaluation import Evaluation

class Pipeline:
    
    def __init__(self):
        self.extractor = ExtractData()
        self.summarizer = SummarizeData()
        self.rag = RAG()
        self.augmentor = Augmentator()
        self.eval = Evaluation()

    def process_document(self, file_path, file_type):

        try:
            # Extracting Data from file
            tables, images, texts = [], [], []
            
            source = ""
            if file_type == "pdf":
                print("Starting Extraction for pdf")
                tables, images, texts = self.extractor.extract_data_from_pdf(file_path)
                source = "pdf"
                print("Completed Extraction for pdf")
            elif file_type == "html":
                print("Starting Extraction for html")
                tables, images, texts = self.extractor.extract_data_from_html(file_path)
                
                source = "html"
                print("Completed Extraction for html")
            elif file_type == "md":
                print("Starting Extraction for md")
                tables, images, texts = self.extractor.extract_data_from_md(file_path)
                source = "markdown"
                print("Completed Extraction for md")
            else:
                return JSONResponse(content={"status":"error","message":"File Type not supported"})
            
            
            # Summarizing Data
            print("Start Creating Summary")
            tables_summary = self.summarizer.create_summaries_of_tables(tables)
            print(f"Table Summary : {tables_summary}")
            images_summary = self.summarizer.create_summaries_of_images(images)
            print(f"Images Summary : f{images_summary}")
            print("Summary Generation Part is completed")
            
           
            filename = file_path.split("/")[-1]
            print("Filename : ",filename)
            
            # Adding to Vector Store
            print("Storing text in vector store")
            if len(texts) == 0:
                texts = ["No text data found"]
            else:              
                self.rag.add_data_to_vector_store(f"{source}_texts", texts, filename)
            print("Storing tables in vector store")
            if len(tables_summary) == 0:
                tables_summary = ["No table data found"]
            else:
                self.rag.add_data_to_vector_store(f"{source}_tables", tables_summary, filename)
            print("Storing images summary in vector store")
            if len(images_summary) == 0:
                images_summary = ["No image data found"]
            else:
                self.rag.add_data_to_vector_store(f"{source}_images", images_summary, filename)
            print("Vector Store Completed")

            return JSONResponse(content={"status": "success", "filename": filename})
        except Exception as e:
            return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
    def query(self, query_text, k=2):

        try:
            retrieved_data = self.rag.retrieve_data(query_text, k)
        
            response = self.augmentor.generate_response(retrieved_data, query_text)
            
            if len(retrieved_data) > 0:
                eval_results = self.eval.evaluate(query_text, [doc['page_content'] for doc in retrieved_data], response)
            else:
                eval_results = {
                                    "answer_relevancy": {
                                        "score": "",
                                        "reason": "No retrieve data found"
                                    },
                                    "faithfulness": {
                                        "score": "",
                                        "reason": "No retrieve data found"
                                    }
                                }
            response_dt = {
                "status":"success",
                "query": query_text,
                "retrieved_data": retrieved_data,
                "response": response,
                "evaluation": eval_results
            }

            return response_dt
        
        except Exception as e:
            print(f"Error in Retrieving and Generating response : {str(e)}")
            response_dt = {
                "status":"error",
                "query": query_text,
                "retrieved_data": [],
                "response": "Error in generating response",
                "evaluation":{
                                    "answer_relevancy": {
                                        "score": "",
                                        "reason": "No retrieve data found"
                                    },
                                    "faithfulness": {
                                        "score": "",
                                        "reason": "No retrieve data found"
                                    }
                                }
            }
            return response_dt