#!/usr/bin/python
import sys, os, operator, re

def listgvs (prodset, stagedset, outputfile):
    try:
        for root, dirs, files in os.walk(prodset):
            for file in files:
                print file, os.path.join(stagedset,file)
                if operator.contains(file,".xml") and os.path.isfile(os.path.join(stagedset,file)): # file exists in both Prod and Staged
                    namevaledict={}
                    filepath = os.path.join(root, file)
                    #pathSep = os.path.sep
                    #onefolderup = root.split(pathSep)[1]
                    fw = open(os.path.join(outputfile,file+'.txt'),"w")
                    newGVset = 1
                    gvname = ""
                    with open(os.path.join(root, file), "r") as gvf:
                        for line in gvf:
                            if operator.contains(line,"<NameValuePair"):
                                newGVset = 0
                            elif (operator.contains(line,"<name>") and newGVset == 0):
                                line = line.strip()
                                endpos = line.find("</name>")
                                gvname = line[6:endpos]
                            elif (operator.contains(line,"<value>") and newGVset == 0):
                                line = line.strip()
                                endpos = line.find("</value>")
                                gvValue = line[7:endpos]
                                namevaledict[gvname] = gvValue
                            elif operator.contains(line,"</NameValuePair"):
                                newGVset = 1
                    with open(os.path.join(stagedset, file), "r") as gvf:
                        fw.write('GV~GV Value in PROD XML~GV Value in Staged XML~Reason')
                        fw.write('\n')
                        for line in gvf:
                            if operator.contains(line,"<NameValuePair"):
                                newGVset = 0
                            elif (operator.contains(line,"<name>") and newGVset == 0):
                                line = line.strip()
                                endpos = line.find("</name>")
                                gvname = line[6:endpos]
                            elif (operator.contains(line,"<value>") and newGVset == 0):
                                line = line.strip()
                                endpos = line.find("</value>")
                                gvValue = line[7:endpos]
                                if (gvname in namevaledict and namevaledict[gvname] != gvValue):
                                    fw.write('%s~%s~"%s"~GV Present in Both XMLs but not matching'%(gvname,namevaledict[gvname],gvValue))
                                    fw.write('\n')
                                    del namevaledict[gvname]
                                elif (gvname in namevaledict and namevaledict[gvname] == gvValue):
                                    del namevaledict[gvname]
                                elif not(gvname in namevaledict):
                                    fw.write('%s~%s~"%s"~GV not present in PROD XML'%(gvname,"",gvValue))
                                    fw.write('\n')
                            elif operator.contains(line,"</NameValuePair"):
                                newGVset = 1
                    for k,v in namevaledict.items():
                        fw.write('%s~%s~"%s"~GV not present in Staged XML'%(k,v,""))
                        fw.write('\n')
    except Exception as e:
        print("Exception: %s" %e)


arg = sys.argv[1:]
def main():
    if (not(os.path.isdir(arg[2]))):
        os.makedirs(arg[2])
    listgvs(arg[0], arg[1], arg[2])

if __name__=='__main__':
    main()
