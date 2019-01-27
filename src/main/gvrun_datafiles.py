#!/usr/bin/python
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


BWProjects="target/BWProjects"
BWTrunk="target/BWSVNTrunk"
reports="target/GVs"

## Function to read csv file in to array.
def readFile(filename):
	f=open(filename)
	reader= csv.reader(f) #csv is a package for reading csv files.
	array=list(reader)
	log.debug("List of GV names and interface names:\n %s" % array)
	return array
	log.debug("List of archive and project names are loaded in to array.")

def writeReport(file,project,gvpath,gvname,prodValue,trunkValue):
	if os.path.isfile(file):
		fw=open(file,"a+")
		data=project+","+gvpath+","+gvname+","+prodValue+","+trunkValue+"\n"
		fw.write(data)
	else:
		fw=open(file,"w+")
		data="PROJECT,GV PATH,GV NAME,PROD VALUE,TRUNK VALUE\n"+project+","+gvpath+","+gvname+","+prodValue+","+trunkValue+"\n"
		fw.write(data)
		fw.close()
		

def compareGV(gvxpath,dirPath):
	log.debug('gvpath %s and dirpath %s' %(gvxpath,dirPath))
	if operator.contains(gvxpath,"/"):
		gvs=gvxpath.rsplit("/",1)
		prodDirPath=os.path.join(os.path.join(BWProjects,dirPath),gvs[0])
		trunkDirPath=os.path.join(os.path.join(BWTrunk,dirPath),gvs[0])
		#print prodDirPath
		if os.path.isdir(prodDirPath) and os.path.isdir(trunkDirPath):
			log.info('Path of defaultVars file is %s and GV name is %s' %(dirPath,gvs[1]))
			prodValue=findgv.getgv(prodDirPath,gvs[1])
			log.info("GV value returned from PRODUCTION copy is %s=%s"%(gvs[1],prodValue))
			trunkValue=findgv.getgv(trunkDirPath,gvs[1])
			log.info("GV value returned from TRUNK copy is %s=%s"%(gvs[1],prodValue))
			if operator.eq(prodValue,trunkValue):
				log.debug("'%s' is EQUAL to '%s'"%(prodValue,trunkValue))
			else:
				#print ("'%s' is NOT EQUAL to '%s'"%(prodValue,trunkValue))
				log.info("Found difference between PRODUCTION and TRUNK values for %s."%(gvs[1]))
				report=os.path.join(reports,"gvReport.csv")
				writeReport(report,dirPath.rpartition("/")[0],os.path.join(dirPath,gvxpath).rpartition("/")[0],gvs[1],prodValue,trunkValue)

	else:
		log.info('GV %s is global variable name.' %gvxpath)

array=[]
apps = {}

with open(arg[0]) as myfile:
    for line in myfile:
        name, value = line.partition(",")[::2]
        apps[name.strip()] = (value.strip())
        log.debug("Loaded all apps in to list\ %s" %apps)

gvall=readFile(arg[1])

## Main program execution
try:
	for interface,gvxpath in gvall:
		if operator.contains(apps,interface):
			log.debug('Corresponding project for interface %s is %s' %(interface,apps[interface]))
			log.info('GV xpath from file is %s' %gvxpath)
			compareGV(gvxpath,os.path.join(apps[interface],'defaultVars'))
		else:
			log.info('There is no interface project mapping for %s' %interface)

except Exception,e:
    log.error("Main program Exception found while processing :: '%s'" %e)
    raise
		
		
	
log.info("<--------------------------------END----------------------------------->\n")
