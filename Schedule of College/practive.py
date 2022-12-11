import datetime
date = '2023.12.18'

date_date = datetime.datetime.strptime(date,'%Y.%m.%d')

flag = date_date + datetime.timedelta(days=1)

print(flag)