"""Read, Create or delete events from google calendar"""
import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import MutualTLSChannelError

class GoogleCalendar:
    """interact with google calendar services"""
    SERVICE_NAME = 'calendar'
    VERSION = 'v3'
    resource = None

    def __init__(self, calendar_id = None, credential = None):
        self.calendar_id = calendar_id
        try:
            self.resource = build('calendar', 'v3', credentials = credential.content)
        except MutualTLSChannelError as err:
            print(err)

    def get_events_by_title(self, event_title):
        """
        Return all upcoming events with a specific name
        """
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        try:
            events = self.resource.events().list(calendarId=self.calendar_id, timeMin=now,
                                                 q=event_title).execute()
            events = events.get('items', [])
            return events
        except HttpError as err:
            print(err)


    def upcoming_events(self, number_of_events = 10):
        """Return a list of upcoming events"""
        now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
        try:
            events = self.resource.events().list(calendarId=self.calendar_id, timeMin=now,
                                              maxResults=number_of_events, singleEvents=True,
                                              orderBy='startTime').execute()
            events = events.get('items', [])
            return events
        except HttpError as err:
            print(err)

    def add_event(self, event_name, description, start, end, color=1):
        """
        Add a new event to the calendar
        TODO create event dataclass?
        """
        event_body = {
                    'summary': event_name,
                    'description': description,
                    'start': {
                                'dateTime': start,
                                'timeZone': 'CST',    
                            },
                    'end': {
                                'dateTime': end,
                                'timeZone': 'CST',
                            },
                    'colorId':color,
                    'reminders': {
                                    'useDefault': False,
                                    'overrides': [
                                    {'method': 'popup', 'minutes': 24 * 60},
                                    {'method': 'popup', 'minutes': 72 * 60},
                                    ],
                                },
        }
        try:
            event = self.resource.events().insert(calendarId=self.calendar_id, body=event_body).execute()
            print (f"Created '{event_name}': {event.get('htmlLink')}")
        except HttpError as err:
            print(err)

    def delete_event(self, event_id):
        """
        Remove event from Calendar
        """
        ##if (event['summary'] == "event name"):
        self.resource.events().delete(calendarId='primary',eventId=event_id).execute()
