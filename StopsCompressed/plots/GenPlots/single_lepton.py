''' FWLite example
'''
# Standard imports
import ROOT, copy
from DataFormats.FWLite import Events, Handle
from PhysicsTools.PythonAnalysis import *
from math   import sqrt
import argparse, os
from helpers import *

    
parser = argparse.ArgumentParser(description='Process some arguements')
parser.add_argument("-f", type=str, action='append', nargs='+',
                   help='location of root file')
parser.add_argument("-o", type=str,
                    help='output_directory')

parser.add_argument("-mst", type=str,
                    help='mass of stop')

parser.add_argument("-truetau", type=str,
                    help='true time in mm')
parser.add_argument("-newtau", type=str,
                    help='new time in mm (for no reweighting give same as truetau)')

parser.add_argument("-truebr", type=str,
                    help='true BR (four body)')
parser.add_argument("-newbr", type=str,
                    help='new BR (four body) (for no reweighting give same as truebr)')
args = parser.parse_args()

outdir = args.o
if not os.path.exists(outdir):os.mkdir(outdir)
infile = args.f[0]

mst = float( args.mst)
true_time = float(args.truetau)
new_time = float(args.newtau)

true_br = float(args.truebr)
new_br = float(args.newbr)

c_in_mm = 3e11 # speed of light in mm per second

#brnaching ratio of W to electron and muon
Wbr = 0.2

#new_br is either the same as true_br or is the target BR so just take new_br for finding normalisation
br = Wbr*new_br
xsec = get_xsec(mst = mst)*(2*br -br*br)*get_filter_eff(mst = mst)

print 'prodxsec = ', get_xsec(mst = mst)
print 'newbr = ', new_br
print 'filter_eff =', get_filter_eff(mst = mst)
print 'xsec = ', xsec
#sys.exit()
events = Events(infile)
# GEN
edmCollections = { 
'genParticles':{'type':'vector<reco:GenParticle>', 'label': ( "genParticles", "", "GEN" ) },
'genMET':{'type':'vector<reco::GenMET>', 'label': ( "genMetTrue", "", "GEN" ) },
'ak4GenJets':{'type':'vector<reco:GenJet>', 'label': ( "ak4GenJets", "", "GEN" ) }
   }

# add handles
for k, v in edmCollections.iteritems(): v['handle'] = Handle(v['type'])

nevents = events.size()
#nevents = 100

cutflowfile = open(outdir+'/stop_cutflow_eff.txt', 'w')

f = ROOT.TFile( outdir+'/stop_tot.root', 'recreate' )
hist_MET = ROOT.TH1F("MET", "MET of events", 1000, 0 , 1000)
hist_UNMET = ROOT.TH1F("UnMET", "MET of unweighted events", 1000, 0 , 1000)
hist_REMET = ROOT.TH1F("ReMET", "MET of reweighted events", 1000, 0 , 1000)
hist_stop_time_from_rho = ROOT.TH1F("stop_time_from_rho", "stop time", 5000, 0, 5000)
hist_stop_time_rwt = ROOT.TH1F("stop_time_rwt", "reweighted stop time", 5000, 0, 5000)
hist_muon_lxy = ROOT.TH1F("muon_lxy", "Lxy of the muon emerging from stop", 10000, 0, 50)
hist_muon_dxy = ROOT.TH1F("muon_dxy", "dxy of the muon emerging from stop", 10000, 0, 100)
hist_muon_lxy_2D = ROOT.TH2F( "muon_lxy_2D", '2D Lxy of muons', 1000, 0., 1000, 1000, 0, 1000 )
hist_muon_dxy_2D = ROOT.TH2F( "muon_dxy_2D", '2D Dxy of muons', 1000, 0., 1000, 1000, 0, 1000 )
hist_muon_pt = ROOT.TH1F("muon_pt", "pt of muon arising from stop", 1000, 0, 100)
hist_genjet_pt = ROOT.TH1F("genjet_pt", "pt of hardest gen level jet", 1000, 0, 500)

