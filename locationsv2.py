#!python3
#################################################
# RADAR Example: Retrieving Location metadata
# Author: Daniel.T.Osborne@usace.army.mil
#################################################

import sys
import http.client as httplib,urllib.parse as urllib
import json

HOST="cwms-data.usace.army.mil:443"
PATH="/cwms-data"

conn = None

if __name__ == "__main__":
	# JSONv2 endpoint is very different from v1
	headers = { 'Accept': "application/json;version=2" }
	url = PATH + "/catalog/LOCATIONS"

	params = {
		"office": 'SPK',		# Valid options can be determined by examining the Office ID column in the output from offices.py
		"like": 'Lake Kaweah',	# Location name or search string. POSIX regular expression. RADAR can timeout if the search takes too long.
		"unitSystem": 'EN',		# By default metric will be fetched
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

		print(f"{'Location ID':40s} {'Elevation':>10s} {'Latitude':>9s} {'Longitude':>9s} {'Full Name'}")
		for location in locations['entries']:
			elevation = "Unknown"
			latitude = "Unknown"
			longitude = "Unknown"
			name = location['name']
			longName = location.get('long-name', location.get('public-name', ""))

			if location.get('elevation') is not None: elevation = f"{location['elevation']:>7.1f} {location['unit']:<2s}"
			if location.get('latitude') is not None: latitude = f"{location['latitude']:>9.4f}"
			if location.get('longitude') is not None: longitude = f"{location['longitude']:>9.4f}"

			print(f"{name:40s} {elevation:>10s} {latitude:>9s} {longitude:>9s} {longName}")
	except json.JSONDecodeError as err:
		print(str(err))
		print(repr(data))
