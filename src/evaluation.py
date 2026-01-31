
from deepeval import evaluate
from deepeval.metrics import AnswerRelevancyMetric
from deepeval.metrics import ContextualRecallMetric
from deepeval.test_case import LLMTestCase
from deepeval.metrics import ContextualRelevancyMetric
from deepeval.metrics import FaithfulnessMetric
from src.llm import model
from deepeval.models.base_model import DeepEvalBaseLLM
from langchain_openai import ChatOpenAI


class CustomDeepEvalModel(DeepEvalBaseLLM):
    def __init__(self, model: ChatOpenAI):
        self.model = model

    def load_model(self):
        return self.model

    def generate(self, prompt: str) -> str:
        """Generate text from the model given a prompt string."""
        response = self.model.invoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    async def a_generate(self, prompt: str) -> str:
        """Asynchronous generation"""
        response = await self.model.ainvoke(prompt)
        return response.content if hasattr(response, "content") else str(response)

    def get_model_name(self) -> str:
        """Return the underlying model name"""
        return self.model.model_name


class Evaluation:
    
    def __init__(self):
        
        self.model = CustomDeepEvalModel(model)
        
        self.answer_relevancy_metric = AnswerRelevancyMetric(threshold=0.7,model=self.model,include_reason=True)

        self.faithfulness_metric = FaithfulnessMetric(threshold=0.7,model=self.model,include_reason=True)

    def evaluate(self, query, retrieval_context, actual_output):
        try:
            test_case = LLMTestCase(
            input=query,
            retrieval_context=retrieval_context,
            actual_output=actual_output
            )
            self.answer_relevancy_metric.measure(test_case)
            self.faithfulness_metric.measure(test_case)
            return {
                "answer_relevancy": {
                    "score": self.answer_relevancy_metric.score,
                    "reason": self.answer_relevancy_metric.reason
                },
                "faithfulness": {
                    "score": self.faithfulness_metric.score,
                    "reason": self.faithfulness_metric.reason
                }
            }
        except Exception as e:
            print(f"Error in Evaluation : {str(e)}")
            return {
                                    "answer_relevancy": {
                                        "score": "",
                                        "reason": "No retrieve data found"
                                    },
                                    "faithfulness": {
                                        "score": "",
                                        "reason": "No retrieve data found"
                                    }
                                }