hist_all = ROOT.TH1F("all_evts","All reweighted events", 1, 0, 5)

hist_HT = ROOT.TH1F("HT","HT of gen level jets", 1, 0, 5)
hist_el5 = ROOT.TH1F("el5","electron > 5", 1, 0, 5)
hist_mu35 = ROOT.TH1F("mu35","mu > 3.5", 1, 0, 5)
hist_met200 = ROOT.TH1F("met200","met > 200", 1, 0, 5)
hist_ht300 = ROOT.TH1F("ht300","ht > 300", 1, 0, 5)
hist_ptj1100 = ROOT.TH1F("ptj1100","pt(j1) > 100", 1, 0, 5)
hist_ptj250 = ROOT.TH1F("ptj250","pt(j2) > 50", 1, 0, 5)
hist_dphi25 = ROOT.TH1F("dphi25","dephi < 2.5", 1, 0, 5)

hist_dxy_02_1 = ROOT.TH1F("dxy_02_1","dxy > 1", 1, 0, 5)
hist_dxy_1_10 = ROOT.TH1F("dxy1_10","1 < dxy < 10", 1, 0, 5)
hist_2bdy_dxy_1_10 = ROOT.TH1F("dxy_2bdy_1_10","1 < dxy < 10 (2bdy)", 1, 0, 5)
hist_4bdy_dxy_1_10 = ROOT.TH1F("dxy_4bdy_1_10","1 < dxy < 10 (4bdy)", 1, 0, 5)
hist_mixed_dxy_1_10 = ROOT.TH1F("dxy_mixed_1_10","1 < dxy < 10 (mixed)", 1, 0, 5)

hist_2bdy_dxy_02_1 = ROOT.TH1F("dxy_2bdy_02_1","1 < dxy < 10 (2bdy)", 1, 0, 5)
hist_4bdy_dxy_02_1 = ROOT.TH1F("dxy_4bdy_02_1","1 < dxy < 10 (4 bdy)", 1, 0, 5)
hist_mixed_dxy_02_1 = ROOT.TH1F("dxy_mixed_02_1","1 < dxy < 10 (mixed)", 1, 0, 5)


hist_mu35.Sumw2()
hist_met200.Sumw2()
hist_ht300.Sumw2()
hist_ptj1100.Sumw2()
hist_ptj250.Sumw2()
hist_dphi25.Sumw2()

