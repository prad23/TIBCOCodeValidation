import sys,os,datetime, csv, fileinput as file, logging as log,operator,filecmp,compareSchemas_v1 as compare

#log.config.fileConfig('../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk_VerifySchemas.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
# create logger
log=log.getLogger('TIBCO_SVN_NewTrunk_VerifySchemas')

#dt=datetime.datetime.now()
log.info("<-------------------------------START---------------------------------->\n")


SchemasDir="target/Schemas"
SVNTrunkSchemas="target/TIBCOSharedSchemas"
lenSchemasDir=15
lenSVNTrunkSchemas=26

def findFile(filename,path):
	dirPath=os.path.join(SchemasDir,path)
	if os.path.exists(dirPath):
		log.info("Found corresponding directory %s in target Schemas dir" %(dirPath[lenSchemasDir:]))
		schemas=[name for name in os.listdir(dirPath.rpartition('/')[0]) 
				if name.rpartition('.xsd')[0].startswith(filename.rpartition('.xsd')[0]) 
					and operator.contains(name.rpartition('.xsd')[0],filename.rpartition('.xsd')[0])]
		log.info("Found %s file(s) that are similar to %s in dir %s" %(len(schemas),filename,dirPath))
		i=0
		while i < len(schemas):
			log.info('Schema found %s.' %(schemas[i]))
			trunkSchemaFilePath=os.path.join(SVNTrunkSchemas,path)
			schemaDirFilePath=os.path.join(dirPath.rpartition('/')[0],schemas[i])
			log.info('Comparing %s and %s' %(trunkSchemaFilePath,schemaDirFilePath))
			compare.checkSum(trunkSchemaFilePath,schemaDirFilePath)
			i+=1


def visitfile(filenamepath):
	filename=os.path.basename(filenamepath)
	dirPath=filenamepath.rpartition('/')[0]
	log.debug('Current directory path :: %s' %(dirPath))
	findFile(filename,filenamepath[lenSVNTrunkSchemas:])

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


try:
	if not os.path.isdir(SchemasDir):
		log.error("No directory found %s" %SchemasDir)
		raise
	else:
		log.info('Walking through Trunk SharedSchemas directory: %s' %SVNTrunkSchemas)
		walktree(SVNTrunkSchemas)
		
except Exception,e:
	log.error('Exception occurred while processing main program %s' %e)
	raise

log.info("<--------------------------------END----------------------------------->\n")