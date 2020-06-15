#!/bin/bash
export SCRAM_ARCH=slc6_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_18/src ] ; then 
 echo release CMSSW_10_2_18 already exists
else
scram p CMSSW_10_2_18
fi
cd CMSSW_10_2_18/src
eval `scram runtime -sh`



scram b
cd  ../../
echo $PWD

cmsDriver.py Workspace/DegenerateStopAnalysis/python/fragments/T2tt_displaced_200_160_20_mod.py   \
--python_filename Workspace/DegenerateStopAnalysis/python/cfgs/T2tt_displaced_200_160_20_mod_cfg.py  \
--fileout file:/afs/cern.ch/user/s/sukulkar/work/sukulkar/public/stop_samples/T2tt_displaced_200_160_20_mod.root \
--step LHE,GEN --eventcontent RECOSIM  --mc \
--conditions 102X_upgrade2018_realistic_v11 --beamspot Realistic25ns13TeVEarly2018Collision --era Run2_2018 --geometry DB:Extended\
--nThreads 8 \
-n 50000 \
--no_exec  || exit $? ;

