import time
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime

def compare_time(time_start=None, time_end=None):
    if time_start == time_end == None:
        return 0
    else:
        if time_start == None:
            time_start = time.gmtime()
            datetime_start = datetime(time_start.tm_year, time_start.tm_mon, time_start.tm_mday, time_start.tm_hour,
                                time_start.tm_min, time_start.tm_sec)

            datetime_end = datetime(time_end.year, time_end.month, time_end.day, time_end.hour,
                                    time_end.minute, time_end.second) #datetime.strptime(time_end, '%Y-%m-%dT%H:%M:%SZ')
        else:
            time_end = time.gmtime()
            datetime_end = datetime(time_end.tm_year, time_end.tm_mon, time_end.tm_mday, time_end.tm_hour,
                                      time_end.tm_min, time_end.tm_sec)

            datetime_start = datetime(time_start.year, time_start.month, time_start.day, time_start.hour,
                                      time_start.minute, time_start.second) #datetime.strptime(time_start, '%Y-%m-%dT%H:%M:%SZ')

        return (datetime_end - datetime_start).total_seconds()


def is_on_time(value_dict, _time):
    # compare value == time of anything in [month, day, hour, minute]
    if value_dict['type'] == 'any':
        return True
    elif value_dict['type'] == 'distance':
        if value_dict['value'] == _time:
            return True
    elif value_dict['type'] == 'range_list':
        if _time in range(value_dict['value'][0], value_dict['value'][1]+1):
            return True
    elif value_dict['type'] == 'value_list':
        if _time in value_dict['value']:
            return True
    return False


def is_run_job(datetime_now, job_dict, index):
    #print datetime_now
    #print job_dict
    time_job_list = ['month', 'day', 'hour', 'minute']
    time_now_list = [datetime_now.month, datetime_now.day, datetime_now.hour, datetime_now.minute]
    if index == len(time_job_list):
        # bypass validation
        return True
    #print time_job_list[index]
    if is_on_time(job_dict[time_job_list[index]], time_now_list[index]):
        # fibonacci
        return is_run_job(datetime_now, job_dict, index+1)
    return False
