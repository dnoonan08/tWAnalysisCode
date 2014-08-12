#!/bin/bash
 export SCRAM_ARCH=slc5_amd64_gcc462
 source /opt/osg/app/cmssoft/cms/cmsset_default.sh
 /bin/hostname
 /bin/date
 /bin/pwd
 /bin/df
 /bin/ls
 /bin/ls -l /home
 /bin/ls -l /home/t3-ku
 /bin/sleep 5
 cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/
 /bin/sleep 5
 eval $(scram runtime -sh)
 /bin/sleep 5
 cd /home/t3-ku/dnoonan/TMVA-v4.1.2/test/
 /bin/sleep 5

BDTversion="AdaBoostDefault_NewTests"

TMVAdirectory="ManyRegions_v4"

#Set 0 is all, 1 is no MET, 2 is no Met, jetPT, looseJetPt, NlooseCentralJets variables
 variableSet=0

 case "$1" in
     0) root -b -q -x doSamples_v4.C\(\"TWChannel\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     1) root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     2) root -b -q -x doSamples_v4.C\(\"ZJets\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     3) root -b -q -x doSamples_v4.C\(\"WJets\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     4) root -b -q -x doSamples_v4.C\(\"TChannel\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     5) root -b -q -x doSamples_v4.C\(\"SChannel\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     6) root -b -q -x doSamples_v4.C\(\"WW\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     7) root -b -q -x doSamples_v4.C\(\"WZ\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     8) root -b -q -x doSamples_v4.C\(\"ZZ\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

     9) root -b -q -x doSamples_v4.C\(\"Data_DoubleElectron_Run2012A\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     10) root -b -q -x doSamples_v4.C\(\"Data_DoubleElectron_Run2012B\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     11) root -b -q -x doSamples_v4.C\(\"Data_DoubleElectron_Run2012C\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     12) root -b -q -x doSamples_v4.C\(\"Data_DoubleElectron_Run2012D\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

     13) root -b -q -x doSamples_v4.C\(\"Data_DoubleMu_Run2012A\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     14) root -b -q -x doSamples_v4.C\(\"Data_DoubleMu_Run2012B\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     15) root -b -q -x doSamples_v4.C\(\"Data_DoubleMu_Run2012C\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     16) root -b -q -x doSamples_v4.C\(\"Data_DoubleMu_Run2012D\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

     17) root -b -q -x doSamples_v4.C\(\"Data_MuEG_Run2012A\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     18) root -b -q -x doSamples_v4.C\(\"Data_MuEG_Run2012B\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     19) root -b -q -x doSamples_v4.C\(\"Data_MuEG_Run2012C\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     20) root -b -q -x doSamples_v4.C\(\"Data_MuEG_Run2012D\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

#      21) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      22) root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

 esac