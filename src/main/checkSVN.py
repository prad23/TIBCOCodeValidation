#!/usr/bin/python
import sys,os,datetime, csv, fileinput as file, logging as log ,re,copyme,operator,errno,compare

#log.config.fileConfig('../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_Check_NewTrunk.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
# create logger
log=log.getLogger('TIBCO_SVN_Check_NewTrunk')

log.info("<-------------------------------START---------------------------------->")

BWProject="target/BWProjects"
SVNTrunkDir="target/BWSVNTrunk"

## Main program execution
try:
	for dir in os.listdir(SVNTrunkDir):
		SVNProjectDir=SVNTrunkDir+'/'+dir
		log.info('SVN directory visiting: %s' %SVNProjectDir)
		log.info('Checking for %s in %s.'%(dir,BWProject))
		NewTrunkDir=os.path.join(BWProject,dir)
		if os.path.exists(NewTrunkDir):
			log.info("Found corresponding %s in %s " %(dir,NewTrunkDir))
			compare.compareDirs(SVNProjectDir,NewTrunkDir)
		else:
			log.info("%s Not found in %s" %(dir,NewTrunkDir))
		
except Exception,e:
	log.error("Exception occurred while processing checkSVN script execution %s" %e)
	raise
		
	
log.info("<--------------------------------END----------------------------------->\n")
