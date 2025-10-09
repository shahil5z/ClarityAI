# src/generation/answer_generator.py

from typing import List
from langchain.schema import Document
from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()

class AnswerGenerator:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS
        
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            openai_api_key=Config.OPENAI_API_KEY,
            request_timeout=30  # Add timeout to prevent hanging
        )
        
        self.qa_chain = load_qa_chain(self.llm, chain_type="stuff")
    
    def generate_answer(self, question: str, documents: List[Document]) -> str:
        """Generate an answer based on a question and relevant documents."""
        try:
            logger.info(f"Generating answer for question: {question}")
            
            # Use the QA chain with proper parameters
            result = self.qa_chain.run(
                input_documents=documents,
                question=question
            )
            
            logger.info("Answer generated successfully")
            return result
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise