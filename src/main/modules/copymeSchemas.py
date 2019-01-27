import os,shutil,compareSchemas as compare,logging as log,operator,md5

#log.config.fileConfig('../../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk_Schemas.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
log = log.getLogger('TIBCO_SVN_NewTrunk_CopyMeSchemas')

def copy_file(filename,srcPath,dstPath):
    try:
        log.info('%s,%s,%s'%(filename,srcPath,dstPath))
        srcFilePath=srcPath.rpartition('/')[0]
        lenPath=len(srcFilePath.rpartition('_root/')[0])+6
        dstFullPath=srcFilePath[lenPath:]
        dstFile=os.path.join(os.path.join(dstPath,dstFullPath),filename)
        if not os.path.isdir(os.path.join(dstPath,dstFullPath)):
            os.makedirs(os.path.join(dstPath,dstFullPath))
        if not os.path.isfile(dstFile):
            copy(srcPath,dstFile)
        else:
            compare.checkSum(srcPath,dstFile)
    except Exception,e:
        log.error("Exception found while processing copy_file function :: '%s'" %e)
        raise

def writeMeta(MetaDir,srcFile,dstFile):
    f=open(os.path.join(MetaDir,os.path.basename(dstFile))+'.meta','a+')
    f.write('%s,%s\n'%(srcFile,md5.new(open(srcFile,'rb').read()).hexdigest()))
    log.debug("Writing meta file with md5 checksum for %s in meta directory %s." %(os.path.basename(dstFile),MetaDir))
    f.close()

def copy(srcfile,dstfile):
    log.debug('Copying file from %s to %s' %(srcfile,dstfile))
    shutil.copyfile(srcfile, dstfile)
    metaDir=os.path.join(dstfile.rpartition('/')[0],'MetaDir')
    if not os.path.isdir(metaDir):
        os.mkdir(metaDir)
    f=open(os.path.join(metaDir,os.path.basename(dstfile))+'.meta','a+')
    f.write('%s,%s\n'%(srcfile,md5.new(open(srcfile,'rb').read()).hexdigest()))
    log.debug("Written meta file for %s in meta directory %s." %(os.path.basename(dstfile),metaDir))
    f.close()

def copy2(srcfile,dstfile):
    metaDir=os.path.join(dstfile.rpartition('/')[0],'MetaDir')
    if not os.path.isdir(metaDir):
        os.mkdir(metaDir)
    srcfilename=os.path.basename(srcfile)
    count=len([name for name in os.listdir(dstfile.rpartition('/')[0]) if operator.contains(name,srcfilename.rpartition('.xsd')[0])])
    if operator.gt(count,0):
        log.info('Copying file from %s to %s' %(srcfile,dstfile))
        count+=1
        dstfilenamepath=dstfile.rpartition('.xsd')[0]+'_'+str(count)+'.xsd'
        shutil.copyfile(srcfile,dstfilenamepath)
        writeMeta(metaDir,srcfile,dstfile)