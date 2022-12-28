import time

import schedule

from app.sentry import init_sentry
from tinkoff_to_diadoc import TinkoffToDiadoc


def send_invites_to_diadoc() -> None:
    service = TinkoffToDiadoc()
    service.act()


if __name__ == "__main__":
    init_sentry()

    send_invites_to_diadoc()
    schedule.every().hour.do(send_invites_to_diadoc)

    while True:
        schedule.run_pending()
        time.sleep(1)
