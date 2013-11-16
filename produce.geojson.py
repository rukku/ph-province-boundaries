#import subprocess
from subprocess import call
import shapefile
import os
from dbfpy import dbf 
import csv

#replace spaces
def replacespaces(s):
	return s.replace(' ', '\\ ')

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

#def movedirectories():	
def create_subset(whole, datasource, level):
	for subset in whole:
		#command = 'ogr2ogr -f GeoJSON -where "%s IN (\'%s\')" %s.geojson %s' % (level, subset, subset, datasource)
		#subprocess.call(command)

		outfile = "%s.geojson" % subset
		
		arguments = "%s IN (\'%s\')" % (level, subset)

		call(['ogr2ogr','-f', 'GeoJSON','-where', arguments, outfile, datasource])

#convert to topojson
#pass

def loadISOcodes():
	with open('ISO.csv','rb') as f:
		codes = dict()
		reader = csv.reader(f)
		for row in reader:
			#print row[2], row[0]
			codes[row[0]] = row[1].upper()
			print 
		return codes  

def listFiles():
    ascList = []
    for r,d,f in os.walk("."):
        for files in f:
            if files.endswith(".geojson"):
                #print os.path.join(r,files) 
                out = os.path.join(r,files) + "\n" 
                ascList.append(os.path.join(r,files))
    return ascList

def filenames(filepath):
	return filepath[2:-8]

def fixfilesnames(filepath):
	names = []
	for filepath in filepaths:
		append(filenames(filepath))
	return names

#move to its own folder
def json2folder(files, isocodes):
	
	count = 0
	nomatch = open('nomatches.txt', 'wt')
	isonames = open('isonames.csv','wt')
	nm = []
	shellscript = open('mass-topojson.sh', 'wt')
	for f in files:
		found = 0
		name = filenames(f) 
		for k,v in isocodes.items():
			if name == v:
			#	print k,v
				filename = name + ".topojson"
				jsonfile = name + ".geojson"
				#print filename,type(filename), jsonfile, type(jsonfile)
				
				#command = replacespaces(command)
				filename = replacespaces(filename)
				jsonfile = replacespaces(jsonfile)
				command = "topojson -o {0} {1}\n".format(filename, jsonfile)
				shellscript.write(command)
				isonames.write(name + "," + k + "\n")
				print command
				found = 1
				#print filename
				#call("topojson", "-o", filename, jsonfile, shell=False) #convert to topoJSON
				#call() #create folder and move topoJSON and geoJSON to folder
			else:
				#
				#print name
				continue
		if found == 0: 
			nm.append(name)

	newlist = list(set(nm))
	print len(newlist)
	for n in newlist:
		print n
		nomatch.write(n+"\n")			
		#for k,v in isocodes.iteritems():
			#print k,v

def movefolders():
	isonames = open('isonames.csv', 'rb')
	ison = dict()
	reader = csv.reader(isonames)
	for row in reader:
		ison[row[0]] = row[1]
		#print row
		#ison.append(row)
	return ison
#tests
def est_list():
	prov_list = list_provinces()
	print prov_list

def test_listFiles():
	flist = listFiles()
	for f in flist:
		print filename(f)



#prov = list_provinces()
#create_subset(prov, 'citymuni.shp', 'PROVINCE')

#create_subset(prov, 'citymuni.shp', 'PROVINCE')

#test_listFiles()
#filelist = listFiles()
#isocodes = loadISOcodes()
#son2folder(filelist, isocodes)

movesh = open('topojsonmove.sh', 'wt')
isonames = movefolders()
for name, iso in isonames.iteritems():
	name = replacespaces(name)
	#print name
	geoj = name +".geojson"
	topoj = name +".topojson"

	mkdirtext = "mkdir %s\n" % (iso)  
	movegeojson = "mv %s ./%s/%s\n" % (geoj, iso, geoj)
	movetopojson = "mv %s ./%s/%s\n" % (topoj, iso, topoj)

	print mkdirtext
	print movegeojson
	print movetopojson
	
	movesh.write(mkdirtext)
	movesh.write(movegeojson)
	movesh.write(movetopojson)
	#movetopojson = "mv %s %s" % () 
#for k,v in isocodes.iteritems():
#	print k,v


#checkfields('citymuni.shp')
#listrecords('citymuni.shp')
#shp_to_geojson('citymuni.shp')
#filename = 
#fileList = listFiles()
#for fiLe in fileList:
#	print fiLe

#prov = list_provinces()
#create_subset(prov, 'citymuni.shp', 'PROVINCE')
#test_list()
#print subprocess.call('ogrinfo')
