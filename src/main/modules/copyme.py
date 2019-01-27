import os,shutil,compare,fileinput as file,logging as log,operator
from shutil import copytree,copy2,copystat

#log.config.fileConfig('../../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
log = log.getLogger('TIBCO_SVN_NewTrunk_CopyMe')

def copy_file(rootdir,parDir, projectdir, filename):
    srcfile='target/dataFiles/'+rootdir+parDir+'/'+filename
    dstfile=projectdir+'/'+parDir+'/'+filename
    try:
        if not os.path.exists(dstfile):
            copy(srcfile,dstfile)
        elif os.path.exists(dstfile):
            if operator.contains(srcfile,'substvar') and operator.contains(dstfile,'substvar'):
                compare.filter(srcfile,dstfile)
                copy(srcfile,dstfile)
            else:
                compare.checkSum(srcfile,dstfile)
                copy(srcfile,dstfile)
    except Exception,e:
        log.error("Exception found while processing :: '%s'" %e)
   #return dst

def copy(srcfile,dstfile):
    log.debug('Copying file from %s to %s' %(srcfile,dstfile))
    shutil.copy2(srcfile, dstfile)
    metaDir=os.path.join(dstfile.rpartition('/')[0],'MetaDir')
    if not os.path.isdir(metaDir):
        os.mkdir(metaDir)
    f=open(os.path.join(metaDir,os.path.basename(dstfile))+'.meta','a+')
    f.write('%s\n'%srcfile)
    log.debug("Written meta file for %s in meta directory %s." %(os.path.basename(dstfile),metaDir))
    f.close()

def copy_tree(src, dst, symlinks=True, ignore=None):
    names = os.listdir(src)
    if ignore is not None:
        ignored_names = ignore(src, names)
    else:
        ignored_names = set()

    if(not os.path.exists(dst)):
    	os.makedirs(dst)
    errors = []
    for name in names:
        if name in ignored_names:
            continue
        srcname = os.path.join(src, name)
        dstname = os.path.join(dst, name)
        try:
            if symlinks and os.path.islink(srcname):
                linkto = os.readlink(srcname)
                os.symlink(linkto, dstname)
            elif os.path.isdir(srcname):
                copytree(srcname, dstname, symlinks, ignore)
            else:
                copy2(srcname, dstname)
            # XXX What about devices, sockets etc.?
        except (IOError, os.error) as why:
            errors.append((srcname, dstname, str(why)))
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except IOError as err:
            errors.extend(err.args[0])
    try:
        copystat(src, dst)
   # except WindowsError:
        # can't copy file access times on Windows
        pass
    except OSError as why:
        errors.extend((src, dst, str(why)))