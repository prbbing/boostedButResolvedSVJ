import os,sys,re,optparse,argparse
import numpy as np
import math
from histos import *

ROOT.gSystem.Load("/Users/adminbingxuanliu/Work/MCGeneration/MG5_aMC_v3_5_1/DELPHES/libDelphes.so")
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

parser = argparse.ArgumentParser()
parser.add_argument('-o','--output', dest='output', help='Path to the output file.', default="output.root")
parser.add_argument('-i','--input', dest='input', help='Path to the output file.', default="")
arguments = parser.parse_args()

outf = ROOT.TFile(arguments.output,"RECREATE")
chain = ROOT.TChain("Delphes")
if arguments.input == '':
  print("Need input files!")
  sys.exit(0)
chain.Add(arguments.input)

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()
branchWeight = treeReader.UseBranch("Weight")
branchJet = treeReader.UseBranch("Jet")
branchFatJet = treeReader.UseBranch("FatJet")
branchPhoton = treeReader.UseBranch("Photon")
branchMet = treeReader.UseBranch("MissingET")
branchParticle = treeReader.UseBranch("Particle")

for entry in range(0, numberOfEntries):

  treeReader.ReadEntry(entry)

  #Get weight
  weight = branchWeight.At(0).Weight

  # Get the dark quarks
  xds = []
  for j in range(0,  branchParticle.GetEntries()):
    par = branchParticle.At(j)
    xd = ROOT.TLorentzVector()
    pid = par.PID
    if abs(pid) == 4900101 and par.Status == 23:
      xd.SetPtEtaPhiM(par.PT, par.Eta, par.Phi, par.Mass)
      xds.append(xd)
  if len(xds) < 2:
    continue

  #Get the photon
  photon = ROOT.TLorentzVector()
  for j in range(0,  branchPhoton.GetEntries()):
    pho = branchPhoton.At(j)
    if pho.PT > photon.Pt():
      photon.SetPtEtaPhiM(pho.PT, pho.Eta, pho.Phi, 0)

  # Get the leading jets
  lead_j = ROOT.TLorentzVector()
  sublead_j = ROOT.TLorentzVector()
  third_j = ROOT.TLorentzVector()

  for j in range(0,  branchJet.GetEntries()):
    jet = branchJet.At(j)
    if jet.PT < 25:
      continue
    if abs(jet.Eta) > 4.5:
      continue

    #Photon-jet overlap removal
    jet_vec = ROOT.TLorentzVector()
    if jet_vec.DeltaR(photon) < 0.4:
      continue

    # Find the matched jet indices for Xds
    jet_vec = ROOT.TLorentzVector()
    jet_vec.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet_vec.DeltaR(xds[0]) < 0.2 or jet_vec.DeltaR(xds[1]) < 0.2:
      jet_index.Fill(j, weight)

    # Find the leading jets
    if jet.PT > lead_j.Pt():
      lead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < lead_j.Pt() and jet.PT > sublead_j.Pt():
      sublead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < sublead_j.Pt() and jet.PT > third_j.Pt():
      third_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

  # Get the leading large-R jets
  lead_J = ROOT.TLorentzVector()
  sublead_J = ROOT.TLorentzVector()
  third_J = ROOT.TLorentzVector()

  for j in range(0,  branchFatJet.GetEntries()):
    Jet = branchFatJet.At(j)
    if Jet.PT < 200:
      continue
    if abs(Jet.Eta) > 4.5:
      continue

    #Photon-Jet overlap removal
    Jet_vec = ROOT.TLorentzVector()
    if Jet_vec.DeltaR(photon) < 1.0:
      continue

    # Find the matched Jet indices for Xds
    Jet_vec = ROOT.TLorentzVector()
    Jet_vec.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)
    if Jet_vec.DeltaR(xds[0]) < 0.4 or Jet_vec.DeltaR(xds[1]) < 0.4:
      Jet_index.Fill(j, weight)

    # Find the leading Jets
    if Jet.PT > lead_J.Pt():
      lead_J.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)
    if Jet.PT < lead_J.Pt() and Jet.PT > sublead_J.Pt():
      sublead_J.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)
    if Jet.PT < sublead_J.Pt() and Jet.PT > third_J.Pt():
      third_J.SetPtEtaPhiM(Jet.PT, Jet.Eta, Jet.Phi, Jet.Mass)

  # Get MET
  met = ROOT.TLorentzVector()
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

  leadjPt.Fill(lead_j.Pt(), weight)
  leadjEta.Fill(lead_j.Eta(), weight)
  leadjPhi.Fill(lead_j.Phi(), weight)

  subleadjPt.Fill(sublead_j.Pt(), weight)
  subleadjEta.Fill(sublead_j.Eta(), weight)
  subleadjPhi.Fill(sublead_j.Phi(), weight)

  if third_j.Pt():
    thirdjPt.Fill(third_j.Pt(), weight)
    thirdjEta.Fill(third_j.Eta(), weight)
    thirdjPhi.Fill(third_j.Phi(), weight)

  #Leading large-R jets kinematics

  if lead_J.Pt():
    leadJPt.Fill(lead_J.Pt(), weight)
    leadJEta.Fill(lead_J.Eta(), weight)
    leadJPhi.Fill(lead_J.Phi(), weight)

  if sublead_J.Pt():
    subleadJPt.Fill(sublead_J.Pt(), weight)
    subleadJEta.Fill(sublead_J.Eta(), weight)
    subleadJPhi.Fill(sublead_J.Phi(), weight)

  if third_J.Pt():
    thirdJPt.Fill(third_J.Pt(), weight)
    thirdJEta.Fill(third_J.Eta(), weight)
    thirdJPhi.Fill(third_J.Phi(), weight)

  # photon kinematics

  photonPt.Fill(photon.Pt(), weight)
  photonEta.Fill(photon.Eta(), weight)
  photonPhi.Fill(photon.Phi(), weight)

  # MET kinematics

  metMET.Fill(met.Pt(), weight)
  metPhi.Fill(met.Phi(), weight)

  # leading di-jet pair kinematics

  mjjMass.Fill((lead_j + sublead_j).M(), weight)
  if sublead_J.Pt() and lead_J.Pt():
    mJJMass.Fill((lead_J + sublead_J).M(), weight)
  mXdXdMass.Fill((xds[0] + xds[1]).M(), weight)

  jjdPhi.Fill(lead_j.DeltaPhi(sublead_j), weight)
  if sublead_J.Pt() and lead_J.Pt():
    JJdPhi.Fill(lead_J.DeltaPhi(sublead_J), weight)
  XdXddPhi.Fill(xds[0].DeltaPhi(xds[1]), weight)

  jjdR.Fill(lead_j.DeltaR(sublead_j), weight)
  if sublead_J.Pt():

    JJdR.Fill(lead_J.DeltaR(sublead_J), weight)
  XdXddR.Fill(xds[0].DeltaR(xds[1]), weight)

  # MET-X system kinematics

  # min MET-j dphi among leading two jets
  jminDPhi.Fill(min(lead_j.DeltaPhi(met), sublead_j.DeltaPhi(met)), weight)

  # min MET-J dphi among leading two large-R jets
  if sublead_J.Pt():
    JminDPhi.Fill(min(lead_J.DeltaPhi(met), sublead_J.DeltaPhi(met)), weight)

  else:
    JminDPhi.Fill(lead_J.DeltaPhi(met), weight)

  photonMetDPhi.Fill(photon.DeltaPhi(met), weight)

  leadjMetDPhi.Fill(lead_j.DeltaPhi(met), weight)
  subleadjMetDPhi.Fill(sublead_j.DeltaPhi(met), weight)
  if third_j.Pt():
    thirdjMetDPhi.Fill(third_j.DeltaPhi(met), weight)

  if lead_J.Pt():
    leadJMetDPhi.Fill(lead_J.DeltaPhi(met), weight)
  if sublead_J.Pt():
    subleadJMetDPhi.Fill(sublead_J.DeltaPhi(met), weight)
  if third_J.Pt():
    thirdJMetDPhi.Fill(third_J.DeltaPhi(met), weight)

  dijetMetDPhi.Fill(met.DeltaPhi(lead_j + sublead_j), weight)
  if sublead_J.Pt():
    diJetMetDPhi.Fill(met.DeltaPhi(lead_J + sublead_J), weight)

