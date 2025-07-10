from flask import Flask, request, jsonify
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Email configuration
SENDER_EMAIL = "akashjoel08@gmail.com"  # Your Gmail address
SENDER_PASSWORD = "your-app-password"   # Replace with your Gmail app password
RECIPIENT_EMAIL = "akashjoel08@gmail.com"  # Your email where you want to receive messages

@app.route('/send-email', methods=['POST'])
def send_email():
    try:
        data = request.get_json(force=True)
        if not data:
            return jsonify({'success': False, 'message': 'No JSON data received'}), 400

        name = data.get('name')
        email = data.get('email')
        message = data.get('message')
        
        if not all([name, email, message]):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Create email content
        subject = f"New Contact Form Message from {name}"
        body = f"""
        Name: {name}
        Email: {email}
        Message: {message}
        """
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = RECIPIENT_EMAIL
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        text = msg.as_string()
        server.sendmail(SENDER_EMAIL, RECIPIENT_EMAIL, text)
        server.quit()
        
        return jsonify({'success': True, 'message': 'Email sent successfully'})
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return jsonify({'success': False, 'message': 'Failed to send email'}), 500

@app.route('/')
def home():
    return "Email server is running!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 