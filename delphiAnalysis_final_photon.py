import os,sys,argparse
from tqdm import tqdm

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i","--input", type=str, required=True, default=None, help="input filename")
parser.add_argument("-o","--output", type=str, required=True, default=None, help="output filename")
parser.add_argument("-y","--yStarcut", type=float, default=10, help="yStar Cut")
parser.add_argument("-c","--cool", action='store_true', help="Someone cool is using a MAC m1. But by default, not everyone is cool.")
parser.add_argument("-w","--lumiWeight", type=float, default=1, help="luminosity weight")
parser.add_argument("-x","--xs", type=float, default=0, help="Production cross section")
parser.add_argument("-p","--presel", action='store_true', help="preselection: omit rinv/mass cuts")

args = parser.parse_args()

import ROOT as r
from histos import histos
from functions import *

if args.cool:
  r.gSystem.Load("/cvmfs/sft.cern.ch/lcg/views/LCG_104/arm64-mac13-clang140-opt/lib/libDelphes.dylib")
else:
  r.gSystem.Load("/cvmfs/sft.cern.ch/lcg/views/LCG_104/x86_64-centos7-gcc11-opt/lib/libDelphes.so")

crossSection = args.xs

r.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
r.gInterpreter.Declare('#include "ExRootAnalysis/ExRootTreeReader.h"')
r.gInterpreter.Declare('#include "lester_mt2_bisect.h"')
r.asymm_mt2_lester_bisect.disableCopyrightMessage()


outf = r.TFile(args.output,"RECREATE")
chain = r.TChain("Delphes")
chain.Add(args.input)

# Create object of class ExRootTreeReader

treeReader = r.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

branchEvent = treeReader.UseBranch("Event")
branchWeight = treeReader.UseBranch("Weight")
branchJet = treeReader.UseBranch("Jet")
branchFatJet = treeReader.UseBranch("FatJet")
branchPhoton = treeReader.UseBranch("Photon")
branchMet = treeReader.UseBranch("MissingET")
branchGenMet = treeReader.UseBranch("GenMissingET")

xs = 1

sum = 0
sum_sel = 0

for entry in tqdm(range(0, numberOfEntries)):

  treeReader.ReadEntry(entry)

  weight = branchWeight.At(0).Weight * args.lumiWeight

  sum = sum + weight

  #Get the photon
  photon = r.TLorentzVector()
  for j in range(0,  branchPhoton.GetEntries()):
    pho = branchPhoton.At(j)
    if pho.PT > photon.Pt():
      photon.SetPtEtaPhiM(pho.PT, pho.Eta, pho.Phi, 0)

  # Get the leading jets
  lead_j = r.TLorentzVector()
  sublead_j = r.TLorentzVector()

  for j in range(0,  branchJet.GetEntries()):
    jet = branchJet.At(j)
    if jet.PT < 25:
      continue
    if abs(jet.Eta) > 4.5:
      continue

    jet_vec = r.TLorentzVector()
    jet_vec.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet_vec.DeltaR(photon) < 0.4:
      continue

    # Find the leading jets
    if jet.PT > lead_j.Pt():
      lead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < lead_j.Pt() and jet.PT > sublead_j.Pt():
      sublead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

  if lead_j.Pt() == sublead_j.Pt(): 
    continue    

  #Leading jets kinematics
  
  if photon.Pt() > 150:
    
    sum_sel = sum_sel + weight
   
    if lead_j.Pt() < 25 or sublead_j.Pt() < 25:
      continue
    if abs(lead_j.DeltaPhi(sublead_j)) < 0.8:
      continue
 
    # Get MET
    met = r.TLorentzVector()
    met.SetPtEtaPhiM(branchMet.At(0).MET, 0, branchMet.At(0).Phi,0)
  
    yStar = 0
 
    di_j = lead_j + sublead_j 

    yStar = abs(lead_j.Rapidity() - sublead_j.Rapidity())/2.0
    
    if yStar > args.yStarcut:
      continue
  
    histos["metMET"].Fill(met.Pt(), weight)
    histos["metPhi"].Fill(met.Phi(), weight)
    
    mTjj = TransverseMass(di_j.Px(),di_j.Py(),di_j.M(),met.Px(),met.Py(),0)
    maosjj = MAOS(lead_j, sublead_j, met)
    mjjRecompose = MassRecompose(lead_j, sublead_j, met)

    if not args.presel:
      if met.Pt()/mTjj < 0.4:
        continue
        sum_sel = sum_sel + weight
      if maosjj['mass'] < 200:
        continue

    histos["maosjj"].Fill(maosjj['mass'], weight)
    histos["mjjRecomp"].Fill(mjjRecompose['mass'], weight)
    histos["maosjj_mjjRecomp"].Fill(maosjj['mass'], mjjRecompose['mass'], weight)
    histos["metMET"].Fill(met.Pt(), weight)
    histos["metPhi"].Fill(met.Phi(), weight)
    histos["mTjj"].Fill(mTjj, weight)
    histos["rT"].Fill(met.Pt()/mTjj, weight)
    histos["rinv1_rinv2"].Fill(mjjRecompose['rinv1'], mjjRecompose['rinv2'], weight)
    histos["rinv1_rinv2_maos"].Fill(maosjj['rinv1'], maosjj['rinv2'], weight)
    histos["rinv_ave"].Fill(mjjRecompose['rinvAve'], weight)
    histos["rinv_ave_maos"].Fill(maosjj['rinvAve'], weight)
    histos["rinv_ave_maosjj"].Fill(mjjRecompose['rinvAve'], maosjj['mass'], weight)
    histos["rinv_ave_maos_maosjj"].Fill(maosjj['rinvAve'], maosjj['mass'], weight)
    histos["rinv_ave_mTjj"].Fill(mjjRecompose['rinvAve'], mTjj, weight)
 
    histos["leadjPt"].Fill(lead_j.Pt(), weight)
    histos["leadjEta"].Fill(lead_j.Eta(), weight)
    histos["leadjPhi"].Fill(lead_j.Phi(), weight)

    histos["subleadjPt"].Fill(sublead_j.Pt(), weight)
    histos["subleadjEta"].Fill(sublead_j.Eta(), weight)
    histos["subleadjPhi"].Fill(sublead_j.Phi(), weight)

print("Cross-section: " + str(crossSection))
print("Efficiency: " + str(sum_sel/sum))
print("Total: " + str(sum_sel*crossSection/sum))
lumiWeight = crossSection*140000.0/sum
print("Weight: " + str(lumiWeight))

outf.cd()
for k,v in histos.items():
    v.Write()
outf.Close()
