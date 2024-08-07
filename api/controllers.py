from fastapi import APIRouter, Form, Query, Response
from twilio.twiml.voice_response import VoiceResponse, Dial
from api.models import Tenant, Location, TwilioNumber
from api.utils import get_phone, get_logger, send_email_async, get_or_none
from fastapi.responses import JSONResponse
from config import Envs
import time

router = APIRouter()
logger = get_logger()

SUPPORT_EMAIL_1 = Envs.SUPPORT_EMAIL_1
SUPPORT_EMAIL_2 = Envs.SUPPORT_EMAIL_2
SUPPORT_EMAIL_3 = Envs.SUPPORT_EMAIL_3
SUPPORT_EMAIL_4 = Envs.SUPPORT_EMAIL_4


@router.get(
    "/redirect-call",
)
@router.post(
    "/redirect-call",
)
async def redirect_call(From: str = Form(...), CallStatus: str = Form(...),
                        RecordingUrl: str | None = Form(default=None), To: str = Form(...),
                        priority_num: str | None = Query(default=None, max_length=50)) -> Response:
    caller = From
    twilio_phone = To
    logger.info("Caller: %s calling %s.", str(caller), str(twilio_phone))
    response = VoiceResponse()

    if CallStatus == 'completed':
        return await call_end(From, RecordingUrl, To)

    logger.info(f"{From}, {To}, {priority_num}")
    priority_num = int(priority_num or 0)
    phone = await get_phone(priority_num)

    if phone:
        dial = Dial(
            caller_id=twilio_phone,
            record=True,
            timeout=10,
            method='POST',
            action=f"https://{Envs.CURRENT_DOMAIN}/redirect-call?priority_num={priority_num + 1}")

        dial.number(phone.number)
        response.append(dial)
        logger.info("Caller: %s calling %s.", str(caller), str(phone))
        logger.info(f'Calling to {priority_num + 1} number in order {phone}')
    else:
        response.say(
            'Thank you for calling ****. Sorry we missed your call. All our representatives are currently unavailable. Please leave a message and we will call you back shortly.')
        response.record(timeout=15, transcribe=True, action=f"https://{Envs.CURRENT_DOMAIN}'/call-end")
        logger.info(f'Record writen')

    return Response(content=str(response), media_type="application/xml")


@router.get(
    "/call-end",
)
@router.post(
    "/call-end",
)
async def call_end(From: str = Form(...), RecordingUrl: str = Form(...), To: str = Form(...)) -> Response:
    context = {}
    time.sleep(10)

    twilio_phone = To
    location = await get_or_none(
        Location.select().join(TwilioNumber).where(TwilioNumber.number.contains(twilio_phone[2:])))
    context['to'] = twilio_phone
    context['from'] = From
    context['location'] = location
    context['tenant'] = await get_or_none(Tenant.select().where(Tenant.phone.contains(context['from'][2:])))

    recipients = [email for email in [SUPPORT_EMAIL_1, SUPPORT_EMAIL_2, SUPPORT_EMAIL_3, SUPPORT_EMAIL_4] if email]
    context['url'] = RecordingUrl

    await send_email_async(template='record_template.html', subject='New call from the customer', to=recipients,
                           body=context)
    logger.info(f'email was send to {recipients} with recording {RecordingUrl}')
    response = VoiceResponse()
    response.say('Call finished')
    return Response(content=str(response), media_type="application/xml")


@router.get(
    "/ping"
)
async def ping_me() -> JSONResponse:
    return JSONResponse(content={'status': 'OK'})
