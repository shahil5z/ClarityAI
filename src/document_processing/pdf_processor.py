import os
from typing import List
from pypdf import PdfReader

# UPDATED IMPORTS FOR NEW LANGCHAIN VERSIONS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.schema import Document

from src.utils.config import Config
from src.utils.logger import setup_logger

logger = setup_logger()


class PDFProcessor:
    def __init__(self):
        self.chunk_size = Config.CHUNK_SIZE
        self.chunk_overlap = Config.CHUNK_OVERLAP

        # Updated splitter initialization
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap
        )

    def process_pdf(self, file_path: str) -> List[Document]:
        """Process a PDF file and return a list of document chunks."""
        try:
            logger.info(f"Processing PDF: {file_path}")

            # Extract text
            text = self._extract_text_from_pdf(file_path)

            # Split into chunks
            chunks = self.text_splitter.split_text(text)

            # Convert chunks to LangChain Document objects
            documents = [
                Document(
                    page_content=chunk,
                    metadata={
                        "source": os.path.basename(file_path),
                        "page": i // 10   # rough page estimate
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
        """Extract raw text from a PDF file."""
        try:
            reader = PdfReader(file_path)
            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text

        except Exception as e:
            logger.error(f"Error extracting text from PDF {file_path}: {str(e)}")
            raise
