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
 /bin/sleep 5
 cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/TopQuarkAnalysis/SingleTop/test/
 /bin/sleep 2
 eval $(scram runtime -sh)
 /bin/sleep 2


 case "$1" in
     0) ./mergeAndRun.py Syst tW_DS_v7 TWChannel_DS 1 6;;
     1) ./mergeAndRun.py Syst tW_DS_v7 TWChannel_DS 2 6;;
     2) ./mergeAndRun.py Syst tW_DS_v7 TWChannel_DS 3 6;;
     3) ./mergeAndRun.py Syst tW_DS_v7 TWChannel_DS 4 6;;
     4) ./mergeAndRun.py Syst tW_DS_v7 TWChannel_DS 5 6;;
     5) ./mergeAndRun.py Syst tW_DS_v7 TWChannel_DS 6 6;;

     6) ./mergeAndRun.py Syst tbarW_DS_v7 TbarWChannel_DS 1 6;;
     7) ./mergeAndRun.py Syst tbarW_DS_v7 TbarWChannel_DS 2 6;;
     8) ./mergeAndRun.py Syst tbarW_DS_v7 TbarWChannel_DS 3 6;;
     9) ./mergeAndRun.py Syst tbarW_DS_v7 TbarWChannel_DS 4 6;;
     10) ./mergeAndRun.py Syst tbarW_DS_v7 TbarWChannel_DS 5 6;;
     11) ./mergeAndRun.py Syst tbarW_DS_v7 TbarWChannel_DS 6 6;;

     12) ./mergeAndRun.py Syst tW_Q2_Up_v7 TWChannel_Q2Up 1 3;;
     13) ./mergeAndRun.py Syst tW_Q2_Up_v7 TWChannel_Q2Up 2 3;;
     14) ./mergeAndRun.py Syst tW_Q2_Up_v7 TWChannel_Q2Up 3 3;;
     15) ./mergeAndRun.py Syst tW_Q2_Down_v7 TWChannel_Q2Down 1 3;;
     16) ./mergeAndRun.py Syst tW_Q2_Down_v7 TWChannel_Q2Down 2 3;;
     17) ./mergeAndRun.py Syst tW_Q2_Down_v7 TWChannel_Q2Down 3 3;;

     18) ./mergeAndRun.py Syst tbarW_Q2_Up_v7 TbarWChannel_Q2Up 1 3;;
     19) ./mergeAndRun.py Syst tbarW_Q2_Up_v7 TbarWChannel_Q2Up 2 3;;
     20) ./mergeAndRun.py Syst tbarW_Q2_Up_v7 TbarWChannel_Q2Up 3 3;;
     21) ./mergeAndRun.py Syst tbarW_Q2_Down_v7 TbarWChannel_Q2Down 1 3;;
     22) ./mergeAndRun.py Syst tbarW_Q2_Down_v7 TbarWChannel_Q2Down 2 3;;
     23) ./mergeAndRun.py Syst tbarW_Q2_Down_v7 TbarWChannel_Q2Down 3 3;;

     24) ./mergeAndRun.py Syst tW_TopMass_Up_v7 TWChannel_TopMassUp 1 3;;
     25) ./mergeAndRun.py Syst tW_TopMass_Up_v7 TWChannel_TopMassUp 2 3;;
     26) ./mergeAndRun.py Syst tW_TopMass_Up_v7 TWChannel_TopMassUp 3 3;;
     27) ./mergeAndRun.py Syst tW_TopMass_Down_v7 TWChannel_TopMassDown 1 3;;
     28) ./mergeAndRun.py Syst tW_TopMass_Down_v7 TWChannel_TopMassDown 2 3;;
     29) ./mergeAndRun.py Syst tW_TopMass_Down_v7 TWChannel_TopMassDown 3 3;;

     30) ./mergeAndRun.py Syst tbarW_TopMass_Up_v7 TbarWChannel_TopMassUp 1 3;;
     31) ./mergeAndRun.py Syst tbarW_TopMass_Up_v7 TbarWChannel_TopMassUp 2 3;;
     32) ./mergeAndRun.py Syst tbarW_TopMass_Up_v7 TbarWChannel_TopMassUp 3 3;;
     33) ./mergeAndRun.py Syst tbarW_TopMass_Down_v7 TbarWChannel_TopMassDown 1 3;;
     34) ./mergeAndRun.py Syst tbarW_TopMass_Down_v7 TbarWChannel_TopMassDown 2 3;;
     35) ./mergeAndRun.py Syst tbarW_TopMass_Down_v7 TbarWChannel_TopMassDown 3 3;;


     40) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 1 10;;
     41) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 2 10;;
     42) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 3 10;;
     43) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 4 10;;
     44) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 5 10;;
     45) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 6 10;;
     46) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 7 10;;
     47) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 8 10;;
     48) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 9 10;;
     49) ./mergeAndRun.py Syst TTbar_Matching_Up_v7_New TTBar_MatchingUp_New 10 10;;

     50) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 1 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     51) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 2 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     52) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 3 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     53) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 4 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     54) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 5 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     55) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 6 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     56) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 7 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     57) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 8 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     58) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 9 10  Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;
     59) ./mergeAndRunMultipleSets.py Syst TTBar_MatchingDown_New 10 10 Multi TTbar_Matching_Down_v7_New1 TTbar_Matching_Down_v7_New2 ;;

     60) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 1 10;;
     61) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 2 10;;
     62) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 3 10;;
     63) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 4 10;;
     64) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 5 10;;
     65) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 6 10;;
     66) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 7 10;;
     67) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 8 10;;
     68) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 9 10;;
     69) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New1 TTBar_MatchingDown_New1 10 10;;

     70) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 1 10;;
     71) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 2 10;;
     72) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 3 10;;
     73) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 4 10;;
     74) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 5 10;;
     75) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 6 10;;
     76) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 7 10;;
     77) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 8 10;;
     78) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 9 10;;
     79) ./mergeAndRun.py Syst TTbar_Matching_Down_v7_New2 TTBar_MatchingDown_New2 10 10;;

     80) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 1 10;;
     81) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 2 10;;
     82) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 3 10;;
     83) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 4 10;;
     84) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 5 10;;
     85) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 6 10;;
     86) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 7 10;;
     87) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 8 10;;
     88) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 9 10;;
     89) ./mergeAndRun.py Syst TTbar_Q2_Up_v7_New TTBar_Q2Up_New 10 10;;

     90) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 1 10;;
     91) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 2 10;;
     92) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 3 10;;
     93) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 4 10;;
     94) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 5 10;;
     95) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 6 10;;
     96) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 7 10;;
     97) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 8 10;;
     98) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 9 10;;
     99) ./mergeAndRun.py Syst TTbar_Q2_Down_v7_New TTBar_Q2Down_New 10 10;;


 esac