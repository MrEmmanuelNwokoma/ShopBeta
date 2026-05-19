from celery_app import celery_app
from src.utils.email_service import EmailService



@celery_app.task(bind=True, name="send_email_task")
def dispatch_email(self, email_list: list, subject: str, template_name: str, context: dict = {}):
    """Celery task to send an email using the EmailService."""
    print("dispact email hit")
    try:
        
        EmailService.send_email(
            email_list=email_list,
            subject=subject,
            template_name=template_name,
            context=context
        )
    except Exception as e:
        print(f"Damn......it failed: {str(e)}")  # ADD str(e) here
        self.retry(exc=e, countdown=5)