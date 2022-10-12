import settings
from datetime import datetime


def log_msg(msg: str = "") -> None:
    with open(settings.LOGS_FILE, "a") as f:
        txt = f'[{get_curr_timestamp()}] {msg}'
        f.write(txt)


def get_curr_timestamp():
    return datetime.now().strftime(settings.DATE_FORMAT)
