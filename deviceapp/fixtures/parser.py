import json
import os

##############################################################################
#### This file parses the .txt files and converts them to JSON ###############
##############################################################################

def parseCategory():
	ins = open( "users.txt", "r" )
	out = open("newdata.txt",'w').close()
	out = open("newdata.txt",'w')
	out.write('[')
	array = []
	productcount = 1
	pkcategory = 1
	pksubcategory = 1
	for line in ins:
		line = line.replace("\n","")
		if line.startswith('!'):
			cat = line.split("!")[1]
			cat_s = cat.replace(" ","").replace("-","").replace("/","").lower()
			jd = json.dumps({"pk":str(pkcategory),"model": "deviceapp.category","fields": {"name":cat_s,"displayname":cat,"industry" : 1,"totalunits":0}})
			out.write(jd)
			print jd+","
			pkcategory += 1
		elif line.startswith('#'):
			productcount += 1
		else:
			subcat = line
			subcat_s = subcat.replace(" ","").replace("-","").replace("/","").lower()
			jd = json.dumps({"pk":str(pksubcategory),"model": "deviceapp.subcategory","fields": {"name":subcat_s,"displayname":subcat,"category" :str(productcount),"totalunits":0}})
			out.write(jd)
			print jd+","
			pksubcategory += 1
		out.write(",")
	out.seek(-1, os.SEEK_END)
	out.truncate()
	out.write("]")
	ins.close()
	out.close()
	return

def parseManufacturer():
	ins = open( "manufacturers.txt", "r" ).close()
	ins = open( "manufacturers.txt", "r" )
	out = open("manufacturers.json",'w').close()
	out = open("manufacturers.json",'w')
	out.write('[')
	array = []
	pkcategory = 1
	for line in ins:
		line = line.replace("\n","")
		sub_man = line.replace(" ","").replace("-","").replace("/","").lower()
		jd = json.dumps({"pk":pkcategory,"model": "deviceapp.manufacturer","fields": {"name":sub_man,"displayname":line}})
		out.write(jd)
		print jd+","
		pkcategory += 1
		out.write(",")
	out.seek(-1, os.SEEK_END)
	out.truncate()
	out.write("]")
	ins.close()
	out.close()

def parseLatLong():
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

#parseManufacturer()