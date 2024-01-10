# import datetime module from datetime
from datetime import datetime

# consider the time stamp in string format
# DD/MM/YY H:M:S.micros
time_data = "1999/11/11"

# format the string in the given format :
# day/month/year hours/minutes/seconds-micro
# seconds
format_data = "%Y/%m/%d"

# Using strptime with datetime we will format
# string into datetime
date = datetime.strptime(time_data, format_data)

# display date
print(datetime.today().day)
