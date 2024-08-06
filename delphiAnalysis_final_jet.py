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

'''
#Import dead cells
phis = []
etas = []

dead_phi = open("deadCellPhi.txt")
dead_eta = open("deadCellEta.txt")

for line in dead_phi:
    phis.append(float(line.rstrip('\n')))

for line in dead_eta:
    etas.append(float(line.rstrip('\n')))

# Create object of class ExRootTreeReader
'''

treeReader = r.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()

branchEvent = treeReader.UseBranch("Event")
branchWeight = treeReader.UseBranch("Weight")
branchJet = treeReader.UseBranch("Jet")
branchFatJet = treeReader.UseBranch("FatJet")
branchPhoton = treeReader.UseBranch("Photon")
branchMet = treeReader.UseBranch("MissingET")
branchGenMet = treeReader.UseBranch("GenMissingET")

sum = 0
sum_sel = 0

for entry in tqdm(range(0, numberOfEntries)):

  treeReader.ReadEntry(entry)

  weight = branchWeight.At(0).Weight * args.lumiWeight

  sum = sum + weight

  # Get the leading jets
  lead_j = r.TLorentzVector()
  sublead_j = r.TLorentzVector()
  third_j = r.TLorentzVector()

  for j in range(0,  branchJet.GetEntries()):
    jet = branchJet.At(j)
    if jet.PT < 25:
      continue
    if abs(jet.Eta) > 4.5:
      continue

    # Find the leading jets
    if jet.PT > lead_j.Pt():
      lead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < lead_j.Pt() and jet.PT > sublead_j.Pt():
      sublead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < sublead_j.Pt() and jet.PT > third_j.Pt():
      third_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

  if lead_j.Pt() == sublead_j.Pt() or lead_j.Pt() == third_j.Pt() or third_j.Pt() == sublead_j.Pt():
    continue    

  #Leading jets kinematics
  if lead_j.Pt() > 500:
   
    #Dead cell filter
    #matched = 0
    #for i in range(0, len(phis)): 
    #    delta_r = sqrt(pow(lead_j.Eta() - etas[i], 2) + pow(deltaPhi(lead_j.Phi(), phis[i]), 2))   
    #    if delta_r < 0.1:
    #        matched = 1
    #        break
    #if matched:
    #  continue  
   
    if lead_j.Pt() < 25 or sublead_j.Pt() < 25 or third_j.Pt() < 25:
      continue
    if abs(lead_j.DeltaPhi(sublead_j)) < 0.8 or abs(lead_j.DeltaPhi(third_j)) < 0.8 or abs(sublead_j.DeltaPhi(third_j)) < 0.8:
      continue
 
    # Get MET
    met = r.TLorentzVector()
    met.SetPtEtaPhiM(branchMet.At(0).MET, 0, branchMet.At(0).Phi,0)
  
    yStar = 0
 
    di_j = lead_j + sublead_j 
    leadj_thirdj = lead_j + third_j
    subleadj_thirdj = sublead_j + third_j 

    dphi_jj_1 = abs(lead_j.DeltaPhi(sublead_j))
    dphi_jj_2 = abs(lead_j.DeltaPhi(third_j))
    dphi_jj_3 = abs(sublead_j.DeltaPhi(third_j))
    dphi_jmet_1 =  abs(lead_j.DeltaPhi(met))
    dphi_jmet_2 =  abs(sublead_j.DeltaPhi(met))
    dphi_jmet_3 =  abs(third_j.DeltaPhi(met))

    dphi_1 = abs(met.DeltaPhi(di_j))
    dphi_2 = abs(met.DeltaPhi(leadj_thirdj))
    dphi_3 = abs(met.DeltaPhi(subleadj_thirdj))
    
    dphi_ave_1 = (dphi_jj_1 + dphi_1)/2
    dphi_ave_2 = (dphi_jj_2 + dphi_2)/2
    dphi_ave_3 = (dphi_jj_3 + dphi_3)/2
  
    min_dphi = 0
    isr_pT = 0

    # jet matching
    if dphi_ave_1 < dphi_ave_2 and dphi_ave_1 < dphi_ave_3:
      svj1 = lead_j
      svj2 = sublead_j
      di_svj = di_j
      isrj = third_j
      min_dphi = dphi_1
    if dphi_ave_2 < dphi_ave_1 and dphi_ave_2 < dphi_ave_3:
      svj1 = lead_j
      svj2 = third_j
      di_svj = leadj_thirdj
      isrj = sublead_j
      min_dphi = dphi_2
    if dphi_ave_3 < dphi_ave_1 and dphi_ave_3 < dphi_ave_2:
      svj1 = sublead_j
      svj2 = third_j
      di_svj = subleadj_thirdj
      isrj = lead_j
      min_dphi = dphi_3

    yStar = abs(svj1.Rapidity() - svj2.Rapidity())/2.0
    isr_pT = isrj.Pt()
    if yStar > args.yStarcut or isr_pT < 150:
      continue

    mTjj = TransverseMass(di_svj.Px(),di_svj.Py(),di_svj.M(),met.Px(),met.Py(),0)
    maosjj = MAOS(svj1, svj2, met)
    mjjRecompose = MassRecompose(svj1, svj2, met)
   
    if not args.presel:
      # Apply rinv_ave cut  
      if mjjRecompose['rinvAve'] < 0.4:
        continue
      if maosjj['mass'] < 400:
        sum_sel = sum_sel + weight
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
    histos["jjdPhi"].Fill(min_dphi, weight)
    
    histos["leadjPt"].Fill(lead_j.Pt(), weight)
    histos["leadjEta"].Fill(lead_j.Eta(), weight)
    histos["leadjPhi"].Fill(lead_j.Phi(), weight)
    histos["leadjEtaPhi"].Fill(lead_j.Eta(), lead_j.Phi(), weight)

    histos["subleadjPt"].Fill(sublead_j.Pt(), weight)
    histos["subleadjEta"].Fill(sublead_j.Eta(), weight)
    histos["subleadjPhi"].Fill(sublead_j.Phi(), weight)

    histos["thirdjPt"].Fill(third_j.Pt(), weight)
    histos["thirdjEta"].Fill(third_j.Eta(), weight)
    histos["thirdjPhi"].Fill(third_j.Phi(), weight)

print("Cross-section: " + str(crossSection))
print("Efficiency: " + str(sum_sel/sum))
print("Total: " + str(sum_sel*crossSection/sum))
lumiWeight = crossSection*140000.0/sum
print("Weight: " + str(lumiWeight))

outf.cd()
for k,v in histos.items():
  v.Write()
outf.Close()
