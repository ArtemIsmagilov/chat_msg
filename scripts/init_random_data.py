import random
from datetime import datetime, timedelta

from utils import get_session
from models import Chat, Message


def main():
    def random_datetime_between(start_date, end_date):
        delta = end_date - start_date
        int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
        random_second = random.randrange(int_delta)
        return start_date + timedelta(seconds=random_second)

    d1 = datetime.strptime("1/1/2023 1:00 AM", "%m/%d/%Y %I:%M %p")
    d2 = datetime.strptime("1/1/2024 1:00 AM", "%m/%d/%Y %I:%M %p")

    with get_session() as s:
        buf = []
        for i in range(10):
            ch = Chat(title=f"chat {i}", created_at=random_datetime_between(d1, d2))
            msgs = [
                Message(
                    chat_id=ch.id,
                    text=f"text {j}",
                    created_at=random_datetime_between(d1, d2),
                )
                for j in range(50)
            ]
            ch.messages = msgs
            buf.append(ch)
        s.add_all(buf)
        s.commit()
    print("finish random data")


if __name__ == "__main__":
    main()
