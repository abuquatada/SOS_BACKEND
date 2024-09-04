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
    except Exception as e:
        print(f"An error occurred: {e}")


##--------------------------------------------------Google Form-----------------------



SCOPES_ = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms.responses.readonly']
credentials_json__='D:/SOS/sos_2phasepractice/project/interviewer/service_creds.json'

def create_google_form():
    
    creds = service_account.Credentials.from_service_account_file(
        credentials_json__, scopes=SCOPES_)
    service = build('forms', 'v1', credentials=creds)

    NEW_FORM = {
        "info": {
            "title": "Interview Feedback Form",
            "documentTitle":"Feedback",
        }
    }

    NEW_QUESTION = {
        "requests": [
            {
                "createItem": {
                    "item": {
                        "title": "How satisfied were you with the interview process?",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "choiceQuestion": {
                                    "type": "RADIO",
                                    "options": [
                                        {"value": "Very Satisfied"},
                                        {"value": "Satisfied"},
                                        {"value": "Neutral"},
                                        {"value": "Dissatisfied"},
                                        {"value": "Very Dissatisfied"},
                                    ],
                                    "shuffle": True,
                                },
                            }
                        },
                    },
                    "location": {"index": 0},
                },
            },
               { "createItem": {
                    "item": {
                        "title": "Rating",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "scaleQuestion": {
                                        "low": 1,
                                        "high": 10,
                                        "lowLabel": "Worst",
                                        "highLabel": "Excelent"
                                },
                            }
                        },
                    },
                    "location": {"index": 1},
                }}
        ]
    }

    result = service.forms().create(body=NEW_FORM).execute()
    print('\n\n\n',result,'\n\n\n')
    form_id = result['formId']
    service.forms().batchUpdate(formId=form_id, body=NEW_QUESTION).execute()
    
    
    form_link = f"https://docs.google.com/forms/d/{form_id}/viewform"
    print('\n\n\n',form_link,'\n\n\n')


create_google_form()


def fetch_and_store_responses():
    creds = service_account.Credentials.from_service_account_file(credentials_json__, scopes=SCOPES_)
    service = build('forms', 'v1', credentials=creds)
    form_id="1Nr5n1OBP4YFeOOpfNI-UasCqGymK9-WuELUYR-Bmpuo"
    # response_id = "ACYDBNhc1F-n_Dp8dnaaEvf7UI4Yc17lPMkNPo9bngivfRZ8dp8PxnjTcbDqrDzDQ_77I2s"
    result = service.forms().responses().list(formId=form_id).execute()
    # result = (service.forms().responses().get(formId=form_id, responseId=response_id).execute())
    print('\n\n',result,'\n\n')
    for response in result.get('responses', []):
        print('\n\n',response,'\n\n')

fetch_and_store_responses()