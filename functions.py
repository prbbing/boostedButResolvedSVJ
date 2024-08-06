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

def pt(px, py):
    return np.sqrt(px**2+py**2)

# p = jet, q = met
def rinv_variations(px1, py1, px2, py2, qx1, qy1, qx2, qy2):
    pt1 = pt(px1,py1)
    pt2 = pt(px2,py2)
    qt1 = pt(qx1,qy1)
    qt2 = pt(qx2,qy2)
    # pt of the reconstructed dark jet from summing 2-vecs
    dt1 = pt(px1+qx1,py1+qy1)
    dt2 = pt(px2+qx2,py2+qy2)

    rinvs = {
        'rinv_x': (qx1/(px1+qx1), qx2/(px2+qx2)),
        'rinv_y': (qy1/(py1+qy1), qy2/(py2+qy2)),
        'rinv_t': (qt1/dt1, qt2/dt2),
    }
    rinvs['rinv_xy'] = ((rinvs['rinv_x'][0]+rinvs['rinv_y'][0])/2, (rinvs['rinv_x'][1]+rinvs['rinv_y'][1])/2)

    # add averages
    for key,val in rinvs.items():
        rinvs[key] = (val[0], val[1], (val[0]+val[1])/2)

    return rinvs

def MassRecompose(j1, j2, met):
  px1 = j1.Px()
  px2 = j2.Px()
  py1 = j1.Py()
  py2 = j2.Py()
  pz1 = j1.Pz()
  pz2 = j2.Pz()
  pt1 = j1.Pt()
  pt2 = j2.Pt()
  qx  = met.Px()
  qy  = met.Py()

  a = np.array([[1,1,0,0],[0,0,1,1],[py1,0,-px1,0],[0,py2,0,-px2]])
  b = np.array([qx,qy,0,0])
  x = np.linalg.solve(a, b)
  qx1 = x[0]
  qy1 = x[2]
  qx2 = x[1]
  qy2 = x[3]

  px1_new = px1
  px2_new = px2
  py1_new = py1
  py2_new = py2
  pz1_new = pz1
  pz2_new = pz2
  if x[0]*px1:
    px1_new = px1 + qx1
    py1_new = py1 + qy1
    qt1 = pt(qx1, qy1)
    pz1_new = pz1 + (qt1*pz1)/pt1
  if x[1]*px2:
    px2_new = px2 + qx2
    py2_new = py2 + qy2
    qt2 = pt(qx2, qy2)
    pz2_new = pz2 + (qt2*pz2)/pt2
  e1_new = sqrt(px1_new**2 + py1_new**2 + pz1_new**2 + j1.M()**2)
  e2_new = sqrt(px2_new**2 + py2_new**2 + pz2_new**2 + j2.M()**2)

  j1_new = r.TLorentzVector()
  j1_new.SetPxPyPzE(px1_new,py1_new,pz1_new,e1_new)
  j2_new = r.TLorentzVector()
  j2_new.SetPxPyPzE(px2_new,py2_new,pz2_new,e2_new)

  results = {
    'mass': (j1_new + j2_new).M(),
  }
  results.update(
    rinv_variations(px1, py1, px2, py2, qx1, qy1, qx2, qy2)
  )
  return results

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
  results = {
    'mass': maos_val,
  }
  results.update(
    rinv_variations(lead_j.Px(), lead_j.Py(), sublead_j.Px(), sublead_j.Py(), met1x, met1y, met2x, met2y)
  )
  return results
