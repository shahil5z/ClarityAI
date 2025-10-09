import os
import pandas as pd
from fpdf import FPDF
from datetime import datetime
from typing import List, Dict

class ConversationExporter:
    @staticmethod
    def export_as_text(chat_history: List[Dict]) -> bytes:
        """Export conversation as text file."""
        content = "ClarityAI Conversation Export\n"
        content += f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        for message in chat_history:
            if message["role"] == "user":
                content += f"You: {message['content']}\n\n"
            else:
                content += f"ClarityAI: {message['content']}\n\n"
        
        return content.encode('utf-8')
    
    @staticmethod
    def export_as_pdf(chat_history: List[Dict]) -> bytes:
        """Export conversation as PDF file."""
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        
        pdf.cell(200, 10, txt="ClarityAI Conversation Export", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True, align='C')
        pdf.ln(10)
        
        for message in chat_history:
            if message["role"] == "user":
                pdf.set_font("Arial", size=12, style='B')
                pdf.cell(200, 10, txt=f"You: {message['content']}", ln=True)
                pdf.set_font("Arial", size=12)
            else:
                pdf.set_font("Arial", size=12, style='B')
                pdf.cell(200, 10, txt="ClarityAI:", ln=True)
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=message['content'])
                pdf.ln(5)
        
        # Save to a temporary file and read as bytes
        temp_path = os.path.join("temp", f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf")
        os.makedirs("temp", exist_ok=True)
        pdf.output(temp_path)
        
        with open(temp_path, "rb") as f:
            pdf_bytes = f.read()
        
        os.remove(temp_path)
        return pdf_bytes
    
    @staticmethod
    def export_as_csv(chat_history: List[Dict]) -> bytes:
        """Export conversation as CSV file."""
        data = []
        for message in chat_history:
            data.append({
                "Role": message["role"],
                "Content": message["content"],
                "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        
        df = pd.DataFrame(data)
        return df.to_csv(index=False).encode('utf-8')