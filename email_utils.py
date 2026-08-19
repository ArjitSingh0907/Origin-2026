"""
Sends the "you're registered" confirmation email.
Runs as a FastAPI BackgroundTask so the API response isn't held up
waiting on the SMTP round trip.
"""
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType

from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_STARTTLS=settings.MAIL_STARTTLS,
    MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_confirmation_email(to_email: str, team_name: str, leader_name: str):
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 560px; margin: auto;">
      <h2>You're in, {leader_name}! 🎉</h2>
      <p>Team <b>{team_name}</b> has been successfully registered for
      <b>ORIGIN '26</b>.</p>
      <p>We'll email your team with further instructions, timelines and
      problem statement access closer to the event.</p>
      <p>— Techniki WebDev Team</p>
    </div>
    """
    message = MessageSchema(
        subject="ORIGIN '26 — Registration Confirmed",
        recipients=[to_email],
        body=html,
        subtype=MessageType.html,
    )
    fm = FastMail(conf)
    await fm.send_message(message)