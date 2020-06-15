class triggerSelector:
    def __init__(self, year, era=None):
        if year == 2016:
            self.met     = ["HLT_PFMET90_PFMHT90_IDTight", "HLT_PFMET100_PFMHT100_IDTight", "HLT_PFMET110_PFMHT110_IDTight", "HLT_PFMET120_PFMHT120_IDTight"]
            self.m       = ["HLT_IsoMu24", "HLT_Mu50"]
            self.jet     = ["HLT_PFJet450", "HLT_AK8PFJet450", "HLT_PFHT800"]
            self.e       = ["HLT_Ele27_WPTight_Gsf"] 

        #elif year == 2017:
            #self.mm     = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ", "HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8"]
            #if era in ['C','D','E','F']:
            #    self.mm     += ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8"]
            #if era in ['D','E','F']:
            #    self.mm     += ["HLT_Mu37_TkMu27"]
            #self.m      = ["HLT_IsoMu24", "HLT_IsoMu27", "HLT_Mu50"]
            #self.ee     = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_DoubleEle33_CaloIdL_MW"]
            #self.e      = ["HLT_Ele35_WPTight_Gsf", "HLT_Ele32_WPTight_Gsf_L1DoubleEG"] # no non-isolated triggers in nanoAOD in 2017?HLT_Ele115_CaloIdVT_GsfTrkIdT missing, add single photon trigger? 
            #self.em     = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ"]

        #elif year == 2018:
            #self.mm     = ["HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8", "HLT_Mu37_TkMu27"]
            #self.m      = ["HLT_IsoMu24", "HLT_IsoMu27", "HLT_Mu50"] 
            #self.ee     = ["HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL", "HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ"]
            #self.e      = ["HLT_Ele32_WPTight_Gsf", "HLT_Ele115_CaloIdVT_GsfTrkIdT", "HLT_Ele32_WPTight_Gsf_L1DoubleEG", "HLT_DoubleEle25_CaloIdL_MW"]
            #self.em     = ["HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ", "HLT_Mu27_Ele37_CaloIdL_MW", "HLT_Mu37_Ele27_CaloIdL_MW"]

        else:
            raise NotImplementedError("Trigger selection %r not implemented"%year)

        # define which triggers should be used for which dataset. could join several lists of triggers
        self.MET            = "(%s)"%"||".join( [ "Alt$(%s,0)"%trigger for trigger in self.met ] )
        self.JetHT          = "(%s)"%"||".join( [ "Alt$(%s,0)"%trigger for trigger in self.jet ] )if self.jet else None
        self.SingleMuon     = "(%s)"%"||".join( [ "Alt$(%s,0)"%trigger for trigger in self.m ] ) if self.m else None
        self.SingleElectron = "(%s)"%"||".join( [ "Alt$(%s,0)"%trigger for trigger in self.e ] ) if self.e else None

        # define an arbitrary hierarchy
        if year == 2016 or year == 2017:
            self.PDHierarchy = [ "MET", "JetHT" ,"SingleMuon", "SingleElectron"]
        else:
            # DoubleEG and SingleElectron PDs are merged into EGamma. No change necessary for MC though.
            self.PDHierarchy = [ "MET", "EGamma", "JetHT", "SingleMuon" ]

    def __getVeto(self, cutString):
        return "!%s"%cutString

    def getSelection(self, PD):
        found = False
        cutString = ""
        if PD == "MC":
            return "(%s)"%"||".join([self.MET, self.JetHT, self.SingleMuon, self.SingleElectron])
        else:
            for x in reversed(self.PDHierarchy):
		if not getattr( self, x ): continue 
                if found:
                    cutString += "&&%s"%self.__getVeto(getattr(self,x))
                if x in PD:# == getattr(self, PD):
                    found = True
                    cutString = getattr(self, x)

	    if cutString == "":
		    raise NotImplementedError( "Trigger selection for %s not implemented" %PD )
            return "(%s)"%cutString

