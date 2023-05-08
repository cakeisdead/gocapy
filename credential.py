"""Credentials for google calendar interactions"""
import os.path

from google.auth.transport.requests import Request
from google.auth.exceptions import TransportError
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

class Credential:
    """Credential class"""
    TOKEN_PATH = "token.json"
    SECRET_PATH = "owo.json"
    SCOPES = [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/calendar.events'
        ]
    content = None

    def __init__(self):
        self.load_token(self.TOKEN_PATH)

    def load_token(self, token_path):
        """Checks if token already exists,
        Token contains user's access and refresh tokens
        and is created automatically after
        completing authorization flow for the first time
        """
        if os.path.exists(token_path):
            self.content = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        else:
            self.generate_token(self.SECRET_PATH, token_path)
            return

        if self.token_validation() == "failed":
            self.generate_token(self.SECRET_PATH, token_path)

    def token_validation(self):
        """
        Check for token validity and refresh if possible
        """
        validation_result = "success"
        if self.content is not None or not self.content.valid:
            if self.content and self.content.expired and self.content.refresh_token:
                try:
                    self.refresh_token()
                except TransportError:
                    validation_result = "failed"

        return validation_result

    def refresh_token(self):
        """
        Refresh token
        """
        self.content.refresh(Request())

    def generate_token(self, secret_path, token_path):
        """
        Generate token when missing or expired
        """
        flow = InstalledAppFlow.from_client_secrets_file(secret_path, self.SCOPES)
        self.content = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_path, 'w', encoding="utf8") as token:
            token.write(self.content.to_json())
