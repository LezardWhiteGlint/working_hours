#!/usr/bin/env python
import cgi
#import cgitb
#cgitb.enable()

print "Content-Type: text/html"     # HTML is following
print


#print "<html>\n<body>"
#print '<form enctype="multipart/form-data" action="working_hours.py" method="post">'
#print '<p>File: <input type="file" name="file"></p>'
#print '<p><input type="submit" value="Upload"></p>'
#print "</form>"
#print "</body>\n</html>"



print '<form action = "working_hours.py" method = "post" target = "_blank">'
print '<textarea name = "textcontent" cols = "50" rows = "20">'
print '</textarea>'
print '<input type = "submit" value = "Submit" />'
print "</form>"


#from __future__ import division, unicode_literals
#import codecs
import io
import os
import sys
import re
from datetime import datetime
from bs4 import BeautifulSoup
#abspath = os.path.abspath(__file__)
#dname = os.path.dirname(abspath)
#os.chdir(dname)

#if getattr(sys,'frozen',False):
#    application_path = sys._MEIPASS
     # If the application is run as a bundle, the pyInstaller bootloader
    # extends the sys module by a flag frozen=True and sets the app 
    # path into variable _MEIPASS'.
#else:
#    application_path = os.path.dirname(os.path.abspath(__file__))


if hasattr(sys, 'frozen'):
    basis = sys.executable
else:
    basis = sys.argv[0]
application_path = os.path.split(basis)[0]



time_date = []
time = []
date = []
weekday =[]
status = []
time_cal = []

#filename = 'sample1.html'
filename = os.path.join(application_path, 'sample.html')


#get table content
def table(filename):
    form = cgi.FieldStorage()
#    for key in form.keys():
#        print(key)
    filename = form.getvalue('textcontent')
 #   file = io.open(filename.file,'r',encoding='GBK')
    soup = BeautifulSoup(filename, 'html.parser')
    table = soup.find('table', id='GridView1')
    rows = table.find_all('td')
    content = []
    for r in rows:
            content.append(r.get_text())
    return content

#put content into lists
def split(content):
    for ele in content:
        if len(ele) > 15:
            time_date.append(ele)
        if ele == 'Check In' or ele == 'Check Out':
            status.append(ele)
        if len(ele) > 3 and len(ele) < 15 and ele != 'Check In' and ele != 'Check Out' :
            weekday.append(ele)

    #get time only list
    for t in time_date:
        time.append(t.split()[1])

    for d in time_date:
        date.append(d.split()[0])

    #parse time list and convert them into seconds
    for t in time:
        FMT = '%H:%M:%S'
        time_temp = datetime.strptime(t, FMT)
        seconds = time_temp.hour * 3600 + time_temp.minute * 60 + time_temp.second
        time_cal.append(seconds)
    return time_cal,date

#caculate total time and display
def total_time(time_cal):
    total_time = int(0)
    try:
        for i in range(len(time_cal)):
            if time_cal[i] < time_cal[i+1]:
                daily_time = time_cal[i+1] - time_cal[i]
                half_hours = int(daily_time/1800)
                total_time = half_hours + total_time
    except IndexError:
        pass
    return total_time

def display(total_time):
    hours = int(total_time/2)
    minutes = int(total_time%2)*30
    message = 'Total Working Time:'+str(hours)+':'+str(minutes)
    print """\
    <html><body>
    <p><font size="+50">%s</font></p>
    </body></html>
    """ % (message,)

def daily_hours(time_cal,date):
    daily_h = []
    date_h = []
    try:
        for i in range(len(time_cal)):
            if time_cal[i] < time_cal[i+1]:
                daily_time = time_cal[i+1] - time_cal[i]
                half_hours = int(daily_time/1800)
		if half_hours != 0:
                    daily_h.append(half_hours)
                    date_h.append(date[i+1])
    except IndexError:
        pass
    return daily_h,date_h

def daily_display(daily_h,date):
    #date_new = []
    #time_new =[]
    #result = 0
    #temp = 0
    #try:
       # for i in range(len(date)):
        #    if date[i] == date[i+1]:
         #       temp = daily_h[i] + daily_h[i+1] +temp
          #      result = temp
           # else:
            #    if result !=0:
             #       time_new.append(result)
              #      date_new.append(date[i])
               #     temp = 0
                #    result = 0
	#	if i == len(date) - 1:
	#	    time_new.append(daily_h[i])
         #           date_new.append(date[i])
          #      else:
           #         time_new.append(daily_h[i])
            #        date_new.append(date[i])
    #except IndexError:
     #   pass
   # print('time_new')
   # print(time_new)
   # print('date_new')
   # print(date_new)
    for i in range(len(date)):
        hours = int(daily_h[i]/2)
        minutes = int(daily_h[i]%2)*30
        message = str(hours)+':'+str(minutes)
        print('<p>Date: '+date[i]+'-------'+message+'</p>')
        print "\n"

def app():
    content = table(filename)
    time_cal,date = split(content)
    time_result = total_time(time_cal)
    daily_h,date_h = daily_hours(time_cal,date)
   # print('dailyh')
   # print(daily_h)
   # print('dateh')
   # print(date_h)
    daily_display(daily_h,date_h)
    display(time_result)

app()




