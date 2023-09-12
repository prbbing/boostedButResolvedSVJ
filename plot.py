import os,sys
import argparse
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument("-i","--inputs",type=str,nargs='+',help="input files")
parser.add_argument("-x","--suffix",type=str,default="",help="suffix for output plot filenames")
parser.add_argument("-d","--dir",type=str,default=".",help="directory for output plots")
parser.add_argument("-n","--norm",default=False,action="store_true",help="draw normalized plots")
args = parser.parse_args()

import ROOT as r
r.gROOT.SetBatch()

def print_can(can,pname,pdir,psuff,pformats):
    for pformat in pformats:
        can.Print("{}/{}{}.{}".format(pdir,pname,"_"+psuff if len(psuff)>0 else "",pformat),pformat)

pformats = ["pdf","png"]
colors = [r.kBlack, r.kBlue, r.kCyan + 2, r.kMagenta + 2, r.kMagenta, r.kPink - 9, r.kOrange + 7, r.kRed, r.kYellow + 3, r.kGreen + 2, r.kGray + 1]

if not os.path.isdir(args.dir):
    os.makedirs(args.dir, exist_ok=True)

# get and group the hists
plots = defaultdict(list)
maxs = defaultdict(float)
for i,input in enumerate(args.inputs):
    iname = input.replace("out_","").replace(".root","")
    ifile = r.TFile.Open(input)
    ikeys = [k.GetName() for k in ifile.GetListOfKeys()]
    for ikey in ikeys:
        ihist = ifile.Get(ikey)
        ihist.SetDirectory(0)
        if ihist.GetDimension()==2:
            pname = ikey+"_"+iname
        else:
            pname = ikey
        if args.norm:
            ihist.Scale(1.0/ihist.Integral())
        maxs[pname] = max(maxs[pname],ihist.GetMaximum())
        plots[pname].append((iname,ihist))
    ifile.Close()

# make the plots
for pname,hists in plots.items():
    can = r.TCanvas()
    can.cd()
    # 2D case: one hist per canvas
    if len(hists)==1 and hists[0][1].GetDimension()==2:
        h0 = hists[0][1]
        psplit = pname.split('_')
        h0.SetTitle("")
        h0.SetStats(0)
        h0.GetXaxis().SetTitle(psplit[0])
        h0.GetYaxis().SetTitle(psplit[1])
        h0.GetZaxis().SetTitle("{} ({})".format("arbitrary units" if args.norm else "events", psplit[2]))
        h0.Draw("colz")
    else:
        leg = r.TLegend(0.5,0.5,1.0,1.0)
        leg.SetTextFont(42)
        leg.SetTextSize(0.04)
        leg.SetBorderSize(0)
        leg.SetFillColor(r.kWhite)
        leg.SetLineColor(r.kWhite)
        leg.SetFillStyle(0)
        leg.SetLineWidth(0)
        leg.SetFillStyle(1001)
        leg.SetFillColorAlpha(0,0.6)
        for i,(name,hist) in enumerate(hists):
            hist.SetTitle("")
            hist.SetStats(0)
            hist.GetXaxis().SetTitle(pname)
            hist.GetYaxis().SetTitle("arbitrary units" if args.norm else "events")
            hist.GetYaxis().SetRangeUser(0,maxs[pname])
            hist.SetLineColor(colors[i])
            hist.SetMarkerColor(colors[i])
            leg.AddEntry(hist,name,"l")
            draw = "hist{}".format(" same" if i>0 else "")
            hist.Draw(draw)
        leg.Draw()
    print_can(can,pname,args.dir,args.suffix,pformats)
