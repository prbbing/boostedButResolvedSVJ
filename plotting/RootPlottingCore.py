import os,sys,re
from pathlib import Path
from math import *
from array import *
from ROOT import *

from Cosmetics import *


######################################################################
# Function to draw ratio histogram                                   #
# relErrMax sets the threshold to merge the bins until the errors    # 
# on any bins in the ratio histograms are less than this threshold   #
######################################################################

def ratioHistogram( numHist, denHist, yLabel = "", relErrMax = 0.10, xMin = 0.0, xMax = 0.0):
  if numHist.GetNbinsX() > denHist.GetNbinsX():
    numHistTmp = denHist.Clone()
    for binNum in range(1, denHist.GetNbinsX() + 1):
      numHistTmp.SetBinContent(binNum, numHist.GetBinContent(numHist.FindBin(denHist.GetBinCenter(binNum))))
    numHist = numHistTmp.Clone()   
  if numHist.GetNbinsX() < denHist.GetNbinsX():
    denHistTmp = denHist.Clone()
    for binNum in range(1, numHist.GetNbinsX() + 1):
      denHistTmp.SetBinContent(binNum, denHist.GetBinContent(denHist.FindBin(numHist.GetBinCenter(binNum))))
    denHist = denHistTmp.Clone()   
  
  if not numHist:
      print("Error:  trying to run ratioHistogram but numHist is invalid")
      return
  if not denHist:
      print("Error:  trying to run ratioHistogram but denHist is invalid")
      return
  
  def groupR(group):
      Num,Den = [float(sum(hist.GetBinContent(i) for i in group)) for hist in [numHist,denHist]]
      return Num/Den if Den else 0
  def groupErr(group):
      Num,Den = [float(sum(hist.GetBinContent(i) for i in group)) for hist in [numHist,denHist]]
      NumErr2,DenErr2 = [sum(hist.GetBinError(i)**2 for i in group) for hist in [numHist,denHist]]
      if Num > 0 and Den > 0 and Num != Den:
        return sqrt(NumErr2/pow(Den,2) + DenErr2*pow(Num,2)/pow(Den,4))  
      else:
          return 0
  def regroup(groups):
      err,iG = max( (groupErr(g),groups.index(g)) for g in groups )
      if err < float(relErrMax) or len(groups)<3 or (float(relErrMax) < 0) : return groups
      iH = max( [iG-1,iG+1], key = lambda i: groupErr(groups[i]) if 0<=i<len(groups) else -1 )
      iLo,iHi = sorted([iG,iH])
      return regroup(groups[:iLo] + [groups[iLo]+groups[iHi]] + groups[iHi+1:])

  groups = regroup( [(i,) for i in range(1,1+numHist.GetNbinsX())] )
  ratio = TH1F("ratio","",len(groups), array('d', [numHist.GetBinLowEdge(min(g)) for g in groups ] + [numHist.GetXaxis().GetBinUpEdge(numHist.GetNbinsX())]) )
  ratio.GetXaxis().SetTitle(numHist.GetXaxis().GetTitle())
  for i,g in enumerate(groups) :
    ratio.SetBinContent(i+1,groupR(g))
    ratio.SetBinError(i+1,groupErr(g))
 
  if xMin and xMax:
    ratio.SetAxisRange(xMin,xMax,"x")
  ratio.GetYaxis().SetTitle(yLabel)
  ratio.GetYaxis().SetLabelSize(0.3)
  ratio.GetYaxis().SetNdivisions(505)
  ratio.GetXaxis().SetNdivisions(510)
  ratio.GetXaxis().SetTitle(numHist.GetXaxis().GetTitle())
  ratio.SetLineColor(1)
  ratio.SetLineWidth(2)
  return ratio

