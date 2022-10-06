from pandas import *
import datetime
import calendar
from dateutil.relativedelta import relativedelta


def get_csv_column(filename, column):
    data = read_csv(filename)
    return data[column].tolist()


def week_time(year):
    weektime = []
    ret = []
    loop_day = datetime.datetime.strptime(f"{year}-01-01", "%Y-%m-%d")

    # 52 first weeks
    for i in range(1, 53):
        start = str(loop_day)[:10]
        end = str(loop_day + datetime.timedelta(days=6))[:10]
        ret.append({
            "week": i,
            "after": f"{start}T00:00:00Z",
            "before": f"{end}T23:59:59Z"
        })
        try:
            loop_day = loop_day + datetime.timedelta(days=7)
        except:
            pass
    # last week
    start = str(loop_day)[:10]
    ret.append({
        "week": 53,
        "after": f"{start}T00:00:00Z",
        "before": f"{year}-12-31T23:59:59Z"
    })
    return ret


def year_time(year):
    return {
        "after": f"{year}-01-01T00:00:00Z",
        "before": f"{year}-12-31T23:59:59Z"
    }


def last_two_weeks_time():
    ret = []
    # today = datetime.datetime.strptime(datetime.now(), "%Y-%m-%d")
    for i in range(14):
        date = datetime.datetime.strftime(
            datetime.datetime.now() - datetime.timedelta(days=i), "%Y-%m-%d")
        ret.append({
            'date': datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i), "%d-%m-%y"),
            'date_sorter': int(datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i), "%y"))*10000+
                            int(datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i), "%m"))*100+
                            int(datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=i), "%d")),
            "after": f"{date}T00:00:00Z",
            "before": f"{date}T23:59:59Z"
        })
    return ret[::-1]


if __name__ == "__main__":
    # week_time('2022')
    print(last_two_weeks_time())
