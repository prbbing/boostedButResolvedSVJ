import os,sys,argparse
import numpy as np
from tqdm import tqdm
from histos import histos

def TransverseMass(px1, py1, m1, px2, py2, m2):
  E1 = np.sqrt(px1**2+py1**2+m1**2)
  E2 = np.sqrt(px2**2+py2**2+m2**2)
  MTsq = (E1+E2)**2-(px1+px2)**2-(py1+py2)**2
  return np.sqrt(max(MTsq,0.0))

def MAOS(lead_j, sublead_j, met):
  mT2 = r.asymm_mt2_lester_bisect.get_mT2(
    lead_j.M(), lead_j.Px(), lead_j.Py(),
    sublead_j.M(), sublead_j.Px(), sublead_j.Py(),
    met.Px(), met.Py(), 0.0, 0.0, 0
  )
  met1x, met1y = r.asymm_mt2_lester_bisect.ben_findsols(mT2,
    lead_j.Px(), lead_j.Py(), lead_j.M(), 0.0,
    sublead_j.Px(), sublead_j.Py(),
    met.Px(), met.Py(), sublead_j.M(), 0.0
  )
  met1t = np.sqrt(met1x**2+met1y**2)
  met2x = met.Px() - met1x
  met2y = met.Py() - met1y
  met2t = np.sqrt(met2x**2+met2y**2)
  met1z = met1t*lead_j.Pz()/lead_j.Pt()
  met2z = met2t*sublead_j.Pz()/sublead_j.Pt()
  v_met1 = r.TLorentzVector()
  v_met1.SetPxPyPzE(met1x,met1y,met1z,np.sqrt(met1t**2+met1z**2))
  v_met2 = r.TLorentzVector()
  v_met2.SetPxPyPzE(met2x,met2y,met2z,np.sqrt(met2t**2+met2z**2))
  maos_val = (lead_j + sublead_j + v_met1 + v_met2).M()
  return maos_val

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-i","--input", type=str, required=True, default=None, help="input filename")
parser.add_argument("-o","--output", type=str, required=True, default=None, help="output filename")
parser.add_argument("-n","--nevents", type=int, default=-1, help="restrict number of events (for testing)")
args = parser.parse_args()

import ROOT as r
r.gSystem.Load("/cvmfs/sft.cern.ch/lcg/views/LCG_104/x86_64-centos7-gcc11-opt/lib/libDelphes.so")
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
if args.nevents<0: args.nevents = numberOfEntries
numberOfEntries = min(args.nevents, numberOfEntries)
branchWeight = treeReader.UseBranch("Weight")
branchJet = treeReader.UseBranch("Jet")
branchFatJet = treeReader.UseBranch("FatJet")
branchPhoton = treeReader.UseBranch("Photon")
branchMet = treeReader.UseBranch("MissingET")
branchParticle = treeReader.UseBranch("Particle")

