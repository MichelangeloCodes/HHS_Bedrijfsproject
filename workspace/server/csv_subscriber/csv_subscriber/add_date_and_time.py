import datetime

def get_date():
    today = datetime.date.today()  # Get the current date
    return today

def get_time():
    now = datetime.datetime.now().time()  # Get the current time
    return now



