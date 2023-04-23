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
