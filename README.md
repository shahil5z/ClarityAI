# ClarityAI

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-orange)
![OpenAI](https://img.shields.io/badge/OpenAI-API-blue)
![LangChain](https://img.shields.io/badge/LangChain-RAG-purple)
![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-orange)
![SentenceTransformers](https://img.shields.io/badge/SentenceTransformers-NLP-blue)
![DeepTranslator](https://img.shields.io/badge/DeepTranslator-Translation-green)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Visualization-red)
![Seaborn](https://img.shields.io/badge/Seaborn-Visualization-blue)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-orange)
![WordCloud](https://img.shields.io/badge/WordCloud-Analytics-purple)
![PyPDF](https://img.shields.io/badge/PyPDF-Document-blue)
![python-docx](https://img.shields.io/badge/python--docx-Document-green)
![FPDF2](https://img.shields.io/badge/FPDF2-PDF-orange)
![FAISS](https://img.shields.io/badge/FAISS-VectorDB-purple)
![License](https://img.shields.io/badge/License-MIT-green)

## Project Overview

ClarityAI is an AI-powered document intelligence system that processes, understands, and answers questions about uploaded documents. It combines NLP, RAG (Retrieval-Augmented Generation), and LLM pipelines to provide accurate, context-aware responses. The system supports both English and German languages, making it suitable for global markets, particularly German-speaking regions.

# Table of Contents

1. [Features](#features)
2. [Use Cases](#use-cases)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Screenshots](#screenshots)
6. [Live Demo](#live-demo)
7. [License](#license)

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
-![image alt](https://github.com/shahil5z/ClarityAI/blob/4b414f91ffe4879c10bbec6e95d6f722af75cf16/Sample/1.png)

*The first question is answered in English, while the second question demonstrates AI responding in German.*

3. **Conversation Analytics**  
-![image alt](https://github.com/shahil5z/ClarityAI/blob/4b414f91ffe4879c10bbec6e95d6f722af75cf16/Sample/2.png)

*Shows detailed analytics of Q&A sessions, including trends, response times, and session summaries.*

4. **Word Clouds & General Analytics**  
-![image alt](https://github.com/shahil5z/ClarityAI/blob/4b414f91ffe4879c10bbec6e95d6f722af75cf16/Sample/3.png)

*Displays questions word cloud, answers word cloud, and additional general analytics data for insights.*

## Live Demo

ClarityAI is deployed on Streamlit Cloud for private access.  
Currently, the app is accessible **only to approved users**.

**Demo URL:** [https://clarity-ai.streamlit.app](https://clarity-ai.streamlit.app)

If you’d like to explore the live demo, please **contact me on [LinkedIn](https://www.linkedin.com/in/shohrab-haque/)** and **drop your email** so I can provide you access.

## License

This project is licensed under the MIT License.  
See the [LICENSE](License) file for details.
