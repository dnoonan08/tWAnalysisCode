#!/usr/bin/env python

import sys

if not '-b' in sys.argv:
    sys.argv.append( '-b' )

from ROOT import *

from array import *

import itertools

from ZjetSF_3 import *

RunA = True
RunB = True
RunC = True
RunD = True

quickRun = False
verbose = True

from ttSpinSF import *

pickTop = True #False will pick antitop

DS_symm = False

BDT = 'AdaBoostDefault_NewTests'

nBins = 50
limits = 1.001
#limitLow = -0.38
#limitHigh = 0.32
limitLow = -1.001
limitHigh = 1.001

RmeasurementCut = 0.0

useDS = True
useZJetSF = True

useTopMass = True
useTopPtReweight = False

UnEvenBins = False
ThreeBins = False
FourBins = False
SixBins = False

_1BinCR = False
#_1BinCR = True


# directory = "v3_Rmeasurement"
directory = "ManyRegions_v4"

if 'AdaBoostDefault_NewTests' in BDT:
    nBins = 35
    limitLow = -0.4
    limitHigh = 0.3    
    UnEvenBins = False

useOverflow = False
    
i=0

ExtraNames = "_TopPtSpinSysts"
ExtraNames = "_TopPtSpinSysts_NoTopMass"
ExtraNames = ""

rmSysts = list()

while i < len(sys.argv):
    arg = sys.argv[i]
    print arg
    if arg == '-b':
        print
#        i += 1
#        continue
    elif 'thetaInputFileCreator' in arg:
        print
#        i += 1
#        continue        
    elif '-d' in arg:
        i += 1
        directory = sys.argv[i]
    elif '-nBins' in arg:
        i += 1
        nBins = int(sys.argv[i])
    elif '-bdt' in arg:
        i += 1
        BDT = sys.argv[i]
    elif '-limitLow' in arg:
        print 'ChangeLowLimit'
        i += 1
        limitLow = float(sys.argv[i])
        print limitLow
    elif '-limitHigh' in arg:
        print 'ChangeHighLimit'
        i += 1
        limitHigh = float(sys.argv[i])
        print limitHigh
    elif '-limit' in arg:
        i += 1
        limits = float(sys.argv[i])
    elif '-rm' in arg:
        i += 1
        rmSysts.append(sys.argv[i])
    elif '1BinCR' in arg:
        _1BinCR=True
    elif 'UnEvenBins' in arg:
        UnEvenBins = True
    elif '-n' in arg:
        i+=1
        ExtraNames+=sys.argv[i]
    elif 'overflow' in arg:
        useOverflow = True
    elif 'DSsymm' in arg:
        DS_symm = True
    elif 'TopPtReweight' in arg:
        useTopPtReweight = True
        ExtraNames += "TopPtReweight"
    elif 'NoTopMass' in arg:
        useTopMass = False
        ExtraNames += "NoTopMass"
    elif arg=='AntiTop':
        print 'AntiTop is picked'
        pickTop = False
    elif arg=='Top':
        print 'Top is picked'
        pickTop = True
    elif '-Rcut' in arg:
        i += 1
        RmeasurementCut = float(sys.argv[i])
    else:
        print arg is 'Top'
        print arg is "Top"
        print arg=='Top'
        print 'Top' in arg
        print "Unknown argument: " + arg

    i += 1    

print limitLow, limitHigh, nBins

if RmeasurementCut == 0.0:
    RmeasurementCut = -0.01

if DS_symm:
    ExtraNames += "_symmDS"

if UnEvenBins:
    if ThreeBins:
        ExtraNames += "_3UnevenBins"
    elif FourBins:
        ExtraNames += "_4UnevenBins"
    elif SixBins:
        ExtraNames += "_6UnevenBins"
    else:
        ExtraNames += "_5UnevenBins"
else:
    ExtraNames += "_"+str(nBins) + "Bins"
    if useOverflow:
        ExtraNames += "wOverflow"
if _1BinCR:
    ExtraNames += "_1BinCR"
if 'MET40' in directory:
    ExtraNames += "_MET40"
elif 'MET50' in directory:
    ExtraNames += "_MET50"
elif directory == 'v4':
    ExtraNames += "_MET30"


fileList = ['TWChannel_T.root',
            'TWChannel_Tbar.root',
            'TTbarNew.root',
#            'TTbar.root',
            'TChannel.root',
            'SChannel.root',
            'ZJets.root',
            'WJets.root',
            'WW.root',
            'WZ.root',
            'ZZ.root',
            'DATA']


fileHistoInput = [0,
                  1,
                  2,
                  3,
                  3,
                  3,
                  3,
                  3,
                  3,
                  3,
                  -1]

DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
Systs = ['JER','JES','UnclusteredMET','LES','PDF','BtagSF','PU']
#Systs = ['JER','UnclusteredMET','LES','PDF','BtagSF','LepSF']


# ExtraTWSysts = ['TopMass','Q2']
# ExtraTTbarSysts = ['TopMass', 'Q2','Matching', 'TopPt', 'SpinCorr']
ExtraTWSysts = ['TopMass','Q2']
ExtraTTbarSysts = ['TopMass','Q2','Matching', 'TopPt']

for syst in rmSysts:
    if syst in Systs:
        Systs.remove(syst)
    if syst in ExtraTTbarSysts:
        ExtraTTbarSysts.remove(syst)
    if syst in ExtraTWSysts:
        ExtraTWSysts.remove(syst)

if 'TopMass' in rmSysts:
    useTopMass = False

