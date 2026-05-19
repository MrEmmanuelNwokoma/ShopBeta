from jinja2 import Environment, FileSystemLoader
import resend
from src.core.pydantic_configuration import config
import os

resend.api_key = config.RESEND_API_KEY

# Setup Jinja2 environment
template_env = Environment(
    loader=FileSystemLoader(os.path.join(
        os.path.dirname(__file__), "../templates"))
)


class EmailService:
    """Wrapper around Resend API with template support."""

    @staticmethod
    def send_email(email_list: list, subject: str, template_name: str, context: dict = {}):
        template = template_env.get_template(template_name)
        html_body = template.render(**context)

        try:
            resend.Emails.send({
                "from": config.MAIL_FROM,
                "to": email_list,
                "subject": subject,
                "html": html_body,
            })
        except Exception as e:
            print(f"[EmailService] Error sending email: {e}")
            raise