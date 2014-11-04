#!/usr/bin/env python
import caldav
from ConfigParser import SafeConfigParser
from django.utils.encoding import smart_str, smart_unicode
from datetime import datetime, timedelta
import smtplib
import time
import pytz
from email.mime.text import MIMEText
from icalendar import Calendar, Event
import vobject
import string
import re
regex_temp = re.compile(r'^Temp=(.*)')

home_tz = pytz.timezone('Europe/London')

def get_calendar():
    """
    Get the calendar.
    """
    parser = SafeConfigParser()
    parser.read('./config.ini')
    url = parser.get('calendar', 'url')
    client = caldav.DAVClient(url)
    principal = caldav.Principal(client)
    calendars = principal.calendars()
    return calendars[0]

def main():
    cal = get_calendar()
    now = datetime.now(tz=home_tz) # timezone?
    timeMin = home_tz.localize(datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second ))
    timeMax = home_tz.localize(datetime(year=now.year, month=now.month, day=now.day, hour=now.hour, minute=now.minute, second=now.second ) + timedelta(minutes=1))
    #print timeMax
    #print timeMin
    return_temp = 13.6654

    evs = cal.date_search(timeMin, timeMax)
    for event in evs:
       try:
	cal = Calendar.from_ical(smart_str(event.data))
        ev0 = cal.walk('vevent')[0]
        parsedCal = vobject.readOne(event.data)
	tempstring = str(ev0['SUMMARY']).replace("\\,",",")
        match = regex_temp.search(tempstring)

	if match:
		target_temp = float(match.group(1))
		return_temp = target_temp
       except Exception, exc:
		return_temp = 13.6654
       #print return_temp
       return return_temp

if __name__ == '__main__':
    main()
