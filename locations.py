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
	# /locations doesn't support JSONv2, use /catalog instead.
	headers = { 'Accept': "application/json" }
	url = PATH + "/locations"

	params = {
		"office": 'SAW',	# Valid options can be determined by examining the Office ID column in the output from offices.py
		"names": '*',	# Location name or search string. * is wildcard
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
		for location in locations['locations']['locations']:
			elevation = "Unknown"
			latitude = "Unknown"
			longitude = "Unknown"
			geo = location['geolocation']
			name = location['identity']['name']
			longName = location['label']['long-name'] or location['label']['public-name'] or ""

			if geo is not None:
				elev = geo['elevation']
				if elev is not None and elev['value'] is not None:
					elevation = f"{elev['value']:>7.1f} {elev['unit']:<2s}"
				
				if geo['latitude'] is not None: latitude = f"{geo['latitude']:>9.4f}"
				if geo['longitude'] is not None: longitude = f"{geo['longitude']:>9.4f}"

			print(f"{name:40s} {elevation:>10s} {latitude:>9s} {longitude:>9s} {longName}")
	except json.JSONDecodeError as err:
		print(str(err))
		print(repr(data))
