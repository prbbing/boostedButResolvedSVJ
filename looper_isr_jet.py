import os,sys
from XS import crossSections

# Z' 1000 GeV
isrs = {
  "0to100"   : 44.1, 
  "100to200" : 5.9,
  "200to300" : 1.86,
  "300to400" : 0.75,
  "400to500" : 0.37, 
  "500toinf" : 0.42,
}
# Z' 500 GeV
#isrs = {
#  "0to100"   : 352.8, 
#  "100to200" : 31.02,
#  "200to300" : 8.35,
#  "300to400" : 2.86,
#  "400to500" : 1.14, 
#  "500toinf" : 1.00,
#}

# Z' 1000 GeV
weight = {
  "0to100"   : 0.604, 
  "100to200" : 1.141,
  "200to300" : 1.821,
  "300to400" : 1.715,
  "400to500" : 2.613, 
  "500toinf" : 4.97,
}

# Z' 500 GeV
#weight = {
#  "0to100"   : 1.18, 
#  "100to200" : 1.08,
#  "200to300" : 1.11,
#  "300to400" : 1.10,
#  "400to500" : 1.06, 
#  "500toinf" : 1.09,
#}

rinvs = ["0p1", "0p5", "0p9"]

for rinv in rinvs:
    print(rinv)
    for isr in isrs:
        print(isr)
        command = "python3 delphiAnalysis_final_jet.py -i /Users/adminbingxuanliu/Library/CloudStorage/Dropbox/BoostedButResolvedSVJ/NewSignalFatJetPt50/Z1000_rinv" + str(rinv) + "_JetISR" + isr + ".root -o " + "output_Z1000_JetISR" + str(isr) + "_rinv" + str(rinv)  +  ".root -c -x " + str(isrs[isr]) + " -w " + str(weight[isr])
        #command = "python3 delphiAnalysis_final_jet.py -i /Users/adminbingxuanliu/Library/CloudStorage/Dropbox/BoostedButResolvedSVJ/NewSignalFatJetPt50/Z1000_rinv" + str(rinv) + "_JetISR" + isr + ".root -o " + "output_Z1000_JetISR" + str(isr) + "_rinv" + str(rinv)  +  "_yStar0p8.root -c -x " + str(isrs[isr])
        os.system(command)

