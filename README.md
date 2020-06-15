# cms_stop_grid
Setup for creating degenerate stop samples with cmssw
This repository contains the pythia fragments and the associated setup to create generator level samples with cmssw. 
The pythia fragments are set in directory
sample_generation/Workspace/DegenerateStopAnalysis/python/fragments

The fragment contains "on-shell" W in the stop decays, with a 100% branching ratio. A pythia filter is setup to filter out muons out of the W decays. This needs to be verified. No two body deacys are at the moment introduced but this is easy. 

For every fragment, the stop - LSP mass and LSP lifetime needs to be adjusted. If needed two body decay modes should be added. 

To create the cfg out of the fragments, please run create_one_cfg.py script after adjusting the name of the fragment file. Please also adjust the path to output root file. Keep the number of events to 50k to be consistent with the wgt setup in the fragment, defined as wgt = 50/matching efficiency. 50 == number of events in thousands. 

To run the cfg use the run_cfg.sh script. The script takes the cfg name as an input. It sets up a temperory cmssw directory and removes it after the run.
