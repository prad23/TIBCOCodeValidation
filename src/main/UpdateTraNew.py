  import os, operator, re
def updatetra(oldset, newset, outputfile):
  try:
    dict_linesfromoldtra={}
    lst_startstringstobecompied=["EnableMemorySavingMode","java.heap.size","MaxJobs.","FlowLimit.","Engine.ThreadCount","EnableOnStartup.","java.thread.stack.size"]
    linesafterrepo = []
    print("in")
    for root, dirs, files in os.walk(newset):
      for file in files:
        print(file)
        if file.endswith(".tra"):
          print(file)
          filepath = os.path.join(root,file)
          newdir = os.path.join(outputfile,root.split(os.sep)[-1])
          if not os.path.exists(newdir):
            os.makedirs(newdir) 
          fw = open(os.path.join(outputfile,root.split(os.sep)[-1],file),"w")
          with open(os.path.join(oldset, root.split(os.sep)[-1], file), "r") as oldtra:
            repoURLInd = 1
            for oldtraline in oldtra:
              for startlinestring in lst_startstringstobecompied:
                if oldtraline.find(startlinestring)==0:
                  dict_linesfromoldtra[oldtraline.split("=")[0]]= oldtraline
              if oldtraline.find("tibco.repourl")==0:
                repoURLInd = 0;
              elif repoURLInd ==0:
                linesafterrepo.append(oldtraline)
            #print(dict_linesfromoldtra)
          with open(os.path.join(root, file), "r") as newtra:
            repoURLInd = 1
            for newtraline in newtra:
              replacedfromoldInd = 1
              for startlinestring in lst_startstringstobecompied:
                #print("newtraline: "+newtraline)
                #print(newtraline.find(startlinestring)==0)
                if newtraline.find(startlinestring)==0:
                  #print(dict_linesfromoldtra[newtraline.split("=")[0]])
                  fw.write(dict_linesfromoldtra[newtraline.split("=")[0]])
                  replacedfromoldInd = 0
              if newtraline.find("tibco.repourl")==0:
                repoURLInd = 0
                fw.write(newtraline)
              elif replacedfromoldInd == 0:
                pass
              elif repoURLInd ==0:
                for oldtralastline in linesafterrepo:
                  fw.write(oldtralastline)
              else:
                fw.write(newtraline)
          for oldtralastline in linesafterrepo:
            fw.write(oldtralastline)
          dict_linesfromoldtra={}
          linesafterrepo = []
  except Exception as e:
    print("Exception: %s" %e)
if __name__ == "__main__":
  import sys
  print("This %s" %sys.argv[0])
  updatetra(sys.argv[1],sys.argv[2],sys.argv[3])
