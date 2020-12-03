def convert_to_24_hour_time(t):
    if t[-2:]=='pm':
        splits=t.split(":")
        hour=splits[0]
        splits[0]=str(int(hour)+12) if not int(hour)==12 else "0"
        t=":".join(splits)
    return t

#from https://www.geeksforgeeks.org/python-program-to-find-day-of-the-week-for-a-given-date/
def findDay(date):
    date = str(date)
    year, month, day = (int(i) for i in date.split('-'))
    born = datetime.date(year, month, day)
    return born.strftime("%A")
