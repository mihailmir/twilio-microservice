from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from config import Envs
from api.models import SupportPhone
import logging


mail_conf = ConnectionConfig(
    MAIL_USERNAME=Envs.EMAIL_HOST_USER,
    MAIL_PASSWORD=Envs.EMAIL_HOST_PASSWORD,
    MAIL_FROM=Envs.EMAIL_FROM,
    MAIL_PORT=Envs.EMAIL_PORT,
    MAIL_SERVER=Envs.EMAIL_HOST,
    MAIL_FROM_NAME=Envs.EMAIL_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    TEMPLATE_FOLDER='templates'
)


def get_logger():
    return logging.getLogger(__name__)


async def send_email_async(template: str, subject: str, to: [str], body: dict):
    message = MessageSchema(
        subject=subject,
        recipients=to,
        template_body=body,
        subtype='html',
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message, template_name=template, )


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current UTC time

    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def get_phone(priority_num):
    phones = []
    support_phones = SupportPhone.select().order_by(SupportPhone.priority).where(SupportPhone.active == True)
    for phone in support_phones:
        phones.append(phone)
    try:
        phone = phones[priority_num]
    except IndexError:
        return None
    return phone