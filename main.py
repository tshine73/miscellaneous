from datetime import datetime

from tshine73_utils.date_utils import format_datetime


def main():
    current_date_time = format_datetime(datetime.now())
    print(f"current date time is {current_date_time}")

if __name__ == "__main__":
    main()