if not useTopMass:
    if 'TopMass' in ExtraTTbarSysts:
        ExtraTTbarSysts.remove('TopMass')
    if 'TopMass' in ExtraTWSysts:
        ExtraTWSysts.remove('TopMass')

                   
regions = ['1j1tT','1j1tTbar','2j1t','2j2t']


reader_tW_tbarW = TMVA.Reader( "!Color:!Silent" )

__lepJetPt               = array('f',[0])
__lepPt                  = array('f',[0])
__lepJetDR               = array('f',[0])
__lepJetDPhi             = array('f',[0])
__lepJetDEta             = array('f',[0])
__lepJetM                = array('f',[0])
__lepPtRelJet            = array('f',[0])
__lepPtRelJetSameLep     = array('f',[0])
__lepJetCosTheta_boosted = array('f',[0])

reader_tW_tbarW.AddVariable ("lepJetPt",              __lepJetPt          )
reader_tW_tbarW.AddVariable ("lepPt",                 __lepPt             )
reader_tW_tbarW.AddVariable ("lepJetDR",              __lepJetDR          )
reader_tW_tbarW.AddVariable ("lepJetDPhi",            __lepJetDPhi        )
reader_tW_tbarW.AddVariable ("lepJetDEta",            __lepJetDEta        )
reader_tW_tbarW.AddVariable ("lepJetM",               __lepJetM           )
reader_tW_tbarW.AddVariable ("lepPtRelJet",           __lepPtRelJet       )
reader_tW_tbarW.AddVariable ("lepPtRelJetSameLep",    __lepPtRelJetSameLep)
reader_tW_tbarW.AddVariable ("lepJetCosTheta_boosted",__lepJetCosTheta_boosted )


reader_tW_tbarW.BookMVA("BDT", "../weights/test_tW_tbarW_tW_tbarW_April15GradBoost500Trees.weights.xml")


