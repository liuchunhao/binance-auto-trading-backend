import datetime
import time

def render_epoch_time(epoch_time: int, format='%Y-%m-%d %H:%M:%S')->str:
    epoch_time = epoch_time // 1000  # convert miliseconds to seconds
    human_time = datetime.datetime.fromtimestamp(epoch_time).strftime(format)
    return human_time

def date_to_epoch(date: datetime.datetime)->int:
    return int(time.mktime(date.timetuple()) * 1000)

def get_days_ago(days: int=1)->datetime.datetime:
    date = datetime.datetime.now() - datetime.timedelta(days=days)
    return date

def get_day_count(start: datetime.datetime, end: datetime.datetime)->int:
    return (end - start).days   

def epoch_to_date(epoch: str)->datetime.datetime:
    return datetime.datetime.fromtimestamp(int(epoch) / 1000)
