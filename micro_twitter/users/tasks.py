import logging

from micro_twitter.common import utils
from micro_twitter.config.celery import app

logger = logging.getLogger("email_logger")


@app.task(bind=True)
def send_email(self, subject, message, recipient):
    try:
        utils.send_email(subject=subject, message=message, recipient=recipient)
        logger.info(f"Email sent to {recipient} successfully.")
    except Exception:
        logger.exception("[Email Exception]")
