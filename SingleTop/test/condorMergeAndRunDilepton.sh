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
     0) ./mergeAndRun.py tW_Dilepton_v7            TWChannelDilepton 1 5;;
     1) ./mergeAndRun.py tW_Dilepton_v7            TWChannelDilepton 2 5;;
     2) ./mergeAndRun.py tW_Dilepton_v7            TWChannelDilepton 3 5;;
     3) ./mergeAndRun.py tW_Dilepton_v7            TWChannelDilepton 4 5;;
     4) ./mergeAndRun.py tW_Dilepton_v7            TWChannelDilepton 5 5;;
     5) ./mergeAndRun.py tbarW_Dilepton_v7         TbarWChannelDilepton 1 5;;
     6) ./mergeAndRun.py tbarW_Dilepton_v7         TbarWChannelDilepton 2 5;;
     7) ./mergeAndRun.py tbarW_Dilepton_v7         TbarWChannelDilepton 3 5;;
     8) ./mergeAndRun.py tbarW_Dilepton_v7         TbarWChannelDilepton 4 5;;
     9) ./mergeAndRun.py tbarW_Dilepton_v7         TbarWChannelDilepton 5 5;;
     10) ./mergeAndRun.py TTbar_Dilepton_v7         TTBarDilepton 1 5;;
     11) ./mergeAndRun.py TTbar_Dilepton_v7         TTBarDilepton 2 5;;
     12) ./mergeAndRun.py TTbar_Dilepton_v7         TTBarDilepton 3 5;;
     13) ./mergeAndRun.py TTbar_Dilepton_v7         TTBarDilepton 4 5;;
     14) ./mergeAndRun.py TTbar_Dilepton_v7         TTBarDilepton 5 5;;

 esac