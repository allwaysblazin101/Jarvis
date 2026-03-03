from datetime import datetime


def calculate_response_time(last_message_time: datetime, reply_time: datetime):

    if not last_message_time:
        return None

    diff = reply_time - last_message_time

    return diff.total_seconds() / 60