HistoLists = list()
for chan in ChanName:
    chanList = list()
    
    for reg in regions:

        if "Bagging" in BDT and UnEvenBins:

            if ThreeBins:
                nBins = 3        
                newBins = array('d',[-1.001,-0.97,0.97,1.001])
            elif FourBins:
                nBins = 4
                newBins = array('d',[-1.001,-0.995,0.,0.995,1.001])
            elif SixBins:
                nBins = 6
                newBins = array('d',[-1.001,-0.995,-0.8,0.0,0.8,0.995,1.001])
            else:
                nBins = 5            
                newBins = array('d',[-1.001,-0.995,-0.7,0.7,0.995,1.001])

                
            if '1j1t' not in reg and _1BinCR:
                nBins = 1
                newBins = array('d',[-1.001,1.001])

            tw = TH1F(chan+reg+ "__twdr","",nBins,newBins)
            tw.Sumw2()
            tbarw = TH1F(chan+reg+ "__tbarwdr","",nBins,newBins)
            tbarw.Sumw2()
            tt = TH1F(chan+reg+ "__tt","",nBins,newBins)
            tt.Sumw2()
            other = TH1F(chan+reg+ "__other","",nBins,newBins)
            other.Sumw2()
            data = TH1F(chan+reg+ "__DATA","",nBins,newBins)

            twList = list()
            tbarwList = list()
            ttList = list()
            otherList = list()
            dataList = list()
            twsyst = list()
            tbarwsyst = list()
            ttsyst = list()
            othersyst = list()
        
            
            for syst in Systs:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,newBins)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,newBins)
                tempsystTW = [twsystUp,twsystDown]
                tbarwsystUp = TH1F(chan+reg+ "__tbarwdr__"+syst + "__plus","",nBins,newBins)
                tbarwsystDown = TH1F(chan+reg+ "__tbarwdr__"+syst + "__minus","",nBins,newBins)
                tempsystTbarW = [tbarwsystUp,tbarwsystDown]
                ttbarsystUp = TH1F(chan+reg+ "__tt__"+syst + "__plus","",nBins,newBins)
                ttbarsystDown = TH1F(chan+reg+ "__tt__"+syst + "__minus","",nBins,newBins)
                tempsystTT = [ttbarsystUp,ttbarsystDown]
                othersystUp = TH1F(chan+reg+ "__other__"+syst + "__plus","",nBins,newBins)
                othersystDown = TH1F(chan+reg+ "__other__"+syst + "__minus","",nBins,newBins)
                tempsystOTHER = [othersystUp,othersystDown]
                twsyst.append(tempsystTW)
                tbarwsyst.append(tempsystTbarW)
                ttsyst.append(tempsystTT)
                othersyst.append(tempsystOTHER)

            for syst in ExtraTWSysts:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,newBins)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,newBins)
                tempsystTW = [twsystUp,twsystDown]
                twsyst.append(tempsystTW)
                tbarwsystUp = TH1F(chan+reg+ "__tbarwdr__"+syst + "__plus","",nBins,newBins)
                tbarwsystDown = TH1F(chan+reg+ "__tbarwdr__"+syst + "__minus","",nBins,newBins)
                tempsystTbarW = [tbarwsystUp,tbarwsystDown]
                tbarwsyst.append(tempsystTbarW)

            for syst in ExtraTTbarSysts:
                ttbarsystUp = TH1F(chan+reg+ "__tt__"+syst + "__plus","",nBins,newBins)
                ttbarsystDown = TH1F(chan+reg+ "__tt__"+syst + "__minus","",nBins,newBins)
                tempsystTT = [ttbarsystUp,ttbarsystDown]
                ttsyst.append(tempsystTT)

            #ADDING IN DRDS Histo By Hand
        
            if useDS:
                twsystUp = TH1F(chan+reg+ "__twdr__DRDS__plus","",nBins,newBins)
                twsystDown = TH1F(chan+reg+ "__twdr__DRDS__minus","",nBins,newBins)
                tempsystTW = [twsystUp,twsystDown]
                twsyst.append(tempsystTW)
                tbarwsystUp = TH1F(chan+reg+ "__tbarwdr__DRDS__plus","",nBins,newBins)
                tbarwsystDown = TH1F(chan+reg+ "__tbarwdr__DRDS__minus","",nBins,newBins)
                tempsystTbarW = [tbarwsystUp,tbarwsystDown]
                tbarwsyst.append(tempsystTbarW)

            #ADDING IN ZJET SF HISTOS BY HAND
            if useZJetSF:
                zjetSFUp = TH1F(chan+reg+ "__other__ZjetSF__plus","",nBins,newBins)
                zjetSFDown = TH1F(chan+reg+ "__other__ZjetSF__minus","",nBins,newBins)
                tempsystOther = [zjetSFUp,zjetSFDown]
                othersyst.append(tempsystOther)


        else:

            tw = TH1F(chan+reg+ "__twdr","",nBins,limitLow,limitHigh)
            tw.Sumw2()
            tbarw = TH1F(chan+reg+ "__tbarwdr","",nBins,limitLow,limitHigh)
            tbarw.Sumw2()
            tt = TH1F(chan+reg+ "__tt","",nBins,limitLow,limitHigh)
            tt.Sumw2()
            other = TH1F(chan+reg+ "__other","",nBins,limitLow,limitHigh)
            other.Sumw2()
            data = TH1F(chan+reg+ "__DATA","",nBins,limitLow,limitHigh)

            twList = list()
            tbarwList = list()
            ttList = list()
            otherList = list()
            dataList = list()
            twsyst = list()
            tbarwsyst = list()
            ttsyst = list()
            othersyst = list()
        
            for syst in Systs:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,limitLow,limitHigh)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTW = [twsystUp,twsystDown]

                tbarwsystUp = TH1F(chan+reg+ "__tbarwdr__"+syst + "__plus","",nBins,limitLow,limitHigh)
                tbarwsystDown = TH1F(chan+reg+ "__tbarwdr__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTbarW = [tbarwsystUp,tbarwsystDown]

                ttbarsystUp = TH1F(chan+reg+ "__tt__"+syst + "__plus","",nBins,limitLow,limitHigh)
                ttbarsystDown = TH1F(chan+reg+ "__tt__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTT = [ttbarsystUp,ttbarsystDown]

                othersystUp = TH1F(chan+reg+ "__other__"+syst + "__plus","",nBins,limitLow,limitHigh)
                othersystDown = TH1F(chan+reg+ "__other__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystOTHER = [othersystUp,othersystDown]

                twsyst.append(tempsystTW)
                tbarwsyst.append(tempsystTbarW)
                ttsyst.append(tempsystTT)
                othersyst.append(tempsystOTHER)

            for syst in ExtraTWSysts:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,limitLow,limitHigh)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTW = [twsystUp,twsystDown]
                twsyst.append(tempsystTW)

                tbarwsystUp = TH1F(chan+reg+ "__tbarwdr__"+syst + "__plus","",nBins,limitLow,limitHigh)
                tbarwsystDown = TH1F(chan+reg+ "__tbarwdr__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTbarW = [tbarwsystUp,tbarwsystDown]
                tbarwsyst.append(tempsystTbarW)

            for syst in ExtraTTbarSysts:
                ttbarsystUp = TH1F(chan+reg+ "__tt__"+syst + "__plus","",nBins,limitLow,limitHigh)
                ttbarsystDown = TH1F(chan+reg+ "__tt__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTT = [ttbarsystUp,ttbarsystDown]
                ttsyst.append(tempsystTT)

            #ADDING IN DRDS Histo By Hand
        
            if useDS:
                twsystUp = TH1F(chan+reg+ "__twdr__DRDS__plus","",nBins,limitLow,limitHigh)
                twsystDown = TH1F(chan+reg+ "__twdr__DRDS__minus","",nBins,limitLow,limitHigh)
                tempsystTW = [twsystUp,twsystDown]
                twsyst.append(tempsystTW)

                tbarwsystUp = TH1F(chan+reg+ "__tbarwdr__DRDS__plus","",nBins,limitLow,limitHigh)
                tbarwsystDown = TH1F(chan+reg+ "__tbarwdr__DRDS__minus","",nBins,limitLow,limitHigh)
                tempsystTbarW = [tbarwsystUp,tbarwsystDown]
                tbarwsyst.append(tempsystTbarW)

            #ADDING IN ZJET SF HISTOS BY HAND
            if useZJetSF:
                zjetSFUp = TH1F(chan+reg+ "__other__ZjetSF__plus","",nBins,limitLow,limitHigh)
                zjetSFDown = TH1F(chan+reg+ "__other__ZjetSF__minus","",nBins,limitLow,limitHigh)
                tempsystOther = [zjetSFUp,zjetSFDown]
                othersyst.append(tempsystOther)



        twList.append(tw)
        twList.append(twsyst)
        tbarwList.append(tbarw)
        tbarwList.append(tbarwsyst)
        ttList.append(tt)
        ttList.append(ttsyst)
        otherList.append(other)
        otherList.append(othersyst)
        dataList.append(data)
        regionList = list()
        regionList.append(twList)
        regionList.append(tbarwList)
        regionList.append(ttList)
        regionList.append(otherList)
        regionList.append(dataList)
        chanList.append(regionList)
    HistoLists.append(chanList)

for chan in range(3):
    for reg in range(4):
        if regions[reg] == '1j1tT': pickTop = True
        if regions[reg] == '1j1tTbar': pickTop = False
        _reg = regions[reg]
        if '1j1t' in _reg:
            _reg = '1j1t'
        for fileNum in range(len(fileList)):
            file = fileList[fileNum]

            vartree = TChain(Folder[chan]+'/'+_reg)
            tree = TChain(BDT + '_' + ChanName[chan] + '_' + _reg)

#             if 'TTbar' in file:
#                 directory = 'TopPtReweighting'
#             else:
#                 directory = 'v11_MET50'

#             if file == 'DATA':
#                 tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012A_Output.root")
#                 tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012B_Output.root")
#                 tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012C_Output.root")
#                 tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012D_Output.root")
#                 vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012A.root')
#                 vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012B.root')
#                 vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012C.root')
#                 vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012D.root')                
#             else:                
            if not file == 'DATA':
                fileName = file.replace('.roo', '_Output.roo')
                print fileName
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                vartree.Add('../tmvaFiles/'+directory+'/'+file)
                

            nEvents = tree.GetEntries()*1.

            print nEvents
            print ChanName[chan], regions[reg], _reg, file
            
            evtCount = 0.
            percent = 0.0
            progSlots = 25.    

#             print file
            if not verbose: print file
            
            for event,var in itertools.izip(tree,vartree):
#            for event in tree:
                evtCount += 1.
                if evtCount/nEvents > percent and verbose:
                    k = int(percent*progSlots)
                    progress = file+' 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                    sys.stdout.write(progress)
                    sys.stdout.flush()
                    percent += 1./progSlots

                if quickRun and evtCount > 200: break

                _BDT       = event.BDT
                if useOverflow:
                    if _BDT < limitLow:
                        _BDT = limitLow + .001
                    if _BDT > limitHigh:
                        _BDT = limitHigh - .001
            
                _weightA   = event.weightA
                _weightB   = event.weightB
                _weightC   = event.weightC
                _weightD   = event.weightD

                _VweightA   = var.weightA
                _VweightB   = var.weightB
                _VweightC   = var.weightC
                _VweightD   = var.weightD

                _weight = 0

                if _reg == '1j1t':
                    lepJetPt_PosLep               = var.lepJetPt_PosLep            
                    lepPt_PosLep                  = var.lepPt_PosLep               
                    lepJetDR_PosLep               = var.lepJetDR_PosLep            
                    lepJetDPhi_PosLep             = var.lepJetDPhi_PosLep          
                    lepJetDEta_PosLep             = var.lepJetDEta_PosLep          
                    lepJetM_PosLep                = var.lepJetM_PosLep             
                    lepPtRelJet_PosLep            = var.lepPtRelJet_PosLep         
                    jetPtRelLep_PosLep            = var.jetPtRelLep_PosLep         
                    lepPtRelJetSameLep_PosLep     = var.lepPtRelJetSameLep_PosLep  
                    lepPtRelJetOtherLep_PosLep    = var.lepPtRelJetOtherLep_PosLep 
                    lepJetMt_PosLep               = var.lepJetMt_PosLep            
                    lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep
                    lepJetPt_NegLep               = var.lepJetPt_NegLep            
                    lepPt_NegLep                  = var.lepPt_NegLep               
                    lepJetDR_NegLep               = var.lepJetDR_NegLep            
                    lepJetDPhi_NegLep             = var.lepJetDPhi_NegLep          
                    lepJetDEta_NegLep             = var.lepJetDEta_NegLep          
                    lepJetM_NegLep                = var.lepJetM_NegLep             
                    lepPtRelJet_NegLep            = var.lepPtRelJet_NegLep         
                    jetPtRelLep_NegLep            = var.jetPtRelLep_NegLep         
                    lepPtRelJetSameLep_NegLep     = var.lepPtRelJetSameLep_NegLep  
                    lepPtRelJetOtherLep_NegLep    = var.lepPtRelJetOtherLep_NegLep 
                    lepJetMt_NegLep               = var.lepJetMt_NegLep            
                    lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep
            
                    __lepJetPt[0]               = lepJetPt_PosLep          
                    __lepPt[0]                  = lepPt_PosLep             
                    __lepJetDR[0]               = lepJetDR_PosLep          
                    __lepJetDPhi[0]             = lepJetDPhi_PosLep        
                    __lepJetDEta[0]             = lepJetDEta_PosLep        
                    __lepJetM[0]                = lepJetM_PosLep           
                    __lepPtRelJet[0]            = lepPtRelJet_PosLep       
                    __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_PosLep
                    __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_PosLep
    
                    positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
        
                    __lepJetPt[0]               = lepJetPt_NegLep          
                    __lepPt[0]                  = lepPt_NegLep             
                    __lepJetDR[0]               = lepJetDR_NegLep          
                    __lepJetDPhi[0]             = lepJetDPhi_NegLep        
                    __lepJetDEta[0]             = lepJetDEta_NegLep        
                    __lepJetM[0]                = lepJetM_NegLep           
                    __lepPtRelJet[0]            = lepPtRelJet_NegLep       
                    __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_NegLep
                    __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_NegLep
            
                    negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")

                    if abs(positiveLepBDT - negativeLepBDT) < RmeasurementCut:
                        continue
    
                    if pickTop and negativeLepBDT > positiveLepBDT:
                        continue
    
                    if not pickTop and positiveLepBDT > negativeLepBDT:
                        continue
                    
                if _weightA != _VweightA or _weightB != _VweightB or _weightC != _VweightC or _weightD != _VweightD:
                    print "BIG ISSUE"
                    sys.exit(1)

                if RunA:
                    _weight = _weight + _weightA
                if RunB:
                    _weight = _weight + _weightB
                if RunC:
                    _weight = _weight + _weightC
                if RunD:
                    _weight = _weight + _weightD

                _met       = var.met


                _weightDown = _weight
                _weightUp = _weight

                if useZJetSF:
                    if "ZJets" in file:
                        _ZjetSF = ZjetSF(_met, chan)
                        _weight = _weight*_ZjetSF
                        _weightUp = 2.*_weight-_weightDown

                if useZJetSF:
                    if fileHistoInput[fileNum]==3:
                        HistoLists[chan][reg][fileHistoInput[fileNum]][1][-1][0].Fill(_BDT, _weightUp)
                        HistoLists[chan][reg][fileHistoInput[fileNum]][1][-1][1].Fill(_BDT, _weightDown)

                if 'TTbar' in file:
                    if useTopPtReweight:
                        _topPTSF =  var.weightTopPt - 1.
                        startWeight = _weight
                        _weight = startWeight*(1+_topPTSF)
                        HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('TopPt')-len(ExtraTTbarSysts)][0].Fill(_BDT, startWeight*(1.+2*_topPTSF))
                        HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('TopPt')-len(ExtraTTbarSysts)][1].Fill(_BDT, startWeight)
                    else:
                        _topPTSF =  var.weightTopPt - 1.                                        
                        HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('TopPt')-len(ExtraTTbarSysts)][0].Fill(_BDT, _weight*(1.+_topPTSF))
                        HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('TopPt')-len(ExtraTTbarSysts)][1].Fill(_BDT, _weight*(1.-_topPTSF))


                    _NlooseJet20Central = var.NlooseJet20Central
                    _ptsys              = var.ptsys
                    _centralityJLL      = var.centralityJLL

