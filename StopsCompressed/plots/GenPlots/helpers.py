import numpy as np
import sys, os
import ROOT
import argparse, glob, random
M_PI = 3.14


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

def weight_time_pdf(tau1, tau2, t):
    oldpdf = 1/tau1*np.exp(-t/tau1)
    newpdf = 1/tau2*np.exp(-t/tau2)
    return newpdf/oldpdf
    #return 1/oldpdf

def get_eff(histA, histB, histC):
    errorA = ROOT.Double()
    histA_int = histA.IntegralAndError(0, -1, errorA)
    errorB = ROOT.Double()
    histB_int = histB.IntegralAndError(0, -1, errorB)
    histC_int = histC.Integral(0, -1)
    pEff = ROOT.TEfficiency(histA, histB)
    pEff_eff = pEff.GetEfficiency(1)
    pEff_err = (pEff.GetEfficiencyErrorLow(1) + pEff.GetEfficiencyErrorUp(1))/2
    return histA_int, errorA, pEff_eff, pEff_err, histA_int/histC_int

def get_xsec(mst = 200.):
   # xsec returned in fb
   stoparray = [200., 250., 300., 350., 400., 450., 500., 550.]
   xsecarray = [0.755E+05, 0.248E+05, 0.100E+05, 0.443E+04, 0.215E+04, 0.111E+04, 0.609E+03, 0.347E+03]
   if mst < stoparray[0]: return -1.
   if mst > stoparray[-1]: rerurn -1.
   xsec = np.interp(mst, stoparray, xsecarray)   
   return xsec

def get_filter_eff(mst = 200.):
   stoparray = [200., 300., 400., 500.]
   effarray = [0.12, 0.185, 0.235, 0.265]
   if mst < stoparray[0]: return None
   if mst > stoparray[-1]: return None
   eff = np.interp(mst, stoparray, effarray)
   return eff
   

