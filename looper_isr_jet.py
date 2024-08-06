import os,sys
from XS import crossSections

# indexing: Zprime mass, pt range

isrs = {
  1000: {
    "0to100"   : 44.1,
    "100to200" : 5.9,
    "200to300" : 1.86,
    "300to400" : 0.75,
    "400to500" : 0.37,
    "500toinf" : 0.42,
  },
  500: {
    "0to100"   : 352.8,
    "100to200" : 31.02,
    "200to300" : 8.35,
    "300to400" : 2.86,
    "400to500" : 1.14,
    "500toinf" : 1.00,
  }
}

weight = {
  1000: {
    "0to100"   : 0.60,
    "100to200" : 1.141,
    "200to300" : 1.821,
    "300to400" : 1.715,
    "400to500" : 2.613,
    "500toinf" : 4.97,
  },
  500: {
    "0to100"   : 1.18,
    "100to200" : 1.08,
    "200to300" : 1.11,
    "300to400" : 1.10,
    "400to500" : 1.06,
    "500toinf" : 1.09,
  }
}

if "bing" in os.environ["USER"]:
  sample_dir = "/Users/adminbingxuanliu/Library/CloudStorage/Dropbox/BoostedButResolvedSVJ/NewSignalFatJetPt50/"
  flags = "-c"
else:
  sample_dir = "../"
  flags = "--presel"
masses = [500, 1000]
rinvs = ["0p1", "0p5", "0p9"]

for mass in masses:
  print(mass)
  for rinv in rinvs:
    print(rinv)
    for isr in isrs[mass]:
      print(isr)
      command = "python3 delphiAnalysis_final_jet.py -i "+sample_dir+"Z"+str(mass)+"_rinv" + str(rinv) + "_JetISR" + isr + ".root -o " + "output_Z"+str(mass)+"_JetISR" + str(isr) + "_rinv" + str(rinv)  +  ".root "+flags+" -x " + str(isrs[mass][isr]) + " -w " + str(weight[mass][isr])+" -y 0.8"
      os.system(command)
