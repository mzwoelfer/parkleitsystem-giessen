from datetime import datetime, timezone


def epoch_to_hhmm(epoch_time):
    timestamp = datetime.fromtimestamp(epoch_time, timezone.utc).replace(tzinfo=None)
    return timestamp.isoformat()