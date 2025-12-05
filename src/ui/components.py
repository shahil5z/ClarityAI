# src/ui/components.py

import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
import streamlit as st
import tempfile
from datetime import datetime
import base64
from src.utils.analytics import ConversationAnalytics

def render_chat_history(chat_history):
    """Render the chat history with download options."""
    for i, message in enumerate(chat_history):
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**ClarityAI:** {message['content']}")
            
            # Add download button for AI response
            if st.download_button(
                label="Download Answer",
                data=message['content'],
                file_name=f"clarityai_answer_{i}.txt",
                mime="text/plain",
                key=f"download_{i}"
            ):
                st.success("Answer downloaded!")
            
            # Show source documents
            if "sources" in message and message["sources"]:
                with st.expander("View Source Documents"):
                    for j, doc in enumerate(message["sources"]):
                        st.markdown(f"**Source {j+1}:**")
                        st.write(doc.page_content)
                        st.markdown("---")
            
        st.markdown("---")

def render_document_manager(uploaded_files, remove_file_callback):
    """Render document management section."""
    st.subheader("Document Manager")
    
    if not uploaded_files:
        st.info("No documents uploaded yet.")
        return
    
    # Display uploaded files
    files_df = pd.DataFrame({
        "Filename": [file.name for file in uploaded_files],
        "Size (KB)": [round(file.size / 1024, 2) for file in uploaded_files],
        "Type": [file.name.split('.')[-1].upper() for file in uploaded_files]
    })
    
    st.dataframe(files_df)
    
    # Document removal
    st.subheader("Remove Documents")
    selected_files = st.multiselect(
        "Select documents to remove",
        options=uploaded_files,
        format_func=lambda x: x.name
    )
    
    if st.button("Remove Selected", type="secondary"):
        remove_file_callback(selected_files)
        st.success("Selected documents removed!")

def render_feedback_system():
    """Render feedback system for AI responses."""
    st.subheader("Was this response helpful?")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👍 Yes", key="feedback_yes"):
            st.session_state.feedback = "positive"
            st.success("Thank you for your feedback!")
    
    with col2:
        if st.button("👎 No", key="feedback_no"):
            st.session_state.feedback = "negative"
            st.info("We'll improve based on your feedback.")

def render_export_options(chat_history):
    """Render export options for conversation."""
    st.subheader("Export Conversation")
    
    export_format = st.selectbox(
        "Select export format",
        ["Text", "PDF", "CSV"]
    )
    
    if st.button("Export Conversation"):
        if export_format == "Text":
            export_as_text(chat_history)
        elif export_format == "PDF":
            export_as_pdf(chat_history)
        elif export_format == "CSV":
            export_as_csv(chat_history)

