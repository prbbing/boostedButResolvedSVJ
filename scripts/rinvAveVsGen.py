import os,sys
from math import *
from ROOT import *
from array import array

massList = ["Z1000_JetISR500","Z500_GammaISR150"]
signalList = ["rinv0p1", "rinv0p5", "rinv0p9"]
rinvList = ["rinv_xy_ave", "rinv_xy_ave_maos"]

def getHist(file,hname,proc,mrange=None,mvar=None):
    cname = proc
    if mrange is not None:
        cname += "_"+mvar
    hist = file.Get(hname).Clone(cname)
    if mrange is not None:
        b1 = hist.GetYaxis().FindBin(mrange[0])
        b2 = hist.GetYaxis().FindBin(mrange[1])
        hist = hist.ProjectionX(proc, b1, b2)
    if not hname.startswith("rT"):
        hist.Rebin(2)
    return hist

rinv_vals = [float(s[-3:].replace('p','.')) for s in signalList]
for mass in massList:
    print(mass)
    points = {}
    outf = TFile("rinvAveVsGen_"+mass+".root", "RECREATE")
    for signal in signalList:
        print(signal)
        sigFile = TFile("output_"+ mass + "_" + signal + ".root")
        for rinv in rinvList:
            if not rinv in points: points[rinv] = {'x': rinv_vals, 'y': [], 'ye': []}
            sigHist = sigFile.Get(rinv)
            points[rinv]['y'].append(sigHist.GetMean())
            points[rinv]['ye'].append(sigHist.GetMeanError())
    # make graphs
    for rinv in rinvList:
        points[rinv] = {k:array('d',v) for k,v in points[rinv].items()}
        g = TGraphErrors(len(signalList), points[rinv]['x'], points[rinv]['y'], nullptr, points[rinv]['ye'])
        g.SetName(rinv)
        outf.cd()
        g.Write()
    outf.Close()