######################################################################
# Function to draw s/sqrt{b} histogram                               #
######################################################################
def sOverBHistogram( numHist, denHist, xMin = 0.0, xMax = 0.0):

  if numHist.GetNbinsX() > denHist.GetNbinsX():
    numHistTmp = denHist.Clone()
    for binNum in range(1, denHist.GetNbinsX() + 1):
      numHistTmp.SetBinContent(binNum, numHist.GetBinContent(numHist.FindBin(denHist.GetBinCenter(binNum))))
    numHist = numHistTmp.Clone()
  if numHist.GetNbinsX() < denHist.GetNbinsX():
    denHistTmp = denHist.Clone()
    for binNum in range(1, numHist.GetNbinsX() + 1):
      denHistTmp.SetBinContent(binNum, denHist.GetBinContent(denHist.FindBin(numHist.GetBinCenter(binNum))))
    denHist = denHistTmp.Clone()

  if not numHist:
      print ("Error:  trying to run sOverBHistogram but numHist is invalid")
      return
  if not denHist:
      print ("Error:  trying to run sOverBHistogram but denHist is invalid")
      return

  sig = denHist.Clone()

  for binNum in range(denHist.GetNbinsX() + 1):
    if numHist.GetBinContent(binNum):
      sig.SetBinContent(binNum, numHist.GetBinContent(binNum)/sqrt(denHist.GetBinContent(binNum)))
      sig.SetBinError(binNum, 0)
    else:
      sig.SetBinContent(binNum, 0)
      sig.SetBinError(binNum, 0)

  if xMin and xMax:
    sig.SetAxisRange(xMin,xMax,"x")
  sig.GetXaxis().SetTitle(denHist.GetXaxis().GetTitle())
  sig.GetYaxis().SetTitle("Significance")
  sig.GetXaxis().SetTitleSize(0.25)
  sig.GetYaxis().SetTitleSize(0.25)
  sig.GetYaxis().SetTitleOffset(0.4)
  sig.GetXaxis().SetTitleOffset(0.5)
  sig.GetXaxis().SetLabelSize(0.25)
  sig.GetYaxis().SetLabelSize(0.25)
  sig.SetFillColor(4)
  sig.SetLineColor(4)
  sig.GetYaxis().SetLabelSize(0.1)
  sig.SetAxisRange(-5,5,"y")

  return sig



#################################################################
# Function to draw stacked histograms                           #
# stackSources and taskSetup is defined in the run time config  #
# file                        				        #
#################################################################

