import google.generativeai as genai
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

class AIProcessor:
    def __init__(self):
        self.model_list = []
        self.current_model_index = 0
        self.discover_models()

    def discover_models(self):
        try:
            available = genai.list_models()
            for m in available:
                if 'generateContent' in m.supported_generation_methods:
                    name = m.name.lower()
                    if not any(word in name for word in ['tts', 'image', 'robotics', 'video', 'clip']):
                        self.model_list.append(m.name)
        except Exception as e:
            print(f"Discovery Error: {e}")

    def analyze_email(self, email_content):
        if not self.model_list:
            return {"category": "Promotional", "summary": "No models available", "deadline": None, "link": None}

        prompt = f"""
        Analyze this email. Return a JSON object. 
        The key for the type MUST be 'category'.
        Classify as 'Promotional', 'Assignment', 'Meeting', 'Interview', or 'Commitment'.
        
        A 'Commitment' is when the user or someone else promises to do something by a specific date.
        
        If it is an 'Assignment', provide 'study_pointers': 3 key research terms.
        
        Extract:
        - category: (Assignment, Meeting, Interview, or Commitment)
        - summary: 1-sentence summary.
        - deadline: Date and time (ISO format).
        - link: URL (if any).
        - company: Organization name (if any).
        - subject: Main topic.
        
        Email Content: {email_content}
        """

        attempts = 0
        while attempts < len(self.model_list):
            try:
                model = genai.GenerativeModel(self.model_list[self.current_model_index])
                response = model.generate_content(prompt)
                text = response.text.strip()
                start_idx, end_idx = text.find('{'), text.rfind('}')
                if start_idx != -1 and end_idx != -1:
                    raw_data = json.loads(text[start_idx:end_idx+1])
                    normalized = {k.lower(): v for k, v in raw_data.items()}
                    if 'classification' in normalized: normalized['category'] = normalized['classification']
                    for key in ['category', 'summary', 'deadline', 'link']:
                        if key not in normalized: normalized[key] = None
                    return normalized
                else: raise ValueError("No JSON")
            except Exception as e:
                if "429" in str(e):
                    self.current_model_index = (self.current_model_index + 1) % len(self.model_list)
                    attempts += 1
                    time.sleep(0.5)
                else: break
        return {"category": "Promotional", "summary": "Error", "deadline": None, "link": None}
