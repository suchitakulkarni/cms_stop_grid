
import numpy as np
import sys, os
import ROOT
import argparse, glob, random
M_PI = 3.14
speed_of_light = 3E8 #m/s

def dxy(x, y, px, py):
    dxy = abs(y*px -x*py)/np.sqrt(px*px+py*py);
    return dxy;

def DeltaPhi(phi1, phi2):
    dPhi = phi1 - phi2;
    if (dPhi  >  M_PI): dPhi -= 2*M_PI
    if (dPhi <= - M_PI): dPhi += 2*M_PI
    return abs(dPhi)

def DeltaR(eta1, eta2, phi1, phi2):
    dEta = eta1 - eta2
    dPhi = DeltaPhi(phi1, phi2)
    return np.sqrt(dEta*dEta + dPhi*dPhi)


def smearing_function():
    xarray = np.linspace(-1000, 1000, 2000)
    fxarray = []
    for x in xarray:
        constant = 1
        mean = -1.72142e+00;
        sigma = 1.32009e+01 * (1 - 0.0843956);
        alpha = 1.66707e+00 * (1 - 0.0498447);
        z = (x - mean) / sigma;
        alpha = abs(alpha);
        norm1 = sigma * np.sqrt(2 * np.pi) * np.erf(alpha / np.sqrt(2));
        norm2 = sigma * np.exp(-alpha * alpha / 2) / alpha;
        norm3 = norm2;
        constant /= (norm1 + norm2 + norm3);
        if (z < -alpha) :
            fxarray.append(constant * np.exp(+alpha * (z + 0.5 * alpha)))
        elif (z > +alpha):
            fxarray.append(constant * np.exp(-alpha * (z - 0.5 * alpha)))
        else:
            fxarray.append(constant * np.exp(-0.5 * z * z))
    
    val = random.uniform(-1000, 1000)
    return np.interp(val, xarray, fxarray)
    
class part(object):
    def __init__(self, PID, E, P, pT, eta, phi, charge):
        self.PID = PID
        self.P = P
        self.E = E
        self.pt = pT
        self.eta = eta
        self.phi = phi
        self.charge = charge
    def __str__(self):
        return str(self.__dict__)

def geteff(ineta = 2., inlxy = 200.):
    '''inFileName = "official_acce_eff_EW/HEPData-ins1641262-v3-Tracklet_Acceptance_times_Efficiency_EW.csv"

    inlines = open(inFileName, 'r').read().split('\n')
    outarray =[ineta, inlxy, 0]
    for aline in inlines:
        if not aline.strip(): continue
        if '#' in aline: continue
        etalow = float(aline.split(',')[1])
        etahigh = float(aline.split(',')[2])
        lxylow = float(aline.split(',')[4])
        lxyhigh= float(aline.split(',')[5])
        eff = float(aline.split(',')[6])
        if ineta >= etalow and ineta < etahigh and inlxy >= lxylow and inlxy < lxyhigh:
            outarray = [ineta, inlxy, eff]'''
    outarray =[ineta, inlxy, 0]
    afile = ROOT.TFile('official_acce_eff_EW/DisappearingTrack2016-TrackAcceptanceEfficiency.root')
    hist = afile.Get('ElectroweakEfficiency')
    
    eff = hist.GetBinContent(hist.FindBin(ineta, inlxy))
    outarray = [ineta, inlxy, eff]
    return outarray


def geteff_strong(ineta = 2., inlxy = 200.):
    outarray =[ineta, inlxy, 0]
    afile = ROOT.TFile('official_acce_eff_EW/DisappearingTrack2016-TrackAcceptanceEfficiency.root')
    hist = afile.Get('StrongEfficiency')

    eff = hist.GetBinContent(hist.FindBin(ineta, inlxy))
    outarray = [ineta, inlxy, eff]
    return outarray


def remove_overlap_dR(list1, list2, deltaR):
    '''will remove objects from list1 if deltaR is less than specified'''
    listfin = []
    if len(list1) == 0: return list1
    if len(list2) == 0: return list1
    toremove = []
    for partB in list2:
        for partA in list1:
            dR =  DeltaR(partA.eta, partB.eta, partA.phi, partB.phi)
            if (dR < deltaR): list1.remove(partA)
    return list1

def make_particle(d, i):

    mom = np.sqrt(d.Particle_Px[i]*d.Particle_Px[i]+d.Particle_Py[i]*d.Particle_Py[i]+d.Particle_Pz[i]*d.Particle_Pz[i])
    #particle = part(d.Particle_PID[i], d.Particle_E[i], d.Particle_P[i], d.Particle_PT[i], d.Particle_Eta[i], d.Particle_Phi[i], d.Particle_Charge[i])
    particle = part(d.Particle_PID[i], d.Particle_E[i], mom, d.Particle_PT[i], d.Particle_Eta[i], d.Particle_Phi[i], d.Particle_Charge[i])
    particle.px = d.Particle_Px[i]
    particle.py = d.Particle_Py[i]
    particle.pz = d.Particle_Pz[i]
    particle.lxy = np.sqrt(d.Particle_X[i]*d.Particle_X[i] + d.Particle_Y[i]*d.Particle_Y[i])
    particle.mass = d.Particle_Mass[i]
    particle.charge = d.Particle_Charge[i]
    particle.pid = d.Particle_PID[i]
    #beta = d.Particle_P[i]/d.Particle_E[i]
    beta = mom/d.Particle_E[i]
    gamma = 0
    if beta < 1: gamma = 1/np.sqrt(1-beta*beta)
    else: beta = 0; gamma = 0
    particle.beta = beta
    particle.gamma = gamma
    particle.momentum = mom
    #particle.momentum = d.Particle_P[i]
    return particle

def draw_from_lifetime(tracklet, tau):
    beta = tracklet.beta
    gamma = tracklet.gamma
    decayvec = ROOT.TVector3()
    llpmomentum = ROOT.TVector3()
    llpmomentum.SetXYZ(tracklet.px, tracklet.py, tracklet.pz);
    decayvec = llpmomentum.Unit() * ROOT.gRandom.Exp(speed_of_light * 1e3 * tau * 1e-9 * gamma * beta)
    decaydist = decayvec.Perp()
    eta = decayvec.PseudoRapidity()
    return decaydist, eta
