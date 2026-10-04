import os

import firebase_admin
from firebase_admin import credentials, messaging
from src.core.pydantic_configuration import config


class FirebaseClient:
    def __init__(self):
        # No credentials file (for example on the demo deploy): stay disabled
        # instead of crashing the whole app at import time.
        self.enabled = False
        path = config.FIREBASE_CREDENTIALS
        if not path or not os.path.isfile(path):
            return

        cred = credentials.Certificate(path)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        self.enabled = True

    async def send_notification(self, token: str, title: str, body: str, data: dict):
        if not self.enabled:
            return None

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data,
            token=token
        )
        try:
            response = messaging.send(message)
            return response
        except messaging.UnregisteredError:
            raise
        except Exception as e:
            raise

firebase_client = FirebaseClient()