#                     if not 'TTbarNew' in file:
#                         spinSF = ttSpinSF(_NlooseJet20Central,_centralityJLL, _ptsys, _reg)-1.
#                         HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('SpinCorr')-len(ExtraTTbarSysts)][0].Fill(_BDT, _weight*(1.+spinSF))
#                         HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('SpinCorr')-len(ExtraTTbarSysts)][1].Fill(_BDT, _weight*(1.-spinSF))
                    
                    
                

                if "DATA" in file:
                    _weight = 1.


                HistoLists[chan][reg][fileHistoInput[fileNum]][0].Fill(_BDT, _weight)
                HistoLists[chan][reg][-1][0].Fill(_BDT, _weight)
            if verbose: print


            SystList = Systs[:]
            if "TTbar" in file:
                SystList += ExtraTTbarSysts
                SystList.remove("TopPt")
                if "SpinCorr" in SystList: SystList.remove("SpinCorr")
            if "DATA" in file:
                SystList = []

            for s in range(len(SystList)):
                syst = SystList[s]
                tree = TChain(BDT + '_' + ChanName[chan] + '_' + _reg)
                vartree = TChain(Folder[chan]+'/'+_reg)

                fileName = file.replace('.ro','_'+syst+'Up_Output.ro')

                _varFileName = file.replace('.ro','_'+syst+'Up.ro')

                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                vartree.Add('../tmvaFiles/'+directory+'/'+_varFileName)


                nEvents = tree.GetEntries()*1.

