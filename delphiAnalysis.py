import ROOT
import os,sys,re
import numpy as np
import math
ROOT.gSystem.Load("/Users/adminbingxuanliu/Work/MCGeneration/MG5_aMC_v3_5_1/DELPHES/libDelphes.so")
ROOT.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
ROOT.gInterpreter.Declare('#include "external/ExRootAnalysis/ExRootTreeReader.h"')

outf = ROOT.TFile("output.root","RECREATE")
mass = ROOT.TH1D("mass","mass",30,0,1500)
minDPhi = ROOT.TH1D("minDPhi","minDPhi",32,0,3.2)
leadjet_pt = ROOT.TH1D("pt_lead","pt_lead",20,0,1000)
subleadjet_pt = ROOT.TH1D("pt_sublead","pt_sublead",20,0,1000)
dPhi_sublead = ROOT.TH1D("dPhi_sublead","dphi_sublead",32,0,3.2)
dPhi_lead = ROOT.TH1D("dPhi_lead","dPhi_lead",32,0,3.2)
dPhi_2D = ROOT.TH2D("dPhi_2D","dPhi_2D", 32,0,3.2, 32,0,3.2)
dPhi_y = ROOT.TH1D("dPhi_y","dPhi_y",32,0,3.2)

chain = ROOT.TChain("Delphes")
chain.Add("Events/run_01/Z500_GammaISR500_rinv0p5.root")

# Create object of class ExRootTreeReader
treeReader = ROOT.ExRootTreeReader(chain)
numberOfEntries = treeReader.GetEntries()
branchWeight = treeReader.UseBranch("Weight")
branchJet = treeReader.UseBranch("Jet")
branchMuon = treeReader.UseBranch("Muon")
branchPhoton = treeReader.UseBranch("Photon")
branchMet = treeReader.UseBranch("MissingET")

for entry in range(0, numberOfEntries):

  treeReader.ReadEntry(entry)

  weight = branchWeight.At(0).Weight

  lead_j = ROOT.TLorentzVector()
  sublead_j = ROOT.TLorentzVector()

  for j in range(0,  branchJet.GetEntries()):
    jet = branchJet.At(j)
    if jet.PT < 25:
      continue
    if abs(jet.Eta) > 2.5:
      continue
    if jet.PT > lead_j.Pt():
      lead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)
    if jet.PT < lead_j.Pt() and jet.PT > sublead_j.Pt():
      sublead_j.SetPtEtaPhiM(jet.PT, jet.Eta, jet.Phi, jet.Mass)

  leadjet_pt.Fill(lead_j.Pt(), weight)
  subleadjet_pt.Fill(sublead_j.Pt(), weight)


  if branchJet.GetEntries() < 2:
    continue

  met = ROOT.TLorentzVector()
  met.SetPtEtaPhiM(branchMet.At(0).MET, 0, branchMet.At(0).Phi,0)

  photon = ROOT.TLorentzVector()

  for j in range(0,  branchPhoton.GetEntries()):
    pho = branchPhoton.At(j)
    if pho.PT > photon.Pt():
      photon.SetPtEtaPhiM(pho.PT, pho.Eta, pho.Phi, 0)


  minDPhi.Fill(min([lead_j.DeltaPhi(met), sublead_j.DeltaPhi(met)]), weight)
  dPhi_lead.Fill(lead_j.DeltaPhi(met), weight)
  dPhi_sublead.Fill(sublead_j.DeltaPhi(met), weight)
  dPhi_2D.Fill(lead_j.DeltaPhi(met), sublead_j.DeltaPhi(met), weight)
  dPhi_y.Fill(met.DeltaPhi(photon), weight)

  mass.Fill((lead_j + sublead_j ).M(), weight)

outf.cd()
mass.Write()
minDPhi.Write()
dPhi_lead.Write()
dPhi_sublead.Write()
dPhi_2D.Write()
dPhi_y.Write()
leadjet_pt.Write()
subleadjet_pt.Write()
outf.Close()
~                  
