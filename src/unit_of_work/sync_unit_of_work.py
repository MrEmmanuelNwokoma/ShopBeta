from sqlalchemy.orm import Session
from src.repositories.sync_notification_repo import SyncNotificationRepository
from src.repositories.sync_notification_recipient_repo import SyncNotificationRecipientRepository



class SyncUnitOfWork:
    def __init__(self, session: Session):
        self.session = session

        self.sync_notification_repo = SyncNotificationRepository(session)
        self.sync_notification_recipient_repo = SyncNotificationRecipientRepository(session)

    

    def __enter__(self):
        self.session.begin()
        return self
    
    def __exit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self.session.rollback()
        else:
            self.session.commit()
            