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
     0) ./mergeAndRun.py v2/MuEG_Run2012A-22Jan2013-v1_v3 Data  MuEG Run2012A-22Jan2013  1 1;;
     1) ./mergeAndRun.py v2/MuEG_Run2012B-22Jan2013-v1_v3 Data  MuEG Run2012B-22Jan2013  1 5;;
     2) ./mergeAndRun.py v2/MuEG_Run2012B-22Jan2013-v1_v3 Data  MuEG Run2012B-22Jan2013  2 5;;
     3) ./mergeAndRun.py v2/MuEG_Run2012B-22Jan2013-v1_v3 Data  MuEG Run2012B-22Jan2013  3 5;;
     4) ./mergeAndRun.py v2/MuEG_Run2012B-22Jan2013-v1_v3 Data  MuEG Run2012B-22Jan2013  4 5;;
     5) ./mergeAndRun.py v2/MuEG_Run2012B-22Jan2013-v1_v3 Data  MuEG Run2012B-22Jan2013  5 5;;
     6) ./mergeAndRun.py v2/MuEG_Run2012C-22Jan2013-v1_v3 Data  MuEG Run2012C-22Jan2013  1 5;;
     7) ./mergeAndRun.py v2/MuEG_Run2012C-22Jan2013-v1_v3 Data  MuEG Run2012C-22Jan2013  2 5;;
     8) ./mergeAndRun.py v2/MuEG_Run2012C-22Jan2013-v1_v3 Data  MuEG Run2012C-22Jan2013  3 5;;
     9) ./mergeAndRun.py v2/MuEG_Run2012C-22Jan2013-v1_v3 Data  MuEG Run2012C-22Jan2013  4 5;;
     10) ./mergeAndRun.py v2/MuEG_Run2012C-22Jan2013-v1_v3 Data  MuEG Run2012C-22Jan2013  5 5;;
     11) ./mergeAndRun.py v2/MuEG_Run2012D-22Jan2013-v1_v3 Data  MuEG Run2012D-22Jan2013  1 5;;
     12) ./mergeAndRun.py v2/MuEG_Run2012D-22Jan2013-v1_v3 Data  MuEG Run2012D-22Jan2013  2 5;;
     13) ./mergeAndRun.py v2/MuEG_Run2012D-22Jan2013-v1_v3 Data  MuEG Run2012D-22Jan2013  3 5;;
     14) ./mergeAndRun.py v2/MuEG_Run2012D-22Jan2013-v1_v3 Data  MuEG Run2012D-22Jan2013  4 5;;
     15) ./mergeAndRun.py v2/MuEG_Run2012D-22Jan2013-v1_v3 Data  MuEG Run2012D-22Jan2013  5 5;;

     16) ./mergeAndRun.py v2/DoubleMu_Run2012A-22Jan2013-v1_v3 Data  DoubleMu Run2012A-22Jan2013  1 1;;
     17) ./mergeAndRun.py v2/DoubleMu_Run2012B-22Jan2013-v1_v3 Data  DoubleMu Run2012B-22Jan2013  1 5;;
     18) ./mergeAndRun.py v2/DoubleMu_Run2012B-22Jan2013-v1_v3 Data  DoubleMu Run2012B-22Jan2013  2 5;;
     19) ./mergeAndRun.py v2/DoubleMu_Run2012B-22Jan2013-v1_v3 Data  DoubleMu Run2012B-22Jan2013  3 5;;
     20) ./mergeAndRun.py v2/DoubleMu_Run2012B-22Jan2013-v1_v3 Data  DoubleMu Run2012B-22Jan2013  4 5;;
     21) ./mergeAndRun.py v2/DoubleMu_Run2012B-22Jan2013-v1_v3 Data  DoubleMu Run2012B-22Jan2013  5 5;;
     22) ./mergeAndRun.py v2/DoubleMu_Run2012C-22Jan2013-v1_v3 Data  DoubleMu Run2012C-22Jan2013  1 5;;
     23) ./mergeAndRun.py v2/DoubleMu_Run2012C-22Jan2013-v1_v3 Data  DoubleMu Run2012C-22Jan2013  2 5;;
     24) ./mergeAndRun.py v2/DoubleMu_Run2012C-22Jan2013-v1_v3 Data  DoubleMu Run2012C-22Jan2013  3 5;;
     25) ./mergeAndRun.py v2/DoubleMu_Run2012C-22Jan2013-v1_v3 Data  DoubleMu Run2012C-22Jan2013  4 5;;
     26) ./mergeAndRun.py v2/DoubleMu_Run2012C-22Jan2013-v1_v3 Data  DoubleMu Run2012C-22Jan2013  5 5;;
     27) ./mergeAndRun.py v2/DoubleMu_Run2012D-22Jan2013-v1_v3 Data  DoubleMu Run2012D-22Jan2013  1 5;;
     28) ./mergeAndRun.py v2/DoubleMu_Run2012D-22Jan2013-v1_v3 Data  DoubleMu Run2012D-22Jan2013  2 5;;
     29) ./mergeAndRun.py v2/DoubleMu_Run2012D-22Jan2013-v1_v3 Data  DoubleMu Run2012D-22Jan2013  3 5;;
     30) ./mergeAndRun.py v2/DoubleMu_Run2012D-22Jan2013-v1_v3 Data  DoubleMu Run2012D-22Jan2013  4 5;;
     31) ./mergeAndRun.py v2/DoubleMu_Run2012D-22Jan2013-v1_v3 Data  DoubleMu Run2012D-22Jan2013  5 5;;

     32) ./mergeAndRun.py v2/DoubleElectron_Run2012A-22Jan2013-v1_v3 Data  DoubleElectron Run2012A-22Jan2013  1 1;;
     33) ./mergeAndRun.py v2/DoubleElectron_Run2012B-22Jan2013-v1_v3 Data  DoubleElectron Run2012B-22Jan2013  1 5;;
     34) ./mergeAndRun.py v2/DoubleElectron_Run2012B-22Jan2013-v1_v3 Data  DoubleElectron Run2012B-22Jan2013  2 5;;
     35) ./mergeAndRun.py v2/DoubleElectron_Run2012B-22Jan2013-v1_v3 Data  DoubleElectron Run2012B-22Jan2013  3 5;;
     36) ./mergeAndRun.py v2/DoubleElectron_Run2012B-22Jan2013-v1_v3 Data  DoubleElectron Run2012B-22Jan2013  4 5;;
     37) ./mergeAndRun.py v2/DoubleElectron_Run2012B-22Jan2013-v1_v3 Data  DoubleElectron Run2012B-22Jan2013  5 5;;
     38) ./mergeAndRun.py v2/DoubleElectron_Run2012C-22Jan2013-v1_v3 Data  DoubleElectron Run2012C-22Jan2013  1 5;;
     39) ./mergeAndRun.py v2/DoubleElectron_Run2012C-22Jan2013-v1_v3 Data  DoubleElectron Run2012C-22Jan2013  2 5;;
     40) ./mergeAndRun.py v2/DoubleElectron_Run2012C-22Jan2013-v1_v3 Data  DoubleElectron Run2012C-22Jan2013  3 5;;
     41) ./mergeAndRun.py v2/DoubleElectron_Run2012C-22Jan2013-v1_v3 Data  DoubleElectron Run2012C-22Jan2013  4 5;;
     42) ./mergeAndRun.py v2/DoubleElectron_Run2012C-22Jan2013-v1_v3 Data  DoubleElectron Run2012C-22Jan2013  5 5;;
     43) ./mergeAndRun.py v2/DoubleElectron_Run2012D-22Jan2013-v1_v3 Data  DoubleElectron Run2012D-22Jan2013  1 5;;
     44) ./mergeAndRun.py v2/DoubleElectron_Run2012D-22Jan2013-v1_v3 Data  DoubleElectron Run2012D-22Jan2013  2 5;;
     45) ./mergeAndRun.py v2/DoubleElectron_Run2012D-22Jan2013-v1_v3 Data  DoubleElectron Run2012D-22Jan2013  3 5;;
     46) ./mergeAndRun.py v2/DoubleElectron_Run2012D-22Jan2013-v1_v3 Data  DoubleElectron Run2012D-22Jan2013  4 5;;
     47) ./mergeAndRun.py v2/DoubleElectron_Run2012D-22Jan2013-v1_v3 Data  DoubleElectron Run2012D-22Jan2013  5 5;;

 esac