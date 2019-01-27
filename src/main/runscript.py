#!/usr/bin/python
import sys,os,datetime, csv, fileinput as file, logging as log ,re,copyme,operator,errno

#log.config.fileConfig('../../config/logging.conf')
log.basicConfig(filename='TIBCO_SVN_NewTrunk.log',level=log.INFO,format="%(asctime)-15s:%(name)s:%(process)d:%(levelname)s:%(message)s")
# create logger
log=log.getLogger('TIBCO_SVN_NewTrunk')

#dt=datetime.datetime.now()
log.info("<-------------------------------START---------------------------------->\n")

## Load command line argument to variable.
arg=sys.argv[1:];

## Check for command line argument.
if (len(arg) < 1):
	log.error("At least 1 argument is expected.")

## Check csv file exists.
if (not os.path.isfile(arg[0])):
	log.error("File does not exist.")

## Function to read csv file in to array.
def readFile(filename):
	f=open(filename)
	reader= csv.reader(f) #csv is a package for reading csv files.
	array=list(reader)
	log.debug("List of archive and project names:\n %s" % array)
	return array
#	log.info("List of archive and project names are loaded in to array.")

def findDir(archive,domaindir):
	for dir in os.listdir(domaindir):
		if dir.startswith(archive) and operator.contains(dir,"root"):
			rootdir=os.path.normpath(dir)
			return rootdir
		
	
def visitfile(file,lenrootdir,projectdir,From):
   # log.info('File visiting :: %s' %file)
    lenrootdir=lenrootdir+len('1')
    fileDir=file[lenrootdir:] ## filePath starting from root dir.
    if operator.eq('dir',From):
        parDir=fileDir.rpartition('/')[0] ## abs path for file starting from root dir.
       # log.info("File directory :: %s" %pardir)
    	newfile=open(projectdir+'/mkdirfile.sh', 'a+',0777)
    	if (len(parDir)>0):
    		parDir=re.sub(r' ','\\ ',parDir) # handle whitespace in directory names.
    		newfile.write("mkdir -p %s\n" %parDir)
    		newfile.close()
    else:
    	rootDir=file[17:lenrootdir]
    	parDir=fileDir.rpartition('/')[0]
    	filename=os.path.basename(fileDir)
    #	log.info('%s :: %s :: %s' %(rootDir,parDir,filename))
    	copyme.copy_file(rootDir,parDir,projectdir,filename)


def walktree(top, visitfile,lenrootdir,projectdir,From):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''
    for f in os.listdir(top):
        pathname = os.path.join(top, f)
        if os.path.isdir(pathname):
           # It's a directory, recurse into it
            walktree(pathname, visitfile,lenrootdir,projectdir,From)
        elif os.path.isfile(pathname):
            # It's a file, call the callback function
            visitfile(pathname,lenrootdir,projectdir,From)
        else:
            # Unknown file type, print a message
            log.info('Skipping %s' % pathname)


def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

def createDirs(projectdir):
	cwd=os.getcwd()
	os.chdir(os.path.abspath(projectdir))
	os.system('./mkdirfile.sh')
	log.info('All BW directories required under Project %s are created.' %projectdir)
	os.chdir(cwd)
'''	f = open("mkdirfile.sh", "r")
	lines = set(f.readlines())
	for line in lines:
		try:
			if not os.path.isdir(line):
			#	log.info("Creating director :%s" %line)
				os.system("mkdir -p %s"%line)
		except OSError,e:
			if e.errno != errno.exists():
				raise'''


array=[]
apps=readFile(arg[0])
BWProject="target/BWProjects"
datafilesdir="target/dataFiles"

## Main program execution
try:
	for archive,project in apps:
		#project=re.sub(r'.*TIBCODEV2\\','',p) #re.sub is used from 're' package which acts like replace
		projectdir=BWProject+'/'+project
		if not os.path.exists(projectdir):
			os.makedirs(projectdir)
			log.info("Project directory created --> %s" %projectdir)
		machines=os.listdir(datafilesdir)
		log.info("List of machines in %s are %s" %(datafilesdir,machines))
		for machine in machines:
			log.info("Machine :: %s || Archive :: %s || Project :: %s" % (machine,archive,project))
			machinedir=datafilesdir+"/"+machine
			domains=get_immediate_subdirectories(machinedir)
			for domainname in domains: 
				domaindir=(os.path.join(machinedir,domainname))	
				log.info("Domain dir in machine %s is %s" %(machine,domainname))
				rd=findDir(archive,domaindir)
				if operator.ne(str(rd),'None'):
					rootdir=os.path.join(domaindir,rd)
					log.info("Root directory found :: %s" %(rootdir))
					lenrootdir=len(rootdir)
					walktree(rootdir,visitfile,lenrootdir,projectdir,'dir') ## creating directories in BW project
					createDirs(projectdir)
					walktree(rootdir,visitfile,lenrootdir,projectdir,'files') ## copying files to BW project.
				else:
					log.info("%s Not found" %archive)
except Exception,e:
    log.error("Exception found while processing :: '%s'" %e)
		
		
	
log.info("<--------------------------------END----------------------------------->\n")