def drawStackPlot(taskSetup, stackSources, outputFile):
  Xmin   =  float(taskSetup["Xmin"])
  Xmax   =  float(taskSetup["Xmax"])
  Ymin   =  float(taskSetup["Ymin"])
  Ymax   =  float(taskSetup["Ymax"])
  nameX  =  taskSetup["nameX"]
  nameY  =  taskSetup["nameY"]
  name   =  taskSetup["name"]   
  doLogy =  taskSetup["doLogy"]
  rebinFactor = taskSetup["rebinFactor"]
  doFraction  = taskSetup["doFraction"]  
  doRatio     = taskSetup["doRatio"]
  masterLabel = taskSetup["masterLabel"]
  lumi        = taskSetup["lumi"]
  cme         = taskSetup["cme"]
  relErrMax   = taskSetup["relErrMax"]
  scaleToData = taskSetup["scaleToData"]
  ratioYmin   =  taskSetup["ratioYmin"]
  ratioYmax   =  taskSetup["ratioYmax"]

  canvas = TCanvas("canvas_"+taskSetup["name"], taskSetup["name"],10,10,600,600)
  if taskSetup["doRatio"]: 
    canvas.SetFillStyle(0)
    canvas.Divide(1,2)
    canvas.cd(1)
    gPadSetup(doLogy)
  
    gPad.SetPad(0,0.2,1,1)
    gPad.SetMargin(0.15,0.05,0.01,0.07)
    gPad.SetFillStyle(0)
    gPad.Update()
    gPad.Draw()
    
    canvas.cd(2)
    gPad.SetPad(0,0,1.0,0.32)
    gPad.SetMargin(0.15,0.09,0.4,0.035)
    gPad.SetFillStyle(0)
    gPad.SetGridy(1)
    gPad.Update()
    gPad.Draw()
  else:
    canvas.SetFillStyle(0)
    canvas.Divide(1)
    canvas.cd(1)
    gPadSetup(doLogy)

  canvas.cd(1)
  gPadSetup(doLogy)
  stack = THStack("stack",name)
    
  legend = TLegend(0.7, 0.93 - 0.06*len(stackSources), 0.9, 0.93)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetFillColor(0)
  legend.SetTextSize(0.03)
  legend.SetFillStyle(0)

  normalizations = []
  normHistDic = {}
  hists = []
  totalNorm  = 0
   
  totalMCInputs = 0 
  if "data" in stackSources:
    totalMCInputs = len(stackSources) - 1
  else:
    totalMCInputs = len(stackSources)

  for element in range(0,totalMCInputs):
    stackSource = str(element + 1)
    fileName  = stackSources[stackSource]["filePath"]
    inputFile = TFile(fileName)
    if inputFile.IsZombie() or not inputFile.GetNkeys():
      print("Can not open file: " + fileName)
      continue
    #histTmp = inputFile.Get(stackSources[stackSource]["histPath"]).Clone()

    # hist path is now a list of paths, so add them all together first,
    # use first one to define histTmp
    histTmp = inputFile.Get(stackSources[stackSource]["histPath"][0]).Clone()
    if len(stackSources[stackSource]["histPath"]) > 1:
      for histPath in stackSources[stackSource]["histPath"][1:]:
        histTmp.Add(inputFile.Get(histPath))

    normalizations.append(histTmp.Integral())
    hists.append(histTmp)
    histTmp.SetDirectory(0)
    histTmp.Rebin(rebinFactor)
    oneDHistSetting(histTmp)
    histTmp.SetFillStyle(1001)
    histTmp.SetFillColorAlpha(stackSources[stackSource]["color"],0.7)
    histTmp.SetLineColor(1)
    histTmp.SetLineWidth(1)
    histTmp.SetAxisRange(Ymin,Ymax,"y")
    histTmp.SetAxisRange(Xmin,Xmax,"x")
    totalNorm = totalNorm + normalizations[-1]
    normHistDic[str(normalizations[-1])] = {}
    normHistDic[str(normalizations[-1])]["hist"] = histTmp
    normHistDic[str(normalizations[-1])]["label"] = stackSources[stackSource]["legendLabel"]

  # Determine the total data yields and compute the scale factors to be applied to MC if scaleToData = 1 
  scaleFactor = 1
  if "data" in stackSources:
    dataFile = TFile(stackSources["data"]["filePath"]) 
    dataHist = dataFile.Get(stackSources["data"]["histPath"][0]).Clone()
    # hist path is now a list of paths, so add them all together first,
    # use first one to define histTmp
    if len(stackSources["data"]["histPath"]) > 1:
      for histPath in stackSources["data"]["histPath"][1:]:
        dataHist.Add(inputFile.Get(histPath))

    totalNumberData = dataHist.Integral()
    if scaleToData:
      scaleFactor = totalNumberData/totalNorm
  if not len(normalizations):
    return   
  ##############################################################################################
  # Change the order of the stacked samples so that the smallest contribution is in the bottom # 
  # if sort = 1. Nominally the order is determined by the indices in stackSources              #               ##############################################################################################
  
  if taskSetup["sort"]:
    normalizations.sort()
  totalNumber = 0 
  newHists = []
  if doFraction:
    for i in range(0,len(normalizations)):
      totalNumber = totalNumber + normalizations[i]
      newHist = normHistDic[str(normalizations[i])]["hist"].Clone()
      newHist.SetDirectory(0)
      for binNumber in range(1,newHist.GetNbinsX() + 1):
        totalEntry = 0
        for j in range(0,len(normalizations)): 
          totalEntry = normHistDic[str(normalizations[j])]["hist"].GetBinContent(binNumber) + totalEntry  
        newBinContent = 0
        if totalEntry:
          newBinContent = float(normHistDic[str(normalizations[i])]["hist"].GetBinContent(binNumber)/totalEntry)  
        newHist.SetBinContent(binNumber,newBinContent)
        newHist.SetBinError(binNumber,0)
      norm = round(normalizations[len(normalizations) - i - 1],0)
      normString = str(int(norm))
      normFrac = round(norm/totalNorm,1)*100
      legend.AddEntry(normHistDic[str(normalizations[len(normalizations) - i - 1])]["hist"],normHistDic[str(normalizations[len(normalizations) - i - 1])]["label"] + " (" + normString + ", " + str(normFrac) + "%)" , "f")
      newHists.append(newHist)
    for i in range(0,len(normalizations)):
      normHistDic[str(normalizations[i])]["hist"] = newHists[i]
      stack.Add(normHistDic[str(normalizations[i])]["hist"])
  else:    
    for i in range(0,len(normalizations)):
      normHistDic[str(normalizations[i])]["hist"].Sumw2()
      normHistDic[str(normalizations[i])]["hist"].Scale(scaleFactor)
      newHist = normHistDic[str(normalizations[i])]["hist"].Clone()
      newHist.SetDirectory(0)
      stack.Add(normHistDic[str(normalizations[i])]["hist"])
      totalNorm = totalNorm * scaleFactor
      norm = round(normalizations[len(normalizations) - i - 1]*scaleFactor,0)
      normString = str(int(norm))
      normFrac = round(norm*100.0/totalNorm,1)
      legend.AddEntry(normHistDic[str(normalizations[len(normalizations) - i - 1])]["hist"],normHistDic[str(normalizations[len(normalizations) - i - 1])]["label"], "f")# + " (" + normString + ", " + str(normFrac) + "%)" , "f")
      newHists.append(newHist)

  dataHist = newHists[0].Clone()
  # Create a background hist to show the uncertainty bands
  bkgHist = newHists[0].Clone()
  bkgHist.SetDirectory(0)
  bkgHist.Sumw2()
  for i in range (1,len(normHistDic)):
    bkgHist.Add(newHists[i])
  bkgHist.SetFillStyle(3002)
  bkgHist.SetFillColor(13)
  bkgHist.SetLineWidth(0) 

  if "data" in stackSources:
    dataFile = TFile(stackSources["data"]["filePath"]) 
    dataHist = dataFile.Get(stackSources["data"]["histPath"][0]).Clone()
    # hist path is now a list of paths, so add them all together first,
    # use first one to define histTmp
    if len(stackSources["data"]["histPath"]) > 1:
      for histPath in stackSources["data"]["histPath"][1:]:
        dataHist.Add(inputFile.Get(histPath))

    totalNumberData = dataHist.Integral()
    dataHist.SetMarkerStyle(20)
    dataHist.SetMarkerSize(1)
    dataHist.SetLineColor(1)
    dataHist.SetLineWidth(2)
    dataHist.SetTitle("") 
    dataHist.GetXaxis().SetTitle(nameX) 
    dataHist.SetStats(0)
    dataHist.SetAxisRange(Ymin,Ymax,"y")
    dataHist.SetAxisRange(Xmin,Xmax,"x")
    legend.AddEntry(dataHist,stackSources["data"]["legendLabel"], "lep")# + " (" + str(totalNumberData) +  ")","lep")

  else:
    for i in range (1,len(normHistDic)):
      dataHist.Add(newHists[i]) 
    dataHist.SetMarkerStyle(20)
    dataHist.SetMarkerStyle(20)
    dataHist.SetMarkerColor(1)
    dataHist.SetLineColor(1)
    dataHist.SetLineWidth(1.2)
    legend.AddEntry(dataHist,"Total MC "  + " (" + str(totalNumber) +  ")","lep")
  
  stack.SetTitle("")
  stack.Draw("HIST")
  stack.SetMaximum(Ymax)
  stack.SetMinimum(Ymin)
  stack.GetXaxis().SetLimits(Xmin, Xmax);
  stack.GetXaxis().SetLabelSize(0.035)
  stack.GetYaxis().SetLabelSize(0.035)
  stack.GetXaxis().SetTitleSize(0.05)
  stack.GetYaxis().SetTitleSize(0.05)
  stack.GetXaxis().SetTitleOffset(1.5)
  stack.GetYaxis().SetNdivisions(505)
  stack.GetXaxis().SetNdivisions(505)
  stack.GetYaxis().SetTitleOffset(1.25) 
 
  stack.GetXaxis().SetMoreLogLabels()
  stack.GetXaxis().SetTitle(nameX)
  stack.GetYaxis().SetTitle(nameY)
  if doRatio:
    stack.GetHistogram().GetXaxis().SetLabelSize(0)
    stack.GetHistogram().GetXaxis().SetTitleSize(0)
    stack.GetHistogram().GetXaxis().SetLabelOffset(0)
    stack.GetHistogram().GetXaxis().SetTitleOffset(0)
  stack.Draw("HIST")
  drawLabel(hists[-1],nameX,nameY)

  dataHist.Draw("p same")
  bkgHist.Draw("A E2 same")
  legend.Draw("same")
  drawAtlasLabel(masterLabel,lumi,cme, 0.17, doRatio)

  if doRatio:
    canvas.cd(2)
    histTmp = ratioHistogram(dataHist, bkgHist, str(taskSetup["ratioYLabel"]), relErrMax, Xmin,Xmax)
    histTmp.SetDirectory(0)
    histTmp.SetStats(0)
    histTmp.SetName(name)
    histTmp.SetAxisRange(ratioYmin,ratioYmax,"y")
    # Fix me: somehow the ratio hist always adds the overflow bin..
    histTmp.SetAxisRange(Xmin,Xmax-1, "x")
    histTmp.GetXaxis().SetMoreLogLabels()
    histTmp.GetYaxis().SetTitleSize(0.12)
    histTmp.GetYaxis().SetLabelSize(0.1)
    histTmp.GetYaxis().SetTitleOffset(0.45)
    histTmp.GetXaxis().SetTitleSize(0.12)
    histTmp.GetXaxis().SetLabelSize(0.1)
    histTmp.SetMarkerStyle(20)
    histTmp.Draw("p")
    histTmp.GetXaxis().Draw("p")
    histTmp.GetYaxis().Draw("p")
    outputFile.cd()
    histTmp.Write()
  gPad.Update()
  gPad.Modified()
  
  gPad.RedrawAxis()
  outputFile.cd()
  fname = Path(outputFile.GetName())
  canvas.Print(str(fname.with_suffix('.pdf')))
  canvas.Write()
  canvas.Print(str(fname.with_suffix('.png')))
  canvas.Write()

