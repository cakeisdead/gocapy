"""Add, Delete and List google calendar events from Python"""
import json
from credential import Credential
from google_calendar import GoogleCalendar

def load_json(path):
    """Load json file and return contents"""
    with open(path, mode="r", encoding="UTF-8") as file:
        data = json.load(file)
    return data

if __name__ == "__main__":
    #events = load_json("study_guide.json")
    
    # Initialize credentials and calendar object
    creds = Credential()
    calendar = GoogleCalendar('primary', creds)

    # Get upcoming events
    events = calendar.upcoming_events(3)

    if not events:
        print('No upcoming events found.')

    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        ##if (event['summary'] == "event name"):
        ##    service.events().delete(calendarId='primary',eventId=event['id']).execute()
