l#!/usr/bin/python
import sys,os,datetime, csv, fileinput as file, logging as log ,operator,FindGV as findgv

#log.config.fileConfig('../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_GV_COMPARE.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
# create logger
log=log.getLogger('TIBCO_SVN_GV_COMPARE')

#dt=datetime.datetime.now()
log.info("<-------------------------------START---------------------------------->\n")

## Load command line argument to variable.
arg=sys.argv[1:];

## Check for command line argument.
if (len(arg) < 2):
	log.error("At least 2 arguments are expected.")

## Check csv file exists.
if (not os.path.isfile(arg[0])):
	log.error("ArchiveProjectMapping.csv does not exist.")
if(not os.path.isfile(arg[1])):
	log.error("projectGVmappings.csv does not exist.")



BWProjects="target/EXPORT_PROD_10232017"
BWTrunk="target/BWSVNTrunk"
reports="target/GVs"
array=[]
apps={}
xmls={}

## Function to read csv file in to array.
def readFile(filename):
	f=open(filename)
	reader= csv.reader(f) #csv is a package for reading csv files.
	array=list(reader)
	log.debug("List of GV names and interface names:\n %s" % array)
	return array
	log.debug("List of archive and project names are loaded in to array.")

def writeReport(file,project,gvpath,prodValue,trunkValue):
	fw=open(file,"a+")
	data=project+","+gvpath+","+prodValue+","+trunkValue+"\n"
	fw.write(data)


def compareGV(gvxpath,dirPath,prodXmlPath):
	log.info('gvpath %s, dirpath %s, prodXmlPath %s' %(gvxpath,dirPath,prodXmlPath))
	if operator.contains(gvxpath,"/"):
		gvs=gvxpath.rsplit("/",1)
		trunkDirPath=os.path.join(os.path.join(BWTrunk,dirPath),gvs[0])
		#print prodXmlPath
		if os.path.isfile(prodXmlPath) and os.path.isdir(trunkDirPath):
			log.info('Path of defaultVars file is %s and GV name is %s' %(prodXmlPath,gvs[1]))
			prodValue=findgv.getgv(prodXmlPath,gvxpath)
			log.info("GV value returned from PRODUCTION copy is %s=%s"%(gvs[1],prodValue))
			trunkValue=findgv.getgv(trunkDirPath,gvs[1])
			log.info("GV value returned from TRUNK copy is %s=%s"%(gvs[1],prodValue))
			if operator.eq(prodValue,trunkValue):
				log.debug("'%s' is EQUAL to '%s'"%(prodValue,trunkValue))
				report=os.path.join(reports,"gvReportMatching.csv")
				writeReport(report,dirPath.rpartition("/")[0],gvxpath,prodValue,trunkValue)
			else:
				#print ("'%s' is NOT EQUAL to '%s'"%(prodValue,trunkValue))
				log.info("Found difference between PRODUCTION and TRUNK values for %s."%(gvs[1]))
				report=os.path.join(reports,"gvReportDifferences.csv")
				#	writeReport(report,dirPath.rpartition("/")[0],os.path.join(dirPath,gvxpath).rpartition("/")[0],gvs[1],prodValue,trunkValue)
				writeReport(report,dirPath.rpartition("/")[0],gvxpath,prodValue,trunkValue)

	else:
		log.info('GV %s is global variable name.' %gvxpath)


def findXML(interface,dirPath):
	'''recursively descend the directory tree rooted at dirPath,
       calling the callback function for each regular file'''
	top=dirPath
	for f in os.listdir(top):
		pathname = os.path.join(top, f)
		if os.path.isdir(pathname):
			# It's a directory, recurse into it
			findXML(interface,pathname)
		elif os.path.isfile(pathname):
			# It's a file, call the callback function
			if operator.contains(pathname,interface+"-"):
				if operator.contains(pathname,".xml"):
					log.info("Found file name %s that contains interface %s"%(pathname,interface))
					xmls[interface]=pathname

		else:
			# Unknown file type, print a message
			log.debug('Skipping %s' % pathname)
	return xmls

with open(arg[0]) as myfile:
	for line in myfile:
		name, value = line.partition(",")[::2]
		apps[name.strip()] = (value.strip())
		log.debug("Loaded all apps in to list\ %s" %apps)

gvall=readFile(arg[1])
noInterfaceMapping=[]
uniqueDiff=[]
## Main program execution
try:
	for interface,gvxpath in gvall:
		log.info("Looking for interface %s in BWProjects %s"%(interface,BWProjects))
		if operator.contains(apps,interface):
			if not xmls.get(interface,None):
				xmls={}
				xmls=findXML(interface,BWProjects)
			#	print xmls
			log.debug('Corresponding project for interface %s is %s' %(interface,apps[interface]))
			log.info('GV xpath from file is %s' %gvxpath)
			if xmls.viewvalues():
				compareGV(gvxpath,os.path.join(apps[interface],'defaultVars'),xmls[interface])
		else:
			log.debug('There is no interface project mapping for %s' %interface)
			noInterfaceMapping.append(interface)

	fw=open(os.path.join(reports,"no-interface-mapping.txt"),"a+")
	data=set(noInterfaceMapping)
	fw.write("\n".join(data))
	fw.close()
	uniqueDiff=open(os.path.join(reports,"gvReportDifferences.csv"))
	uniqueData=set(uniqueDiff)
	f=open(os.path.join(reports,"gvReportDifferences.csv"),"w")
	f.write("".join(uniqueData))
	f.close()

except Exception,e:
	log.error("Main program Exception found while processing :: '%s'" %e)
	raise



log.info("<--------------------------------END----------------------------------->\n")
