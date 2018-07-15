#this class generate date for this week

from datetime import datetime,timedelta

def weeklist_maker():
    weeklist = []
    today = datetime.today()
    weekday_now = today.weekday()
    monday = today - timedelta(days=weekday_now)
    for i in range(7):
        weekday = monday + timedelta(days=i)
        result = str(weekday).split()[0]
        weeklist.append(result)
    return weeklist


    
    
    

