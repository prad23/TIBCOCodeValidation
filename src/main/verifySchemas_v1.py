import sys,os,datetime, csv, fileinput as file, logging as log,operator,filecmp,compareSchemas_v1 as compare,re

#log.config.fileConfig('../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk_VerifySchemas.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
# create logger
log=log.getLogger('TIBCO_SVN_NewTrunk_VerifySchemas')

#dt=datetime.datetime.now()
log.info("<-------------------------------START---------------------------------->\n")


BWProjects="target/Schemas"
SVNTrunkSchemas="target/TIBCOSharedSchemas"
lenBWProjects=15
lenSVNTrunkSchemas=26

def countFiles(file,filePath,dirPath):
	regex=file.rpartition('.xsd')[0]+'_\d'
	schemas=[name for name in os.listdir(filePath) if re.search(regex,name.rpartition('.xsd')[0])]
	if operator.gt(len(schemas),0):
		log.info("Found %s file(s) that are similar to %s in dir %s" %(len(schemas),file,dirPath.rpartition('/')[0]))
		i=0
		while i < len(schemas):
			trunkSchemaFilePath=os.path.join(SVNTrunkSchemas,dirPath)[lenSVNTrunkSchemas:]
			schemaDirFilePath=os.path.join(filePath.rpartition('/')[0],schemas[i])
			log.info('Now comparing %s and %s' %(schemaDirFilePath,trunkSchemaFilePath))
			compare.checkSum(schemaDirFilePath,trunkSchemaFilePath)
			i+=1

def findFile(filename,path):
	log.info('Will search for filename %s in Trunk SharedSchemas %s' %(filename,SVNTrunkSchemas))
	for root,dirs,files in os.walk(SVNTrunkSchemas):
		for file in files:
			dirPath=os.path.join(root,file)
			if operator.eq(file,filename):
				schemaDirFilePath=os.path.join(path.rpartition('/')[0],file)
				trunkSchemaFilePath=os.path.join(SVNTrunkSchemas,dirPath)[lenSVNTrunkSchemas:]
				log.info('Comparing %s and %s ' %(schemaDirFilePath,trunkSchemaFilePath))
				compare.checkSum(schemaDirFilePath,trunkSchemaFilePath)
				filePath=path.rpartition('/')[0]
				log.info("Searching for similar %s files in %s " %(file,filePath))
				countFiles(file,filePath,dirPath)
					

def visitfile(filenamepath):
	filename=os.path.basename(filenamepath)
	dirPath=filenamepath.rpartition('/')[0]
	log.debug('Current directory path :: %s' %(dirPath))
	if  "MetaDir" not in str(filenamepath) and "NoDiffReport" not in str(filenamepath):
		findFile(filename,filenamepath)

def walktree(top):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        if os.path.isdir(pathname):
        	walktree(pathname)
        elif os.path.isfile(pathname):
            # It's a file, call the callback function
            visitfile(pathname)
        else:
            # Unknown file type, print a message
            log.info('Skipping %s' % pathname)

def walk(top):
	for root,dirs,files in os.walk(top):
		for d in dirs:
			if operator.eq(d,'Schemas'):
				SchemasDir=os.path.join(root,d)
				if  "MetaDir" not in str(SchemasDir) and "NoDiffReport" not in str(SchemasDir):
					log.info('Walking through Schemas directory: %s' %SchemasDir)
					walktree(SchemasDir)

try:
	if not os.path.isdir(BWProjects):
		log.error("No directory found %s" %BWProjects)
		raise
	else:
		log.info("Searching for Schemas directory in %s" %(BWProjects))
		walk(BWProjects)
				
except Exception,e:
	log.error('Exception occurred while processing main program %s' %e)
	raise

log.info("<--------------------------------END----------------------------------->\n")