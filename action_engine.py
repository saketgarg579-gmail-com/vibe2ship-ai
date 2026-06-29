from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

class ActionEngine:
    def __init__(self, user_phone):
        self.sid = os.getenv("TWILIO_ACCOUNT_SID")
        self.token = os.getenv("TWILIO_AUTH_TOKEN")
        self.from_num = os.getenv("TWILIO_PHONE_NUMBER")
        self.to_num = user_phone 
        self.client = Client(self.sid, self.token)

    def format_time_left(self, minutes_left):
        total_seconds = int(round(minutes_left * 60))
        if total_seconds <= 0:
            return "now"
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        
        parts = []
        if hours > 0:
            parts.append(f"{hours} hr{'s' if hours > 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} min{'s' if minutes > 1 else ''}")
        if seconds > 0 or not parts:
            parts.append(f"{seconds} sec{'s' if seconds > 1 else ''}")
        
        if len(parts) == 1:
            return parts[0]
        elif len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        else:
            return f"{parts[0]}, {parts[1]}, and {parts[2]}"

    def send_sms(self, category, minutes_left):
        try:
            time_str = self.format_time_left(minutes_left)
            if category.lower() == 'assignment':
                msg = f"🚨 Vibe2Ship: Your assignment is DUE in {time_str}!"
            elif category.lower() == 'commitment':
                msg = f"🚨 Vibe2Ship: Your commitment is due in {time_str}!"
            else:
                msg = f"🚨 Vibe2Ship: Your {category} starts in {time_str}!"
            
            self.client.messages.create(body=msg, from_=self.from_num, to=self.to_num)
        except Exception as e: print(f"SMS Error: {e}")

    def trigger_phone_call(self, category, minutes_left):
        try:
            time_str = self.format_time_left(minutes_left)
            # Make voice call pronunciation friendlier by expanding abbreviations
            voice_time_str = time_str.replace("hr", "hour").replace("min", "minute").replace("sec", "second")
            if category.lower() == 'assignment':
                msg = f"Alert! Your assignment is due in {voice_time_str}. Finish it now."
            elif category.lower() == 'commitment':
                msg = f"Alert! You have a commitment due in {voice_time_str}."
            else:
                msg = f"Alert! Your {category} is starting in {voice_time_str}."
            
            self.client.calls.create(twiml=f'<Response><Say>{msg}</Say></Response>', to=self.to_num, from_=self.from_num)
        except Exception as e: print(f"Call Error: {e}")

