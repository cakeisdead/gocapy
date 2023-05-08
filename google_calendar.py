"""Read, Create or delete events from google calendar"""
import datetime
from dataclasses import dataclass
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.exceptions import MutualTLSChannelError

@dataclass
class Event:
    """Placeholder for an event"""
    name: str
    description: str
    date: str
    start_time: str = "00:00"
    end_time: str = start_time
    time_zone: str = "CST"
    color: int = 8
    """
    (1, Lavender), (2, Sage), (3, Grape), 
    (4, Flamingo), (5, Banana), (6, Tangerine), 
    (7, Peacock), (8, Graphite), (9, Blueberry), 
    (10, Basil), (11, Tomato),
    """
    def body(self):
        """Generate the body of the event"""
        return {
                    'summary': self.name,
                    'description': self.description,
                    'start': {
                                'dateTime': self.date + self.start_time,
                                'timeZone': self.time_zone,    
                            },
                    'end': {
                                'dateTime': self.date + self.end_time,
                                'timeZone': self.time_zone,
                            },
                    'colorId':self.color,
                    'reminders': {
                                    'useDefault': False,
                                    'overrides': [
                                    {'method': 'popup', 'minutes': 24 * 60},
                                    {'method': 'popup', 'minutes': 72 * 60},
                                    ],
                                },
        }

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

    def add_event(self, event):
        """
        Add a new event to the calendar
        """
        try:
            new_event = self.resource.events().insert(
                    calendarId=self.calendar_id,
                    body=event.body()).execute()
            print (f"Created '{event.name}': {new_event.get('htmlLink')}")
        except HttpError as err:
            print(err)

    def delete_event(self, event_id):
        """
        Remove event from Calendar
        """
        ##if (event['summary'] == "event name"):
        self.resource.events().delete(calendarId='primary',eventId=event_id).execute()
