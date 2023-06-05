#!/bin/bash

cd /afs/cern.ch/user/a/almuhamm/private/CMSSW_12_4_8/src/
cmsenv 
cd /afs/cern.ch/user/a/almuhamm/private/CMSSW_12_4_8/src/L1NanoAOD/l1macros/

#python3 performances_nano.py -i /eos/cms/store/data/Run2023B/Muon0/NANOAOD/PromptNanoAODv11p9_v1-v2/2810000/06a66d98-1c17-4e11-88f5-86fe954c911b.root -o histos.root -c ZToMuMu --max_events -1 --config /afs/cern.ch/user/a/almuhamm/private/CMSSW_12_4_8/src/L1NanoAOD/config_cards/full_ZToMuMu.yaml

python3 performances_nano.py  -i $1 -o $2 -c $3 --max_events -1 --config /afs/cern.ch/user/a/almuhamm/private/CMSSW_12_4_8/src/L1NanoAOD/config_cards/full_ZToMuMu.yaml
