from flask import Flask, request, jsonify
from functions import fetch_subject_info,fetch_sem_info
app = Flask(__name__)

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get request data from Dialogflow
    req = request.get_json(silent=True, force=True)
    
    # Extract the intent name from the request
    intent_name = req.get('queryResult').get('intent').get('displayName')

    # Initialize response
    response = ""

    # Logic to respond to the 'MCA Info' intent
    if intent_name == 'MCA Info':
        response = "MCA is a two-year course focusing on computer applications and software development."
    elif intent_name=="Subject_Info":
        response=fetch_subject_info(req)
    elif intent_name=="Semester_Info":
        response=fetch_sem_info(req)


    return response

if __name__ == '__main__':
    # Run the Flask app on port 5000
    app.run(debug=True, port=5000)
