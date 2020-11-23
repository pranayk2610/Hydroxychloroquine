def convert_to_24_hour_time(t):
    if t[-2:]=='pm':
        splits=t.split(":")
        hour=splits[0]
        splits[0]=str(int(hour)+12) if not int(hour)==12 else "0"
        t=":".join(splits)
    return t
