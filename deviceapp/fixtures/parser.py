import json
import os

##############################################################################
#### This file parses the .txt files and converts them to JSON ###############
##############################################################################

def parseCategory():
	#Open the relevant files
	ins = open( "categories_formatted.txt", "r" )
	out = open("categories.json",'w').close()
	out = open("categories.json",'w')
	out.write('[')
	dict = {}
	counter = 1
	for line in ins:
		line = line.replace("\n","").replace("--",'').replace("****",'')
		elements = line.split('!')
		parent = None
		if len(elements) > 2:
			parent = dict[elements[2]][0]
		main = True if not parent else False
		json_string = {"pk":counter,"model": "listing.category","fields": {"name":store(elements[1]),"displayname":elements[1],"parent":parent,"industry":[1],"main":main}}
		dict[elements[0]] = (counter,elements[1])
		out.write(json.dumps(json_string))
		out.write(",")
		out.write('\n')
		counter += 1
	out.seek(-1, os.SEEK_END)
	out.truncate()
	out.write("]")
	ins.close()
	out.close()
	return

def store(name):
	name = name.replace(" ","_").replace("/","",).replace("&","and").replace("-",'').lower()
	return name



	
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


parseCategory()