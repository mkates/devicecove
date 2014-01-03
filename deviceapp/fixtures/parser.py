import json
import os

##############################################################################
#### This file parses the .txt files and converts them to JSON ###############
##############################################################################

def parseCategory():
	#Open the relevant files
	ins = open( "text_files/categories.txt", "r" )
	sub = open( "text_files/subcategories.txt", "r" )
	out = open("categories_and_subcategories.json",'w').close()
	out = open("categories_and_subcategories.json",'w')
	out.write('[')
	#Extract categories into an array
	#format 'id' = ['name,'pk']
	cat_array = {}
	value = ''
	type = 0
	count = 1
	for line in ins:
		line = line.replace("\n","")
		if type == 0:
			value = line
			type = 1
		else:
			cat_array[line] = [value,count]
			count += 1
			type = 0
	#Extract subcategories into an array
	#format 'name' = ['category_pk','category_pk',...]
	sub_array = {}
	type = 0
	for line in sub:
		line = line.replace("\n","")
		if type == 0:
			line = line.replace(",","")
			value = line
			type = 1
		else:
			line = line.split(',')
			references = []
			for nums in line:
				references.append(int(nums))
			sub_array[value] = references
			type = 0	
	# Populate subcatparsed from the two arrays
	categories = cat_array
	subcategories = sub_array
	cat_conc_array =[]
	for key,value in categories.items():
		cat_concat = value[0].replace(" ","").replace("/","").replace(',','').replace('-','').lower()
		cat_conc_array.append(cat_concat)
		out.write(json.dumps({"pk":value[1],"model": "deviceapp.category","fields": {"name":cat_concat,"displayname":value[0],"industry" : 1,"totalunits":0}}))
		out.write(',\n')
	counter = 1
	for key,value in subcategories.items():
		sub_concat = key.replace(" ","").replace("/","").replace(',','').replace('-','').lower()
		cats = []
		for cat in value:
			cats.append(categories[str(cat)][1])
		out.write(json.dumps({"pk":counter,"model": "deviceapp.subcategory","fields": {"name":sub_concat,"displayname":key,"maincategory":cats[0],"category" :cats,"totalunits":0}}))
		out.write(',\n')
		counter += 1
	out.seek(-1, os.SEEK_END)
	out.truncate()
	out.write("]")
	ins.close()
	out.close()
	sub.close()
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


parseCategory()