# StopsCompressed
The most important file here is in ```plots/GenPlots/single_lepton.py```
This file will take an inpur root file or a collection and put generator level cuts as well as perform reweighting in branching ratio and lifetime dimension. To run:
```python single_lepton.py -h```

To setup  this repository
```
cmsrel CMSSW_10_2_12_patch1
cd CMSSW_10_2_12_patch1/src
cmsenv
git cms-init
git clone https://github.com/HephyAnalysisSW/StopsCompressed
git clone https://github.com/HephyAnalysisSW/Samples.git
git clone https://github.com/HephyAnalysisSW/RootTools.git
git clone https://github.com/HephyAnalysisSW/Analysis.git
git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools

#compile
scram b -j9
```
