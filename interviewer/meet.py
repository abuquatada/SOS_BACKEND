from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
from datetime import timedelta



SCOPES = ['https://www.googleapis.com/auth/calendar']
credentials_json = "D:/SOS/sos_2phasepractice/project/interviewer/credentials.json"
# credentials_json = "D:/sos_backup/sos_backup/interviewer/credentials_json.json"
token_json = "D:/SOS/sos_2phasepractice/project/interviewer/token.json"

def create_google_meet_event(interview,phase_name):
    print(f'\n\n\n{interview}\n\n\n')
    creds = None
    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_json, SCOPES)
            creds = flow.run_local_server(port=50450)
        with open(token_json, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    event = {
        'summary': f'Interview with Candidate Round - {phase_name}',
        'description': interview["notes"],
        'start': {
            'dateTime': (interview['scheduled_date']+ timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': (interview['scheduled_date']+ timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            'timeZone': 'Asia/Kolkata',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': f"{interview['application_id']}",
                'conferenceSolutionKey': {
                    'type': 'hangoutsMeet'
                },
                'status': {
                    'statusCode': 'success'
                }
            },
        },
    }
    print(f'\n\n\n{event}\n\n\n')
    try:
        event = service.events().insert(calendarId='primary', body=event, conferenceDataVersion=1).execute()
        print(f"Meet link: {event['hangoutLink']}")
        return event['hangoutLink']
    except Exception as e:
        print(f"An error occurred: {e}")


##--------------------------------------------------Google Form-----------------------



SCOPES_ = ['https://www.googleapis.com/auth/forms.body', 'https://www.googleapis.com/auth/forms.responses.readonly']
credentials_json__='D:/SOS/sos_2phasepractice/project/interviewer/service_creds.json'

def google_form(interview_data):
    creds = service_account.Credentials.from_service_account_file(
        credentials_json__, scopes=SCOPES_)
    service = build('forms', 'v1', credentials=creds)

    NEW_FORM = {
        "info": {
            # "title": f"Interview Feedback Form - {interview_data}",
            "title": f"Interview Feedback Form - {interview_data["applicant_name"]}",
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
                }
                },
               { "createItem": {
                    "item": {
                        "title": "Comments",
                        "questionItem": {
                            "question": {
                                "required": True,
                                "textQuestion": {
                                      "paragraph": True
                                    
                                },
                            }
                        },
                    },
                    "location": {"index": 2},
                }
                }
        ]
    }

    result = service.forms().create(body=NEW_FORM).execute()
    form_id = result['formId']
    result_update = service.forms().batchUpdate(formId=form_id, body=NEW_QUESTION).execute()
    # print(f'\n\n\nResult__ - {result_update}\n\n\n')
    # print(f'\n\n\nResult - {result}\n\n\n')
    return result , result_update

# google_form()

def fetch_and_store_responses(google_form_id):
    creds = service_account.Credentials.from_service_account_file(credentials_json__, scopes=SCOPES_)
    service = build('forms', 'v1', credentials=creds)
    # form_id='1YoRZf3CTShDZc6w9fwASqsc_p40nGXjA3hoYOTYM01w'
    form_id=google_form_id
    result = service.forms().responses().list(formId=form_id).execute()
    # print('\n\n\n',f"this is result{result}",'\n\n\n')
    # result = (service.forms().responses().get(formId=form_id, responseId=response_id).execute())
    for response in result.get('responses', []):
        # print('\n\n\n',f'this is reponse{response}','\n\n\n')
        return response
    
# fetch_and_store_responses()    