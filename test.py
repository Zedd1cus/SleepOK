import re
def isValidTime(time):
    regex = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
    p = re.compile(regex)
    if time == "":
        return False
    m = re.search(p, time)
    if m is None:
        return False
    else:
        return True

print(isValidTime('01:50'))


def verify_time_of_notification(time: str) -> bool:
    regex = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
    p = re.compile(regex)
    if time == "":
        return False
    m = re.search(p, time)
    if m is None:
        return False
    else:
        return True
