#!/bin/bash
 source /opt/osg/app/cmssoft/cms/cmsset_default.sh
 export SCRAM_ARCH=slc5_amd64_gcc462
 /bin/hostname
 /bin/date
 /bin/pwd
 /bin/df
 /bin/ls
 /bin/ls -l /home
 /bin/ls -l /home/t3-ku
 /bin/sleep 30
 cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/TopQuarkAnalysis/SingleTop/test/
 /bin/sleep 2
 eval $(scram runtime -sh)
 /bin/sleep 2


 case "$1" in
     0)  ./mergeAndRun.py tW_SemiLep1_v7 TWChannelSemilepton1 1 1 ;;
     1)  ./mergeAndRun.py tW_SemiLep2_v7 TWChannelSemilepton2 1 1 ;;
     2)  ./mergeAndRun.py tbarW_SemiLep1_v7 TbarWChannelSemilepton1 1 1 ;;
     3)  ./mergeAndRun.py tbarW_SemiLep2_v7 TbarWChannelSemilepton2 1 1 ;;
        
     4)  ./mergeAndRun.py Syst tW_Q2_Up_SemiLep1_v7 TWChannel_Q2UpSemiLep1 1 1 ;;
     5)  ./mergeAndRun.py Syst tW_Q2_Up_SemiLep2_v7 TWChannel_Q2UpSemiLep2 1 1 ;;
     6)  ./mergeAndRun.py Syst tW_Q2_Down_SemiLep1_v7 TWChannel_Q2DownSemiLep1 1 1 ;;
     7)  ./mergeAndRun.py Syst tW_Q2_Down_SemiLep2_v7 TWChannel_Q2DownSemiLep2 1 1 ;;
     8)  ./mergeAndRun.py Syst tbarW_Q2_Up_SemiLep1_v7 TbarWChannel_Q2UpSemiLep1 1 1 ;;
     9)  ./mergeAndRun.py Syst tbarW_Q2_Up_SemiLep2_v7 TbarWChannel_Q2UpSemiLep2 1 1 ;;
     10) ./mergeAndRun.py Syst tbarW_Q2_Down_SemiLep1_v7 TbarWChannel_Q2DownSemiLep1 1 1 ;;
     11) ./mergeAndRun.py Syst tbarW_Q2_Down_SemiLep2_v7 TbarWChannel_Q2DownSemiLep2 1 1 ;;

 esac