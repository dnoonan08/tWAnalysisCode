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
/bin/sleep 3
cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/TopQuarkAnalysis/SingleTop/test/
/bin/sleep 3
eval $(scram runtime -sh)
/bin/sleep 3
cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/TopQuarkAnalysis/SingleTop/test/macros
/bin/sleep 3

case "$1" in

    0)  ./getCutflow_v2.py TWChannel ;;
    1)  ./getCutflow_v2.py TTbar ;;
    2)  ./getCutflow_v2.py TTbarNew ;;
    3)  ./getCutflow_v2.py TChannel ;;
    4)  ./getCutflow_v2.py SChannel ;;
    5)  ./getCutflow_v2.py ZJets1    ;;
    6)  ./getCutflow_v2.py ZJets2    ;;
    7)  ./getCutflow_v2.py ZJets3    ;;
    8)  ./getCutflow_v2.py ZJets4    ;;
    9)  ./getCutflow_v2.py ZJets5    ;;
    10) ./getCutflow_v2.py WJets    ;;
    11) ./getCutflow_v2.py WW       ;;
    12) ./getCutflow_v2.py WZ       ;;
    13) ./getCutflow_v2.py ZZ       ;;
    14) ./getCutflow_v2.py Data_MuEG_Run2012A ;;
    15) ./getCutflow_v2.py Data_MuEG_Run2012B;;
    16) ./getCutflow_v2.py Data_MuEG_Run2012C;;
    17) ./getCutflow_v2.py Data_MuEG_Run2012D;;
    18) ./getCutflow_v2.py Data_DoubleMu_Run2012A;;
    19) ./getCutflow_v2.py Data_DoubleMu_Run2012B;;
    20) ./getCutflow_v2.py Data_DoubleMu_Run2012C;;
    21) ./getCutflow_v2.py Data_DoubleMu_Run2012D;;
    22) ./getCutflow_v2.py Data_DoubleElectron_Run2012A;;
    23) ./getCutflow_v2.py Data_DoubleElectron_Run2012B;;
    24) ./getCutflow_v2.py Data_DoubleElectron_Run2012C;;
    25) ./getCutflow_v2.py Data_DoubleElectron_Run2012D;;
    26) ./getCutflow_v2.py TWChannel_Q2Up ;;
    27) ./getCutflow_v2.py TWChannel_Q2Down ;;
    28) ./getCutflow_v2.py TTBarNew_Q2Up ;;
    29) ./getCutflow_v2.py TTBarNew_Q2Down ;;
    30) ./getCutflow_v2.py TTBarNew_MatchingUp ;;
    31) ./getCutflow_v2.py TTBarNew_MatchingDown1 ;;
    32) ./getCutflow_v2.py TTBarNew_MatchingDown2 ;;
    33) ./getCutflow_v2.py TTBarNew_MatchingDown ;;
    34) ./getCutflow_v2.py TWChannel_TopMassUp ;;
    35) ./getCutflow_v2.py TWChannel_TopMassDown ;;
    36) ./getCutflow_v2.py TTBarNew_TopMassUp ;;
    37) ./getCutflow_v2.py TTBarNew_TopMassDown ;;
    38) ./getCutflow_v2.py TWChannel_DS ;;
    39) ./getCutflow_v2.py TWChannel_Q2UpFull ;;
    40) ./getCutflow_v2.py TWChannel_Q2DownFull ;;
    41) ./getCutflow_v2.py TWDilepton ;;
    42) ./getCutflow_v2.py TWDilepton_New ;;

    
esac
