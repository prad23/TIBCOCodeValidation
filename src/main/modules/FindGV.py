import os, operator, re
def getgv(dirpath,gv):
     try:
          file=dirpath
          gvValue=""
       #  print file
          if not operator.contains(dirpath,'.xml'):
               file=dirpath+'/'+'defaultVars.substvar'
          #print file
          with open(file,"r") as gvf:
               for line in gvf:
                    #print(line)
                    if operator.contains(line,gv):
                         line = line.strip()
                         endpos = line.find("</name>")
                         gvname = line[6:endpos]
                        # print("gvname %s"%gvname)
                         if operator.eq(gvname,gv):
                              value=next(gvf).strip()
                              #print value
                              endpos = value.find("</value>")
                              gvValue = value[7:endpos]
                              #print gvValue
                              return gvValue
          return gvValue
     except Exception as e:
          print("FindGV Exception: %s" %e)
