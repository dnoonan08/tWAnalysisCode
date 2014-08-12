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

from ttSpinSF import *

DS_symm = False

BDT = 'AdaBoostDefault_NewTests'

nBins = 50
limits = 1.001
#limitLow = -0.38
#limitHigh = 0.32
limitLow = -1.001
limitHigh = 1.001

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
    else:
        print "Unknown argument: " + arg

    i += 1    

print limitLow, limitHigh, nBins


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


fileList = ['TWChannel.root',
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
                  2,
                  2,
                  2,
                  2,
                  2,
                  2,
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
                   
regions = ['1j1t','2j1t','2j2t']

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
            tt = TH1F(chan+reg+ "__tt","",nBins,newBins)
            tt.Sumw2()
            other = TH1F(chan+reg+ "__other","",nBins,newBins)
            other.Sumw2()
            data = TH1F(chan+reg+ "__DATA","",nBins,newBins)

            twList = list()
            ttList = list()
            otherList = list()
            dataList = list()
            twsyst = list()
            ttsyst = list()
            othersyst = list()
        
            
            for syst in Systs:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,newBins)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,newBins)
                tempsystTW = [twsystUp,twsystDown]
                ttbarsystUp = TH1F(chan+reg+ "__tt__"+syst + "__plus","",nBins,newBins)
                ttbarsystDown = TH1F(chan+reg+ "__tt__"+syst + "__minus","",nBins,newBins)
                tempsystTT = [ttbarsystUp,ttbarsystDown]
                othersystUp = TH1F(chan+reg+ "__other__"+syst + "__plus","",nBins,newBins)
                othersystDown = TH1F(chan+reg+ "__other__"+syst + "__minus","",nBins,newBins)
                tempsystOTHER = [othersystUp,othersystDown]
                twsyst.append(tempsystTW)
                ttsyst.append(tempsystTT)
                othersyst.append(tempsystOTHER)

            for syst in ExtraTWSysts:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,newBins)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,newBins)
                tempsystTW = [twsystUp,twsystDown]
                twsyst.append(tempsystTW)

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

            #ADDING IN ZJET SF HISTOS BY HAND
            if useZJetSF:
                zjetSFUp = TH1F(chan+reg+ "__other__ZjetSF__plus","",nBins,newBins)
                zjetSFDown = TH1F(chan+reg+ "__other__ZjetSF__minus","",nBins,newBins)
                tempsystOther = [zjetSFUp,zjetSFDown]
                othersyst.append(tempsystOther)


        else:

            tw = TH1F(chan+reg+ "__twdr","",nBins,limitLow,limitHigh)
            tw.Sumw2()
            tt = TH1F(chan+reg+ "__tt","",nBins,limitLow,limitHigh)
            tt.Sumw2()
            other = TH1F(chan+reg+ "__other","",nBins,limitLow,limitHigh)
            other.Sumw2()
            data = TH1F(chan+reg+ "__DATA","",nBins,limitLow,limitHigh)

            twList = list()
            ttList = list()
            otherList = list()
            dataList = list()
            twsyst = list()
            ttsyst = list()
            othersyst = list()
        
            for syst in Systs:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,limitLow,limitHigh)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTW = [twsystUp,twsystDown]
                ttbarsystUp = TH1F(chan+reg+ "__tt__"+syst + "__plus","",nBins,limitLow,limitHigh)
                ttbarsystDown = TH1F(chan+reg+ "__tt__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTT = [ttbarsystUp,ttbarsystDown]
                othersystUp = TH1F(chan+reg+ "__other__"+syst + "__plus","",nBins,limitLow,limitHigh)
                othersystDown = TH1F(chan+reg+ "__other__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystOTHER = [othersystUp,othersystDown]
                twsyst.append(tempsystTW)
                ttsyst.append(tempsystTT)
                othersyst.append(tempsystOTHER)

            for syst in ExtraTWSysts:
                twsystUp = TH1F(chan+reg+ "__twdr__"+syst + "__plus","",nBins,limitLow,limitHigh)
                twsystDown = TH1F(chan+reg+ "__twdr__"+syst + "__minus","",nBins,limitLow,limitHigh)
                tempsystTW = [twsystUp,twsystDown]
                twsyst.append(tempsystTW)

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

            #ADDING IN ZJET SF HISTOS BY HAND
            if useZJetSF:
                zjetSFUp = TH1F(chan+reg+ "__other__ZjetSF__plus","",nBins,limitLow,limitHigh)
                zjetSFDown = TH1F(chan+reg+ "__other__ZjetSF__minus","",nBins,limitLow,limitHigh)
                tempsystOther = [zjetSFUp,zjetSFDown]
                othersyst.append(tempsystOther)



        twList.append(tw)
        twList.append(twsyst)
        ttList.append(tt)
        ttList.append(ttsyst)
        otherList.append(other)
        otherList.append(othersyst)
        dataList.append(data)
        regionList = list()
        regionList.append(twList)
        regionList.append(ttList)
        regionList.append(otherList)
        regionList.append(dataList)
        chanList.append(regionList)
    HistoLists.append(chanList)

for chan in range(3):
    for reg in range(3):
        for fileNum in range(len(fileList)):
            file = fileList[fileNum]

            vartree = TChain(Folder[chan]+'/'+regions[reg])
            tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])

