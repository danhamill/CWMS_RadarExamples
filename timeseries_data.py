#!python3
#################################################
# RADAR Example: Retrieving Available Timeseries
# Author: Daniel.T.Osborne@usace.army.mil
#################################################

import sys
import http.client as httplib,urllib.parse as urllib
import json
from datetime import datetime, timezone

# 3rd party module
import pytz

HOST="cwms-data.usace.army.mil:443"
PATH="/cwms-data"

conn = None
tz = pytz.timezone("PST8PDT")

start = datetime(2022, 1, 1, 0, 0, 0, tzinfo=tz)
end = datetime(2022, 2, 1, 0, 0, 0, tzinfo=tz)

if __name__ == "__main__":
	headers = { 'Accept': "application/json;version=2" }
	url = PATH + "/timeseries"

	params = {
		# Valid options can be determined by examining the Office ID column in the output from offices.py
		"office": 'SPK',
		# Valid options can be determined by examining the Timeseries ID column in the output from timeseries.py
		"name": 'Lake Kaweah.Stor-Top Con.Inst.~1Day.0.Calc-val',
		"unit": 'EN',
		# Times can either be entered in the full ISO-8601 format, including time zone offset and name (currently broken)
		# or just the date and time, with the the timezone specified separately.
		"begin": f"{start.strftime('%Y-%m-%dT%H:%M:%S')}",
		"end": f"{end.strftime('%Y-%m-%dT%H:%M:%S')}",
		"timezone": tz.zone,
	}

	conn = httplib.HTTPSConnection( HOST )
	conn.request("GET", url + "?" + urllib.urlencode(params), None, headers )
	print("Fetching: %s" % "https://" + HOST + url, file=sys.stderr)

	response = conn.getresponse()
	data = response.read().decode('utf-8')

	try:
		timeseries = json.loads(data)
		# Uncomment to print the raw JSON returned from RADAR
		#print(json.dumps(locations, indent="\t", separators=(',', ': ')))
		unit = timeseries['units']
		print(f"Data for {timeseries['name']}:")
		print(f"{'Date Time':16s} {unit:>9s} {'Quality':>7s}")
		for dt,val,qal in timeseries['values']:
			# Timestamp in result is always in milliseconds since unix epoch (UTC).
			date = datetime.fromtimestamp(dt / 1000, timezone.utc)
			print(f"{date.strftime('%Y-%m-%d %H:%M'):16s} {val:>9.2f} {qal:>7d}")

	except json.JSONDecodeError as err:
		print(str(err))
		print(repr(data))
