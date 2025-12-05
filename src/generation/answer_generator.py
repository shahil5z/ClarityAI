# src/generation/answer_generator.py

from typing import List
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()

class AnswerGenerator:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or Config.MODEL_NAME
        self.temperature = Config.TEMPERATURE
        self.max_tokens = Config.MAX_TOKENS
        
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            api_key=Config.OPENAI_API_KEY,
            timeout=30
        )
        
        # Create prompt template
        self.prompt = ChatPromptTemplate.from_template(
            """Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context: {context}

            Question: {input}
            
            Answer:"""
        )
    
    def generate_answer(self, question: str, documents: List[Document]) -> str:
        """Generate an answer based on a question and relevant documents."""
        try:
            logger.info(f"Generating answer for question: {question}")
            
            # Combine document contents
            context = "\n\n".join([doc.page_content for doc in documents])
            
            # Format prompt with context and question
            formatted_prompt = self.prompt.format(context=context, input=question)
            
            # Generate answer using LLM
            result = self.llm.invoke(formatted_prompt)
            
            # Extract content from response
            if hasattr(result, 'content'):
                answer = result.content
            else:
                answer = str(result)
            
            logger.info("Answer generated successfully")
            return answer
        except Exception as e:
            logger.error(f"Error generating answer: {str(e)}")
            raise
