#!/bin/bash    

args=("$@")
#cmsRun ${args[0]}

# the directory of the script
#DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
DIR=$PWD
# the temp directory used, within $DIR
# omit the -p parameter to create a temporal directory in the default location
WORK_DIR=`mktemp -d -p "$DIR"`

# check if tmp dir was created
if [[ ! "$WORK_DIR" || ! -d "$WORK_DIR" ]]; then
  echo "Could not create temp dir"
  exit 1
fi

# deletes the temp directory
function cleanup {      
  rm -rf "$WORK_DIR"
  echo "Deleted temp working directory $WORK_DIR"
}

echo "------- will put output in"
echo ${args[0]/".py"/".root"}
# register the cleanup function to be called on the EXIT signal
trap cleanup EXIT

#cd $WORK_DIR
#export SCRAM_ARCH=slc6_amd64_gcc700
#source /cvmfs/cms.cern.ch/cmsset_default.sh
#if [ -r CMSSW_7_1_30/src ] ; then 
# echo release CMSSW_7_1_30 already exists
#else
#scram p CMSSW_7_1_30
#fi
#cd CMSSW_7_1_30/src
#eval `scram runtime -sh`

cd $WORK_DIR
export SCRAM_ARCH=slc6_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_9_3_15/src ] ; then 
 echo release CMSSW_9_3_15 already exists
else
scram p CMSSW CMSSW_9_3_15
fi
cd CMSSW_9_3_15/src
eval `scram runtime -sh`


#curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SUS-RunIIFall18GS-00015 --retry 2 --create-dirs -o Configuration/GenProduction/python/SUS-RunIIFall18GS-00015-fragment.py 
#[ -s Configuration/GenProduction/python/SUS-RunIIFall18GS-00015-fragment.py ] || exit $?;

scram b
cp -r ~/Workspace ./
echo $PWD

scram b -j8
echo ls -lrth
cmsDriver.py Workspace/DegenerateStopAnalysis/python/fragments/${args[0]}    \
--python_filename Workspace/DegenerateStopAnalysis/python/cfgs/${args[0]}   \
--fileout file:/eos/user/s/sukulkar/stop_samples/${args[0]/".py"/"_2.root"} \
--step LHE,GEN --eventcontent RECOSIM  --mc \
--conditions  93X_mc2017_realistic_v3 --beamspot Realistic25ns13TeVEarly2017Collision --era Run2_2017 --geometry DB:Extended\
--nThreads 8 \
-n 200000 \
--no_exec  

cd Workspace/DegenerateStopAnalysis/python/cfgs/
cmsRun ${args[0]}
#cmsRun T2tt_displaced_200_160_20mm_with_filter_br_03_HT_filter.py
echo $PWD
