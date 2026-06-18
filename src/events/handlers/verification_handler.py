from src.events.verification_event import VerificationRequestedEvent
from src.tasks.email_task import dispatch_email

def handle_verification_token_created(event: VerificationRequestedEvent):
    assert isinstance(event, VerificationRequestedEvent)
    user = event
    

    dispatch_email.delay(   
        email_list=[user.email],
        subject="Verification Token Sent!!",
        template_name="test_template.html",
        context={"FIRST_NAME": user.first_name, "USER_TOKEN": user.verification_token}
    )