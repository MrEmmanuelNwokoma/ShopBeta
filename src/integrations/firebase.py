import asyncio
import logging
import os

import firebase_admin
from firebase_admin import credentials, messaging
from src.core.pydantic_configuration import config

logger = logging.getLogger(__name__)

MAX_TOKENS_PER_CALL = 500  # FCM multicast limit


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

    async def send_notification(
        self,
        tokens: list[str],
        title: str,
        body: str,
        data: dict[str, str],
    ) -> list[str]:
        """Send to many device tokens. Returns the tokens FCM says are dead."""
        if not self.enabled:
            return []

        invalid_tokens: list[str] = []

        for i in range(0, len(tokens), MAX_TOKENS_PER_CALL):
            chunk = tokens[i : i + MAX_TOKENS_PER_CALL]

            message = messaging.MulticastMessage(
                notification=messaging.Notification(title=title, body=body),
                data=data,
                tokens=chunk,
            )

            # firebase-admin is blocking, so run it off the event loop
            response = await asyncio.to_thread(
                messaging.send_each_for_multicast, message
            )

            for token, result in zip(chunk, response.responses):
                if result.success:
                    continue
                if isinstance(
                    result.exception,
                    (messaging.UnregisteredError, messaging.SenderIdMismatchError),
                ):
                    invalid_tokens.append(token)
                else:
                    logger.warning(
                        "FCM send failed for a token: %s", result.exception
                    )

        return invalid_tokens


firebase_client = FirebaseClient()