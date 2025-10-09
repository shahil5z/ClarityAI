import os
import json
from datetime import datetime
from typing import Dict, List

class FeedbackCollector:
    def __init__(self):
        self.feedback_file = os.path.join("data", "feedback.json")
        os.makedirs("data", exist_ok=True)
        
        # Initialize feedback file if it doesn't exist
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, "w") as f:
                json.dump([], f)
    
    def collect_feedback(self, feedback_type: str, question: str, answer: str, sources: List = None):
        """Collect user feedback on AI responses."""
        feedback_data = {
            "timestamp": datetime.now().isoformat(),
            "feedback_type": feedback_type,  # "positive" or "negative"
            "question": question,
            "answer": answer,
            "sources": sources if sources else []
        }
        
        # Load existing feedback
        with open(self.feedback_file, "r") as f:
            feedback_list = json.load(f)
        
        # Add new feedback
        feedback_list.append(feedback_data)
        
        # Save updated feedback
        with open(self.feedback_file, "w") as f:
            json.dump(feedback_list, f, indent=2)
    
    def get_feedback_summary(self) -> Dict:
        """Get a summary of collected feedback."""
        with open(self.feedback_file, "r") as f:
            feedback_list = json.load(f)
        
        total_feedback = len(feedback_list)
        positive_feedback = sum(1 for f in feedback_list if f["feedback_type"] == "positive")
        negative_feedback = total_feedback - positive_feedback
        
        return {
            "total_feedback": total_feedback,
            "positive_feedback": positive_feedback,
            "negative_feedback": negative_feedback,
            "positive_percentage": (positive_feedback / total_feedback * 100) if total_feedback > 0 else 0
        }