import imaplib
import email
from email.header import decode_header
import PyPDF2
import io

class EmailManager:
    def __init__(self, user, password):
        self.user = user
        self.password = password

    def extract_pdf_text(self, pdf_bytes):
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
            text = ""
            for i in range(min(len(pdf_reader.pages), 3)): # Read first 3 pages
                text += pdf_reader.pages[i].extract_text() + "\n"
            return text
        except Exception as e:
            print(f"PDF Error: {e}")
            return ""

    def fetch_unread_emails(self):
        emails_data = []
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.user, self.password)
            mail.select("inbox")
            status, messages = mail.search(None, 'UNSEEN')
            
            if not messages[0]: return []

            for num in messages[0].split():
                status, data = mail.fetch(num, '(RFC822)')
                for response_part in data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        subject = decode_header(msg["Subject"])[0][0]
                        if isinstance(subject, bytes): subject = subject.decode()
                        
                        body = ""
                        attachment_text = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                content_type = part.get_content_type()
                                if content_type == "text/plain":
                                    payload = part.get_payload(decode=True)
                                    if payload: body = payload.decode(errors='ignore')
                                elif content_type == "application/pdf":
                                    pdf_bytes = part.get_payload(decode=True)
                                    attachment_text += self.extract_pdf_text(pdf_bytes)
                        else:
                            payload = msg.get_payload(decode=True)
                            if payload: body = payload.decode(errors='ignore')
                        
                        # Combine everything for the AI to analyze
                        full_content = f"Subject: {subject}\nBody: {body}\nPDF Content: {attachment_text}"
                        emails_data.append({"subject": subject, "body": full_content})
            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Email Error: {e}")
        return emails_data
