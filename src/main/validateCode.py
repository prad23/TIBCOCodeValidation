#!/usr/bin/python
import sys
sys.path.append("./modules")
#print(sys.path)
import os, datetime, csv, fileinput as file, logging as log, operator, compare, extract

# log.config.fileConfig('../../config/logging.conf')
log.basicConfig(filename='TIBCO_Code_Validation.log', level=log.INFO,
                format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
# create logger
log = log.getLogger(__name__)

log.info("<-------------------------------START---------------------------------->")

arg = sys.argv[1:]


def findHtmlFiles(dirPath):
    for root, dir, files in os.walk(dirPath):
        for file in files:
            if operator.contains(file, ".html"):
                log.info("Found html file at %s: "%(os.path.join(root, file)))
                print("HTML file path: %s" % os.path.abspath(os.path.join(root, file)))


def dirExecute(dir1, dir2):
    try:
        for dir in os.listdir(dir2):
            SVNProjectDir = dir2 + '/' + dir
            log.info('SVN directory visiting: %s' % SVNProjectDir)
            log.info('Checking for %s in %s.' % (dir, dir1))
            NewTrunkDir = os.path.join(dir1, dir)
            if os.path.exists(NewTrunkDir):
                log.info("Found corresponding %s in %s " % (dir, NewTrunkDir))
                compare.compareAllDirs(SVNProjectDir, NewTrunkDir)
            else:
                log.info("%s Not found in %s" % (dir, NewTrunkDir))
        findHtmlFiles(dir1)

    except Exception as e:
        log.error("Exception occurred while listing and comparing directories: %s" % e)
        raise


def validateArchive(dir):
    try:
        #print dir
        dirname = []
        for file in os.listdir(dir):
            filePath=os.path.join(dir,file)
            if operator.contains(filePath,".ear") or operator.contains(filePath,".aar"):
                log.info("Archive file path is %s " %filePath)
                dir1 = extract.extractEars(dir, filePath)
                dirname.append(dir1)
                log.info("Archive file extracted to dir: %s"%dir1)
            elif (operator.contains(filePath,".zip")):
                log.info("Zip file path is %s " % (filePath) )
                dir1 = extract.extractZip(dir, filePath)
                dirname.append(dir1)
                log.info("ZIP file extracted to dir: %s" % dir1)
      # print dirname[0],dirname[1]
        compare.compareAllDirs(dirname[0],dirname[1])
        findHtmlFiles(dir)
    except Exception as e:
        log.error ("Error occurred while extracting Archive: %s" % e)
        raise


# Main program execution
def main():
    """
	@author: PGODAVARTHI
	@description: Compared ear files in a directory or take directories and does the comparision.
	-----
	Parameters:
	1. Ear files Directory
	or
	2. 2 BW directories
	"""
    if operator.eq(len(arg),1):
        validateArchive(arg[0])
    elif operator.eq(len(arg),2):
        dirExecute(arg[0], arg[1])
    else:
        raise Exception("Check your arguments. This program only accepts EAR files directory or Directories as arguments.")


if __name__ == '__main__':
    main()

log.info("<--------------------------------END----------------------------------->\n")
