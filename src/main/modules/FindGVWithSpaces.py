import os, operator, re
def findgvs (projpath, outputfile):
     try:
          regex = r".*\S.*"
          fw = open(outputfile,"w")
          for root, dirs, files in os.walk(projpath):
               for file in files:
                    filepath = os.path.join(root, file)
                    if operator.contains(filepath,"defaultVars"):
                         newGVset = 1
                         gvname = ""
                         with open(os.path.join(root, file), "r") as gvf:
                              for line in gvf:
                                   #print(line)
                                   #print(newGVset)
                                   #print(gvname)
                                   if operator.contains(line,"<globalVariable>"):
                                        #print("in")
                                        newGVset = 0
                                   elif (operator.contains(line,"<name>") and newGVset == 0):
                                        line = line.strip()
                                        endpos = line.find("</name>")
                                        gvname = line[6:endpos]
                                        #print("in1%s"%line)
                                   elif (operator.contains(line,"<value>") and newGVset == 0):
                                        line = line.strip()
                                        endpos = line.find("</value>")
                                        gvValue = line[7:endpos]
                                        #print("in2%s"%line)
                                        if (re.search(regex,gvValue)is None and operator.ne(gvValue,"")):
                                             gvpath = gvf.name[:gvf.name.find("defaultVars.substvar")]
                                             fw.write('%s%s = "%s"'%(gvpath,gvname,gvValue))
                                             fw.write('\n')
                                             #print('%s%s = "%s"'%(gvpath,gvname,gvValue))
                                   elif operator.contains(line,"</globalVariable>"):
                                        #print("in3")
                                        newGVset = 1
     except Exception as e:
          print("Exception: %s" %e)
     finally:
          fw.close()