hist_dxy_1_10.Sumw2()
hist_dxy_02_1.Sumw2()
print 'total number of events = ', nevents
#nevents = 5000
mothers = []
for i in range(nevents):
  #print 'new event'
  event_2bdy = False
  event_4bdy = False
  event_mixed = False
  newweight  = 1
  daughter_muons = []
  daughter_electrons = []
  daughter_LSPs = []
  total_ht = 0
  if i % 5000 == 0: print 'processing %s event' %(i)
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
  
  # Just get the MET and HT of the eveny
  for p in products['genMET']: met = p.pt() #hist_MET.Fill(p.pt())

  for p in products['ak4GenJets']: total_ht = total_ht + p.pt()
  # create containers for electrons, muons. I start with stop so that I can remove taus, I look for W decays to muons or electrons, no taus.
  for p in products['genParticles']: 
      if abs(p.pdgId()) == 1000006 and p.status() == 22:
        while abs(p.daughter(0).pdgId()) == 1000006: p = p.daughter(0)
        for i in  range(int(p.numberOfDaughters())):
           d1 =  p.daughter(i)
           if abs(d1.pdgId()) == 1000022 and d1.status() == 1: daughter_LSPs.append(d1)
           if abs(d1.pdgId()) == 1000022 and d1.status() != 1:
              gd1 =  d1.daughter(0)
              if abs(gd1.pdgId()) == 1000022 and gd1.status() == 1: daughter_LSPs.append(gd1)
              while abs(gd1.pdgId()) in [1000022] and gd1.status() != 1:
                  gd1 = gd1.daughter(0)
                  if abs(gd1.pdgId()) == 1000022 and gd1.status() == 1: daughter_LSPs.append(gd1)
           if abs(d1.pdgId()) == 24:
              while abs(d1.daughter(0).pdgId()) == 24: d1 = d1.daughter(0)
              for j in  range(int(d1.numberOfDaughters())):
                  gd1 =  d1.daughter(j)
                  if abs(gd1.pdgId()) == 13 and gd1.status() == 1: daughter_muons.append(gd1)
                  while abs(gd1.pdgId()) in [13] and gd1.status() != 1: 
                     gd1 = gd1.daughter(0)
	             if abs(gd1.pdgId()) == 13 and gd1.status() == 1: daughter_muons.append(gd1)
                  if abs(gd1.pdgId()) == 11 and gd1.status() == 1: daughter_electrons.append(gd1)
                  while abs(gd1.pdgId()) in [11] and gd1.status() != 1:
                     gd1 = gd1.daughter(0)
                     if abs(gd1.pdgId()) == 11 and gd1.status() == 1: daughter_electrons.append(gd1)

  newweight = 1.0
  # Determine the correct weight of the event, I start with every LSP, work upwords to find progenitor stop and then compute the weight for BR or lighteime reweighting
  for lsp in daughter_LSPs:
     stopweight = 1.0
     mom = lsp
     while mom.pdgId() == lsp.pdgId(): mom = mom.mother()
     if int(mom.numberOfDaughters()) == 2 : event_2bdy =  True
     if int(mom.numberOfDaughters()) == 3 : event_4bdy = True
     if (new_br != true_br):
        if int(mom.numberOfDaughters()) == 2 : stopweight = stopweight*((1-new_br)/(1-true_br))
        if int(mom.numberOfDaughters()) == 3 : stopweight = stopweight*(new_br/true_br)
     else: stopweight = 1.0
     neut_rho = lsp.vertex().rho()
     stop_rho = mom.vertex().rho()
     stop_lxy = neut_rho - stop_rho
     stop_time = stop_lxy*mom.mass()/mom.pt()
     hist_stop_time_from_rho.Fill(stop_time, 1)
     if (true_time != new_time): stopweight =  stopweight*weight_time_pdf(true_time, new_time, stop_time*10)
     else: stopweight = stopweight*1.0
     hist_stop_time_rwt.Fill(stop_time, stopweight)
     newweight = newweight*stopweight

  #Now apply all cuts
  # The first histogram are uncut events
  hist_all.Fill(1, newweight)
  # Determine if the event has two body, four body or mixed events, this is book keeping has no effect for sensitivity, events in SR
  if event_2bdy == True and event_4bdy == True: event_mixed = True; event_2bdy = False; event_4bdy = False
  # MET requirement
  if met < 200: continue
  hist_met200.Fill(1, newweight)
  # HT requirement
  if total_ht < 300: continue
  hist_ht300.Fill(1, newweight)
  # leading jet
  if products['ak4GenJets'][0].pt() < 100 and abs(products['ak4GenJets'][0].eta()) < 2.5: continue
  hist_ptj1100.Fill(1, newweight)
  #subleading jet
  if products['ak4GenJets'][1].pt() < 50 and abs(products['ak4GenJets'][1].eta()) < 2.5: continue
  hist_ptj250.Fill(1, newweight)
  # delta phi betweeen jets
  if DeltaPhi(products['ak4GenJets'][0].phi(), products['ak4GenJets'][1].phi()) > 2.5: continue
  hist_dphi25.Fill(1, newweight)
  #Following histograms are only for verification purposes, have no effect on events in SR
  hist_genjet_pt.Fill(products['ak4GenJets'][0].pt(), newweight)
  hist_HT.Fill(total_ht, newweight)
  hist_MET.Fill(met, newweight)
  # Now let's check if we have at least one electron or muon in the SR
  # start with electrons
  
  goodel = False
  goodmu = False
  if len(daughter_electrons) >= 1:
    for el in daughter_electrons:
       mom = el
       while abs(mom.pdgId()) != 1000006: mom = mom.mother()
       el_rho = el.vertex().rho()
       stop_rho = mom.vertex().rho()
       stop_lxy = el_rho - stop_rho
       goodel = False
       #goodel = (el.pt() > 5 and abs(el.eta()) < 2.5 and stop_lxy < 5) 
       goodel = (el.pt() > 5 and abs(el.eta()) < 2.5) 
       if goodel: break
  # check for muons
  if len(daughter_muons) >= 1:
      for mu in daughter_muons:
         goodmu = False
         goodmu = (mu.pt() > 3.5 and abs(mu.eta()) < 2.4)
         if goodmu:  break
  # Check if either electron or muon passes criteria
  if (goodmu or goodel): hist_mu35.Fill(1, newweight)
  else: continue
  # Verification purposes Lxy histo, no impact of SR
  for lsp in daughter_LSPs:
     mom = lsp
     while mom.pdgId() == lsp.pdgId(): mom = mom.mother()
     neut_rho = lsp.vertex().rho()
     stop_rho = mom.vertex().rho()
     stop_lxy = neut_rho - stop_rho
     #t = lxy*stop_mass/stop_pt 
     stop_time = stop_lxy*mom.mass()/mom.pt()
     hist_stop_time_from_rho.Fill(stop_time, 1)
     hist_stop_time_rwt.Fill(stop_time, newweight)

  lep_lxy = []
  lep_dxy = []
  # check now if in SR we have electrons or muons
  condition_dxy_02 =  False
  condition_dxy_1 =  False
  # create a lepton array
  lepton_array = daughter_muons
  lepton_array.extend(daughter_electrons)
  # In principle the pT eta cuts should not be necessary below but I am just being cautious
  for lepton in lepton_array:
     mom = lepton
     while abs(mom.pdgId()) != 1000006: mom = mom.mother()
     lepton_rho = lepton.vertex().rho()
     stop_rho = mom.vertex().rho()
     lepton_lxy = abs(lepton_rho - stop_rho)
     lep_lxy.append(lepton_lxy)
     lepton_dxy = dxy(lepton.vertex().x() - mom.vertex().x(), lepton.vertex().y() - mom.vertex().y(), lepton.px(), lepton.py())
     lep_dxy.append(lepton_dxy)
     hist_muon_lxy.Fill(lepton_lxy, newweight)
     hist_muon_dxy.Fill(lepton_dxy, newweight)
     hist_muon_pt.Fill(lepton.pt(), newweight)
     if abs(lepton.pdgId()) == 13:
        condition_dxy_02 = (lepton.pt() > 3.5 and abs(lepton.eta()) < 2.4 and 0.2 < lepton_dxy < 1) or condition_dxy_02
        condition_dxy_1 = (lepton.pt() > 3.5 and abs(lepton.eta()) < 2.4 and 1 < lepton_dxy < 10) or condition_dxy_1
     if abs(lepton.pdgId()) == 11:
        condition_dxy_02 = (lepton.pt() > 5 and abs(lepton.eta()) < 2.5 and 0.2 < lepton_dxy < 1) or condition_dxy_02
        condition_dxy_1 = (lepton.pt() > 5 and abs(lepton.eta()) < 2.5 and 1 < lepton_dxy < 5) or condition_dxy_1

  if condition_dxy_02: 
	hist_dxy_02_1.Fill(1, newweight)#; print "found good lepton, dxy < 1"
        if event_2bdy == True: hist_2bdy_dxy_02_1.Fill(1, newweight)
        if event_4bdy == True: hist_4bdy_dxy_02_1.Fill(1, newweight)
        if event_mixed == True: hist_mixed_dxy_02_1.Fill(1, newweight)
  if condition_dxy_1: 
        hist_dxy_1_10.Fill(1, newweight)#; print "found good lepton, dxy < 10"
        if event_2bdy == True: hist_2bdy_dxy_1_10.Fill(1, newweight)
        if event_4bdy == True: hist_4bdy_dxy_1_10.Fill(1, newweight)
        if event_mixed == True: hist_mixed_dxy_1_10.Fill(1, newweight)
  

