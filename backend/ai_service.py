import os
import json
import re
from dotenv import load_dotenv
import google.generativeai as genai

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
load_dotenv(dotenv_path)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-1.5-flash')

def analyze_comments(comments, video_title):
    if not comments:
        return {
            'summary': 'No comments available for analysis.',
            'sentiment': 'unknown',
            'best_for': 'unknown',
            'exam_ready': False,
            'difficulty': 'unknown',
            'top_insights': []
        }

    comment_texts = "\n".join([f"- {c['text']}" for c in comments[:80]])

    prompt = f"""
You are analyzing YouTube comments for the video: "{video_title}"

Here are the top comments:
{comment_texts}

Based on these comments, provide a JSON response with exactly these fields:
{{
    "summary": "2-3 sentence summary of what viewers think about this video",
    "sentiment": "positive/negative/mixed",
    "best_for": "who this video is best for (e.g., beginners, intermediate learners, exam prep)",
    "exam_ready": true or false (is this good for last minute exam prep based on comments),
    "difficulty": "beginner/intermediate/advanced",
    "top_insights": ["insight 1", "insight 2", "insight 3"]
}}

Return only valid JSON, nothing else.
"""

    response = model.generate_content(prompt)
    text = response.text.strip()
    text = re.sub(r'```json|```', '', text).strip()
    
    try:
        return json.loads(text)
    except:
        return {
            'summary': text[:200],
            'sentiment': 'positive',
            'best_for': 'general audience',
            'exam_ready': False,
            'difficulty': 'intermediate',
            'top_insights': []
        }