import ROOT as r

#############################
#Histogram definitions
#############################

histos = dict(

#Leading jets kinematics

leadjPt = r.TH1D("leadjPt","leadjPt",20,0,1000),
leadjEta = r.TH1D("leadjEta","leadjEta",50,-5, 5),
leadjPhi = r.TH1D("leadjPhi","leadjPhi",64,-3.2,3.2),

subleadjPt = r.TH1D("subleadjPt","subleadjPt",20,0,1000),
subleadjEta = r.TH1D("subleadjEta","subleadjEta",50,-5, 5),
subleadjPhi = r.TH1D("subleadjPhi","subleadjPhi",64,-3.2,3.2),

thirdjPt = r.TH1D("thirdjPt","thirdjPt",20,0,1000),
thirdjEta = r.TH1D("thirdjEta","thirdjEta",50,-5, 5),
thirdjPhi = r.TH1D("thirdjPhi","thirdjPhi",64,-3.2,3.2),

#Leading large-R jets kinematics

leadJPt = r.TH1D("leadJPt","leadJPt",20,0,1000),
leadJEta = r.TH1D("leadJEta","leadJEta",50,-5, 5),
leadJPhi = r.TH1D("leadJPhi","leadJPhi",64,-3.2,3.2),

subleadJPt = r.TH1D("subleadJPt","subleadJPt",20,0,1000),
subleadJEta = r.TH1D("subleadJEta","subleadJEta",50,-5, 5),
subleadJPhi = r.TH1D("subleadJPhi","subleadJPhi",64,-3.2,3.2),

thirdJPt = r.TH1D("thirdJPt","thirdJPt",20,0,1000),
thirdJEta = r.TH1D("thirdJEta","thirdJEta",50,-5, 5),
thirdJPhi = r.TH1D("thirdJPhi","thirdJPhi",64,-3.2,3.2),

# photon kinematics

photonPt = r.TH1D("photonPt","photonPt",20,0,1000),
photonEta = r.TH1D("photonEta","photonEta",50,-5,5),
photonPhi = r.TH1D("photonPhi","photonPhi",64,-3.2,3.2),

# MET kinematics

metMET = r.TH1D("metMET","metMET",20,0,1000),
metPhi = r.TH1D("metPhi","metPhi",64,-3.2,3.2),

# leading di-jet pair kinematics

mjjMass = r.TH1D("mjjMass","mjjMass",30,0,1500),
mJJMass = r.TH1D("mJJMass","mJJMass",30,0,1500),
mXdXdMass = r.TH1D("mXdXdMass","mXdXdMass",30,0,1500),

jjdPhi = r.TH1D("jjdPhi","jjdPhi",32,0,3.2),
JJdPhi = r.TH1D("JJdPhi","JJdPhi",32,0,3.2),
XdXddPhi = r.TH1D("XdXddPhi","XdXddPhi",32,0,3.2),

jjdR = r.TH1D("jjdR","jjdR",50,0,5),
JJdR = r.TH1D("JJdR","JJdR",50,0,5),
XdXddR = r.TH1D("XdXddR","XdXddR",50,0,5),

# MET-X system kinematics

# min MET-j dphi among leading two jets
jminDPhi = r.TH1D("jminDPhi","jminDPhi",32,0,3.2),

# min MET-J dphi among leading two large-R jets
JminDPhi = r.TH1D("JminDPhi","JminDPhi",32,0,3.2),

photonMetDPhi = r.TH1D("photonMetDPhi","photonMetDPhi",32,0,3.2),

leadjMetDPhi = r.TH1D("leadjMetDPhi","leadjMetDPhi",32,0,3.2),
subleadjMetDPhi = r.TH1D("subleadjMetDPhi","subleadjMetDPhi",32,0,3.2),
thirdjMetDPhi = r.TH1D("thirdjMetDPhi","thirdjMetDPhi",32,0,3.2),

leadJMetDPhi = r.TH1D("leadJMetDPhi","leadJMetDPhi",32,0,3.2),
subleadJMetDPhi = r.TH1D("subleadJMetDPhi","subleadJMetDPhi",32,0,3.2),
thirdJMetDPhi = r.TH1D("thirdJMetDPhi","thirdJMetDPhi",32,0,3.2),

dijetMetDPhi = r.TH1D("dijetMetDPhi","dijetMetDPhi",32,0,3.2),
diJetMetDPhi = r.TH1D("diJetMetDPhi","diJetMetDPhi",32,0,3.2),

# Truth matching
# Jet index of the Xds
jet_index = r.TH1D("jet_index","jet_index",10,0,10),
Jet_index = r.TH1D("Jet_index","Jet_index",10,0,10),

)
