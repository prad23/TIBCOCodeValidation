import fileinput,re,errno,operator

def reSub(fileInput,fileOutput):
    target=open(fileOutput,'w+b')
    target.truncate()
    try:
        for line in fileinput.input(fileInput):
            regex='<a(.*?)</a>|<span class=\"diff_sub\">|</span>|<span class="diff_chg">|<span class="diff_add">'
            if "modTime" in line:
                line=re.sub(r'%s'%regex, r'', line.rstrip())
                target.write(line)
            elif re.search(r'#!.*?==',line)is not None:
                line=re.sub(r'%s'%regex, r'', line.rstrip())
                target.write(line)
            else:
                target.write(line)
        target.close()
        
    except IOError:
        raise

def replace(file,char):
    outfile=open('temp_%s.txt'%char,'w')
    outfile.truncate()
    for line in open(file).readlines():
        if operator.contains(line,'modTime'):
        #    log.info('present :%s' %line)
            line=re.sub(r'<modTime>(.*)</modTime>','<modTime>1111</modTime>',line)
        #    log.info(line)
            outfile.write(line)
        elif operator.contains(line,'#!'):
        #    log.info('present :%s' %line)
            line=re.sub(r'<value>(.*)</value>','<value>password</value>',line)
        #    log.info(line)
            outfile.write(line)
        else:
           #log.info('not present %s' %line)
            outfile.write(line)
    return outfile