# scale histograms to normalize events
scale = ROOT.Double()
scale = xsec/hist_all.Integral(0, -1)
hist_all.Scale(scale)
hist_met200.Scale(scale)
hist_ht300.Scale(scale)
hist_ptj1100.Scale(scale)
hist_ptj250.Scale(scale)
hist_dphi25.Scale(scale)
hist_el5.Scale(scale)
hist_mu35.Scale(scale)
hist_dxy_02_1.Scale(scale)
hist_dxy_1_10.Scale(scale)
hist_mixed_dxy_1_10.Scale(scale)
hist_4bdy_dxy_1_10.Scale(scale)
hist_2bdy_dxy_1_10.Scale(scale)
hist_mixed_dxy_02_1.Scale(scale)
hist_4bdy_dxy_02_1.Scale(scale)
hist_2bdy_dxy_02_1.Scale(scale)

# write out a text file
print 'final numbe of events are = ', hist_all.Integral(0, -1)
cutflowfile.write('#file processed are\n')
cutflowfile.write('# %s \n' %(infile))
cutflowfile.write('# Total number of generated events = %s \n' %(nevents))
cutflowfile.write('#True tau = %s \n' %(true_time))
cutflowfile.write('#Reweighted tau = %s \n' %(new_time))
cutflowfile.write('# True BR = %s \n' %(true_br))
cutflowfile.write('# Reweighted BR = %s \n' %(new_br))

