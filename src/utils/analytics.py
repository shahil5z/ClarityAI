# src/utils/analytics.py

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from collections import Counter
import re
from typing import List, Dict, Any
import base64
import io
from datetime import datetime

class ConversationAnalytics:
    def __init__(self):
        self.stop_words = set([
            'the', 'a', 'an', 'and', 'or', 'but', 'if', 'because', 'as', 'until', 'while',
            'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into',
            'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from',
            'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
            'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
            'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
            'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
            'will', 'just', 'don', 'should', 'now', 'what', 'is', 'are', 'was', 'were',
            'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
            'doing', 'would', 'could', 'shall', 'will', 'should', 'may', 'might', 'must'
        ])
    
    def generate_analytics(self, chat_history: List[Dict]) -> Dict[str, Any]:
        """Generate comprehensive analytics from conversation history."""
        if not chat_history:
            return {}
        
        # Extract questions and answers
        questions = []
        answers = []
        
        for msg in chat_history:
            if msg['role'] == 'user':
                # Ensure content is a string
                content = msg['content']
                if isinstance(content, str):
                    questions.append(content)
                elif isinstance(content, (list, tuple)):
                    # If it's a list or tuple, join elements into a string
                    questions.append(' '.join(str(item) for item in content))
                else:
                    # Convert to string if it's another type
                    questions.append(str(content))
            elif msg['role'] == 'assistant':
                # Ensure content is a string
                content = msg['content']
                if isinstance(content, str):
                    answers.append(content)
                elif isinstance(content, (list, tuple)):
                    # If it's a list or tuple, join elements into a string
                    answers.append(' '.join(str(item) for item in content))
                else:
                    # Convert to string if it's another type
                    answers.append(str(content))
        
        # Basic statistics
        stats = {
            'total_questions': len(questions),
            'total_answers': len(answers),
            'avg_question_length': sum(len(q) for q in questions) / len(questions) if questions else 0,
            'avg_answer_length': sum(len(a) for a in answers) / len(answers) if answers else 0,
        }
        
        # Word frequency analysis
        question_words = self._extract_words(questions)
        answer_words = self._extract_words(answers)
        
        # Top keywords
        top_question_keywords = self._get_top_keywords(question_words)
        top_answer_keywords = self._get_top_keywords(answer_words)
        
        # Question complexity
        complexity_scores = [self._calculate_complexity(q) for q in questions]
        avg_complexity = sum(complexity_scores) / len(complexity_scores) if complexity_scores else 0
        
        # Topic analysis
        topics = self._identify_topics(questions)
        
        # Generate word clouds
        question_wordcloud = self._generate_wordcloud(question_words)
        answer_wordcloud = self._generate_wordcloud(answer_words)
        
        # Generate charts
        question_length_chart = self._generate_length_chart(questions, "Question Lengths")
        answer_length_chart = self._generate_length_chart(answers, "Answer Lengths")
        
        return {
            'stats': stats,
            'top_question_keywords': top_question_keywords,
            'top_answer_keywords': top_answer_keywords,
            'avg_complexity': avg_complexity,
            'topics': topics,
            'question_wordcloud': question_wordcloud,
            'answer_wordcloud': answer_wordcloud,
            'question_length_chart': question_length_chart,
            'answer_length_chart': answer_length_chart,
            'complexity_distribution': self._generate_complexity_distribution(complexity_scores)
        }
    
    def _extract_words(self, texts: List[str]) -> List[str]:
        """Extract meaningful words from texts."""
        words = []
        for text in texts:
            # Ensure text is a string
            if not isinstance(text, str):
                text = str(text)
                
            # Clean text: lowercase and remove punctuation
            clean_text = re.sub(r'[^\w\s]', '', text.lower())
            # Split into words and filter out stop words
            words.extend([word for word in clean_text.split() if word not in self.stop_words and len(word) > 2])
        return words
    
    def _get_top_keywords(self, words: List[str], top_n: int = 10) -> List[Dict[str, int]]:
        """Get top keywords with their frequencies."""
        counter = Counter(words)
        return [{"word": word, "count": count} for word, count in counter.most_common(top_n)]
    
    def _calculate_complexity(self, text: str) -> float:
        """Calculate question complexity based on various factors."""
        # Ensure text is a string
        if not isinstance(text, str):
            text = str(text)
            
        # Factors: length, number of question words, complex words
        length_factor = min(len(text.split()) / 20, 1.0)  # Normalize to 0-1
        
        question_words = ["what", "why", "how", "when", "where", "who", "which", "whom", "whose"]
        question_word_count = sum(1 for word in text.lower().split() if word in question_words)
        question_word_factor = min(question_word_count / 3, 1.0)  # Normalize to 0-1
        
        # Complex words (longer than 6 characters)
        complex_words = [word for word in text.split() if len(word) > 6]
        complex_word_factor = min(len(complex_words) / 5, 1.0)  # Normalize to 0-1
        
        # Overall complexity (weighted average)
        complexity = (length_factor * 0.4) + (question_word_factor * 0.3) + (complex_word_factor * 0.3)
        return complexity
    
    def _identify_topics(self, questions: List[str]) -> List[Dict[str, Any]]:
        """Identify main topics from questions."""
        # Simple topic identification based on keywords
        topic_keywords = {
            "Contract": ["contract", "agreement", "clause", "terms", "party", "sign", "legal"],
            "Employment": ["job", "work", "employee", "employer", "salary", "position", "hire"],
            "Technical": ["how", "technical", "system", "process", "method", "technology", "software"],
            "Financial": ["money", "payment", "cost", "price", "financial", "budget", "expense"],
            "Policy": ["policy", "rule", "regulation", "guideline", "procedure", "compliance"],
            "General": []
        }
        
        topic_counts = {topic: 0 for topic in topic_keywords}
        
        for question in questions:
            # Ensure question is a string
            if not isinstance(question, str):
                question = str(question)
                
            words = set(question.lower().split())
            max_count = 0
            best_topic = "General"
            
            for topic, keywords in topic_keywords.items():
                if topic == "General":
                    continue
                count = sum(1 for keyword in keywords if keyword in words)
                if count > max_count:
                    max_count = count
                    best_topic = topic
            
            topic_counts[best_topic] += 1
        
        # Convert to percentage and sort
        total = sum(topic_counts.values())
        topics = [
            {"topic": topic, "percentage": round((count / total) * 100, 1) if total > 0 else 0}
            for topic, count in topic_counts.items()
        ]
        topics.sort(key=lambda x: x["percentage"], reverse=True)
        
        return topics
    
    def _generate_wordcloud(self, words: List[str]) -> str:
        """Generate a word cloud and return as base64 string."""
        if not words:
            return ""
        
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(words))
        
        # Convert to base64
        img_buffer = io.BytesIO()
        wordcloud.to_image().save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        
        return img_str
    
    def _generate_length_chart(self, texts: List[str], title: str) -> str:
        """Generate a length distribution chart and return as base64 string."""
        if not texts:
            return ""
        
        lengths = [len(text.split()) for text in texts]
        
        plt.figure(figsize=(10, 6))
        sns.histplot(lengths, bins=20, kde=True)
        plt.title(title)
        plt.xlabel('Word Count')
        plt.ylabel('Frequency')
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        return img_str
    
    def _generate_complexity_distribution(self, complexity_scores: List[float]) -> str:
        """Generate a complexity distribution chart and return as base64 string."""
        if not complexity_scores:
            return ""
        
        plt.figure(figsize=(10, 6))
        sns.histplot(complexity_scores, bins=10, kde=True)
        plt.title('Question Complexity Distribution')
        plt.xlabel('Complexity Score (0-1)')
        plt.ylabel('Frequency')
        
        # Convert to base64
        img_buffer = io.BytesIO()
        plt.savefig(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_str = base64.b64encode(img_buffer.read()).decode()
        plt.close()
        
        return img_str