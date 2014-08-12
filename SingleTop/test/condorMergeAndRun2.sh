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
     0)  ./mergeAndRun.py tW_DR_v7         TWChannel 1 1;;
     1)  ./mergeAndRun.py tbarW_DR_v7      TbarWChannel 1 1;;
     2)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 1 10;;
     3)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 2 10;;
     4)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 3 10;;
     5)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 4 10;;
     6)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 5 10;;
     7)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 6 10;;
     8)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 7 10;;
     9)  ./mergeAndRun.py TTbar_v7newSpin TTBarNew 8 10;;
     10) ./mergeAndRun.py TTbar_v7newSpin TTBarNew 9 10;;
     11) ./mergeAndRun.py TTbar_v7newSpin TTBarNew 10 10;;

     12) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 1 5;;
     13) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 2 5;;
     14) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 3 5;;
     15) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 4 5;;
     16) ./mergeAndRun.py DYJets_M10-50_v7 ZJetsLowMass 5 5;;

     17) ./mergeAndRun.py DYJets_M50_v7    ZJets 1 20;;
     18) ./mergeAndRun.py DYJets_M50_v7    ZJets 2 20;;
     19) ./mergeAndRun.py DYJets_M50_v7    ZJets 3 20;;
     20) ./mergeAndRun.py DYJets_M50_v7    ZJets 4 20;;
     21) ./mergeAndRun.py DYJets_M50_v7    ZJets 5 20;;
     22) ./mergeAndRun.py DYJets_M50_v7    ZJets 6 20;;
     23) ./mergeAndRun.py DYJets_M50_v7    ZJets 7 20;;
     24) ./mergeAndRun.py DYJets_M50_v7    ZJets 8 20;;
     25) ./mergeAndRun.py DYJets_M50_v7    ZJets 9 20;;
     26) ./mergeAndRun.py DYJets_M50_v7    ZJets 10 20;;
     27) ./mergeAndRun.py DYJets_M50_v7    ZJets 11 20;;
     28) ./mergeAndRun.py DYJets_M50_v7    ZJets 12 20;;
     29) ./mergeAndRun.py DYJets_M50_v7    ZJets 13 20;;
     30) ./mergeAndRun.py DYJets_M50_v7    ZJets 14 20;;
     31) ./mergeAndRun.py DYJets_M50_v7    ZJets 15 20;;
     32) ./mergeAndRun.py DYJets_M50_v7    ZJets 16 20;;
     33) ./mergeAndRun.py DYJets_M50_v7    ZJets 17 20;;
     34) ./mergeAndRun.py DYJets_M50_v7    ZJets 18 20;;
     35) ./mergeAndRun.py DYJets_M50_v7    ZJets 19 20;;
     36) ./mergeAndRun.py DYJets_M50_v7    ZJets 20 20;;

     37) ./mergeAndRun.py WJets_v7         WJets 1 2;;
     38) ./mergeAndRun.py WJets_v7         WJets 2 2;;
     39) ./mergeAndRun.py WW_v7           WW 1 3;;
     40) ./mergeAndRun.py WZ_v7           WZ 1 3;;
     41) ./mergeAndRun.py ZZ_v7           ZZ 1 3;;
     42) ./mergeAndRun.py T_tChannel_v7    TChannel 1 1;;
     43) ./mergeAndRun.py Tbar_tChannel_v7 TbarChannel 1 1;;
     44) ./mergeAndRun.py T_sChannel_v7    SChannel 1 1;;
     45) ./mergeAndRun.py Tbar_sChannel_v7 SbarChannel 1 1;;

     46) ./mergeAndRun.py WW_v7           WW 2 3;;
     47) ./mergeAndRun.py WZ_v7           WZ 2 3;;
     48) ./mergeAndRun.py ZZ_v7           ZZ 2 3;;

     49) ./mergeAndRun.py WW_v7           WW 3 3;;
     50) ./mergeAndRun.py WZ_v7           WZ 3 3;;
     51) ./mergeAndRun.py ZZ_v7           ZZ 3 3;;


 esac