cutflowfile.write(" cut name \t \t tot events \t tot error \t cut eff \t cut eff error \t relative eff \n")

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_all, hist_all, hist_all)
cutflowfile.write( 'No cut \t  \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_met200, hist_all, hist_all)
cutflowfile.write( 'MET > 200  \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_ht300, hist_all, hist_met200)
cutflowfile.write( 'HT > 300  \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_ptj1100, hist_all, hist_ht300)
cutflowfile.write( 'pt(j1) > 100 \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_ptj250, hist_all, hist_ptj1100)
cutflowfile.write('pt(j1) > 100 \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_dphi25, hist_all, hist_ptj250)
cutflowfile.write('dphi > 2.5 \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

#histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_el5, hist_all, hist_dphi25)
#cutflowfile.write('el > 5 \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_mu35, hist_all, hist_dphi25)
cutflowfile.write('mu > 3.5 \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_2bdy_dxy_02_1, hist_all, hist_mu35)
cutflowfile.write('0.2 < dxy < 1 (2bdy) \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_4bdy_dxy_02_1, hist_all, hist_mu35)
cutflowfile.write('0.2 < dxy < 1 (4bdy) \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_mixed_dxy_02_1, hist_all, hist_mu35)
cutflowfile.write('0.2 < dxy < 1 (mixed) \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_2bdy_dxy_1_10, hist_all, hist_mu35)
cutflowfile.write('1 < dxy < 10(2bdy) \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_4bdy_dxy_1_10, hist_all, hist_mu35)
cutflowfile.write('1 < dxy < 10(4bdy) \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_mixed_dxy_1_10, hist_all, hist_mu35)
cutflowfile.write('1 < dxy < 10(mixed) \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_dxy_02_1, hist_all, hist_mu35)
cutflowfile.write('0.2 < dxy < 1 \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

histint, error, pEff_eff, pEff_err, cut_eff = get_eff(hist_dxy_1_10, hist_all, hist_mu35)
cutflowfile.write('1 < dxy < 10 \t \t %0.2E \t %0.2E \t %0.2E \t %0.2E \t %0.2E \n' %(histint, error, pEff_eff, pEff_err, cut_eff))

f.Write()
f.Close()
cutflowfile.close()
