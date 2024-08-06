import numpy as np
from math import *

import ROOT as r
r.gInterpreter.Declare('#include "classes/DelphesClasses.h"')
r.gInterpreter.Declare('#include "ExRootAnalysis/ExRootTreeReader.h"')
r.gInterpreter.Declare('#include "lester_mt2_bisect.h"')
r.asymm_mt2_lester_bisect.disableCopyrightMessage()

def deltaPhi(phi1, phi2):
    delta_phi = 0
    if phi1 - phi2 > pi: 
        delta_phi = 2*pi - (phi1 - phi2)
    elif phi1 - phi2 < -pi:
        delta_phi = -2*pi - (phi1 - phi2)
    else:
        delta_phi = phi1 - phi2
    return delta_phi

def TransverseMass(px1, py1, m1, px2, py2, m2):
  E1 = np.sqrt(px1**2+py1**2+m1**2)
  E2 = np.sqrt(px2**2+py2**2+m2**2)
  MTsq = (E1+E2)**2-(px1+px2)**2-(py1+py2)**2
  return np.sqrt(max(MTsq,0.0))

def MassRecompose(j1, j2, met):
  px1 = j1.Px()
  px2 = j2.Px()
  py1 = j1.Py()
  py2 = j2.Py()
  pz1 = j1.Pz()
  pz2 = j2.Pz()
  pt1 = j1.Pt()
  pt2 = j2.Pt()
  px  = met.Px()
  py  = met.Py()

  a = np.array([[1,1,0,0],[0,0,1,1],[py1,0,-px1,0],[0,py2,0,-px2]])
  b = np.array([px,py,0,0])
  x = np.linalg.solve(a, b)
  px1_new = px1
  px2_new = px2
  py1_new = py1
  py2_new = py2
  pz1_new = pz1
  pz2_new = pz2
  if x[0]*px1:
    px1_new = px1 + x[0]
    py1_new = py1 + x[2]
    pt1_new = np.sqrt(x[0]**2+x[2]**2)
    pz1_new = pz1 + (pt1_new*pz1)/pt1
  if x[1]*px2:
    px2_new = px2 + x[1]
    py2_new = py2 + x[3]
    pt2_new = np.sqrt(x[1]**2+x[3]**2)
    pz2_new = pz2 + (pt2_new*pz2)/pt2
  e1_new = sqrt(px1_new**2 + py1_new**2 + pz1_new**2 + j1.M()**2)
  e2_new = sqrt(px2_new**2 + py2_new**2 + pz2_new**2 + j2.M()**2)

  pz = (x[0]*pz1)/px1 + (x[1]*pz2)/px2
  met.SetPz(pz)

  j1_new = r.TLorentzVector()
  j1_new.SetPxPyPzE(px1_new,py1_new,pz1_new,e1_new)
  j2_new = r.TLorentzVector()
  j2_new.SetPxPyPzE(px2_new,py2_new,pz2_new,e2_new)

  rinv_1 = x[0]/(px1 + x[0])
  rinv_2 = x[1]/(px2 + x[1])
  return {
    'mass': (j1_new + j2_new).M(),
    'rinv1': rinv_1,
    'rinv2': rinv_2,
    'rinvAve': (rinv_1 + rinv_2)/2,
  }

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
  vec_sum_1 = np.sqrt((lead_j.Px() + met1x)**2 + (lead_j.Py() + met1y)**2)
  vec_sum_2 = np.sqrt((sublead_j.Px() + met2x)**2 + (sublead_j.Py() + met2y)**2)
  rinv_1 = v_met1.Pt()/vec_sum_1
  rinv_2 = v_met2.Pt()/vec_sum_2
  return {
    'mass': maos_val,
    'rinv1': rinv_1,
    'rinv2': rinv_2,
    'rinvAve': (rinv_1+rinv_2)/2,
  }
