import os,sys
from XS import crossSections

isrs = {
  "150"   : 0.17, 
}

weight = {
  "150"   : 0.491,
}

rinvs = ["0p1", "0p5", "0p9"]

for rinv in rinvs:
    print(rinv)
    for isr in isrs:
        print(isr)
        command = "python3 delphiAnalysis_real_photon.py -i /Users/adminbingxuanliu/Library/CloudStorage/Dropbox/BoostedButResolvedSVJ/NewSignalFatJetPt50/Z500_rinv" + str(rinv) + "_ISR" + isr + ".root -o " + "output_Z500_GammaISR" + str(isr) + "_rinv" + str(rinv)  +  ".root -c -x " + str(isrs[isr]) + " -w " + str(weight[isr])
        #command = "python3 delphiAnalysis_real_photon.py -i /Users/adminbingxuanliu/Library/CloudStorage/Dropbox/BoostedButResolvedSVJ/NewSignalFatJetPt50/Z500_rinv" + str(rinv) + "_ISR" + isr + ".root -o " + "output_Z500_GammaISR" + str(isr) + "_rinv" + str(rinv)  +  "_yStar0p8_rT0p4.root -c -x " + str(isrs[isr])
        os.system(command)

