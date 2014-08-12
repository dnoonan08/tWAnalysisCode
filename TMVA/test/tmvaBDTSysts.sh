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
     0)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     1)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     2)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     3)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     4)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     5)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     6)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     7)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     8)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     9)   root -b -q -x doSamples_v4.C\(\"TWChannel\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     10)  root -b -q -x doSamples_v4.C\(\"TWChannel\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     11)  root -b -q -x doSamples_v4.C\(\"TWChannel\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     12)  root -b -q -x doSamples_v4.C\(\"TWChannel\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     13)  root -b -q -x doSamples_v4.C\(\"TWChannel\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
	  
     14)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     15)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     16)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     17)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     18)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     19)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     20)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     21)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     22)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     23)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     24)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     25)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     26)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     27)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     28)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     29)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     30)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     31)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     32)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"MatchingUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     33)  root -b -q -x doSamples_v4.C\(\"TTbarNew\",\"MatchingDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
	  
     34)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     35)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     36)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     37)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     38)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     39)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     40)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     41)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     42)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     43)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     44)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     45)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     46)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     47)  root -b -q -x doSamples_v4.C\(\"ZJets\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
	  
     48)  root -b -q -x doSamples_v4.C\(\"WJets\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     49)  root -b -q -x doSamples_v4.C\(\"WJets\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     50)  root -b -q -x doSamples_v4.C\(\"WJets\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     51)  root -b -q -x doSamples_v4.C\(\"WJets\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     52)  root -b -q -x doSamples_v4.C\(\"WJets\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     53)  root -b -q -x doSamples_v4.C\(\"WJets\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     54)  root -b -q -x doSamples_v4.C\(\"WJets\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     55)  root -b -q -x doSamples_v4.C\(\"WJets\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     56)  root -b -q -x doSamples_v4.C\(\"WJets\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     57)  root -b -q -x doSamples_v4.C\(\"WJets\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     58)  root -b -q -x doSamples_v4.C\(\"WJets\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     59)  root -b -q -x doSamples_v4.C\(\"WJets\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     60)  root -b -q -x doSamples_v4.C\(\"WJets\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     61)  root -b -q -x doSamples_v4.C\(\"WJets\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
	  
     62)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     63)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     64)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     65)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     66)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     67)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     68)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     69)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     70)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     71)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     72)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     73)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     74)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     75)  root -b -q -x doSamples_v4.C\(\"TChannel\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
	  
     76)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     77)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     78)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     79)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     80)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     81)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     82)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     83)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     84)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     85)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     86)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     87)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     88)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     89)  root -b -q -x doSamples_v4.C\(\"SChannel\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
	  
     90)  root -b -q -x doSamples_v4.C\(\"WW\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     91)  root -b -q -x doSamples_v4.C\(\"WW\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     92)  root -b -q -x doSamples_v4.C\(\"WW\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     93)  root -b -q -x doSamples_v4.C\(\"WW\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     94)  root -b -q -x doSamples_v4.C\(\"WW\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     95)  root -b -q -x doSamples_v4.C\(\"WW\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     96)  root -b -q -x doSamples_v4.C\(\"WW\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     97)  root -b -q -x doSamples_v4.C\(\"WW\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     98)  root -b -q -x doSamples_v4.C\(\"WW\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     99)  root -b -q -x doSamples_v4.C\(\"WW\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     100) root -b -q -x doSamples_v4.C\(\"WW\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     101) root -b -q -x doSamples_v4.C\(\"WW\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     102) root -b -q -x doSamples_v4.C\(\"WW\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     103) root -b -q -x doSamples_v4.C\(\"WW\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

     104) root -b -q -x doSamples_v4.C\(\"WZ\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     105) root -b -q -x doSamples_v4.C\(\"WZ\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     106) root -b -q -x doSamples_v4.C\(\"WZ\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     107) root -b -q -x doSamples_v4.C\(\"WZ\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     108) root -b -q -x doSamples_v4.C\(\"WZ\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     109) root -b -q -x doSamples_v4.C\(\"WZ\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     110) root -b -q -x doSamples_v4.C\(\"WZ\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     111) root -b -q -x doSamples_v4.C\(\"WZ\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     112) root -b -q -x doSamples_v4.C\(\"WZ\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     113) root -b -q -x doSamples_v4.C\(\"WZ\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     114) root -b -q -x doSamples_v4.C\(\"WZ\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     115) root -b -q -x doSamples_v4.C\(\"WZ\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     116) root -b -q -x doSamples_v4.C\(\"WZ\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     117) root -b -q -x doSamples_v4.C\(\"WZ\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

     118) root -b -q -x doSamples_v4.C\(\"ZZ\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     119) root -b -q -x doSamples_v4.C\(\"ZZ\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     120) root -b -q -x doSamples_v4.C\(\"ZZ\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     121) root -b -q -x doSamples_v4.C\(\"ZZ\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     122) root -b -q -x doSamples_v4.C\(\"ZZ\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     123) root -b -q -x doSamples_v4.C\(\"ZZ\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     124) root -b -q -x doSamples_v4.C\(\"ZZ\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     125) root -b -q -x doSamples_v4.C\(\"ZZ\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     126) root -b -q -x doSamples_v4.C\(\"ZZ\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     127) root -b -q -x doSamples_v4.C\(\"ZZ\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     128) root -b -q -x doSamples_v4.C\(\"ZZ\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     129) root -b -q -x doSamples_v4.C\(\"ZZ\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     130) root -b -q -x doSamples_v4.C\(\"ZZ\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
     131) root -b -q -x doSamples_v4.C\(\"ZZ\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;

     132) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",0,$variableSet\);;
     133) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",1,$variableSet\);;
     134) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",2,$variableSet\);;
     135) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",3,$variableSet\);;
     136) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",4,$variableSet\);;
     137) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",5,$variableSet\);;
     138) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",6,$variableSet\);;
     139) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",7,$variableSet\);;
     140) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",8,$variableSet\);;
     141) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",9,$variableSet\);;
     142) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",10,$variableSet\);;
     143) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",11,$variableSet\);;
     144) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",12,$variableSet\);;
     145) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",13,$variableSet\);;
     146) root -b -q -x doSamplesSep.C\(\"TWChannel_DS\",\"$BDTversion\",\"$TMVAdirectory\",14,$variableSet\);;

     147) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",0,$variableSet\);;
     148) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",1,$variableSet\);;
     149) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",2,$variableSet\);;
     150) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",3,$variableSet\);;
     151) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",4,$variableSet\);;
     152) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",5,$variableSet\);;
     153) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",6,$variableSet\);;
     154) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",7,$variableSet\);;
     155) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",8,$variableSet\);;
     156) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",9,$variableSet\);;
     157) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",10,$variableSet\);;
     158) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",11,$variableSet\);;
     159) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",12,$variableSet\);;
     160) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",13,$variableSet\);;
     161) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",14,$variableSet\);;

     162) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",0,$variableSet\);;
     163) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",1,$variableSet\);;
     164) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",2,$variableSet\);;
     165) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",3,$variableSet\);;
     166) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",4,$variableSet\);;
     167) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",5,$variableSet\);;
     168) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",6,$variableSet\);;
     169) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",7,$variableSet\);;
     170) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",8,$variableSet\);;
     171) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",9,$variableSet\);;
     172) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",10,$variableSet\);;
     173) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",11,$variableSet\);;
     174) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",12,$variableSet\);;
     175) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",13,$variableSet\);;
     176) root -b -q -x doSamplesSep.C\(\"TWChannel_TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",14,$variableSet\);;

     177) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",0,$variableSet\);;
     178) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",1,$variableSet\);;
     179) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",2,$variableSet\);;
     180) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",3,$variableSet\);;
     181) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",4,$variableSet\);;
     182) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",5,$variableSet\);;
     183) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",6,$variableSet\);;
     184) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",7,$variableSet\);;
     185) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",8,$variableSet\);;
     186) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",9,$variableSet\);;
     187) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",10,$variableSet\);;
     188) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",11,$variableSet\);;
     189) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",12,$variableSet\);;
     190) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",13,$variableSet\);;
     191) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",14,$variableSet\);;

     192) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",0,$variableSet\);;
     193) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",1,$variableSet\);;
     194) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",2,$variableSet\);;
     195) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",3,$variableSet\);;
     196) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",4,$variableSet\);;
     197) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",5,$variableSet\);;
     198) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",6,$variableSet\);;
     199) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",7,$variableSet\);;
     200) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",8,$variableSet\);;
     201) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",9,$variableSet\);;
     202) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",10,$variableSet\);;
     203) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",11,$variableSet\);;
     204) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",12,$variableSet\);;
     205) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",13,$variableSet\);;
     206) root -b -q -x doSamplesSep.C\(\"TWChannel_Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",14,$variableSet\);;

#      207) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"BtagSFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      208) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"BtagSFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      209) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"JERUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      210) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"JERDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      211) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"JESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      212) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"JESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      213) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"LESUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      214) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"LESDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      215) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"PUUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      216) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"PUDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      217) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"PDFUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      218) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"PDFDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      219) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"UnclusteredMETUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      220) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"UnclusteredMETDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      221) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"TopMassUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      222) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"TopMassDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      223) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"Q2Up\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      224) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"Q2Down\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      225) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"MatchingUp\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;
#      226) root -b -q -x doSamples_v4.C\(\"TTbarPowheg\",\"MatchingDown\",\"$BDTversion\",\"$TMVAdirectory\",$variableSet\);;



 esac