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

    # Get events by name
    events = calendar.get_events_by_title("Web Development")
    for event in events:
        print(event)
        # delete events
        # calendar.delete_event(event['id'])
    

    # Add events from json file
    events = load_json("study_calendar.json")
    for event in events:
        # Map columns from file into corresponding variables
        name = event["course"]
        description = event["course"]
        start = event["date"] + "T" + event["start_time"] + ":00.000"
        end = event["date"] + "T" + event["end_time"] + ":00.000"
        # calendar.add_event(name, description, start, end, 6)

    ##if (event['summary'] == "event name"):
    ##    service.events().delete(calendarId='primary',eventId=event['id']).execute()
