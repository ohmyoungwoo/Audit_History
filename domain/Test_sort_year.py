import datetime as dt
from dateutil.parser import parse

list_datetime = ['2024-04-16','2022-04-16','2022-05-16','2023-04-16']
list_year =[]

for datetime in list_datetime:
    list_year.append(parse(datetime).year)
    
print(list_year)
list_year.sort()
print (list_year)