#################################################################
# Functions to draw comparison plots                            #
# This is probably the most useful plot to debug any problems   #
# compareSources is defined in config                             #
#################################################################

def drawComparisonPlot(taskSetup, compareSources, outputFile):
  Xmin   =  float(taskSetup["Xmin"])
  Xmax   =  float(taskSetup["Xmax"])
  Ymin   =  float(taskSetup["Ymin"])
  Ymax   =  (taskSetup["Ymax"])
  nameX  =  taskSetup["nameX"]
  nameY  =  taskSetup["nameY"]
  name   =  taskSetup["name"]   
  doLogy =  taskSetup["doLogy"]
  rebinFactor = taskSetup["rebinFactor"]
  doFraction  = taskSetup["doFraction"]  
  doRatio     = taskSetup["doRatio"]
  masterLabel = taskSetup["masterLabel"]
  lumi        = taskSetup["lumi"]
  cme         = taskSetup["cme"]
  relErrMax   = taskSetup["relErrMax"]
  scaleToData = taskSetup["scaleToData"]
  ratioYmin   =  taskSetup["ratioYmin"]
  ratioYmax   =  taskSetup["ratioYmax"]
  normalized = taskSetup["normalized"]
 
  canvas = TCanvas("canvas_"+taskSetup["name"],taskSetup["name"],10,10,600,600)
  if doRatio and len(compareSources) > 1: 
    canvas.SetFillStyle(0)
    canvas.Divide(1,2)
    canvas.cd(1)
    gPadSetup(doLogy)
  
    gPad.SetPad(0,0.2,1,1)
    gPad.SetMargin(0.15,0.05,0.01,0.07)
    gPad.SetFillStyle(0)
    gPad.Update()
    gPad.Draw()
    
    canvas.cd(2)
    gPad.SetPad(0,0,1.0,0.32)
    gPad.SetMargin(0.15,0.09,0.4,0.035)
    gPad.SetFillStyle(0)
    gPad.SetGridy(1)
    gPad.Update()
    gPad.Draw()
  else:
    canvas.SetFillStyle(0)
    canvas.Divide(1)
    canvas.cd(1)
    gPadSetup(doLogy)
  
  canvas.cd(1)
  gPadSetup(doLogy)
    
  legend = TLegend(0.6, 0.93 - 0.06*len(compareSources), 0.9, 0.93)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetFillColor(0)
  legend.SetTextSize(0.03)
  legend.SetFillStyle(0)
 
  canvas.cd(1)
  hbase = TH1D("hbase","",1,Xmin,Xmax)
  hbase.GetYaxis().SetRangeUser(Ymin,Ymax)
  hbase.Draw("hist")
  if normalized:
    nameY = "Arbitrary Units"
  drawLabel(hbase,nameX,nameY)
  hists = []
  for element in range(0,len(compareSources)):
    compareSource = str(element + 1)
    fileName  = compareSources[compareSource]["filePath"]
    inputFile = TFile(fileName)
    if inputFile.IsZombie() or not inputFile.GetNkeys():
      print ("Can not open file: " + fileName)
      continue
    else:
      print (compareSources[compareSource]["histPath"][0])

    histTmp = inputFile.Get(compareSources[compareSource]["histPath"][0]).Clone()
    if len(compareSources[compareSource]["histPath"]) > 1:
      for histPath in compareSources[compareSource]["histPath"][1:]:
        histTmp.Add(inputFile.Get(histPath))
    
    histTmp.Rebin(rebinFactor)
    
    if normalized:
      histTmp.Sumw2()
      histTmp.Scale(1/histTmp.Integral()) 
    histTmp.SetDirectory(0)
    
    oneDHistSetting(histTmp)
    histTmp.SetTitle("")
    histTmp.SetStats(0)
    histTmp.SetMarkerStyle(compareSources[compareSource]["style"])
    histTmp.SetMarkerColor(compareSources[compareSource]["color"])
    histTmp.SetLineColor(compareSources[compareSource]["color"])
    histTmp.SetLineWidth(2)
    histTmp.SetLineStyle(1)
    histTmp.SetAxisRange(Ymin,Ymax,"y")
    histTmp.SetAxisRange(Xmin,Xmax,"x")
    
    drawOption = compareSources[compareSource]["drawOption"]
    legendDrawOption = "lep"
    if drawOption == "histo":
      legendDrawOption = "l"
      histTmp.SetFillColor(0)
    if drawOption == "histo f":
      legendDrawOption = "f"
      histTmp.SetFillColor(compareSources[compareSource]["color"])
    legend.AddEntry(histTmp,compareSources[compareSource]["legendLabel"],legendDrawOption)
    hists.append(histTmp)
    histTmp.Draw("same " + drawOption)
    inputFile.Close()
  legend.Draw("same")
  drawAtlasLabel(masterLabel, lumi,cme, doRatio)
  if doRatio and len(compareSources) > 1:
    canvas.cd(2)
    histTmp = ratioHistogram(hists[0], hists[1], str(taskSetup["ratioYLabel"]), relErrMax,Xmin,Xmax) 
    #histTmp = sOverBHistogram(hists[0], hists[1], Xmin,Xmax) 
    histTmp.SetDirectory(0)
    histTmp.SetStats(0)
    histTmp.SetName(taskSetup["name"])
    histTmp.SetAxisRange(ratioYmin,ratioYmax,"y")
    histTmp.SetAxisRange(Xmin,Xmax-1, "x")
    #histTmp.SetFillColor(4)
    histTmp.SetLineColor(4)
    histTmp.GetXaxis().SetMoreLogLabels()
    histTmp.GetYaxis().SetTitleSize(0.1)
    histTmp.GetYaxis().SetLabelSize(0.1)
    histTmp.GetYaxis().SetTitleOffset(0.4)
    histTmp.GetXaxis().SetTitleSize(0.1)
    histTmp.GetXaxis().SetLabelSize(0.1)
    histTmp.GetXaxis().SetTitleOffset(1.5)
    histTmp.GetXaxis().SetTitle(nameX)
    histTmp.Draw("same p")
    histTmp.GetXaxis().Draw("same")
    histTmp.GetYaxis().Draw("same")
    outputFile.cd()
    histTmp.Write()

  canvas.cd(1)
  hists[0].GetXaxis().Draw("same")
  hists[0].GetYaxis().Draw("same")
  gPad.Update()
  gPad.Modified()
  gPad.RedrawAxis()
  outputFile.cd()
  canvas.Print("canvas_"+taskSetup["name"] + ".pdf");
  canvas.Write()
