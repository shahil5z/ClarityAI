# ClarityAI

## Project Overview

ClarityAI is an AI-powered document intelligence system that processes, understands, and answers questions about uploaded documents. It combines NLP, RAG (Retrieval-Augmented Generation), and LLM pipelines to provide accurate, context-aware responses. The system supports both English and German languages, making it suitable for global markets, particularly German-speaking regions.

# Table of Contents

1. [Features](#features)
2. [Use Cases](#use-cases)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Screenshots](#screenshots)
6. [License](#license)

## Features

* Document Processing: Supports PDF and Word document processing with advanced text extraction
* Intelligent Q&A: Ask questions about document content and receive accurate answers
* Multilingual Support: Full support for English and German languages, including automatic translation
* Document Management: Upload, view, and manage multiple documents
* Conversation History: Maintain a complete history of questions and answers
* Export Capabilities: Export conversations in Text, PDF, or CSV formats
* Analytics Dashboard: Comprehensive analysis of Q&A sessions with visualizations
* Feedback System: Rate AI responses to help improve system performance
* Advanced Settings: Fine-tune AI parameters for customized responses

## Use Cases

* LegalTech: Contract analysis, legal research, compliance checking, document summarization
* HRTech: Resume processing, candidate matching, HR policy analysis, employee onboarding
* EdTech: Educational content analysis, student support, research assistance, study guide generation

## Technology Stack

* Core: Python, Streamlit, OpenAI API, LangChain
* NLP/AI: Hugging Face Transformers, Sentence Transformers, Deep Translator
* Data Visualization: Matplotlib, Seaborn, WordCloud, Plotly
* Document Processing: PyPDF, python-docx, FPDF2
* Vector Database: FAISS

## Project Structure

```
ClarityAI/
├── src/
│   ├── document_processing/    # Document extraction and processing
│   ├── embedding/            # Text embedding and vector storage
│   ├── retrieval/            # Document retrieval and similarity search
│   ├── generation/           # Answer generation using LLMs
│   ├── translation/          # Multilingual translation capabilities
│   ├── utils/                # Configuration and utility functions
│   └── ui/                   # User interface components
├── tests/                    # Test files
├── temp/                     # Temporary file storage
├── .env                      # Environment variables
└── requirements.txt          # Project dependencies
```

## Screenshots

Here are some screenshots demonstrating ClarityAI in action:

1. **Q&A Interface**  
![Q&A Screenshot](path/to/qa_screenshot.png)  
*The first question is answered in English, while the second question demonstrates AI responding in German.*

2. **Conversation Analytics**  
![Analytics Screenshot](path/to/analytics_screenshot.png)  
*Shows detailed analytics of Q&A sessions, including trends, response times, and session summaries.*

3. **Word Clouds & General Analytics**  
![Word Clouds Screenshot](path/to/wordclouds_screenshot.png)  
*Displays questions word cloud, answers word cloud, and additional general analytics data for insights.*


## License

This project is licensed under the MIT License.  
See the [LICENSE](LICENSE) file for details.