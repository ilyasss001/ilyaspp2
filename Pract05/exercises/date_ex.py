#1 Write a Python program to subtract five days from current date.
from datetime import datetime, timedelta

today = datetime.now()
new_date = today - timedelta(days=5)

print("Current date:", today)
print("5 days ago:", new_date)
#2 Write a Python program to print yesterday, today, tomorrow.
from datetime import datetime, timedelta

today = datetime.now()
yesterday = today - timedelta(days=1)
tomorrow = today + timedelta(days=1)

print("Yesterday:", yesterday)
print("Today:", today)
print("Tomorrow:", tomorrow)
#3 Write a Python program to drop microseconds from datetime.
from datetime import datetime

now = datetime.now()
no_microseconds = now.replace(microsecond=0)

print("With microseconds:", now)
print("Without microseconds:", no_microseconds)
#4 Write a Python program to calculate two date difference in seconds.
from datetime import datetime

date1 = datetime(2025, 6, 1, 12, 0, 0)
date2 = datetime(2025, 6, 5, 15, 30, 0)

difference = date2 - date1
seconds = difference.total_seconds()

print("Difference in seconds:", seconds)