outf.cd()
leadjPt.Write()
leadjEta.Write()
leadjPhi.Write()

subleadjPt.Write()
subleadjEta.Write()
subleadjPhi.Write()

thirdjPt.Write()
thirdjEta.Write()
thirdjPhi.Write()

#Leading large-R jets kinematics

leadJPt.Write()
leadJEta.Write()
leadJPhi.Write()

subleadJPt.Write()
subleadJEta.Write()
subleadJPhi.Write()

thirdJPt.Write()
thirdJEta.Write()
thirdJPhi.Write()

# photon kinematics

photonPt.Write()
photonEta.Write()
photonPhi.Write()

# MET kinematics

metMET.Write()
metPhi.Write()

# leading di-jet pair kinematics

mjjMass.Write()
mJJMass.Write()
mXdXdMass.Write()

jjdPhi.Write()
JJdPhi.Write()
XdXddPhi.Write()

jjdR.Write()
JJdR.Write()
XdXddR.Write()

# MET-X system kinematics

# min MET-j dphi among leading two jets
jminDPhi.Write()

# min MET-J dphi among leading two large-R jets
JminDPhi.Write()

photonMetDPhi.Write()

leadjMetDPhi.Write()
subleadjMetDPhi.Write()
thirdjMetDPhi.Write()

leadJMetDPhi.Write()
subleadJMetDPhi.Write()
thirdJMetDPhi.Write()

dijetMetDPhi.Write()
diJetMetDPhi.Write()

jet_index.Write()
Jet_index.Write()

outf.Close()
