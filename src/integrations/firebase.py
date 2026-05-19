import firebase_admin
from firebase_admin import credentials, messaging
from src.core.pydantic_configuration import config


class FirebaseClient:
    def __init__(self):
        cred = credentials.Certificate(config.FIREBASE_CREDENTIALS)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
    
    async def send_notification(self, token: str, title: str, body: str, data: dict):
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