for entry in tqdm(range(0, numberOfEntries)):

  treeReader.ReadEntry(entry)

  #Get weight
  weight = branchWeight.At(0).Weight

  # Get the dark quarks
  xds = []
  for j in range(0,  branchParticle.GetEntries()):
    par = branchParticle.At(j)
    xd = r.TLorentzVector()
    pid = par.PID
    if abs(pid) == 4900101 and par.Status == 23:
      xd.SetPtEtaPhiM(par.PT, par.Eta, par.Phi, par.Mass)
      xds.append(xd)
  if len(xds) < 2:
    continue

  #Get the photon
  photon = r.TLorentzVector()
  for j in range(0,  branchPhoton.GetEntries()):
    pho = branchPhoton.At(j)
    if pho.PT > photon.Pt():
      photon.SetPtEtaPhiM(pho.PT, pho.Eta, pho.Phi, 0)

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

    #Photon-jet overlap removal
    jet_vec = r.TLorentzVector()
    if jet_vec.DeltaR(photon) < 0.4:
      continue

    # Find the matched jet indices for Xds
    jet_vec = r.TLorentzVector()
    jet_vec.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet_vec.DeltaR(xds[0]) < 0.2 or jet_vec.DeltaR(xds[1]) < 0.2:
      histos["jet_index"].Fill(j, weight)

    # Find the leading jets
    if jet.PT > lead_j.Pt():
      lead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < lead_j.Pt() and jet.PT > sublead_j.Pt():
      sublead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < sublead_j.Pt() and jet.PT > third_j.Pt():
      third_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

  # Get the leading large-R jets
  lead_J = r.TLorentzVector()
  sublead_J = r.TLorentzVector()
  third_J = r.TLorentzVector()

  for j in range(0,  branchFatJet.GetEntries()):
    Jet = branchFatJet.At(j)
    if Jet.PT < 200:
      continue
    if abs(Jet.Eta) > 4.5:
      continue

    #Photon-Jet overlap removal
    Jet_vec = r.TLorentzVector()
    if Jet_vec.DeltaR(photon) < 1.0:
      continue

    # Find the matched Jet indices for Xds
    Jet_vec = r.TLorentzVector()
    Jet_vec.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)
    if Jet_vec.DeltaR(xds[0]) < 0.4 or Jet_vec.DeltaR(xds[1]) < 0.4:
      histos["Jet_index"].Fill(j, weight)

    # Find the leading Jets
    if Jet.PT > lead_J.Pt():
      lead_J.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)
    if Jet.PT < lead_J.Pt() and Jet.PT > sublead_J.Pt():
      sublead_J.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)
    if Jet.PT < sublead_J.Pt() and Jet.PT > third_J.Pt():
      third_J.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)

  # Get MET
  met = r.TLorentzVector()
  met.SetPtEtaPhiM(branchMet.At(0).MET, 0, branchMet.At(0).Phi,0)

  # Event selections

  if photon.Pt() < 150:
    continue
  if lead_j.Pt() <= 0 or sublead_j.Pt() <= 0:
    continue
  if lead_j.DeltaR(sublead_j) < 0.4:
    continue

  # Fill histograms

  #Leading jets kinematics

  histos["leadjPt"].Fill(lead_j.Pt(), weight)
  histos["leadjEta"].Fill(lead_j.Eta(), weight)
  histos["leadjPhi"].Fill(lead_j.Phi(), weight)

  histos["subleadjPt"].Fill(sublead_j.Pt(), weight)
  histos["subleadjEta"].Fill(sublead_j.Eta(), weight)
  histos["subleadjPhi"].Fill(sublead_j.Phi(), weight)

  if third_j.Pt():
    histos["thirdjPt"].Fill(third_j.Pt(), weight)
    histos["thirdjEta"].Fill(third_j.Eta(), weight)
    histos["thirdjPhi"].Fill(third_j.Phi(), weight)

  #Leading large-R jets kinematics

  if lead_J.Pt():
    histos["leadJPt"].Fill(lead_J.Pt(), weight)
    histos["leadJEta"].Fill(lead_J.Eta(), weight)
    histos["leadJPhi"].Fill(lead_J.Phi(), weight)

  if sublead_J.Pt():
    histos["subleadJPt"].Fill(sublead_J.Pt(), weight)
    histos["subleadJEta"].Fill(sublead_J.Eta(), weight)
    histos["subleadJPhi"].Fill(sublead_J.Phi(), weight)

  if third_J.Pt():
    histos["thirdJPt"].Fill(third_J.Pt(), weight)
    histos["thirdJEta"].Fill(third_J.Eta(), weight)
    histos["thirdJPhi"].Fill(third_J.Phi(), weight)

  # photon kinematics

  histos["photonPt"].Fill(photon.Pt(), weight)
  histos["photonEta"].Fill(photon.Eta(), weight)
  histos["photonPhi"].Fill(photon.Phi(), weight)

  # MET kinematics

  histos["metMET"].Fill(met.Pt(), weight)
  histos["metPhi"].Fill(met.Phi(), weight)

  # leading di-jet pair kinematics

  di_j = lead_j + sublead_j
  di_J = None
  histos["mjjMass"].Fill(di_j.M(), weight)
  if sublead_J.Pt() and lead_J.Pt():
    di_J = lead_J + sublead_J
    histos["mJJMass"].Fill(di_J.M(), weight)
  histos["mXdXdMass"].Fill((xds[0] + xds[1]).M(), weight)

  histos["jjdPhi"].Fill(lead_j.DeltaPhi(sublead_j), weight)
  if sublead_J.Pt() and lead_J.Pt():
    histos["JJdPhi"].Fill(lead_J.DeltaPhi(sublead_J), weight)
  histos["XdXddPhi"].Fill(xds[0].DeltaPhi(xds[1]), weight)

  histos["jjdR"].Fill(lead_j.DeltaR(sublead_j), weight)
  if sublead_J.Pt():

    histos["JJdR"].Fill(lead_J.DeltaR(sublead_J), weight)
  histos["XdXddR"].Fill(xds[0].DeltaR(xds[1]), weight)

  # dijet-MET kinematics

  mTjj = TransverseMass(di_j.Px(),di_j.Py(),di_j.M(),met.Px(),met.Py(),0)
  histos["mTjj"].Fill(mTjj, weight)
  maosjj = MAOS(lead_j, sublead_j, met)
  histos["maosjj"].Fill(maosjj, weight)

  if di_J is not None:
    mTJJ = TransverseMass(di_J.Px(),di_J.Py(),di_J.M(),met.Px(),met.Py(),0)
    histos["mTJJ"].Fill(mTJJ, weight)
    maosJJ = MAOS(lead_J, sublead_J, met)
    histos["maosJJ"].Fill(maosJJ, weight)

  # MET-X system kinematics

  # min MET-j dphi among leading two jets
  jminDPhi = min(lead_j.DeltaPhi(met), sublead_j.DeltaPhi(met))
  histos["jminDPhi"].Fill(jminDPhi)

  # min MET-J dphi among leading two large-R jets
  if sublead_J.Pt():
    JminDPhi = min(lead_J.DeltaPhi(met), sublead_J.DeltaPhi(met))
  else:
    JminDPhi = lead_J.DeltaPhi(met)
  histos["JminDPhi"].Fill(JminDPhi, weight)

  histos["photonMetDPhi"].Fill(photon.DeltaPhi(met), weight)

  histos["leadjMetDPhi"].Fill(lead_j.DeltaPhi(met), weight)
  histos["subleadjMetDPhi"].Fill(sublead_j.DeltaPhi(met), weight)
  if third_j.Pt():
    histos["thirdjMetDPhi"].Fill(third_j.DeltaPhi(met), weight)

  if lead_J.Pt():
    histos["leadJMetDPhi"].Fill(lead_J.DeltaPhi(met), weight)
  if sublead_J.Pt():
    histos["subleadJMetDPhi"].Fill(sublead_J.DeltaPhi(met), weight)
  if third_J.Pt():
    histos["thirdJMetDPhi"].Fill(third_J.DeltaPhi(met), weight)

  histos["dijetMetDPhi"].Fill(met.DeltaPhi(lead_j + sublead_j), weight)
  if sublead_J.Pt():
    histos["diJetMetDPhi"].Fill(met.DeltaPhi(lead_J + sublead_J), weight)

  # 2D dphi
  histos["jMetDPhi2D"].Fill(lead_j.DeltaPhi(met), sublead_j.DeltaPhi(met), weight)
  if sublead_J.Pt():
    histos["JMetDPhi2D"].Fill(lead_J.DeltaPhi(met), sublead_J.DeltaPhi(met), weight)
  histos["jminDPhi_photonPt"].Fill(jminDPhi, photon.Pt(), weight)
  if sublead_J.Pt():
    histos["JminDPhi_photonPt"].Fill(JminDPhi, photon.Pt(), weight)

outf.cd()
for k,v in histos.items():
    v.Write()
outf.Close()
