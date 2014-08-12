#!/bin/bash
 export SCRAM_ARCH=slc5_amd64_gcc434
#  export SCRAM_ARCH=slc5_amd64_gcc462
 source /opt/osg/app/cmssoft/cms/cmsset_default.sh
 /bin/hostname
 /bin/date
 /bin/pwd
 /bin/df
 /bin/ls
 /bin/sleep 30
 cd /home/t3-ku/dnoonan/CMSSW_4_2_8_patch7/src
#  cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_5/src/
 eval $(scram runtime -sh)
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/boost/boost_1_49_0/
 cd CURRENTDIR
 #The $1 is the theta python configuration file (handled by the .condor configuration)

 case "$1" in
     0) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVRunTheta.py ;;
     1) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVRunTheta_emu.py ;;
     2) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVRunTheta_mumu.py ;;
     3) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVRunTheta_ee.py ;;
     4) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVRunTheta_emu_ee.py ;;
     5) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVRunTheta_emu_mumu.py ;;
     6) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVRunTheta_ee_mumu.py ;;

 esac