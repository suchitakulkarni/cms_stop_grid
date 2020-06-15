''' FWLite example
'''
# Standard imports
import ROOT
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math   import sqrt
import argparse, os
from helpers import *
parser = argparse.ArgumentParser(description='Process some arguements')
parser.add_argument("-f", type=str,
                   help='location of root file')
parser.add_argument("-o", type=str,
                    help='output_directory')
args = parser.parse_args()

outdir = args.o
if not os.path.exists(outdir):os.mkdir(outdir)
infile = args.f


small = False
#events = Events(['file:/afs/cern.ch/user/s/sukulkar/work/sukulkar/public/T2tt_displaced_200_180_5.root'])
events = Events(['file:%s' %(infile)])
# Use 'edmDumpEventContent <file>' to list all products. Then, make a simple dictinary as below for the products you want to read.
# vector<reco::GenMET>                  "genMetTrue"            ""         "GEN" 

# GEN
edmCollections = { 
'genParticles':{'type':'vector<reco:GenParticle>', 'label': ( "genParticles", "", "GEN" ) },
'genMET':{'type':'vector<reco::GenMET>', 'label': ( "genMetTrue", "", "GEN" ) },
'ak4GenJets':{'type':'vector<reco:GenJet>', 'label': ( "ak4GenJets", "", "GEN" ) }
   }

# add handles
for k, v in edmCollections.iteritems(): v['handle'] = Handle(v['type'])

nevents = 1 if small else events.size()

cutflowfile = open(outdir+'/stop_cutflow_eff.txt', 'w')

f = ROOT.TFile( outdir+'/stop_tot.root', 'recreate' )
hist_lxy_stop = ROOT.TH1F("lxy_stop", "Stops Transverse decay length (13 TeV);Lxy[cm];number of events", 10000, 0, 10)
hist_stop_rho = ROOT.TH1F("rho_stop", "stop transverse decay length", 10000, 0, 10)
hist_pt_stop = ROOT.TH1F("pt_stop", "pT of stops", 1000, 0 , 1000)
hist_MET = ROOT.TH1F("MET", "MET of events", 1000, 0 , 1000)
hist_stop_time = ROOT.TH1F("stop_time", "stop time", 1000, 0 , 20)
hist_stop_time_from_rho = ROOT.TH1F("stop_time_from_rho", "stop time", 1000, 0, 20)
hist_muon_lxy = ROOT.TH1F("muon_lxy", "Lxy of the muon emerging from stop", 10000, 0, 50)
hist_muon_dxy = ROOT.TH1F("muon_dxy", "dxy of the muon emerging from stop", 10000, 0, 100)
hist_muon_lxy_2D = ROOT.TH2F( "muon_lxy_2D", '2D Lxy of muons', 1000, 0., 1000, 1000, 0, 1000 )
hist_muon_dxy_2D = ROOT.TH2F( "muon_dxy_2D", '2D Dxy of muons', 1000, 0., 1000, 1000, 0, 1000 )
hist_muon_pt = ROOT.TH1F("muon_pt", "pt of muon arising from stop", 1000, 0, 100)
hist_genjet_pt = ROOT.TH1F("genjet_pt", "pt of hardest gen level jet", 1000, 0, 500)
hist_HT = ROOT.TH1F("HT","HT of gen level jets", 1000, 0, 1000)