#                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    

                if not verbose: print file+" "+syst+'Up'
            
                for event,var in itertools.izip(tree,vartree):
#                for event in tree:
                    evtCount += 1.
                    if evtCount/nEvents > percent and verbose:
                        k = int(percent*progSlots)
                        progress = file+" "+syst+'Up 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots

                    if quickRun and  evtCount > 200: break
 


                    _BDT                        = event.BDT                   
                    if useOverflow:
                        if _BDT < limitLow:
                            _BDT = limitLow + .001
                        if _BDT > limitHigh:
                            _BDT = limitHigh - .001
            
                    _weightA                    = event.weightA
                    _weightB                    = event.weightB
                    _weightC                    = event.weightC
                    _weightD                    = event.weightD
                    
                    _weight = 0

                    if RunA:
                        _weight = _weight + _weightA
                    if RunB:
                        _weight = _weight + _weightB
                    if RunC:
                        _weight = _weight + _weightC
                    if RunD:
                        _weight = _weight + _weightD

                    _met       = var.met


                    if _reg == '1j1t':
                        lepJetPt_PosLep               = var.lepJetPt_PosLep            
                        lepPt_PosLep                  = var.lepPt_PosLep               
                        lepJetDR_PosLep               = var.lepJetDR_PosLep            
                        lepJetDPhi_PosLep             = var.lepJetDPhi_PosLep          
                        lepJetDEta_PosLep             = var.lepJetDEta_PosLep          
                        lepJetM_PosLep                = var.lepJetM_PosLep             
                        lepPtRelJet_PosLep            = var.lepPtRelJet_PosLep         
                        jetPtRelLep_PosLep            = var.jetPtRelLep_PosLep         
                        lepPtRelJetSameLep_PosLep     = var.lepPtRelJetSameLep_PosLep  
                        lepPtRelJetOtherLep_PosLep    = var.lepPtRelJetOtherLep_PosLep 
                        lepJetMt_PosLep               = var.lepJetMt_PosLep            
                        lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep
                        lepJetPt_NegLep               = var.lepJetPt_NegLep            
                        lepPt_NegLep                  = var.lepPt_NegLep               
                        lepJetDR_NegLep               = var.lepJetDR_NegLep            
                        lepJetDPhi_NegLep             = var.lepJetDPhi_NegLep          
                        lepJetDEta_NegLep             = var.lepJetDEta_NegLep          
                        lepJetM_NegLep                = var.lepJetM_NegLep             
                        lepPtRelJet_NegLep            = var.lepPtRelJet_NegLep         
                        jetPtRelLep_NegLep            = var.jetPtRelLep_NegLep         
                        lepPtRelJetSameLep_NegLep     = var.lepPtRelJetSameLep_NegLep  
                        lepPtRelJetOtherLep_NegLep    = var.lepPtRelJetOtherLep_NegLep 
                        lepJetMt_NegLep               = var.lepJetMt_NegLep            
                        lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep
                
                        __lepJetPt[0]               = lepJetPt_PosLep          
                        __lepPt[0]                  = lepPt_PosLep             
                        __lepJetDR[0]               = lepJetDR_PosLep          
                        __lepJetDPhi[0]             = lepJetDPhi_PosLep        
                        __lepJetDEta[0]             = lepJetDEta_PosLep        
                        __lepJetM[0]                = lepJetM_PosLep           
                        __lepPtRelJet[0]            = lepPtRelJet_PosLep       
                        __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_PosLep
                        __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_PosLep
        
                        positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
            
                        __lepJetPt[0]               = lepJetPt_NegLep          
                        __lepPt[0]                  = lepPt_NegLep             
                        __lepJetDR[0]               = lepJetDR_NegLep          
                        __lepJetDPhi[0]             = lepJetDPhi_NegLep        
                        __lepJetDEta[0]             = lepJetDEta_NegLep        
                        __lepJetM[0]                = lepJetM_NegLep           
                        __lepPtRelJet[0]            = lepPtRelJet_NegLep       
                        __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_NegLep
                        __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_NegLep
                
                        negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")

                        if abs(positiveLepBDT - negativeLepBDT) < RmeasurementCut:
                            continue
                        
                        if pickTop and negativeLepBDT > positiveLepBDT:
                            continue
    
                        if not pickTop and positiveLepBDT > negativeLepBDT:
                            continue
        
                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF


                    HistoLists[chan][reg][fileHistoInput[fileNum]][1][s][0].Fill(_BDT, _weight)

                if verbose: print

                tree = TChain(BDT + '_' + ChanName[chan] + '_' + _reg)
                vartree = TChain(Folder[chan]+'/'+_reg)
                fileName = file.replace('.ro','_'+syst+'Down_Output.ro')
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)

                _varFileName = file.replace('.ro','_'+syst+'Down.ro')
                vartree.Add('../tmvaFiles/'+directory+'/'+_varFileName)


                nEvents = tree.GetEntries()*1.

