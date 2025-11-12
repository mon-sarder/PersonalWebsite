from flask_mail import Message
from config.config import Config

def send_contact_notification(mail, name, email, message):
    """
    Send email notification when someone submits the contact form
    """
    try:
        msg = Message(
            subject=f"New Contact Form Submission from {name}",
            recipients=[Config.ADMIN_EMAIL],
            body=f"""
You have received a new contact form submission:

Name: {name}
Email: {email}

Message:
{message}

---
This is an automated notification from your portfolio website.
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False

def send_confirmation_email(mail, recipient_email, name):
    """
    Send confirmation email to the person who submitted the form
    """
    try:
        msg = Message(
            subject="Thanks for reaching out!",
            recipients=[recipient_email],
            body=f"""
Hi {name},

Thank you for contacting me through my portfolio website. I have received your message and will get back to you soon.

Best regards
            """
        )
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending confirmation email: {e}")
        return False