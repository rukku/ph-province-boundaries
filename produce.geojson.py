#import subprocess
from subprocess import call
import shapefile
from dbfpy import dbf 

#list provinces
def list_provinces():
	provinces = []
	db = dbf.Dbf("citymuni.dbf")
	for rec in db:
		#print rec["PROVINCE"]
		province = rec["PROVINCE"]
		if province not in provinces:
			provinces.append(province)
			print province,"added!"
	return provinces

#extract by filter
def create_subset(whole, datasource, level):
	for subset in whole:
		#command = 'ogr2ogr -f GeoJSON -where "%s IN (\'%s\')" %s.geojson %s' % (level, subset, subset, datasource)
		#subprocess.call(command)

		outfile = "%s.geojson" % subset
		
		arguments = "%s IN (\'%s\')" % (level, subset)

		call(['ogr2ogr','-f', 'GeoJSON','-where', arguments, outfile, datasource])
		
		#print subprocess.call('orginfo')

#convert shp to geojson

def shp_to_geojson(source):
   # read the shapefile
   reader = shapefile.Reader(source)
   fields = reader.fields[1:]
   field_names = [field[0] for field in fields]
   buffer = []
 
   for sr in reader.shapeRecords():       
       atr = dict(zip(field_names, sr.record))
       geom = sr.shape.__geo_interface__
       buffer.append(dict(type="Feature", \
        geometry=geom, properties=atr))    
   # write the GeoJSON file
   from json import dumps
   geojson = open("pyshp-demo.json", "w")
   geojson.write(dumps({"type": "FeatureCollection",\
    "features": buffer}, indent=2) + "\n")
   geojson.close()

def checkfields(shp):
	reader = shapefile.Reader(shp)
	fields = reader.fields[1:]
	field_names = [field[0] for field in fields]
	for field in fields:
		print field

def listrecords(shp):
	reader = shapefile.Reader(shp)
	records = reader.records()
	for record in records:
		print record[5]

def listfiles():
	pass

def movedirectories():	
	pass
#convert to topojson
#pass


#move to its own folder


#tests
def est_list():
	prov_list = list_provinces()
	print prov_list

#checkfields('citymuni.shp')
#listrecords('citymuni.shp')
#shp_to_geojson('citymuni.shp')
#filename = 

prov = list_provinces()
create_subset(prov, 'citymuni.shp', 'PROVINCE')
#test_list()
#print subprocess.call('ogrinfo')