#                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
                if not verbose: print file+" "+syst+'Down'
            
                for event,var in itertools.izip(tree,vartree):
#                for event in tree:
                    evtCount += 1.
                    if evtCount/nEvents > percent and verbose:
                        k = int(percent*progSlots)
                        progress = file+" "+syst+'Down 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots

                    if quickRun and  evtCount > 200: break
 

                    _BDT                        = event.BDT                   
                    if useOverflow:
                        if _BDT < limitLow:
                            _BDT = limitLow + .001
                        if _BDT > limitHigh:
                            _BDT = limitHigh - .001
                
                    _weightA                    = event.weightA
                    _weightB                    = event.weightB
                    _weightC                    = event.weightC
                    _weightD                    = event.weightD
                    
                    _weight = 0

                    if RunA:
                        _weight = _weight + _weightA
                    if RunB:
                        _weight = _weight + _weightB
                    if RunC:
                        _weight = _weight + _weightC
                    if RunD:
                        _weight = _weight + _weightD

                    _met       = var.met

                    if _reg == '1j1t':
                        lepJetPt_PosLep               = var.lepJetPt_PosLep            
                        lepPt_PosLep                  = var.lepPt_PosLep               
                        lepJetDR_PosLep               = var.lepJetDR_PosLep            
                        lepJetDPhi_PosLep             = var.lepJetDPhi_PosLep          
                        lepJetDEta_PosLep             = var.lepJetDEta_PosLep          
                        lepJetM_PosLep                = var.lepJetM_PosLep             
                        lepPtRelJet_PosLep            = var.lepPtRelJet_PosLep         
                        jetPtRelLep_PosLep            = var.jetPtRelLep_PosLep         
                        lepPtRelJetSameLep_PosLep     = var.lepPtRelJetSameLep_PosLep  
                        lepPtRelJetOtherLep_PosLep    = var.lepPtRelJetOtherLep_PosLep 
                        lepJetMt_PosLep               = var.lepJetMt_PosLep            
                        lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep
                        lepJetPt_NegLep               = var.lepJetPt_NegLep            
                        lepPt_NegLep                  = var.lepPt_NegLep               
                        lepJetDR_NegLep               = var.lepJetDR_NegLep            
                        lepJetDPhi_NegLep             = var.lepJetDPhi_NegLep          
                        lepJetDEta_NegLep             = var.lepJetDEta_NegLep          
                        lepJetM_NegLep                = var.lepJetM_NegLep             
                        lepPtRelJet_NegLep            = var.lepPtRelJet_NegLep         
                        jetPtRelLep_NegLep            = var.jetPtRelLep_NegLep         
                        lepPtRelJetSameLep_NegLep     = var.lepPtRelJetSameLep_NegLep  
                        lepPtRelJetOtherLep_NegLep    = var.lepPtRelJetOtherLep_NegLep 
                        lepJetMt_NegLep               = var.lepJetMt_NegLep            
                        lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep
                
                        __lepJetPt[0]               = lepJetPt_PosLep          
                        __lepPt[0]                  = lepPt_PosLep             
                        __lepJetDR[0]               = lepJetDR_PosLep          
                        __lepJetDPhi[0]             = lepJetDPhi_PosLep        
                        __lepJetDEta[0]             = lepJetDEta_PosLep        
                        __lepJetM[0]                = lepJetM_PosLep           
                        __lepPtRelJet[0]            = lepPtRelJet_PosLep       
                        __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_PosLep
                        __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_PosLep
        
                        positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
            
                        __lepJetPt[0]               = lepJetPt_NegLep          
                        __lepPt[0]                  = lepPt_NegLep             
                        __lepJetDR[0]               = lepJetDR_NegLep          
                        __lepJetDPhi[0]             = lepJetDPhi_NegLep        
                        __lepJetDEta[0]             = lepJetDEta_NegLep        
                        __lepJetM[0]                = lepJetM_NegLep           
                        __lepPtRelJet[0]            = lepPtRelJet_NegLep       
                        __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_NegLep
                        __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_NegLep
                
                        negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")

                        if abs(positiveLepBDT - negativeLepBDT) < RmeasurementCut:
                            continue
                        
                        if pickTop and negativeLepBDT > positiveLepBDT:
                            continue
    
                        if not pickTop and positiveLepBDT > negativeLepBDT:
                            continue

                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF

                    HistoLists[chan][reg][fileHistoInput[fileNum]][1][s][1].Fill(_BDT, _weight)

                if verbose: print
                
            if "TWChannel" in file:
                SpecSysts = ['DS','Q2Up','Q2Down','TopMassUp','TopMassDown']
                histSpot = [-1,-2,-2,-3,-3]
                systUpDown = [0,0,1,0,1]
                
                if not useTopMass:
                    SpecSysts = ['DS','Q2Up','Q2Down']
                    histSpot = [-1,-2,-2]
                    systUpDown = [0,0,1]

                if 'Q2' in rmSysts:
                    SpecSysts = ['DS','TopMassUp','TopMassDown']
                    histSpot = [-1,-2,-2,]
                    systUpDown = [0,0,1]

                if 'DS' in rmSysts:
                    SpecSysts = ['Q2Up','Q2Down','TopMassUp','TopMassDown']
                    histSpot = [-1,-1,-2,-2]
                    systUpDown = [0,1,0,1]
                    

                tWName = file[:-5]
                print tWName
                tWnum = 0
                if 'TWChannel_Tbar' in file:
                    tWnum = 1
                for i in range(len(SpecSysts)):
                    syst = SpecSysts[i]
                    
                    tree = TChain(BDT + '_' + ChanName[chan] + '_' + _reg)
                    vartree = TChain(Folder[chan]+'/'+_reg)                    

                    file = tWName+'_'+syst+'.root'
                    fileName = tWName+'_'+syst+'_Output_'+ChanName[chan]+'_'+_reg+'.root'

