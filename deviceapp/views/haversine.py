from math import radians, cos,sin,asin,sqrt, atan2
from deviceapp.models import LatLong

def haversineDistance(zipcode1,zipcode2):
	try:
		zip1 = LatLong.objects.get(zipcode = int(zipcode1))
		zip2 = LatLong.objects.get(zipcode = int(zipcode2))
		lat1 = zip1.latitude
		lon1 = zip1.longitude
		lat2 = zip2.latitude
		lon2 = zip2.longitude
		radius = 6371 # km
		dlat = radians(lat2-lat1)
		dlon = radians(lon2-lon1)
		lat1 = radians(lat1)
		lat2 = radians(lat2)
		a = sin(dlat/2) * sin(dlat/2) + sin(dlon/2) * sin(dlon/2) * cos(lat1) * cos(lat2)
		c = 2 * atan2(sqrt(a),sqrt(1-a)); 
		d = radius * c;
		miles = d*.621371
		if miles < 10:
			miles = round(miles,1)
		else:
			miles = int(miles)
		return miles
	except:
		return -1