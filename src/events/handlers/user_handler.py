from src.events.user_events import UserCreatedEvent
from src.tasks.email_task import dispatch_email



def handle_user_created(event: UserCreatedEvent):
    assert isinstance(event, UserCreatedEvent)
    user = event
    print("I'm here")

    dispatch_email.delay(   
        email_list=[user.email],
        subject="Welcome to ShopBeta!",
        template_name="test_template.html",
        context={"FIRST_NAME": user.first_name, "USER_TOKEN": user.verification_token}
    )


