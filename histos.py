import ROOT

#############################
#Histogram definitions
#############################

#Leading jets kinematics

leadjPt = ROOT.TH1D("leadjPt","leadjPt",20,0,1000)
leadjEta = ROOT.TH1D("leadjEta","leadjEta",50,-5, 5)
leadjPhi = ROOT.TH1D("leadjPhi","leadjPhi",64,-3.2,3.2)

subleadjPt = ROOT.TH1D("subleadjPt","subleadjPt",20,0,1000)
subleadjEta = ROOT.TH1D("subleadjEta","subleadjEta",50,-5, 5)
subleadjPhi = ROOT.TH1D("subleadjPhi","subleadjPhi",64,-3.2,3.2)

thirdjPt = ROOT.TH1D("thirdjPt","thirdjPt",20,0,1000)
thirdjEta = ROOT.TH1D("thirdjEta","thirdjEta",50,-5, 5)
thirdjPhi = ROOT.TH1D("thirdjPhi","thirdjPhi",64,-3.2,3.2)

#Leading large-R jets kinematics

leadJPt = ROOT.TH1D("leadJPt","leadJPt",20,0,1000)
leadJEta = ROOT.TH1D("leadJEta","leadJEta",50,-5, 5)
leadJPhi = ROOT.TH1D("leadJPhi","leadJPhi",64,-3.2,3.2)

subleadJPt = ROOT.TH1D("subleadJPt","subleadJPt",20,0,1000)
subleadJEta = ROOT.TH1D("subleadJEta","subleadJEta",50,-5, 5)
subleadJPhi = ROOT.TH1D("subleadJPhi","subleadJPhi",64,-3.2,3.2)

thirdJPt = ROOT.TH1D("thirdJPt","thirdJPt",20,0,1000)
thirdJEta = ROOT.TH1D("thirdJEta","thirdJEta",50,-5, 5)
thirdJPhi = ROOT.TH1D("thirdJPhi","thirdJPhi",64,-3.2,3.2)

# photon kinematics

photonPt = ROOT.TH1D("photonPt","photonPt",20,0,1000)
photonEta = ROOT.TH1D("photonEta","photonEta",50,-5,5)
photonPhi = ROOT.TH1D("photonPhi","photonPhi",64,-3.2,3.2)

# MET kinematics

metMET = ROOT.TH1D("metMET","metMET",20,0,1000)
metPhi = ROOT.TH1D("metPhi","metPhi",64,-3.2,3.2)

# leading di-jet pair kinematics

mjjMass = ROOT.TH1D("mjjMass","mjjMass",30,0,1500)
mJJMass = ROOT.TH1D("mJJMass","mJJMass",30,0,1500)
mXdXdMass = ROOT.TH1D("mXdXdMass","mXdXdMass",30,0,1500)

jjdPhi = ROOT.TH1D("jjdPhi","jjdPhi",32,0,3.2)
JJdPhi = ROOT.TH1D("JJdPhi","JJdPhi",32,0,3.2)
XdXddPhi = ROOT.TH1D("XdXddPhi","XdXddPhi",32,0,3.2)

jjdR = ROOT.TH1D("jjdR","jjdR",50,0,5)
JJdR = ROOT.TH1D("JJdR","JJdR",50,0,5)
XdXddR = ROOT.TH1D("XdXddR","XdXddR",50,0,5)

# MET-X system kinematics

# min MET-j dphi among leading two jets
jminDPhi = ROOT.TH1D("jminDPhi","jminDPhi",32,0,3.2)

# min MET-J dphi among leading two large-R jets
JminDPhi = ROOT.TH1D("JminDPhi","JminDPhi",32,0,3.2)

photonMetDPhi = ROOT.TH1D("photonMetDPhi","photonMetDPhi",32,0,3.2)

leadjMetDPhi = ROOT.TH1D("leadjMetDPhi","leadjMetDPhi",32,0,3.2)
subleadjMetDPhi = ROOT.TH1D("subleadjMetDPhi","subleadjMetDPhi",32,0,3.2)
thirdjMetDPhi = ROOT.TH1D("thirdjMetDPhi","thirdjMetDPhi",32,0,3.2)

leadJMetDPhi = ROOT.TH1D("leadJMetDPhi","leadJMetDPhi",32,0,3.2)
subleadJMetDPhi = ROOT.TH1D("subleadJMetDPhi","subleadJMetDPhi",32,0,3.2)
thirdJMetDPhi = ROOT.TH1D("thirdJMetDPhi","thirdJMetDPhi",32,0,3.2)

dijetMetDPhi = ROOT.TH1D("dijetMetDPhi","dijetMetDPhi",32,0,3.2)
diJetMetDPhi = ROOT.TH1D("diJetMetDPhi","diJetMetDPhi",32,0,3.2)

# Truth matching
# Jet index of the Xds
jet_index = ROOT.TH1D("jet_index","jet_index",10,0,10)
Jet_index = ROOT.TH1D("Jet_index","Jet_index",10,0,10)
