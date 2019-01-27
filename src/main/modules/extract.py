import os, operator, re, logging as log
from pyunpack import Archive
log = log.getLogger(__name__)


def extractEars(dir, earFilePath):
    try:
        #print earFilePath,Dir
        #if not os.path.isdir("target/Validation"):
        #    os.mkdir("target/Validation")
        if(operator.contains(earFilePath,".ear")):
            earDir = os.path.join(dir,os.path.basename(earFilePath).rpartition(".ear")[0])
        elif(operator.contains(earFilePath,".aar")):
            earDir = os.path.join(dir, os.path.basename(earFilePath).rpartition(".aar")[0])
        print ("EAR directory created: %s" %earDir)
        if not os.path.isdir(earDir):
            os.mkdir(earDir)
        Archive(earFilePath).extractall(earDir)
        log.info("Extracted %s to %s"%(earFilePath,earDir))
        for file in os.listdir(earDir):
            #print file
            if operator.contains(file, ".xml"):
                xmlPath = os.path.join(earDir, file)
                newXmlPath = os.path.join(earDir, "defaultVars.substvar")
                log.info("Found xml file in %s, it is renamed to %s" %(earDir,newXmlPath))
                os.rename(xmlPath, newXmlPath)
        for file in os.listdir(earDir):
            if operator.contains(file,".par") or operator.contains(file,".sar"):
                #print file
                filePath=os.path.join(earDir,file)
                Archive(filePath).extractall(earDir)
                log.info("Extracted %s to %s" %(filePath,earDir))
                os.remove(filePath)
        return earDir
    except Exception as e:
        log.error('Exception occurred while processing %s' % e)
        raise


def extractZip(dir, dirFilePath):
    try:
        zipDir = os.path.join(dir,os.path.basename(dirFilePath).rpartition(".zip")[0])
        if not os.path.isdir(zipDir):
            os.mkdir(zipDir)
        Archive(dirFilePath).extractall(zipDir)
        log.info("Extracted %s to %s" %(dirFilePath, zipDir))
        return zipDir
    except Exception as e:
        print("Error file extracting zip %s" % e)
        raise
