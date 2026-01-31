import base64
import os
import requests
import logging
from unstructured.partition.pdf import partition_pdf
from unstructured.partition.html import partition_html
from unstructured.partition.md import partition_md
from unstructured.chunking.title import chunk_by_title


class ExtractData:
    
    def extract_data_from_pdf(self, pdf_path):
        
        try:
            
            elements = partition_pdf(
                        filename=pdf_path,                  # mandatory
                        strategy="hi_res",
                        extract_images_in_pdf=True,                            # mandatory to set as ``True``
                        extract_image_block_types=["Image"],          # optional
                        extract_image_block_to_payload=True,    
                        infer_table_structure=True,# optional
                        #extract_image_block_output_dir=f"data/{folder_name}/",  # optional - only works when ``extract_image_block_to_payload=False``
                        languages=["eng"],                           # optional
                        )
            
            chunks = chunk_by_title(elements, max_characters=4000, overlap=200)

            images = []
            tables = []
            texts = []
            for chunk in chunks:
                if "CompositeElement" in str(type(chunk)):
                    texts.append(chunk.text)
                    chunk_els = chunk.metadata.orig_elements
                    for el in chunk_els:
                        if "Image" in str(type(el)):
                            images.append(el.metadata.image_base64)
                        elif "Table" in str(type(el)):
                            tables.append(el.metadata.text_as_html)


            return tables, images, texts
            
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return [], [], []
    
    def extract_data_from_html(self, html_path):
        try:
            elements = partition_html(
                                filename=html_path,                  # mandatory
                                extract_image_block_to_payload=True,
                                extract_image_block_types=["Image"],
                                infer_table_structure=True,)
            chunks = chunk_by_title(elements, max_characters=4000, overlap=200)
            tables = []
            images_url = []
            texts = []
            for chunk in chunks:
                if "CompositeElement" in str(type(chunk)):
                    texts.append(chunk.text)
                    chunk_els = chunk.metadata.orig_elements
                    for el in chunk_els:
                        if "Image" in str(type(el)):
                            images_url.append(el.metadata.image_url)
                        elif "Table" in str(type(el)):
                            tables.append(el.metadata.text_as_html)
            allowed_urls_endswith = ['.png', '.jpeg', '.gif', '.webp'] 
            images_url = [url for url in images_url if any(url.lower().endswith(ext) for ext in allowed_urls_endswith)]
            for url in images_url:
                print(url)
            images = self.urls_to_base64(images_url)
            images = [img for img in images if img not in ["", None]]
            
            return tables, images, texts
        except Exception as e:
            print(f"Error in Extraction of HTML : {str(e)}")
            return [], [], []
                
    def extract_data_from_md(self, md_path):
        try:
            
            
            elements = partition_md(filename=md_path)
            chunks = chunk_by_title(elements, max_characters=4000, overlap=200)

            html = []
            texts = []
            images = []
            for chunk in chunks:
                if "CompositeElement" in str(type(chunk)):
                    texts.append(chunk.text)
                    chunk_els = chunk.metadata.orig_elements
                    for el in chunk_els:
                        if "Image" in str(type(el)):
                            images.append(el.metadata.image_url)
                        elif "Table" in str(type(el)):
                            html.append(el.metadata.text_as_html)
            
            images = self.urls_to_base64(images)
            images = [img for img in images if img not in ["", None]]
            return html, images, texts
        except Exception as e:
            print(f"Error in Extraction of MD : {str(e)}")
            return [], [], []
        
    def urls_to_base64(self, urls):
        """Fetch images from a list of URLs and convert them to base64."""
        results = []
        print("Fetching Images")
        for url in urls:
            try:
                response = requests.get(url)
                response.raise_for_status()
                encoded = base64.b64encode(response.content).decode("utf-8")
                results.append(encoded)
            except Exception as e:
                results.append("")
        print("Image Fetch Completed")
        return results