cutdict = {'mu35':0, 'met200':0, 'ht300':0, 'jet1pt100':0, 'jet2pt50':0, 'dphijet25':0, 'lxy1dxy1':0, 'lxy2dxy2':0, 'lxy3dxy3':0, 'dxy02':0, 'dxy1':0}
#histo.Sumw2()
#histol.Sumw2()
mothers = []
#nevents = 50
for i in range(nevents):
  daughter_muons = []
  daughter_LSPs = []
  total_ht = 0
  if i % 100 == 0: print 'processing %s event' %(i)
  events.to(i)
  eaux  = events.eventAuxiliary()
  run   = eaux.run()
  event = eaux.event()
  lumi  = eaux.luminosityBlock()
  #read all products as specifed in edmCollections
  products = {}

  for k, v in edmCollections.iteritems():
    events.getByLabel(v['label'], v['handle'])
    products[k] = v['handle'].product()

  for p in products['genMET']: met = p.pt() #hist_MET.Fill(p.pt())

  #hist_genjet_pt.Fill(products['ak4GenJets'][0].pt())

  for p in products['ak4GenJets']: total_ht = total_ht + p.pt()

  for p in products['genParticles']: 
      if abs(p.pdgId()) == 1000006 and p.status() == 22:
        while abs(p.daughter(0).pdgId()) == 1000006: p = p.daughter(0)
        for i in  range(int(p.numberOfDaughters())):
           d1 =  p.daughter(i)
           if abs(d1.pdgId()) == 1000022 and d1.status() == 1: daughter_LSPs.append(d1)
           if abs(d1.pdgId()) == 13 and d1.status() == 1: daughter_muons.append(d1)
           while abs(d1.pdgId()) in [13] and d1.status() != 1: 
               d1 = d1.daughter(0)
	       if abs(d1.pdgId()) == 13 and d1.status() == 1: daughter_muons.append(d1)
  #cutdict = {'mu35':0, 'met200':0, 'ht300':0, 'jet1pt100':0, 'jet2pt50':0, 'dphijet25':0}
  # at least one muon with pT > 3.5
  mu1 = False
  mu2 = False
  mu1 = (daughter_muons[0].pt() > 3.5 and abs(daughter_muons[0].eta()) < 2.4)
  mu2 = (daughter_muons[1].pt() > 3.5 and abs(daughter_muons[1].eta()) < 2.4)
  if not (mu1 or mu2): continue
  cutdict['mu35'] = cutdict['mu35'] + 1
  if met < 200: continue
  cutdict['met200'] = cutdict['met200'] + 1
  if total_ht < 300: continue
  cutdict['ht300'] = cutdict['ht300'] + 1
  if products['ak4GenJets'][0].pt() < 100 and abs(products['ak4GenJets'][0].eta()) < 2.5: continue
  cutdict['jet1pt100'] = cutdict['jet1pt100'] + 1
  if products['ak4GenJets'][1].pt() < 50 and abs(products['ak4GenJets'][1].eta()) < 2.5: continue
  cutdict['jet2pt50'] = cutdict['jet2pt50'] + 1
  if DeltaPhi(products['ak4GenJets'][0].phi(), products['ak4GenJets'][1].phi()) > 2.5: continue
  cutdict['dphijet25'] = cutdict['dphijet25'] + 1
  hist_genjet_pt.Fill(products['ak4GenJets'][0].pt())
  hist_HT.Fill(total_ht)
  hist_MET.Fill(met)
  for lsp in daughter_LSPs:
     mom = lsp
     while mom.pdgId() == lsp.pdgId(): mom = mom.mother()
     neut_rho = lsp.vertex().rho()
     stop_rho = mom.vertex().rho()
     stop_lxy = neut_rho - stop_rho
     #t = lxy*stop_mass/stop_pt 
     stop_time = stop_lxy*mom.mass()/mom.pt()
     hist_stop_time_from_rho.Fill(stop_time)
  lxy = []
  mu_dxy = []
  for muon in daughter_muons:
     mom = muon
     while abs(mom.pdgId()) == abs(muon.pdgId()): mom = mom.mother()
     muon_rho = muon.vertex().rho()
     stop_rho = mom.vertex().rho()
     muon_lxy = abs(muon_rho - stop_rho)
     lxy.append(muon_lxy)
     muon_dxy = dxy(muon.vertex().x() - mom.vertex().x(), muon.vertex().y() - mom.vertex().y(), muon.px(), muon.py())
     mu_dxy.append(muon_dxy)
     hist_muon_lxy.Fill(muon_lxy)
     hist_muon_dxy.Fill(muon_dxy)
     hist_muon_pt.Fill(muon.pt())
  hist_muon_lxy_2D.Fill(lxy[0], lxy[1])
  hist_muon_dxy_2D.Fill(mu_dxy[0], mu_dxy[1])
  mu1lxy = (lxy[0] > 1 or mu_dxy[0] > 1)
  mu2lxy = (lxy[1] > 1 or mu_dxy[1] > 1)
  if (mu1lxy or mu2lxy): cutdict['lxy1dxy1'] = cutdict['lxy1dxy1'] + 1

  mu1lxy = (lxy[0] > 2 or mu_dxy[0] > 2)
  mu2lxy = (lxy[1] > 2 or mu_dxy[1] > 2)
  if (mu1lxy or mu2lxy): cutdict['lxy2dxy2'] = cutdict['lxy2dxy2'] + 1

  mu1lxy = (lxy[0] > 3 or mu_dxy[0] > 3)
  mu2lxy = (lxy[1] > 3 or mu_dxy[1] > 3)
  if (mu1lxy or mu2lxy): cutdict['lxy3dxy3'] = cutdict['lxy3dxy3'] + 1
  
  dxy02_pass = ( 0.2 < mu_dxy[0] < 1 or 0.2 < mu_dxy[1] < 1 )
  if dxy02_pass: cutdict['dxy02'] = cutdict['dxy02'] + 1
  dxy1_pass = ( 1 < mu_dxy[0] < 10 or 1 < mu_dxy[1] < 10 )
  if dxy1_pass: cutdict['dxy1'] = cutdict['dxy1'] + 1
