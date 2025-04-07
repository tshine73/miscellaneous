from datetime import datetime


def format_datetime(dt, fmt="%Y-%m-%d %H:%M:%S"):
    return dt.strftime(fmt)


def iso_timestamp_to_datetime(ts):
    return datetime.fromisoformat(ts)


def parse_string_to_datetime(date_string, fmt="%Y-%m-%d %H:%M:%S"):
    return datetime.strptime(date_string, fmt)
