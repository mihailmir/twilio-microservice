from fastapi_mail import ConnectionConfig, MessageSchema, FastMail
from peewee_async import AsyncQueryWrapper

from config import Envs
from api.models import SupportPhone, objects
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


def get_logger() -> logging.Logger:
    return logging.getLogger(__name__)


async def send_email_async(template: str, subject: str, to: [str], body: dict) -> None:
    message = MessageSchema(
        subject=subject,
        recipients=to,
        template_body=body,
        subtype='html',
    )

    fm = FastMail(mail_conf)
    await fm.send_message(message, template_name=template, )


def is_time_between(begin_time, end_time, check_time=None) -> bool:
    # If check time is not given, default to current UTC time

    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


async def get_phone(priority_num) -> SupportPhone | None:
    try:
        support_phones = await objects.execute(
            SupportPhone.select().where(SupportPhone.active == True).order_by(SupportPhone.priority).limit(1).offset(
                priority_num - 1))
        return list(support_phones)[0]
    except IndexError:
        return


async def get_or_none(query) -> AsyncQueryWrapper | None:
    try:
        result = await objects.execute(query)
        return list(result)[0]
    except IndexError:
        return
