mport ROOT
import os,sys,re
import numpy as np
import math
ROOT.gSystem.Load("/Users/adminbingxuanliu/Work/MCGeneration/MG5_aMC_v3_5_1/DELPHES/libDelphes.so")
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

outf = ROOT.TFile("output.root","RECREATE")
mass = ROOT.TH1D("mass","mass",30,0,1500)
minDPhi = ROOT.TH1D("minDPhi","minDPhi",32,0,3.2)
dPhi = ROOT.TH1D("dPhi","dPhi",32,0,3.2)

chain = ROOT.TChain("Delphes")
chain.Add("Events/run_01/Z500_rinv0p5.root")

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()
branchJet = treeReader.UseBranch("Jet")
branchMuon = treeReader.UseBranch("Muon")
branchPhoton = treeReader.UseBranch("Photon")
branchMet = treeReader.UseBranch("MissingET")

for entry in range(0, numberOfEntries):
  # Load selected branches with data from specified event
  treeReader.ReadEntry(entry)

  lead_j = ROOT.TLorentzVector()
  sublead_j = ROOT.TLorentzVector()

  # If event contains at least 1 jet
  for j in range(0,  branchJet.GetEntries()):
    jet = branchJet.At(j)
    if jet.PT > lead_j.Pt():
      lead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < lead_j.Pt() and jet.PT > sublead_j.Pt():
      sublead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

  if branchJet.GetEntries() < 2:
    continue

  met = ROOT.TLorentzVector()
  met.SetPtEtaPhiM(branchMet.At(0).MET, 0, branchMet.At(0).Phi,0)

  photon = ROOT.TLorentzVector()

  for j in range(0,  branchPhoton.GetEntries()):
    pho = branchPhoton.At(j)
    if pho.PT > photon.Pt():
      photon.SetPtEtaPhiM(pho.PT, pho.Eta, pho.Phi, 0)


  minDPhi.Fill(min([lead_j.DeltaPhi(met), sublead_j.DeltaPhi(met)]))
  dPhi.Fill(met.DeltaPhi(photon))

  mass.Fill((lead_j + sublead_j ).M())

outf.cd()
mass.Write()
minDPhi.Write()
dPhi.Write()
outf.Close()
