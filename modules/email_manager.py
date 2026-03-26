import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class EmailManager:
    """Manages sending emails using SMTP."""
    
    def __init__(self):
        self.email_address = os.environ.get("EMAIL_ADDRESS")
        self.email_password = os.environ.get("EMAIL_PASSWORD")
        self.smtp_server = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", 587))
        
        # Simple lookup table for names to emails (can be expanded to a DB)
        self.contacts = {
            "john": "john.doe@example.com",
            "sarah": "sarah.smith@example.com",
            "boss": "manager@example.com"
        }

    def is_configured(self):
        return bool(self.email_address and self.email_password)

    def extract_recipient_and_message(self, command: str) -> tuple[str, str]:
        """Extracts recipient name and message body from command."""
        # Simple extraction: "email [name] that [message]" or "send email to [name] saying [message]"
        command = command.lower().replace('send an email', '').replace('send email', '').replace('email', '').strip()
        
        # e.g. "to sarah saying hello" or "sarah that i will be late"
        words = command.split()
        if not words:
            return "", ""
        
        if words[0] == 'to':
            words.pop(0)
            
        if not words:
            return "", ""
            
        name = words[0]
        words.pop(0)
        
        if words and words[0] in ['saying', 'that', 'about']:
            words.pop(0)
            
        message = " ".join(words).strip()
        return name, message

    def send_email(self, command: str) -> str:
        """Parses the command and sends an email."""
        name, message = self.extract_recipient_and_message(command)
        
        if not name:
            return "Who would you like me to email?"
            
        if not message:
            return f"What would you like me to say in the email to {name.title()}?"
            
        recipient_email = self.contacts.get(name.lower(), f"{name.lower()}@example.com")
        
        if not self.is_configured():
            # Mock mode for presentation
            return f"📧 [MOCK] Sent email to {name.title()} ({recipient_email}) saying: '{message}'\n*(Configure .env to send real emails)*"
            
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_address
            msg['To'] = recipient_email
            msg['Subject'] = "Message from Jarvis"
            
            msg.attach(MIMEText(message, 'plain'))
            
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_address, self.email_password)
            server.send_message(msg)
            server.quit()
            
            return f"📧 Successfully sent email to {name.title()} ({recipient_email})."
            
        except Exception as e:
            return f"❌ Failed to send email: {str(e)}"

email_manager = EmailManager()
