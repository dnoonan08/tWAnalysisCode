#!/bin/bash
 export SCRAM_ARCH=slc5_amd64_gcc434
# export SCRAM_ARCH=slc5_amd64_gcc462
 source /opt/osg/app/cmssoft/cms/cmsset_default.sh
 /bin/hostname
 /bin/date
 /bin/pwd
 /bin/df
 /bin/ls
 /bin/sleep 30
 cd /home/t3-ku/dnoonan/CMSSW_4_2_8_patch7/src
# cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_5/src/
 eval $(scram runtime -sh)
 export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:~/boost/boost_1_49_0/
 cd CURRENTDIR
 #The $1 is the theta python configuration file (handled by the .condor configuration)

 case "$1" in
     ITERATION) /home/t3-ku/dnoonan/ThetaTests/NewThetaNov2013/theta/utils2/theta-auto.py analysisJochenSyst8TeVCHANNEL_ITER-PLUS-1_MAXSUBMISSION.py ;;
#      EXTRA) /home/t3-ku/dnoonan/ThetaTests/NewThetaMarch2013_v3/theta/utils2/theta-auto.py analysisJochenSyst8TeV_SplusBCHANNEL.py ;;

 esac