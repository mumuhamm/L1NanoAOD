#!/bin/bash

cd eos/user/a/almuhamm/02.TriggerEff/CMSSW_12_4_8/src/
cmsenv 
cd eos/user/a/almuhamm/02.TriggerEff/CMSSW_12_4_8/src/MacrosNtuples/l1macros/

python3 performances.py --max_events -1 -i $1 -o $2 -c $3 
