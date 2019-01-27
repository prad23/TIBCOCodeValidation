import sys, os, time, difflib, operator,logging as log,filecmp,re,errno,regex

#log.config.fileConfig('../../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk_CheckSchemas.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
log = log.getLogger('TIBCO_SVN_NewTrunk_SchemaCompare')


def cleanupDirs(directory):
    log.info('Cleaning up directory %s.'%directory)
    if not os.listdir(directory):
        os.rmdir(directory)
        cleanupDirs(directory.rpartition('/')[0])

def writeReport(file,filenamepath,diff,htmlFile,htmlDir):
    try:
        if not os.path.isdir(htmlDir):
            os.mkdir(htmlDir)
        f=open(os.path.join(htmlDir,os.path.basename(filenamepath)),'w')
        log.info("Writing HTML report for file %s in HTML report dir %s " %(file,htmlDir))
        f.write(diff)
        if operator.contains(os.path.basename(filenamepath),'substvar'):
            htmlFilePath=os.path.join(htmlDir,os.path.basename(filenamepath))
            finalOutFile=os.path.join(htmlDir,file+'_final.html')
            regex.reSub(htmlFilePath,finalOutFile)
            log.info('Final version after applying filter on modTime and passwords: %s'%finalOutFile)
            os.remove(os.path.join(htmldir,os.path.basename(filenamepath)))
        if operator.contains(htmlDir,'svn') or operator.contains(htmlDir,'Schemas'):
            log.info('Now cleaning up html report %s to show real differences' %htmlFile)
            regexNext='<a href.*?>n</a>'
            exists=0
            with open(htmlFile,'U\r\n') as f:
                for line in f:
                    if re.search(regexNext,line)is not None:
                        exists+=1
            if operator.eq(exists,0):
                log.info('Could not find any other difference apart from namespace, hence deleting file %s' %htmlFile)
                os.remove(htmlFile)
                cleanupDirs(htmlFile.rpartition('/')[0])
    except Exception,e:
        log.error("Exception found while writing HTML Report :: '%s'" %e)
        raise
    finally:
         f.close()

def compareFiles(fromFile,toFile,type):
    try:
        # we're passing these as arguments to the diff function
        fromdate = time.ctime(os.stat(fromFile).st_mtime)
        todate = time.ctime(os.stat(toFile).st_mtime)
        fromlines = open(fromFile, 'U').readlines()
        tolines = open(toFile, 'U').readlines()

        if operator.eq(type,'unified'):
            diff = difflib.unified_diff(fromlines, tolines, fromFile, toFile,
                                        fromdate, todate, n=3)
        elif operator.eq(type,'ndiff'):
            diff = difflib.ndiff(fromlines, tolines)
        elif operator.eq(type,'html'):
            diff = difflib.HtmlDiff().make_file(fromlines, tolines, fromFile,
                                                toFile, context=False,
                                                numlines=5)
        else:
            diff = difflib.context_diff(fromlines, tolines, fromFile, toFile,
                                        fromdate, todate, n=3)

        filename=os.path.basename(toFile)
        if operator.contains(fromFile,'Schemas'):
            svnTrunkReportDir='target/svnTrunkHTMLReports_Schemas_v1'
            htmlDir=os.path.join(svnTrunkReportDir,fromFile.rpartition('/')[0][15:])
            if not os.path.isdir(htmlDir):
                os.makedirs(htmlDir)
        else:
            htmlDir=os.path.join(toFile.rpartition('/')[0],'HTMLReports')
        htmlFile=os.path.join(htmlDir,filename+'.html')
        if not os.path.isfile(htmlFile):
            log.info('logging file %s'%htmlFile)
            writeReport(filename,toFile+'.html',diff,htmlFile,htmlDir)
        else:
            count=len([name for name in os.listdir(htmlDir) if operator.contains(name,filename)])
            if operator.ge(count,0):
                count+=1
                log.info("count of %s ::: %s" %(filename,count))
                writeReport(filename,toFile+'_'+str(count)+'.html',diff,htmlFile,htmlDir)
    except Exception,e:
        log.error('Exception occurred while processing compareFiles %s' %e)
        raise

def checkSum(fromFile,toFile):
    try:
        log.debug("Comparing checksum between %s and %s" %(fromFile,toFile))
        if not filecmp.cmp(fromFile,toFile):
            log.info("Found difference between files %s and %s. Will do a diff and generate a report." %(fromFile,toFile))
            compareFiles(fromFile,toFile,'html')
    except Exception,e:
        log.error("Exception found while comparing checksum :: '%s'" %e)

def filter(fromFile,toFile):
    log.info("About to filter modTime and password for files %s and %s " %(fromFile,toFile))
    cmp1=regex.replace(fromFile,'a')
    cmp2=regex.replace(toFile,'b')
    log.info('Comparing files %s and %s' %(cmp1,cmp2))
    if not filecmp.cmp('temp_a.txt','temp_b.txt'):
        checkSum(fromFile,toFile)
    os.remove('temp_a.txt')
    os.remove('temp_b.txt')

def compareDirs(srcDir,dstDir): #this function is only being used in checking SVNTrunk vs Production Trunk
    try:
        log.info("Comparing svn dir %s and new Trunk dir %s" %(srcDir,dstDir))
        dcmp=filecmp.dircmp(srcDir,dstDir)
        for name in dcmp.diff_files:
            if operator.contains(name,'.xsd'):
                log.info("Differences found for %s between %s and %s "%(name,dcmp.left,dcmp.right))
                srcFile=os.path.join(dcmp.left,name)
                dstFile=os.path.join(dcmp.right,name)
                compareFiles(srcFile,dstFile,'html')
        for subdcmp in dcmp.subdirs.values():
            compareDirs(subdcmp.left,subdcmp.right)
    except Exception,e:
        log.error('Exception occurred while comparing directories. %s' %e)
        raise