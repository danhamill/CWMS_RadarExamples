#!python3
#################################################
# RADAR Example: Retrieving Available Timeseries
# Author: Daniel.T.Osborne@usace.army.mil
#################################################

import sys
import http.client as httplib,urllib.parse as urllib
import json

HOST="cwms-data.usace.army.mil:443"
PATH="/cwms-data"

conn = None

if __name__ == "__main__":
	headers = { 'Accept': "application/json;version=2" }
	url = PATH + "/catalog/TIMESERIES"

	params = {
		"office": 'SPK',					# Valid options can be determined by examining the Office ID column in the output from offices.py
		"like": 'Lake Kaweah.*\.Calc-val',	# Location name or search string. POSIX regular expression.
	}

	conn = httplib.HTTPSConnection( HOST )
	conn.request("GET", url + "?" + urllib.urlencode(params), None, headers )
	print("Fetching: %s" % "https://" + HOST + url, file=sys.stderr)

	response = conn.getresponse()
	data = response.read().decode('utf-8')
	# There is a bug in RADAR that can return CRLF in JSON string, remove any found.
	data = data.replace('\r\n', '')

	try:
		locations = json.loads(data)
		# Uncomment to print the raw JSON returned from RADAR
		#print(json.dumps(locations, indent="\t", separators=(',', ': ')))

		print(f"{'Timeseries ID':80s} {'Interval':>9s} {'Units':>5s}")
		for location in locations['entries']:
			name = location['name']
			units = location['units']
			interval = location['interval']

			print(f"{name:80s} {interval:>9s} {units:>5s}")
	except json.JSONDecodeError as err:
		print(str(err))
		print(repr(data))
