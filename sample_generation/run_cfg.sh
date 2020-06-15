#!/bin/bash    

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

# register the cleanup function to be called on the EXIT signal
#trap cleanup EXIT

cd $WORK_DIR
export SCRAM_ARCH=slc6_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh
if [ -r CMSSW_10_2_18/src ] ; then 
 echo release CMSSW_10_2_18 already exists
else
scram p CMSSW_10_2_18
fi
cd CMSSW_10_2_18/src
eval `scram runtime -sh`

#curl -s --insecure https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/SUS-RunIIFall18GS-00015 --retry 2 --create-dirs -o Configuration/GenProduction/python/SUS-RunIIFall18GS-00015-fragment.py 
#[ -s Configuration/GenProduction/python/SUS-RunIIFall18GS-00015-fragment.py ] || exit $?;

scram b
cp -r ~/Workspace ./
cd Workspace/DegenerateStopAnalysis/python/cfgs/
args=("$@")
cmsRun ${args[0]}
echo $PWD
