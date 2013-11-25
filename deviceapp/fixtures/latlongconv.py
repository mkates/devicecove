#This script simply takes the data from latlong.csv and adds it to latlong.json
#appropriately formatted

import json
import os
ins = open( "latlong.csv", "r" )
out = open("latlong.json",'w').close()
out = open("latlong.json",'w')
out.write('[')
array = []
count = 1
for line in ins:
	line = line.replace('"','')
	a = line.split(",")
	try:
		dict = {"pk":count,"model":"deviceapp.latlong","fields":{"zipcode":a[0],"latitude":float(a[1]),"longitude":float(a[2]),"city":a[3],"state":a[4],"county":a[5].split("\n")[0]}}
		jsoned = json.dumps(dict)
		out.write(jsoned)
		out.write(",")
	except:
		print a
	count += 1
out.seek(-1, os.SEEK_END)
out.truncate()
out.write("]")
ins.close()
out.close()