import sys,os,datetime, csv, fileinput as file, logging as log,operator,copymeSchemas as copy

#log.config.fileConfig('../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk_Schemas.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
# create logger
log=log.getLogger('TIBCO_SVN_NewTrunk_CheckSchemas')

#dt=datetime.datetime.now()
log.info("<-------------------------------START---------------------------------->\n")

dataFiles="target/dataFiles"
SchemasDir="target/Schemas"

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def visitfile(filenamepath):
	filename=os.path.basename(filenamepath)
	if operator.contains(filename,'.xsd'):
	#	log.info("Found schema file %s in SharedSchemas Trunk %s" %(filename,filenamepath.rpartition('/')[0]))
		log.info("Searching for Trunk SharedSchema %s in dataFiles dir %s" %(filenamepath[lenSchemaPath:],dataFiles))
		findFile(filenamepath,dataFiles)

def walktree(dataFilesDir):
	machines=os.listdir(dataFilesDir)
#	log.info("List of machines in %s are %s" %(dataFilesDir,machines))
	for machine in machines:
		machinedir=dataFilesDir+"/"+machine
		domains=get_immediate_subdirectories(machinedir)
		for domain in domains:
			log.info("Scanning through directories for schemas in %s" %(os.path.join(machinedir,domain)))
			for root,subdir,files in os.walk(os.path.join(machinedir,domain)):
				for name in files:
					dataFileSchemaPath=os.path.join(root,name)
					if operator.contains(name,'.xsd'):
						log.debug("Found schema file %s in %s" %(name,dataFileSchemaPath))
						copy.copy_file(name,dataFileSchemaPath,SchemasDir)
					else:
						log.debug("Could not find schema %s in %s" %(name,dataFileSchemaPath))

try:
	if not os.path.isdir(SchemasDir):
		os.makedirs(SchemasDir)
	log.info('Walking through  directory: %s' %dataFiles)
	walktree(dataFiles)
		
except Exception,e:
	log.error('Exception occurred while processing main program %s' %e)
	raise

log.info("<--------------------------------END----------------------------------->\n")