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
     0) ./mergeAndRun.py tW_DR_v7         TWChannel 1 1;;
     1) ./mergeAndRun.py tbarW_DR_v7      TbarWChannel 1 1;;
     2) ./mergeAndRun.py TTbar_v7         TTBar 1 5;;
     3) ./mergeAndRun.py TTbar_v7         TTBar 2 5;;
     4) ./mergeAndRun.py TTbar_v7         TTBar 3 5;;
     5) ./mergeAndRun.py TTbar_v7         TTBar 4 5;;
     6) ./mergeAndRun.py TTbar_v7         TTBar 5 5;;

     7) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 1 5;;
     8) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 2 5;;
     9) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 3 5;;
     10) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 4 5;;
     11) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 5 5;;

     12) ./mergeAndRun.py DYJets_M50_v7    ZJets 1 20;;
     13) ./mergeAndRun.py DYJets_M50_v7    ZJets 2 20;;
     14) ./mergeAndRun.py DYJets_M50_v7    ZJets 3 20;;
     15) ./mergeAndRun.py DYJets_M50_v7    ZJets 4 20;;
     16) ./mergeAndRun.py DYJets_M50_v7    ZJets 5 20;;
     17) ./mergeAndRun.py DYJets_M50_v7    ZJets 6 20;;
     18) ./mergeAndRun.py DYJets_M50_v7    ZJets 7 20;;
     19) ./mergeAndRun.py DYJets_M50_v7    ZJets 8 20;;
     20) ./mergeAndRun.py DYJets_M50_v7    ZJets 9 20;;
     21) ./mergeAndRun.py DYJets_M50_v7    ZJets 10 20;;
     22) ./mergeAndRun.py DYJets_M50_v7    ZJets 11 20;;
     23) ./mergeAndRun.py DYJets_M50_v7    ZJets 12 20;;
     24) ./mergeAndRun.py DYJets_M50_v7    ZJets 13 20;;
     25) ./mergeAndRun.py DYJets_M50_v7    ZJets 14 20;;
     26) ./mergeAndRun.py DYJets_M50_v7    ZJets 15 20;;
     27) ./mergeAndRun.py DYJets_M50_v7    ZJets 16 20;;
     28) ./mergeAndRun.py DYJets_M50_v7    ZJets 17 20;;
     29) ./mergeAndRun.py DYJets_M50_v7    ZJets 18 20;;
     30) ./mergeAndRun.py DYJets_M50_v7    ZJets 19 20;;
     31) ./mergeAndRun.py DYJets_M50_v7    ZJets 20 20;;

     32) ./mergeAndRun.py WJets_v7         WJets 1 2;;
     33) ./mergeAndRun.py WJets_v7         WJets 2 2;;
     34) ./mergeAndRun.py WW_v7           WW 1 3;;
     35) ./mergeAndRun.py WZ_v7           WZ 1 3;;
     36) ./mergeAndRun.py ZZ_v7           ZZ 1 3;;
     37) ./mergeAndRun.py T_tChannel_v7    TChannel 1 1;;
     38) ./mergeAndRun.py Tbar_tChannel_v7 TbarChannel 1 1;;
     39) ./mergeAndRun.py T_sChannel_v7    SChannel 1 1;;
     40) ./mergeAndRun.py Tbar_sChannel_v7 SbarChannel 1 1;;

     41) ./mergeAndRun.py WW_v7           WW 2 3;;
     42) ./mergeAndRun.py WZ_v7           WZ 2 3;;
     43) ./mergeAndRun.py ZZ_v7           ZZ 2 3;;

     44) ./mergeAndRun.py WW_v7           WW 3 3;;
     45) ./mergeAndRun.py WZ_v7           WZ 3 3;;
     46) ./mergeAndRun.py ZZ_v7           ZZ 3 3;;


 esac