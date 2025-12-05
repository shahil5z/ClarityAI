from typing import List
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()

class DocumentRetriever:
    def __init__(self, vector_store: FAISS):
        self.vector_store = vector_store
        self.k = Config.MAX_TOKENS // 100  # Retrieve enough documents to fill context
    
    def get_relevant_documents(self, query: str) -> List[Document]:
        """Retrieve relevant documents based on a query."""
        try:
            logger.info(f"Retrieving documents for query: {query}")
            docs = self.vector_store.similarity_search(query, k=self.k)
            logger.info(f"Retrieved {len(docs)} documents")
            return docs
        except Exception as e:
            logger.error(f"Error retrieving documents: {str(e)}")
            raise