f.Write()
f.Close()

print >> cutflowfile, "#cut name \t absolute efficiency \t relative efficiency"
print >> cutflowfile, 'mu>3.5GeV  %0.2E \t %0.2E' %(float(cutdict['mu35'])/float(nevents), float(cutdict['mu35'])/float(cutdict['mu35']) )
print >> cutflowfile, 'MET>200GeV %0.2E \t %0.2E' %(float(cutdict['met200'])/float(nevents), float(cutdict['met200'])/float(cutdict['mu35']))
print >> cutflowfile, 'HT>300GeV %0.2E \t %0.2E' %(float(cutdict['ht300'])/float(nevents), float(cutdict['ht300'])/float(cutdict['met200']))
print >> cutflowfile, 'pT(j1)>100GeV %0.2E \t %0.2E' %(float(cutdict['jet1pt100'])/float(nevents), float(cutdict['jet1pt100'])/float(cutdict['ht300']))
print >> cutflowfile, 'pT(j2)>50GeV %0.2E \t %0.2E' %(float(cutdict['jet2pt50'])/float(nevents), float(cutdict['jet2pt50'])/float(cutdict['jet1pt100']))
print >> cutflowfile, 'deltaphi(j1,j2)>2.5 %0.2E \t %0.2E' %(float(cutdict['dphijet25'])/float(nevents), float(cutdict['dphijet25'])/float(cutdict['jet2pt50']))
print >> cutflowfile, 'lxy>1cm,dxy>1cm %0.2E \t %0.2E' %(float(cutdict['lxy1dxy1'])/float(nevents), float(cutdict['lxy1dxy1'])/float(cutdict['dphijet25']))
print >> cutflowfile, 'lxy>2cm,dxy>2cm %0.2E \t %0.2E' %(float(cutdict['lxy2dxy2'])/float(nevents), float(cutdict['lxy2dxy2'])/float(cutdict['dphijet25']))
print >> cutflowfile, 'lxy>3cm,dxy>3cm %0.2E \t %0.2E' %(float(cutdict['lxy3dxy3'])/float(nevents), float(cutdict['lxy3dxy3'])/float(cutdict['dphijet25']))
print >> cutflowfile, 'dxy>0.2cm %0.2E \t %0.2E' %(float(cutdict['dxy02'])/float(nevents), float(cutdict['dxy02'])/float(cutdict['dphijet25']))
print >> cutflowfile, 'dxy<0.2cm&dxy<1cm %0.2E \t %0.2E' %(float(cutdict['dxy1'])/float(nevents), float(cutdict['dxy1'])/float(cutdict['dphijet25']))