#                    tree.Add('../tmvaFiles/'+directory+'/'+fileName)
                    tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                    vartree.Add('../tmvaFiles/'+directory+'/'+file)

                    nEvents = tree.GetEntries()*1.

                    #                print nEvents
            
                    evtCount = 0.
                    percent = 0.0
                    progSlots = 25.    

                    if not verbose: print file

            
                    for event,var in itertools.izip(tree,vartree):
#                    for event in tree:
                        evtCount += 1.
                        if evtCount/nEvents > percent and verbose:
                            k = int(percent*progSlots)
                            progress = file+" "+syst+' 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                            sys.stdout.write(progress)
                            sys.stdout.flush()
                            percent += 1./progSlots


                        if quickRun and  evtCount > 200: break
 
                        _BDT                        = event.BDT                   
                        if useOverflow:
                            if _BDT < limitLow:
                                _BDT = limitLow + .001
                            if _BDT > limitHigh:
                                _BDT = limitHigh - .001

                        _weightA                    = event.weightA
                        _weightB                    = event.weightB
                        _weightC                    = event.weightC
                        _weightD                    = event.weightD

                        _VweightA   = var.weightA
                        _VweightB   = var.weightB
                        _VweightC   = var.weightC
                        _VweightD   = var.weightD
                    
                        _weight = 0

                        if _weightA != _VweightA or _weightB != _VweightB or _weightC != _VweightC or _weightD != _VweightD:
                            print "BIG ISSUE"
                            sys.exit(1)


                        if RunA:
                            _weight = _weight + _weightA
                        if RunB:
                            _weight = _weight + _weightB
                        if RunC:
                            _weight = _weight + _weightC
                        if RunD:
                            _weight = _weight + _weightD


                        if _reg == '1j1t':
                            lepJetPt_PosLep               = var.lepJetPt_PosLep            
                            lepPt_PosLep                  = var.lepPt_PosLep               
                            lepJetDR_PosLep               = var.lepJetDR_PosLep            
                            lepJetDPhi_PosLep             = var.lepJetDPhi_PosLep          
                            lepJetDEta_PosLep             = var.lepJetDEta_PosLep          
                            lepJetM_PosLep                = var.lepJetM_PosLep             
                            lepPtRelJet_PosLep            = var.lepPtRelJet_PosLep         
                            jetPtRelLep_PosLep            = var.jetPtRelLep_PosLep         
                            lepPtRelJetSameLep_PosLep     = var.lepPtRelJetSameLep_PosLep  
                            lepPtRelJetOtherLep_PosLep    = var.lepPtRelJetOtherLep_PosLep 
                            lepJetMt_PosLep               = var.lepJetMt_PosLep            
                            lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep
                            lepJetPt_NegLep               = var.lepJetPt_NegLep            
                            lepPt_NegLep                  = var.lepPt_NegLep               
                            lepJetDR_NegLep               = var.lepJetDR_NegLep            
                            lepJetDPhi_NegLep             = var.lepJetDPhi_NegLep          
                            lepJetDEta_NegLep             = var.lepJetDEta_NegLep          
                            lepJetM_NegLep                = var.lepJetM_NegLep             
                            lepPtRelJet_NegLep            = var.lepPtRelJet_NegLep         
                            jetPtRelLep_NegLep            = var.jetPtRelLep_NegLep         
                            lepPtRelJetSameLep_NegLep     = var.lepPtRelJetSameLep_NegLep  
                            lepPtRelJetOtherLep_NegLep    = var.lepPtRelJetOtherLep_NegLep 
                            lepJetMt_NegLep               = var.lepJetMt_NegLep            
                            lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep
                    
                            __lepJetPt[0]               = lepJetPt_PosLep          
                            __lepPt[0]                  = lepPt_PosLep             
                            __lepJetDR[0]               = lepJetDR_PosLep          
                            __lepJetDPhi[0]             = lepJetDPhi_PosLep        
                            __lepJetDEta[0]             = lepJetDEta_PosLep        
                            __lepJetM[0]                = lepJetM_PosLep           
                            __lepPtRelJet[0]            = lepPtRelJet_PosLep       
                            __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_PosLep
                            __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_PosLep
            
                            positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                
                            __lepJetPt[0]               = lepJetPt_NegLep          
                            __lepPt[0]                  = lepPt_NegLep             
                            __lepJetDR[0]               = lepJetDR_NegLep          
                            __lepJetDPhi[0]             = lepJetDPhi_NegLep        
                            __lepJetDEta[0]             = lepJetDEta_NegLep        
                            __lepJetM[0]                = lepJetM_NegLep           
                            __lepPtRelJet[0]            = lepPtRelJet_NegLep       
                            __lepPtRelJetSameLep[0]     = lepPtRelJetSameLep_NegLep
                            __lepJetCosTheta_boosted[0] = lepJetCosTheta_boosted_NegLep
                    
                            negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")

                            if abs(positiveLepBDT - negativeLepBDT) < RmeasurementCut:
                                continue
                            
                            if pickTop and negativeLepBDT > positiveLepBDT:
                                continue
    
                            if not pickTop and positiveLepBDT > negativeLepBDT:
                                continue

                        # This should be the tW__DRDS__plus histogram (last syst of tw list)
                        HistoLists[chan][reg][fileNum][1][histSpot[i]][systUpDown[i]].Fill(_BDT, _weight)
                    if verbose:print


        for i in range(HistoLists[chan][reg][0][0].GetNbinsX()):
            if DS_symm:
                HistoLists[chan][reg][0][1][-1][1].SetBinContent(i+1, HistoLists[chan][reg][0][0].GetBinContent(i+1)*2.0 - HistoLists[chan][reg][0][1][-1][0].GetBinContent(i+1))
                HistoLists[chan][reg][1][1][-1][1].SetBinContent(i+1, HistoLists[chan][reg][1][0].GetBinContent(i+1)*2.0 - HistoLists[chan][reg][1][1][-1][0].GetBinContent(i+1))
            else:
                HistoLists[chan][reg][0][1][-1][1].SetBinContent(i+1,HistoLists[chan][reg][0][0].GetBinContent(i+1))
                HistoLists[chan][reg][1][1][-1][1].SetBinContent(i+1,HistoLists[chan][reg][1][0].GetBinContent(i+1))
        
#        HistoLists[chan][reg][0][1][-1][1] = HistoLists[chan][reg][0][0].Clone(ChanName[chan] + _reg + "__twdr__DRDS__minus")
                    
                
        print


# lepCharge = 'AntiTop'
# if pickTop:
#     lepCharge = 'Top'    

if RmeasurementCut < 0:
    RmeasurementCut = 0.0


#ExtraNames += "_Rcut_%.1f" % (RmeasurementCut)
ExtraNames += "_Rcut_" + str(RmeasurementCut)

if len(rmSysts) > 0:
    removedSysts = "_No"
    for s in rmSysts:
        removedSysts += s
    outFile = TFile('inputFiles/inputFileTheta_Rmeasurement_'+BDT+ExtraNames+removedSysts+'.root','RECREATE')
else:
    outFile = TFile('inputFiles/inputFileTheta_Rmeasurement_'+BDT+ExtraNames+'.root','RECREATE')


for chan in HistoLists:
    for reg in chan:
        for sample in reg:
            sample[0].Write()

for chan in HistoLists:
    for reg in chan:
        for sample in reg:
            if len(sample) > 1:
                for syst in sample[1]:
                    syst[0].Write()
                    syst[1].Write()


                    
