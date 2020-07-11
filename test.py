import datetime
from datetime import datetime, date

'''
start_date=("2020-1-1")
end_date=datetime.today()

start = datetime.strptime(start_date, '%Y-%m-%d')
start_days = datetime.date(start)
print(start_days
'''

start_date=datetime(2020, 1, 1)
end_date=datetime.today()

print(type(start_date))
print(type(end_date))
