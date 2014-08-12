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
/bin/sleep 30
cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/TopQuarkAnalysis/SingleTop/test/
/bin/sleep 3
eval $(scram runtime -sh)
/bin/sleep 3
cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/TopQuarkAnalysis/SingleTop/test/macros
/bin/sleep 3

case "$1" in
    0) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py TWChannel;;
    1) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py TTbarNew ;;
    2) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py TChannel ;;
    3) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py SChannel ;;
    4) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py WJets    ;;
    5) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py WW       ;;
    6) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py WZ       ;;
    7) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py ZZ       ;;
    
    8) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_MuEG_Run2012A ;;
    9) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_MuEG_Run2012B;;
    10) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_MuEG_Run2012C;;
    11) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_MuEG_Run2012D;;
    
    12) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleMu_Run2012A;;
    13) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleMu_Run2012B;;
    14) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleMu_Run2012C;;
    15) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleMu_Run2012D;;
    
    16) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleElectron_Run2012A;;
    17) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleElectron_Run2012B;;
    18) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleElectron_Run2012C;;
    19) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py Data_DoubleElectron_Run2012D;;

    20) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py ZJets1    ;;
    21) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py ZJets2    ;;
    22) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py ZJets3    ;;
    23) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py ZJets4    ;;
    24) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py ZJets5    ;;

    25) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py TWChannel_T;;
    26) ./TMVATupleCreator_v5_RmeasurementMoreRegions.py TWChannel_Tbar;;
    
esac