#!python3
#################################################
# RADAR Example: Retrieving Office IDs
# Author: Daniel.T.Osborne@usace.army.mil
#################################################

import sys
import http.client as httplib
import json

HOST="cwms-data.usace.army.mil:443"
PATH="/cwms-data"

conn = None

if __name__ == "__main__":
	headers = { 'Accept': "application/json;version=2" }
	url = PATH + "/offices"

	conn = httplib.HTTPSConnection( HOST )
	conn.request("GET", url, None, headers )
	print("Fetching: %s" % "https://" + HOST + url, file=sys.stderr)

	response = conn.getresponse()
	data = response.read()
	offices = None

	try:
		# Uncomment to print the raw JSON returned from RADAR
		#print(json.dumps(data, indent="\t", separators=(',', ': ')))

		offices = json.loads(data)

		print(f"{'District':30s}Office ID")
		print(f"{'-'*30}{'-'*10}")
		for office in offices:
			if office['type'] != "DIS": continue	# We only care about districts, since that's who "owns" the data

			print(f"{office['long-name']:30s}{office['name']}")
				
	except json.JSONDecodeError as err:
		print(str(err))
		print(repr(data))
