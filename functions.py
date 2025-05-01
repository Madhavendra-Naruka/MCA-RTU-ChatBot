from flask import Flask, request, jsonify
import pandas as pd
import re
from utility import extract_int
# Load the subject information from the CSV file
subject_info_df = pd.read_csv("subject_info.csv")

def fetch_subject_info(req):
    # Get the subject entity from the request parameters
    subject = req.get('queryResult').get('parameters').get('subject_entity')


    # Extract the numeric part from the subject and compare with Subject Code's numeric part
    subject_numeric = int(re.search(r'\d+', subject).group())  # Extract numeric part from subject
    description_raw = subject_info_df[subject_info_df['Subject Code'] == subject_numeric]['Description'].values[0]
    # Replace literal '\n' with actual newlines if necessary
    description_raw = description_raw.replace('\\n', '\n')  # Ensure '\n' is interpreted correctly

    # Split and format the description
    description_list = description_raw.split('\n')
    formatted_description = []

    for i, concept in enumerate(description_list, start=1):
        formatted_description.append(f"{i}.) {concept.strip()}")  # Format each concept

    # Construct the rich response
    fulfillment_messages = [{
            "text": {
                "text":["This Subject covers:"]
            }
        }]
    for item in formatted_description:
        fulfillment_messages.append({
            "text": {
                "text": [item]
            }
        })

    return jsonify({
        'fulfillmentMessages': fulfillment_messages
    })


def fetch_sem_info(req):
    sem = req.get('queryResult').get('parameters').get('Semester')[0]

    # Check if the input contains a digit and extract semester number
    contains_digit = any(char.isdigit() for char in sem)
    
    if contains_digit:
        sem = int(re.search(r'\d+', sem).group())
    else:
        
        sem = extract_int(sem)
    if sem not in range(1,5):
        return jsonify({
            'fulfillmentText': 'Please provide a valid semester number (1-4). There are only 4 semesters in MCA offered by RTU.'
        })
    # Fetch subject list for the specified semester
    subject_list = subject_info_df[subject_info_df['Semester'] == sem]['Subject'].tolist()

   # Prepare the fulfillment message with text
    fulfillment_messages = [{
        "text": {
            "text": [f"The Semester {sem} has the following subjects:"]
        }
    }]

    # Prepare quick replies (for Test Console)
    quick_replies = []
    for subject in subject_list:
        quick_replies.append(subject)

    # Prepare chips (for Messenger)
    chips = []
    for subject in subject_list:
        chips.append({"text": subject})

    # Add quick replies for Test Console
    fulfillment_messages.append({
        "quickReplies": {
            "title": "Please choose:",
            "quickReplies": quick_replies
        },
        "platform": "PLATFORM_UNSPECIFIED"  # Test Console platform
    })

    # Add chips for Messenger
    fulfillment_messages.append({
        "payload": {
            "richContent": [
                [
                    {
                        "type": "chips",
                        "options": chips
                    }
                ]
            ]
        },
        "platform": "DIALOGFLOW_MESSENGER"  # Messenger platform
    })

    # Return the full response
    return jsonify({
        'fulfillmentMessages': fulfillment_messages
    })




