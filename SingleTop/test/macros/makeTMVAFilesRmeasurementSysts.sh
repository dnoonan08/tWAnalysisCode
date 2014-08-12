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
/bin/sleep 10
cd /home/t3-ku/dnoonan/8TeV_ProductionTest/CMSSW_5_3_11/src/TopQuarkAnalysis/SingleTop/test/macros
eval $(scram runtime -sh)
/bin/sleep 2

case "$1" in
    0)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel JERUp;;
    1)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel JERDown;;
    2)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel JESUp;;
    3)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel JESDown;;
    4)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel UnclusteredMETUp;;
    5)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel UnclusteredMETDown;;
    6)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel BtagSFUp;;
    7)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel BtagSFDown;;
    8)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel PUUp;;
    9)   ./TMVATupleCreator_v5_Rmeasurement.py TWChannel PUDown;;
    10)  ./TMVATupleCreator_v5_Rmeasurement.py TWChannel PDFUp;;
    11)  ./TMVATupleCreator_v5_Rmeasurement.py TWChannel PDFDown;;
    12)  ./TMVATupleCreator_v5_Rmeasurement.py TWChannel LESUp;;
    13)  ./TMVATupleCreator_v5_Rmeasurement.py TWChannel LESDown;;
	 
    14)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar JERUp;;
    15)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar JERDown;;
    16)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar JESUp;;
    17)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar JESDown;;
    18)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar UnclusteredMETUp;;
    19)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar UnclusteredMETDown;;
    20)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar BtagSFUp;;
    21)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar BtagSFDown;;
    22)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar PUUp;;
    23)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar PUDown;;
    24)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar PDFUp;;
    25)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar PDFDown;;
    26)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar LESUp;;
    27)  ./TMVATupleCreator_v5_Rmeasurement.py TTbar LESDown;;
	 
    28)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel JERUp;;
    29)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel JERDown;;
    30)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel JESUp;;
    31)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel JESDown;;
    32)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel UnclusteredMETUp;;
    33)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel UnclusteredMETDown;;
    34)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel BtagSFUp;;
    35)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel BtagSFDown;;
    36)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel PUUp;;
    37)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel PUDown;;
    38)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel PDFUp;;
    39)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel PDFDown;;
    40)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel LESUp;;
    41)  ./TMVATupleCreator_v5_Rmeasurement.py TChannel LESDown;;
	 
    42)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel JERUp;;
    43)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel JERDown;;
    44)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel JESUp;;
    45)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel JESDown;;
    46)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel UnclusteredMETUp;;
    47)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel UnclusteredMETDown;;
    48)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel BtagSFUp;;
    49)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel BtagSFDown;;
    50)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel PUUp;;
    51)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel PUDown;;
    52)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel PDFUp;;
    53)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel PDFDown;;
    54)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel LESUp;;
    55)  ./TMVATupleCreator_v5_Rmeasurement.py SChannel LESDown;;

    56)  ./TMVATupleCreator_v5_Rmeasurement.py WJets JERUp;;
    57)  ./TMVATupleCreator_v5_Rmeasurement.py WJets JERDown;;
    58)  ./TMVATupleCreator_v5_Rmeasurement.py WJets JESUp;;
    59)  ./TMVATupleCreator_v5_Rmeasurement.py WJets JESDown;;
    60)  ./TMVATupleCreator_v5_Rmeasurement.py WJets UnclusteredMETUp;;
    61)  ./TMVATupleCreator_v5_Rmeasurement.py WJets UnclusteredMETDown;;
    62)  ./TMVATupleCreator_v5_Rmeasurement.py WJets BtagSFUp;;
    63)  ./TMVATupleCreator_v5_Rmeasurement.py WJets BtagSFDown;;
    64)  ./TMVATupleCreator_v5_Rmeasurement.py WJets PUUp;;
    65)  ./TMVATupleCreator_v5_Rmeasurement.py WJets PUDown;;
    66)  ./TMVATupleCreator_v5_Rmeasurement.py WJets PDFUp;;
    67)  ./TMVATupleCreator_v5_Rmeasurement.py WJets PDFDown;;
    68)  ./TMVATupleCreator_v5_Rmeasurement.py WJets LESUp;;
    69)  ./TMVATupleCreator_v5_Rmeasurement.py WJets LESDown;;
    
    70)  ./TMVATupleCreator_v5_Rmeasurement.py WW JERUp;;
    71)  ./TMVATupleCreator_v5_Rmeasurement.py WW JERDown;;
    72)  ./TMVATupleCreator_v5_Rmeasurement.py WW JESUp;;
    73)  ./TMVATupleCreator_v5_Rmeasurement.py WW JESDown;;
    74)  ./TMVATupleCreator_v5_Rmeasurement.py WW UnclusteredMETUp;;
    75)  ./TMVATupleCreator_v5_Rmeasurement.py WW UnclusteredMETDown;;
    76)  ./TMVATupleCreator_v5_Rmeasurement.py WW BtagSFUp;;
    77)  ./TMVATupleCreator_v5_Rmeasurement.py WW BtagSFDown;;
    78)  ./TMVATupleCreator_v5_Rmeasurement.py WW PUUp;;
    79)  ./TMVATupleCreator_v5_Rmeasurement.py WW PUDown;;
    80)  ./TMVATupleCreator_v5_Rmeasurement.py WW PDFUp;;
    81)  ./TMVATupleCreator_v5_Rmeasurement.py WW PDFDown;;
    82)  ./TMVATupleCreator_v5_Rmeasurement.py WW LESUp;;
    83)  ./TMVATupleCreator_v5_Rmeasurement.py WW LESDown;;
         
    84)  ./TMVATupleCreator_v5_Rmeasurement.py WZ JERUp;;
    85)  ./TMVATupleCreator_v5_Rmeasurement.py WZ JERDown;;
    86)  ./TMVATupleCreator_v5_Rmeasurement.py WZ JESUp;;
    87)  ./TMVATupleCreator_v5_Rmeasurement.py WZ JESDown;;
    88)  ./TMVATupleCreator_v5_Rmeasurement.py WZ UnclusteredMETUp;;
    89)  ./TMVATupleCreator_v5_Rmeasurement.py WZ UnclusteredMETDown;;
    90)  ./TMVATupleCreator_v5_Rmeasurement.py WZ BtagSFUp;;
    91)  ./TMVATupleCreator_v5_Rmeasurement.py WZ BtagSFDown;;
    92)  ./TMVATupleCreator_v5_Rmeasurement.py WZ PUUp;;
    93)  ./TMVATupleCreator_v5_Rmeasurement.py WZ PUDown;;
    94)  ./TMVATupleCreator_v5_Rmeasurement.py WZ PDFUp;;
    95)  ./TMVATupleCreator_v5_Rmeasurement.py WZ PDFDown;;
    96)  ./TMVATupleCreator_v5_Rmeasurement.py WZ LESUp;;
    97)  ./TMVATupleCreator_v5_Rmeasurement.py WZ LESDown;;
         
    98)  ./TMVATupleCreator_v5_Rmeasurement.py ZZ JERUp;;
    99)  ./TMVATupleCreator_v5_Rmeasurement.py ZZ JERDown;;
    100) ./TMVATupleCreator_v5_Rmeasurement.py ZZ JESUp;;
    101) ./TMVATupleCreator_v5_Rmeasurement.py ZZ JESDown;;
    102) ./TMVATupleCreator_v5_Rmeasurement.py ZZ UnclusteredMETUp;;
    103) ./TMVATupleCreator_v5_Rmeasurement.py ZZ UnclusteredMETDown;;
    104) ./TMVATupleCreator_v5_Rmeasurement.py ZZ BtagSFUp;;
    105) ./TMVATupleCreator_v5_Rmeasurement.py ZZ BtagSFDown;;
    106) ./TMVATupleCreator_v5_Rmeasurement.py ZZ PUUp;;
    107) ./TMVATupleCreator_v5_Rmeasurement.py ZZ PUDown;;
    108) ./TMVATupleCreator_v5_Rmeasurement.py ZZ PDFUp;;
    109) ./TMVATupleCreator_v5_Rmeasurement.py ZZ PDFDown;;
    110) ./TMVATupleCreator_v5_Rmeasurement.py ZZ LESUp;;
    111) ./TMVATupleCreator_v5_Rmeasurement.py ZZ LESDown;;
    	 
    112) ./TMVATupleCreator_v5_Rmeasurement.py TWChannel_DS;;
    113) ./TMVATupleCreator_v5_Rmeasurement.py TWChannel_Q2Up;;
    114) ./TMVATupleCreator_v5_Rmeasurement.py TWChannel_Q2Down;;
    115) ./TMVATupleCreator_v5_Rmeasurement.py TWChannel_TopMassUp;;
    116) ./TMVATupleCreator_v5_Rmeasurement.py TWChannel_TopMassDown;;
    117) ./TMVATupleCreator_v5_Rmeasurement.py TTBar_Q2Up;;
    118) ./TMVATupleCreator_v5_Rmeasurement.py TTBar_Q2Down;;
    119) ./TMVATupleCreator_v5_Rmeasurement.py TTBar_MatchingUp;;
    120) ./TMVATupleCreator_v5_Rmeasurement.py TTBar_MatchingDown;;
    121) ./TMVATupleCreator_v5_Rmeasurement.py TTBar_TopMassUp;;
    122) ./TMVATupleCreator_v5_Rmeasurement.py TTBar_TopMassDown;;

    123) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 JERUp;;		     
    124) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 JERDown;;	     
    125) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 JESUp;;		         	 
    126) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 JESDown;;	     
    127) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 UnclusteredMETUp;;   
    128) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 UnclusteredMETDown;; 
    129) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 BtagSFUp;;	     
    130) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 BtagSFDown;;	     
    131) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 PUUp;;		     
    132) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 PUDown;;	     
    133) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 PDFUp;;		     
    134) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 PDFDown;;	     
    135) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 LESUp;;		     
    136) ./TMVATupleCreator_v5_Rmeasurement.py ZJets1 LESDown;;            

    137) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 JERUp;;		     
    138) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 JERDown;;	     
    139) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 JESUp;;		         	 
    140) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 JESDown;;	     
    141) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 UnclusteredMETUp;;   
    142) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 UnclusteredMETDown;; 
    143) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 BtagSFUp;;	     
    144) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 BtagSFDown;;	     
    145) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 PUUp;;		     
    146) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 PUDown;;	     
    147) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 PDFUp;;		     
    148) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 PDFDown;;	     
    149) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 LESUp;;		     
    150) ./TMVATupleCreator_v5_Rmeasurement.py ZJets2 LESDown;;            

    151) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 JERUp;;		     
    152) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 JERDown;;	     
    153) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 JESUp;;		         	 
    154) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 JESDown;;	     
    155) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 UnclusteredMETUp;;   
    156) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 UnclusteredMETDown;; 
    157) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 BtagSFUp;;	     
    158) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 BtagSFDown;;	     
    159) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 PUUp;;		     
    160) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 PUDown;;	     
    161) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 PDFUp;;		     
    162) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 PDFDown;;	     
    163) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 LESUp;;		     
    164) ./TMVATupleCreator_v5_Rmeasurement.py ZJets3 LESDown;;            

    165) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 JERUp;;		     
    166) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 JERDown;;	     
    167) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 JESUp;;		         	 
    168) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 JESDown;;	     
    169) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 UnclusteredMETUp;;   
    170) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 UnclusteredMETDown;; 
    171) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 BtagSFUp;;	     
    172) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 BtagSFDown;;	     
    173) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 PUUp;;		     
    174) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 PUDown;;	     
    175) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 PDFUp;;		     
    176) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 PDFDown;;	     
    177) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 LESUp;;		     
    178) ./TMVATupleCreator_v5_Rmeasurement.py ZJets4 LESDown;;            

    179) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 JERUp;;		     
    180) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 JERDown;;	     
    181) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 JESUp;;		         	 
    182) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 JESDown;;	     
    183) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 UnclusteredMETUp;;   
    184) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 UnclusteredMETDown;; 
    185) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 BtagSFUp;;	     
    186) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 BtagSFDown;;	     
    187) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 PUUp;;		     
    188) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 PUDown;;	     
    189) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 PDFUp;;		     
    190) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 PDFDown;;	     
    191) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 LESUp;;		     
    192) ./TMVATupleCreator_v5_Rmeasurement.py ZJets5 LESDown;;            

    193)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg JERUp;;
    194)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg JERDown;;
    195)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg JESUp;;
    196)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg JESDown;;
    197)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg UnclusteredMETUp;;
    198)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg UnclusteredMETDown;;
    199)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg BtagSFUp;;
    200)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg BtagSFDown;;
    201)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg PUUp;;
    202)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg PUDown;;
    203)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg PDFUp;;
    204)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg PDFDown;;
    205)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg LESUp;;
    206)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarPowheg LESDown;;

    207)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin JERUp;;
    208)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin JERDown;;
    209)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin JESUp;;
    210)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin JESDown;;
    211)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin UnclusteredMETUp;;
    212)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin UnclusteredMETDown;;
    213)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin BtagSFUp;;
    214)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin BtagSFDown;;
    215)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin PUUp;;
    216)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin PUDown;;
    217)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin PDFUp;;
    218)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin PDFDown;;
    219)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin LESUp;;
    220)  ./TMVATupleCreator_v5_Rmeasurement.py TTbarSpin LESDown;;
    
esac