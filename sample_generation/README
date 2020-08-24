To submit generation of a specific sample, you should do the following: 

0) It is assumed that the repository is cloned in your home directory. The run scripts including run_cfg_with_arg_cmssw_9.sh exe_cfg.sh and the submitCondor.py reside in your CMSSW_version/src/make_samples directory

1) create the correct hadronizer by injecting the stop mass, LSP mass, stop four body and two body branching ratio and the stop lifetime in Workspace/DegenerateStopAnalysis/python/fragements

2) Adjust your output filepath and filename via settings in the file run_cfg_with_arg_cmssw_9.sh

3) inject the name of the file you created in step n in exe_cfg.sh, no filepath is needed. 

4) Run the setup using the following command 
./submitCondor.py --slc6 --queue workday --execFile ~/CMSSW_10_2_18/src/Analysis/Tools/scripts/condor.sh exe_cfg.sh
