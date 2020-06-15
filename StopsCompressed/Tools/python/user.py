import os

if os.environ['USER'] in ['phussain']:
    cache_directory                     = "/afs/hephy.at/data/cms10/StopsCompressed/"
    analysis_results                    = "/afs/hephy.at/data/cms10/StopsCompressed/"
    postProcessing_output_directory     = "/afs/hephy.at/data/cms10/StopsCompressed/nanoTuples/"
    plot_directory                      = "/afs/hephy.at/user/p/phussain/www/stopsCompressed/"
    private_results_directory           = "/afs/hephy.at/data/cms02/"
    
if os.environ['USER'] in ['priya.hussain']:
    results_directory                   = "/mnt/hephy/cms/priya.hussain/StopsCompressed/"
    cache_directory                     = "/mnt/hephy/cms/priya.hussain/StopsCompressed/"
    postProcessing_output_directory     = "/mnt/hephy/cms/priya.hussain/StopsCompressed/nanoTuples/"
    plot_directory                      = "/mnt/hephy/cms/priya.hussain/www/StopsCompressed/"
    private_results_directory           = "/mnt/hephy/cms/priya.hussain/"
if os.environ['USER'] in ['prhussai']:
    results_directory                   = "/afs/cern.ch/work/p/prhussai/private/StopsCompressed"
    postProcessing_output_directory     = "/afs/cern.ch/work/p/prhussai/private/StopsCompressed/nanoTuples/"
    plot_directory                      = "/eos/user/p/prhussai/www/"
    private_results_directory           = "/afs/cern.ch/work/p/prhussai/private/StopsCompressed/results"

if os.environ['USER'] in ['rschoefbeck']:
    results_directory                   = "/afs/hephy.at/data/cms02/StopsCompressed/"
    postProcessing_output_directory     = "/afs/hephy.at/data/cms02/StopsCompressed/nanoTuples/"
    plot_directory                      = "/afs/hephy.at/user/r/rschoefbeck/www/StopsCompressed/"
    private_results_directory           = "/afs/hephy.at/data/cms02/"
