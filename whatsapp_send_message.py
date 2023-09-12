import os
from twilio.rest import Client

# account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
# auth_token = os.environ.get("TWILIO_AUTH_TOKEN")

account_sid = "AC0305409c395cfd34e60562b1d7be4bc3"
auth_token = "f2614fae3b38b3ce41809c7e64ad67e4"

client = Client(account_sid, auth_token)

# Function to send message to WhatsApp
def send_message(message, sender_id):
    try:
        client.messages.create(
            to=sender_id,
            body=message,
            from_='+15595513301'
        )
    except Exception as error:
        print(f'Error at send_message --> {error}')

# send_message("Hey", "+14159673323")

