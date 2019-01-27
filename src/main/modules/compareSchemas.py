import sys, os, time, difflib, operator,logging as log,filecmp,re,errno,regex,md5,copymeSchemas as copy

#log.config.fileConfig('../../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk_Schemas.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
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
        if operator.contains(fromFile,'SharedSchemas'):
            svnTrunkReportDir='target/svnTrunkHTMLReports_Schemas'
            htmlDir=os.path.join(svnTrunkReportDir,fromFile.rpartition('/')[0][18:])
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
        filename=os.path.basename(fromFile)
        srcPath=fromFile.rpartition('/')[0]
        dstPath=toFile.rpartition('/')[0]
        metaDir=os.path.join(dstPath,'MetaDir')
        log.info('%s already exists in target directory %s, so comparing files.' %(filename,dstPath))
        if not filecmp.cmp(fromFile,toFile):
            log.info("Found difference between schemas in %s and %s. Checking checksum in Meta dir %s." %(fromFile,toFile,metaDir))
            metaFile=os.path.join(metaDir,filename+'.meta')
            metaFileLines=open(metaFile,'r').readlines()
            md5CheckSum=md5.new(open(fromFile,'rb').read()).hexdigest()
            count=len([line for line in metaFileLines if operator.contains(line,md5CheckSum)])
            if operator.ge(count,1):
                log.info('Ignoring writing meta information to %s for %s since found same checksum' %(metaDir,filename))
            else:
                copy.copy2(fromFile,toFile)
        else:
            log.info("No difference found between files %s and %s." %(fromFile,toFile))
            NoDiffReport=os.path.join(dstPath,'NoDiffReport')
            txtDir=os.path.join(NoDiffReport,fromFile.rpartition('/')[0][7:])
            if not os.path.isdir(txtDir):
                os.makedirs(txtDir)
            f=open(os.path.join(txtDir,os.path.basename(fromFile))+'.txt','a')
            f.write('%s :IDENTICAL: %s \n'%(fromFile,toFile))
            f.close()
    except Exception,e:
        log.error("Exception found while comparing checksum :: '%s'" %e)
        raise
        
