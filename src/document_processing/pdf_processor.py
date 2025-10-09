import os
from typing import List
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()

class PDFProcessor:
    def __init__(self):
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )
    
    def process_pdf(self, file_path: str) -> List[Document]:
        """Process a PDF file and return a list of document chunks."""
        try:
            logger.info(f"Processing PDF: {file_path}")
            
            # Extract text from PDF
            text = self._extract_text_from_pdf(file_path)
            
            # Split text into chunks
            chunks = self.text_splitter.split_text(text)
            
            # Create documents
            documents = [
                Document(
                    page_content=chunk,
                    metadata={
                        "source": os.path.basename(file_path),
                        "page": i // 10  # Approximate page number
                    }
                )
                for i, chunk in enumerate(chunks)
            ]
            
            logger.info(f"Created {len(documents)} document chunks from {file_path}")
            return documents
            
        except Exception as e:
            logger.error(f"Error processing PDF {file_path}: {str(e)}")
            raise
    
    def _extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from a PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text
        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            raise