#             if 'TTbar' in file:
#                 directory = 'TopPtReweighting'
#             else:
#                 directory = 'v11_MET50'

            if file == 'DATA':
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012A_Output.root")
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012B_Output.root")
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012C_Output.root")
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012D_Output.root")
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012A.root')
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012B.root')
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012C.root')
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012D.root')                
            else:                
                fileName = file.replace('.roo', '_Output.roo')
                print fileName
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                vartree.Add('../tmvaFiles/'+directory+'/'+file)
                

            nEvents = tree.GetEntries()*1.

            print nEvents
            print ChanName[chan], regions[reg], file
            
            evtCount = 0.
            percent = 0.0
            progSlots = 25.    
            
            for event,var in itertools.izip(tree,vartree):
#            for event in tree:
                evtCount += 1.
                if evtCount/nEvents > percent:
                    k = int(percent*progSlots)
                    progress = file+' 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                    sys.stdout.write(progress)
                    sys.stdout.flush()
                    percent += 1./progSlots



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
                    if fileHistoInput[fileNum]==2:
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
#                         spinSF = ttSpinSF(_NlooseJet20Central,_centralityJLL, _ptsys, regions[reg])-1.
#                         HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('SpinCorr')-len(ExtraTTbarSysts)][0].Fill(_BDT, _weight*(1.+spinSF))
#                         HistoLists[chan][reg][fileHistoInput[fileNum]][1][ExtraTTbarSysts.index('SpinCorr')-len(ExtraTTbarSysts)][1].Fill(_BDT, _weight*(1.-spinSF))
                    
                    
                

                if "DATA" in file:
                    _weight = 1.


                HistoLists[chan][reg][fileHistoInput[fileNum]][0].Fill(_BDT, _weight)
            print
#                HistoLists[chan][reg][-1][0].Fill(_BDT, _weight)


            SystList = Systs[:]
            if "TTbar" in file:
                SystList += ExtraTTbarSysts
                SystList.remove("TopPt")
                if "SpinCorr" in SystList: SystList.remove("SpinCorr")
            if "DATA" in file:
                SystList = []

            for s in range(len(SystList)):
                syst = SystList[s]
                tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])
                vartree = TChain(Folder[chan]+'/'+regions[reg])

                fileName = file.replace('.ro','_'+syst+'Up_Output.ro')

                _varFileName = file.replace('.ro','_'+syst+'Up.ro')

                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                vartree.Add('../tmvaFiles/'+directory+'/'+_varFileName)


                nEvents = tree.GetEntries()*1.

#                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
                for event,var in itertools.izip(tree,vartree):
#                for event in tree:
                    evtCount += 1.
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = file+" "+syst+'Up 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots



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

                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF


                    HistoLists[chan][reg][fileHistoInput[fileNum]][1][s][0].Fill(_BDT, _weight)

                print

                tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])
                vartree = TChain(Folder[chan]+'/'+regions[reg])
                fileName = file.replace('.ro','_'+syst+'Down_Output.ro')
                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)

                _varFileName = file.replace('.ro','_'+syst+'Down.ro')
                vartree.Add('../tmvaFiles/'+directory+'/'+_varFileName)


                nEvents = tree.GetEntries()*1.

#                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
                for event,var in itertools.izip(tree,vartree):
#                for event in tree:
                    evtCount += 1.
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = file+" "+syst+'Down 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots



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

                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF

                    HistoLists[chan][reg][fileHistoInput[fileNum]][1][s][1].Fill(_BDT, _weight)

                print
                
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
                    
                
                for i in range(len(SpecSysts)):
                    syst = SpecSysts[i]
                    
                    tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])
                    
                    fileName = 'TWChannel_'+syst+'_Output_'+ChanName[chan]+'_'+regions[reg]+'.root'

#                    tree.Add('../tmvaFiles/'+directory+'/'+fileName)
                    tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)

                    nEvents = tree.GetEntries()*1.

                    #                print nEvents
            
                    evtCount = 0.
                    percent = 0.0
                    progSlots = 25.    
            
                    for event in tree:
                        evtCount += 1.
                        if evtCount/nEvents > percent:
                            k = int(percent*progSlots)
                            progress = file+" "+syst+' 0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                            sys.stdout.write(progress)
                            sys.stdout.flush()
                            percent += 1./progSlots



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

                        # This should be the tW__DRDS__plus histogram (last syst of tw list)
                        HistoLists[chan][reg][0][1][histSpot[i]][systUpDown[i]].Fill(_BDT, _weight)
                    print


        for i in range(HistoLists[chan][reg][0][0].GetNbinsX()):
            if DS_symm:
                HistoLists[chan][reg][0][1][-1][1].SetBinContent(i+1, HistoLists[chan][reg][0][0].GetBinContent(i+1)*2.0 - HistoLists[chan][reg][0][1][-1][0].GetBinContent(i+1))
            else:
                HistoLists[chan][reg][0][1][-1][1].SetBinContent(i+1,HistoLists[chan][reg][0][0].GetBinContent(i+1))
        
#        HistoLists[chan][reg][0][1][-1][1] = HistoLists[chan][reg][0][0].Clone(ChanName[chan] + regions[reg] + "__twdr__DRDS__minus")
                    
                
        print


if len(rmSysts) > 0:
    removedSysts = "_No"
    for s in rmSysts:
        removedSysts += s
    outFile = TFile('inputFiles/inputFileTheta_'+BDT+ExtraNames+removedSysts+'.root','RECREATE')
else:
    outFile = TFile('inputFiles/inputFileTheta_'+BDT+ExtraNames+'.root','RECREATE')

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


                    
