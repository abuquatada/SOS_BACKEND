from django.test import TestCase
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os




SCOPES = ['https://www.googleapis.com/auth/calendar']
credentials_json = "D:/SOS/sos_2phasepractice/project/interviewer/credentials.json"

def create_google_meet_event():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json, SCOPES)
            creds = flow.run_local_server(port=50450)
            print('\n\n\n',creds,'\n\n\n')
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    
    event = {
        'summary': 'Interview with Candidate',
        'description': 'Interview scheduled with the candidate.',
        'start': {
            'dateTime': '2024-09-05T09:00:00+05:30',
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': '2024-09-05T10:00:00+05:30',
            'timeZone': 'Asia/Kolkata',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'sample123',
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
            }
        },
        'attendees': [
            {'email': 'candidate@example.com'},
        ],
    }

    try:
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        print(f"Meet link: {event['hangoutLink']}")
        return event['hangoutLink']
        # store_meet_link_in_database(event['hangoutLink'])
    except Exception as e:
        print(f"An error occurred: {e}")

def store_meet_link_in_database(meet_link):
    print(f"Storing meet link in database: {meet_link}")
    # Placeholder for database storage logic
    # Example: Save the meet_link to your Django model


##-------------------------------------------------------------------------


