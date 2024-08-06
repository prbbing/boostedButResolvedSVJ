import ROOT as r

#############################
#Histogram definitions
#############################

histos = dict(

#Leading jets kinematics

leadjPt = r.TH1D("leadjPt","leadjPt",20,0,1000),
leadjEta = r.TH1D("leadjEta","leadjEta",50,-5, 5),
leadjPhi = r.TH1D("leadjPhi","leadjPhi",64,-3.2,3.2),
leadjEtaPhi = r.TH2D("leadjEtaPhi","leadjEtaPhi",50,-5,5,64,-3.2,3.2),

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

metMET = r.TH1D("metMET","metMET",40,0,2000),
metPhi = r.TH1D("metPhi","metPhi",64,-3.2,3.2),

# leading di-jet pair kinematics

mjjMass = r.TH1D("mjjMass","mjjMass",40,0,2000),
mJJMass = r.TH1D("mJJMass","mJJMass",40,0,2000),
mXdXdMass = r.TH1D("mXdXdMass","mXdXdMass",30,0,1500),

jjdPhi = r.TH1D("jjdPhi","jjdPhi",32,0,3.2),
JJdPhi = r.TH1D("JJdPhi","JJdPhi",32,0,3.2),
XdXddPhi = r.TH1D("XdXddPhi","XdXddPhi",32,0,3.2),
yStar = r.TH1D("yStar","yStar",100,-5,5),

jjdR = r.TH1D("jjdR","jjdR",50,0,5),
JJdR = r.TH1D("JJdR","JJdR",50,0,5),
XdXddR = r.TH1D("XdXddR","XdXddR",50,0,5),

# dijet-met kinematics

mTjj = r.TH1D("mTjj","mTjj",40,0,2000),
mTjjeff = r.TH1D("mTjjeff","mTjjeff",40,0,2000),
mTjjNeg = r.TH1D("mTjjNeg","mTjjNeg",40,0,2000),
mjjRecomp = r.TH1D("mjjRecomp","mjjRecomp",40,0,2000),
mjjRecompeff = r.TH1D("mjjRecompeff","mjjRecomp",40,0,2000),
mTCom = r.TH1D("mTjjCom","mTjjCom",40,0,2000),
maosjj = r.TH1D("maosjj","maosjj",60,0,3000),
maosjjeff = r.TH1D("maosjjeff","maosjjeff",40,0,2000),
mTJJ = r.TH1D("mTJJ","mTJJ",40,0,2000),
maosJJ = r.TH1D("maosJJ","maosJJ",40,0,2000),
rT = r.TH1D("rT","rT",20,0,1),

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

rinv_ave = r.TH1D("rinv_ave","rinv_ave", 500,-5,5),
rinv_ave_maos = r.TH1D("rinv_ave_maos","rinv_ave_maos", 500,-5,5),

# 2D dphi
jMetDPhi2D = r.TH2D("jMetDPhi2D", "jMetDPhi2D", 32,0,3.2, 32,0,3.2),
JMetDPhi2D = r.TH2D("JMetDPhi2D", "JMetDPhi2D", 32,0,3.2, 32,0,3.2),
jminDPhi_photonPt = r.TH2D("jminDPhi_photonPt","jminDPhi_photonPt", 32,0,3.2, 20,0,1000),
JminDPhi_photonPt = r.TH2D("JminDPhi_photonPt","JminDPhi_photonPt", 32,0,3.2, 20,0,1000),
genmetPt_photonPt = r.TH2D("genmetPt_photonPt","genmetPt_photonPt", 20,0,1000, 20,0,1000),
genmetPt_metaugPt = r.TH2D("genmetPt_metaugPt","genmetPt_metaugPt", 20,0,1000, 20,0,1000),
metPt_metaugPt = r.TH2D("metPt_metaugPt","metPt_metaugPt",100,0,100, 100,0,100),
metPhi_metaugPhi = r.TH2D("metPhi_metaugPhi","metPhi_metaugPhi", 64,-3.2,3.2, 64,-3.2,3.2),
genmetEta_photonEta = r.TH2D("genmetEta_photonEta","genmetEta_photonEta", 25,-5,5, 25,-5,5),
genmetEta_dijetEta = r.TH2D("genmetEta_dijetEta","genmetEta_dijetEta", 25,-5,5, 25,-5,5),
genmetEta_metaugEta = r.TH2D("genmetEta_metaugEta","genmetEta_metaugEta", 25,-5,5, 25,-5,5),
genmetPhi_photonPhi = r.TH2D("genmetPhi_photonPhi","genmetPhi_photonPhi", 64,-3.2,3.2, 64,-3.2,3.2),
rinv1_rinv2 = r.TH2D("rinv1_rinv2","rinv1_rinv2", 500,-5,5, 500,-5,5),
rinv1_rinv2_maos = r.TH2D("rinv1_rinv2_maos","rinv1_rinv2_maos", 500,-5,5, 500,-5,5),
rinv_ave_maosjj = r.TH2D("rinv_ave_maosjj","rinv_ave_maosjj", 500,-5,5, 80,0,4000),
rinv_ave_maos_maosjj = r.TH2D("rinv_ave_maos_maosjj","rinv_ave_maos_maosjj", 500,-5,5, 40,0,2000),
rinv_ave_mTjj = r.TH2D("rinv_ave_mTjj","rinv_ave_mTjj", 500,-5,5, 40,0,2000),

# Truth matching
# Jet index of the Xds
jet_index = r.TH1D("jet_index","jet_index",10,0,10),
Jet_index = r.TH1D("Jet_index","Jet_index",10,0,10),

# Pairing 
closestPairToMet = r.TH1D("closestPairToMet","closestPairToMet",3,0,3), 

)
