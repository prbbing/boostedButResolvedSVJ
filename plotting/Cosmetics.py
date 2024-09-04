###################################################
# Cosmetic setups                                 #
# We can also make all thoese configurable but    #
# they are simple enough to be changed on the fly #
###################################################
from ROOT import *

def AtlasLabel(x,y,shift,text="",color=1,size=0.06): 
  l=TLatex() 
  l.SetNDC()
  l.SetTextFont(72)
  l.SetTextColor(color)
  l.SetTextSize(size)
  l.DrawLatex(x,y,"ATLAS Internal")
  if (text!=""):
    p=TLatex()
    p.SetNDC();
    p.SetTextSize(size-0.01)
    p.SetTextFont(42)
    p.SetTextColor(color)
    p.DrawLatex(x+shift,y,text);

def formatLumi(inputLumi, inputCME):
  lumi=inputLumi
  Lumi=" %.1f fb^{-1}" % (lumi/1000.)
  CMELUMI="#sqrt{s} = " + str(inputCME) + " TeV"
  if inputLumi>0:
    CMELUMI += ", "+ Lumi
  return CMELUMI

def myText(x,y,color=1,size=0.04,text=""): 
  l=TLatex()
  l.SetTextSize(size); 
  l.SetTextFont(42)
  l.SetNDC();
  l.SetTextColor(color);
  l.DrawLatex(x,y,text);

def drawAtlasLabel(label, inputLumi, inputCME, shift = 0.0, doRatio = 0):
  CMELUMI = formatLumi(inputLumi, inputCME)
  # Lumi label 
  myText(0.19, 0.89, 1, 0.04, CMELUMI)
  myText(0.19,0.83,1,0.04,label)

def drawLabel(h,nameX,nameY):
  ax=h.GetXaxis()
  ax.SetTitle( nameX )
  ay=h.GetYaxis()
  ay.SetTitle( nameY )
  ax.SetLabelSize(0.04)
  ay.SetLabelSize(0.04)
  ax.SetTitleSize(0.05)
  ay.SetTitleSize(0.05)
  ax.SetTitleOffset(1.5)
  ay.SetTitleOffset(1.5)
  ax.SetLabelOffset(0.01)
  ay.SetLabelOffset(0.008)
  ax.SetNdivisions(505)
  ay.SetNdivisions(505)
  ax.Draw("same")
  ay.Draw("same")

def gPadSetup(logy):
  if logy == 1:
    gPad.SetLogy(1)
  if logy == 2:
    gPad.SetLogx(1)
  if logy == 3:
    gPad.SetLogy(1)
    gPad.SetLogx(1)
  gPad.SetTopMargin(0.05)
  gPad.SetBottomMargin(0.15)
  gPad.SetLeftMargin(0.15)
  gPad.SetRightMargin(0.09)

def oneDHistSetting(hist):
  hist.GetXaxis().SetLabelSize(0.03)
  hist.GetYaxis().SetLabelSize(0.03)
  hist.GetXaxis().SetTitleSize(0.03)
  hist.GetYaxis().SetTitleSize(0.03)
  hist.GetXaxis().SetTitleOffset(1.8)
  hist.GetYaxis().SetNdivisions(505)
  hist.GetXaxis().SetNdivisions(505)
  hist.GetYaxis().SetTitleOffset(1.5)
  hist.SetTitle("")
  hist.SetStats(0) 