def export_as_text(chat_history):
    """Export conversation as text file."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp:
        with open(tmp.name, "w") as f:
            f.write("ClarityAI Conversation Export\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            for message in chat_history:
                # Ensure content is a string
                content = message['content']
                if not isinstance(content, str):
                    if isinstance(content, (list, tuple)):
                        content = ' '.join(str(item) for item in content)
                    else:
                        content = str(content)
                
                if message["role"] == "user":
                    f.write(f"You: {content}\n\n")
                else:
                    f.write(f"ClarityAI: {content}\n\n")
        
        with open(tmp.name, "rb") as f:
            st.download_button(
                label="Download Text File",
                data=f.read(),
                file_name=f"clarityai_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                mime="text/plain"
            )
        
        os.unlink(tmp.name)

def export_as_pdf(chat_history):
    """Export conversation as PDF file with analytics."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Title
    pdf.cell(200, 10, txt="ClarityAI Conversation Export", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
    pdf.ln(10)
    
    # Conversation
    pdf.set_font("Arial", size=12, style='B')
    pdf.cell(200, 10, txt="Conversation", ln=True)
    pdf.set_font("Arial", size=12)
    
    for message in chat_history:
        # Ensure content is a string
        content = message['content']
        if not isinstance(content, str):
            if isinstance(content, (list, tuple)):
                content = ' '.join(str(item) for item in content)
            else:
                content = str(content)
                
        if message["role"] == "user":
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt=f"You: {content}", ln=True)
            pdf.set_font("Arial", size=12)
        else:
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt="ClarityAI:", ln=True)
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, txt=content)
            pdf.ln(5)
    
    # Analytics Section
    pdf.add_page()
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(200, 10, txt="Conversation Analytics", ln=True, align='C')
    pdf.ln(10)
    
    # Generate analytics
    analytics = ConversationAnalytics()
    analytics_data = analytics.generate_analytics(chat_history)
    
    if analytics_data:
        # Basic Statistics
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Basic Statistics", ln=True)
        pdf.set_font("Arial", size=12)
        
        stats = analytics_data['stats']
        pdf.cell(200, 10, txt=f"Total Questions: {stats['total_questions']}", ln=True)
        pdf.cell(200, 10, txt=f"Total Answers: {stats['total_answers']}", ln=True)
        pdf.cell(200, 10, txt=f"Average Question Length: {stats['avg_question_length']:.2f} characters", ln=True)
        pdf.cell(200, 10, txt=f"Average Answer Length: {stats['avg_answer_length']:.2f} characters", ln=True)
        pdf.cell(200, 10, txt=f"Average Question Complexity: {analytics_data['avg_complexity']:.2f}/1.0", ln=True)
        pdf.ln(10)
        
        # Top Keywords
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Top Keywords in Questions", ln=True)
        pdf.set_font("Arial", size=12)
        
        for item in analytics_data['top_question_keywords']:
            pdf.cell(200, 10, txt=f"{item['word']}: {item['count']} occurrences", ln=True)
        
        pdf.ln(5)
        
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Top Keywords in Answers", ln=True)
        pdf.set_font("Arial", size=12)
        
        for item in analytics_data['top_answer_keywords']:
            pdf.cell(200, 10, txt=f"{item['word']}: {item['count']} occurrences", ln=True)
        
        pdf.ln(10)
        
        # Topic Distribution
        pdf.set_font("Arial", size=12, style='B')
        pdf.cell(200, 10, txt="Topic Distribution", ln=True)
        pdf.set_font("Arial", size=12)
        
        for topic in analytics_data['topics']:
            pdf.cell(200, 10, txt=f"{topic['topic']}: {topic['percentage']}%", ln=True)
        
        # Add charts and word clouds
        if analytics_data['question_wordcloud']:
            pdf.add_page()
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt="Questions Word Cloud", ln=True, align='C')
            pdf.image(_decode_base64(analytics_data['question_wordcloud']), x=10, w=190)
        
        if analytics_data['answer_wordcloud']:
            pdf.add_page()
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt="Answers Word Cloud", ln=True, align='C')
            pdf.image(_decode_base64(analytics_data['answer_wordcloud']), x=10, w=190)
        
        if analytics_data['question_length_chart']:
            pdf.add_page()
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt="Question Length Distribution", ln=True, align='C')
            pdf.image(_decode_base64(analytics_data['question_length_chart']), x=10, w=190)
        
        if analytics_data['answer_length_chart']:
            pdf.add_page()
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt="Answer Length Distribution", ln=True, align='C')
            pdf.image(_decode_base64(analytics_data['answer_length_chart']), x=10, w=190)
        
        if analytics_data['complexity_distribution']:
            pdf.add_page()
            pdf.set_font("Arial", size=12, style='B')
            pdf.cell(200, 10, txt="Question Complexity Distribution", ln=True, align='C')
            pdf.image(_decode_base64(analytics_data['complexity_distribution']), x=10, w=190)
    
    # Save to a temporary file and read as bytes
    temp_path = os.path.join("temp", f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
    os.makedirs("temp", exist_ok=True)
    pdf.output(temp_path)
    
    with open(temp_path, "rb") as f:
        pdf_bytes = f.read()
    
    os.remove(temp_path)
    
    st.download_button(
        label="Download PDF",
        data=pdf_bytes,
        file_name=f"clarityai_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
        mime="application/pdf"
    )

def export_as_csv(chat_history):
    """Export conversation as CSV file."""
    data = []
    for message in chat_history:
        # Ensure content is a string
        content = message['content']
        if not isinstance(content, str):
            if isinstance(content, (list, tuple)):
                content = ' '.join(str(item) for item in content)
            else:
                content = str(content)
        
        data.append({
            "Role": message["role"],
            "Content": content,
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
    
    df = pd.DataFrame(data)
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        df.to_csv(tmp.name, index=False)
        
        with open(tmp.name, "rb") as f:
            st.download_button(
                label="Download CSV",
                data=f.read(),
                file_name=f"clarityai_conversation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
        
        os.unlink(tmp.name)

def _decode_base64(base64_string):
    """Decode a base64 string to binary data."""
    return base64.b64decode(base64_string)

def render_analytics(chat_history):
    """Render enhanced analytics dashboard."""
    st.subheader("Conversation Analytics")
    
    if not chat_history:
        st.info("No conversation data available for analytics.")
        return
    
    # Generate analytics
    analytics = ConversationAnalytics()
    analytics_data = analytics.generate_analytics(chat_history)
    
    if not analytics_data:
        st.info("Not enough data to generate analytics.")
        return
    
    # Basic Statistics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Questions", analytics_data['stats']['total_questions'])
    with col2:
        st.metric("Total Answers", analytics_data['stats']['total_answers'])
    with col3:
        st.metric("Avg. Question Complexity", f"{analytics_data['avg_complexity']:.2f}/1.0")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Avg. Question Length", f"{analytics_data['stats']['avg_question_length']:.2f} chars")
    with col2:
        st.metric("Avg. Answer Length", f"{analytics_data['stats']['avg_answer_length']:.2f} chars")
    
    # Top Keywords
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Top Keywords in Questions")
        keywords_df = pd.DataFrame(analytics_data['top_question_keywords'])
        st.bar_chart(keywords_df.set_index('word'))
    
    with col2:
        st.subheader("Top Keywords in Answers")
        keywords_df = pd.DataFrame(analytics_data['top_answer_keywords'])
        st.bar_chart(keywords_df.set_index('word'))
    
    # Topic Distribution
    st.subheader("Topic Distribution")
    topics_df = pd.DataFrame(analytics_data['topics'])
    st.bar_chart(topics_df.set_index('topic'))
    
    # Word Clouds
    col1, col2 = st.columns(2)
    with col1:
        if analytics_data['question_wordcloud']:
            st.subheader("Questions Word Cloud")
            st.image(f"data:image/png;base64,{analytics_data['question_wordcloud']}")
    
    with col2:
        if analytics_data['answer_wordcloud']:
            st.subheader("Answers Word Cloud")
            st.image(f"data:image/png;base64,{analytics_data['answer_wordcloud']}")
    
    # Length Distributions
    col1, col2 = st.columns(2)
    with col1:
        if analytics_data['question_length_chart']:
            st.subheader("Question Length Distribution")
            st.image(f"data:image/png;base64,{analytics_data['question_length_chart']}")
    
    with col2:
        if analytics_data['answer_length_chart']:
            st.subheader("Answer Length Distribution")
            st.image(f"data:image/png;base64,{analytics_data['answer_length_chart']}")
    
    # Complexity Distribution
    if analytics_data['complexity_distribution']:
        st.subheader("Question Complexity Distribution")
        st.image(f"data:image/png;base64,{analytics_data['complexity_distribution']}")
