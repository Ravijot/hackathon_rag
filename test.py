# from src.extraction import ExtractData

# # print(ExtractData().extract_text_from_pdf("data/openai.pdf"))

# tables, images, text = ExtractData().extract_data_from_pdf("data/aadhar.pdf")
# # tables, images, text = ExtractData().extract_data_from_html("data/upi.html")

# # tables, images, text = ExtractData().extract_data_from_markdown("data/README.md")
# print(tables)
# for img in images:
#     print(img[:50])
# print(text)

from src.pipeline import Pipeline
pipeline = Pipeline()
# print(pipeline.process_document("data/aadhar.pdf","pdf"))
print(pipeline.process_document("data/upi.html","html"))
# print("============================================================================================")
# print(pipeline.query("How Unified Payments Interface (UPI) Payment Works in India?"))
# print("============================================================================================")
# print(pipeline.query("List of major UPI apps and their respective sponsor banks"))
# print("============================================================================================")
# print(pipeline.query("Give details of UPI Transaction in December 2019"))
# print("============================================================================================")

# from src.evaluation import Evaluation
# query = "What is the onboarding process?"
# actual_output = "The onboarding process involves several steps including document verification, account setup, and orientation."
# retrieval_context = ["Document verification", "Account setup", "Orientation"]

# evaluator = Evaluation()



# print(evaluator.evaluate_faithfulness(query, actual_output, retrieval_context))