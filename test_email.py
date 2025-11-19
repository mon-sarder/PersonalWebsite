from dotenv import load_dotenv
import os
from flask import Flask
from flask_mail import Mail, Message

# Load environment variables
load_dotenv()

# Create Flask app
app = Flask(__name__)
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

with app.app_context():
    msg = Message(
        'Test Email from Portfolio',
        recipients=[os.getenv('ADMIN_EMAIL')]
    )
    msg.body = 'If you receive this, your email configuration is working!'

    try:
        mail.send(msg)
        print("✅ Email sent successfully!")
        print(f"Check {os.getenv('ADMIN_EMAIL')} for the test email.")
    except Exception as e:
        print(f"❌ Error sending email: {e}")