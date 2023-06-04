#!/bin/bash

cd /afs/cern.ch/user/a/almuhamm/private/CMSSW_12_4_8/src/
cmsenv 
cd /afs/cern.ch/user/a/almuhamm/private/CMSSW_12_4_8/src/MacrosNtuples/l1macros/

python3 performances_nano.py --max_events -1 -i $1 -o $2 -c $3
