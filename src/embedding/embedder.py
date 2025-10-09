from typing import List
from langchain.schema import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()

class DocumentEmbedder:
    def __init__(self, model_name: str = None):
        self.model_name = model_name or Config.EMBEDDING_MODEL
        self.embeddings = HuggingFaceEmbeddings(
            model_name=self.model_name,
            model_kwargs={'device': 'cpu'}
        )
    
    def create_vector_store(self, documents: List[Document]) -> FAISS:
        """Create a vector store from a list of documents."""
        try:
            logger.info(f"Creating vector store with {len(documents)} documents")
            vector_store = FAISS.from_documents(documents, self.embeddings)
            logger.info("Vector store created successfully")
            return vector_store
        except Exception as e:
            logger.error(f"Error creating vector store: {str(e)}")
            raise