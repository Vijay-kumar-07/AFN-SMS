import os
from flask import Flask, request, jsonify
from whatsapp_send_message import send_message
from db2 import db2_instance, update_status,update_status_no
from datetime import datetime
import re
from dateutil import parser
from dateutil.relativedelta import relativedelta


app = Flask(__name__)

def check_follow_up_dates():
    userphone_data = db2_instance()["data"]
    today = datetime.now().date()
    for entry in userphone_data:
        follow_up_date = entry["NEXT_FOLLOWUP_DATE"]
        name = entry["PROSPECT_NAME"]
        userphone = entry["PROSPECT_PHONE"]
        last_date = entry["LAST_INTERACTION_DATE"]
        csr_name = entry["CSR_NAME"]
        case_desc = entry["CASE_DESCRIPTION"]
        
        if follow_up_date == today:
            send_message(f"Hey {name}! Our CSR Agent {csr_name} last interacted with you on {last_date}. We are following up to check if there is an update on the status of your existing loan. Last updated status is '{case_desc}'. \n\n Please confirm if you have closed the existing loan(Y/N):", userphone)     
    else:
        return 'Message Sent to All Users', 200



# Server Port
PORT = os.environ.get("PORT", 3000)

# Home route
@app.route('/')
def home():
    return check_follow_up_dates()

# Define a function to check and send messages

no_pattern = r'\b(?:no(?:pe)?|not\syet?|n|nah)\b'
yes_pattern = r'\b(?:yes|yeah|yup|y|yes\si\sdid|yes\sit\sis)\b'
followup_pattern = r'after (\d+) (day|days|month|months|week|weeks)'
never_pattern = r'never'
# Route for WhatsApp
@app.route('/whatsapp', methods=['POST'])
def whatsapp():
    message = request.form.get("Body")
    sender_id = request.form.get("From")
    no_matches = re.findall(no_pattern, message.lower())
    yes_matches = re.findall(yes_pattern, message.lower())
    follow_up_match = re.search(followup_pattern, message.lower())
    never_match = re.search(never_pattern, message.lower())
    if message.lower() in no_matches: 
        send_message("Thank you for your response.\n\n Do you want us to follow up after few days? You can say 'after 10 days or' 'after 3 weeks'.", sender_id)
        # update_status(sender_id, 'No')
    elif message.lower() in yes_matches:
        send_message('Thank you, your response has been saved,', sender_id)
        update_status(sender_id, 'Yes')
    elif never_match:
        send_message('Thank you, your response has been saved.', sender_id)
        update_status_no(sender_id, 'No','3000-01-01')
    elif follow_up_match:
        # Extract the number of days or months
        quantity = int(follow_up_match.group(1))
        unit = follow_up_match.group(2)
        # Calculate the follow-up date based on the user's request
        today = datetime.now().date()
        if unit == "day" or unit == "days":
            follow_up_date = today + relativedelta(days=quantity)
        elif unit == "month" or unit == "months":
            follow_up_date = today + relativedelta(months=quantity)
        elif unit == "week" or unit == "weeks":
            follow_up_date = today + relativedelta(weeks=quantity)
        # Format the follow-up date as a string
        formatted_follow_up_date = follow_up_date.strftime('%Y-%m-%d')
        # Send a confirmation message to the user
        send_message(f"Great! We will follow up on {formatted_follow_up_date}.", sender_id)
        update_status_no(sender_id, 'No',formatted_follow_up_date)
    else:
        send_message("Please enter a valid response", sender_id)
    return jsonify({"msg": message}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=PORT)
