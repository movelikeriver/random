"""Try the time date util for local and gm.

Usage:
$ date -u +%s && python aa.py 
1471980937

* time:
time.struct_time(tm_year=2016, tm_mon=8, tm_mday=23, tm_hour=19, tm_min=35, tm_sec=37, tm_wday=1, tm_yday=236, tm_isdst=0) 	 time.gmtime()
1472009737.0 	 time.mktime
1471980937 	 calendar.timegm <-- right
time.struct_time(tm_year=2016, tm_mon=8, tm_mday=23, tm_hour=12, tm_min=35, tm_sec=37, tm_wday=1, tm_yday=236, tm_isdst=1) 	 time.localtime()
1471980937.0 	 time.mktime <-- right
1471955737 	 calendar.timegm

* datetime.utcnow():
time.struct_time(tm_year=2016, tm_mon=8, tm_mday=23, tm_hour=19, tm_min=35, tm_sec=37, tm_wday=1, tm_yday=236, tm_isdst=-1) 	 datetime.utcnow()
1472006137.0 	 time.mktime
1471980937 	 calendar.timegm <-- right
time.struct_time(tm_year=2016, tm_mon=8, tm_mday=23, tm_hour=12, tm_min=35, tm_sec=37, tm_wday=1, tm_yday=236, tm_isdst=-1) 	 datetime.now()
1471980937.0 	 time.mktime <-- right
1471955737 	 calendar.timegm

* summary for getting UTC time in sec:
1471980937.24
1471980937
1471980937.0
1471980937
1471980937.0
"""

import calendar
import datetime
import time


def to_timestamp(dt):
    return calendar.timegm(dt.timetuple())

def to_timestamp2(dt):
    return time.mktime(dt.timetuple())


print '\n* time:'
gmt = time.gmtime()
localt = time.localtime()
utc_now = datetime.datetime.utcnow()
local_now = datetime.datetime.now()

print gmt, '\t time.gmtime()'
print time.mktime(gmt), '\t time.mktime'
print calendar.timegm(gmt), '\t calendar.timegm <-- right'

print localt, '\t time.localtime()'
print time.mktime(localt), '\t time.mktime <-- right'
print calendar.timegm(localt), '\t calendar.timegm'

print '\n* datetime.utcnow():'
print utc_now.timetuple(), '\t datetime.utcnow()'
print to_timestamp2(utc_now), '\t time.mktime'
print to_timestamp(utc_now), '\t calendar.timegm <-- right'

print local_now.timetuple(), '\t datetime.now()'
print to_timestamp2(local_now), '\t time.mktime <-- right'
print to_timestamp(local_now), '\t calendar.timegm'

print '\n* summary for getting UTC time in sec:'
print time.time()
print calendar.timegm(time.gmtime())
print time.mktime(time.localtime())
print calendar.timegm(datetime.datetime.utcnow().timetuple())
print time.mktime(datetime.datetime.now().timetuple())
