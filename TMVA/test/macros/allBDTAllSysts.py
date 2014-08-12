#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )

from ROOT import *

from array import *

import itertools

from ZjetSF import *

RunA = False
RunB = False
RunC = False
RunD = False
runPicked = False


#BDT = 'Bagging2000TreesMET50'
BDT = 'AdaBoostDefault_NewTests'

plotInfo = []

if 'AdaBoost' in BDT:
    plotInfo = [['BDT14',14,-0.4,0.3,'BDT Discriminant','Events'],
                ['BDT21',21,-0.4,0.3,'BDT Discriminant','Events'], 
                ['BDT28',28,-0.4,0.3,'BDT Discriminant','Events'],
                ['BDT35',35,-0.4,0.3,'BDT Discriminant','Events'],
                ]
    
if 'Bagging' in BDT:
    plotInfo = [['BDT',50,-1.01,1.01,'BDT Discriminant','Events'],
                ['BDTBinned',5,-1.01,1.01,'BDT Discriminant','Events'],
                ['BDTReBinned',5,0.0,1.0,'BDT Discriminant','Events'],
                ]


useDS = True
useZJetSF = True

useNNLOTTbar = False

useTopPtReweight = False

directory = "ManyRegions_v2"

i=0

ExtraNames = ""

while i < len(sys.argv):
    arg = sys.argv[i]
    if arg == '-b':
        i += 1
        continue
    elif 'thetaInputFileCreator' in arg:
        i += 1
        continue        
    elif '-d' in arg:
        i += 1
        directory = sys.argv[i]
    elif '-nBins' in arg:
        i += 1
        nBins = int(sys.argv[i])
    elif '-bdt' in arg:
        i += 1
        BDT = sys.argv[i]
    elif '-limit' in arg:
        i += 1
        limits = float(sys.argv[i])
    elif '-limitLow' in arg:
        i += 1
        limitLow = float(sys.argv[i])
    elif '-limitHigh' in arg:
        i += 1
        limitHigh = float(sys.argv[i])
    elif arg == 'A':
        RunA = True
        runPicked = True
    elif arg == 'B':
        RunB = True
        runPicked = True
    elif arg == 'C':
        RunC = True
        runPicked = True
    elif arg == 'D':
        RunD = True
        runPicked = True
    elif 'TopPtReweight' in arg:
        useTopPtReweight = True
        ExtraNames += "TopPtReweight"
    elif '1BinCR' in arg:
        _1BinCR=True
    elif 'UnEvenBins' in arg:
        UnEvenBins = True
    elif '-n' in arg:
        i+=1
        ExtraNames+=sys.argv[i]
    else:
        print "Unknown argument: " + arg
    i += 1
    



if not runPicked:
    RunA = True
    RunB = True
    RunC = True
    RunD = True

if RunA and RunB and RunC and RunD:
    runs=''
else:
    runs='_Run'
    if RunA:
        runs+='A'
    if RunB:
        runs+='B'
    if RunC:
        runs+='C'
    if RunD:
        runs+='D'


fileList = ['TWChannel.root',
            'TTbarNew.root',
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
                  3,
                  3,
                  2,
                  3,
                  3,
                  3,
                  3,
                  -1]

DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
Systs = ['JER','JES','UnclusteredMET','LES','PDF','BtagSF','PU']

ExtraTWSysts = ['TopMass','Q2']

ExtraTTbarSysts = ['TopMass', 'Q2','Matching']

                   
regions = ['1j1t','2j1t','2j2t']
regions = ['1j1t','2j1t','2j2t','1j0t','2j0t']

vFolder = {'1j1t':'ManyRegions_v2',
           '2j1t':'ManyRegions_v2',
           '2j2t':'ManyRegions_v2',
           '1j0t':'ManyRegions_v2',
           '2j0t':'ManyRegions_v2',
           }


newBins = array('d',[-1.001,-0.995,-0.7,0.7,0.995,1.001])
                

HistoLists = list()
for chan in ChanName:
    chanList = list()

    HistoMode = list()
    for reg in regions:
        HistoRegion = list()

        

        for i in range(len(fileList)):                        
            Histos = dict()

            fileName = fileList[i].split('.')[0]
            
            for plot in plotInfo:
                Histos[plot[0]] = list()
                Histos[plot[0]].append(TH1F(plot[0]+fileName+chan+reg," ",plot[1],plot[2],plot[3]))
                Histos[plot[0]][0].Sumw2()
                if plot[0] == 'BDTBinned':
                    Histos['BDTBinned'][0] = TH1F('BDTBinned'+fileName+chan+reg," ",5,newBins)
                    Histos['BDTBinned'][0].Sumw2()

                Histos[plot[0]].append(dict()) #list of systematics
                for syst in Systs + ['ZjetSF']:
                    upDown = list()
                    upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                    upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))
                    if plot[0] == 'BDTBinned':
                        upDown[0] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",5,newBins)
                        upDown[1] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",5,newBins)

                    Histos[plot[0]][1][syst] = upDown

                if 'TWChannel' in fileName:
                    for syst in ExtraTWSysts+['DRDS']:
                        upDown = list()
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))
                        if plot[0] == 'BDTBinned':
                            upDown[0] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",5,newBins)
                            upDown[1] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",5,newBins)

                        Histos[plot[0]][1][syst] = upDown

                if 'TTbar' in fileName:
                    for syst in ExtraTTbarSysts:
                        upDown = list()
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))
                        if plot[0] == 'BDTBinned':
                            upDown[0] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",5,newBins)
                            upDown[1] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",5,newBins)

                        Histos[plot[0]][1][syst] = upDown
                        
            HistoRegion.append(Histos)

        HistoMode.append(HistoRegion)

    HistoLists.append(HistoMode)


########
# START GOING THROUGH SAMPLES
########

for chan in range(3):
    for reg in range(len(regions)):
        for fileNum in range(len(fileList)):
            file = fileList[fileNum]

            vartree = TChain(Folder[chan]+'/'+regions[reg])
            tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])

            directory = vFolder[regions[reg]]

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
                evtCount += 1.
                if evtCount/nEvents > percent:
                    k = int(percent*progSlots)
                    progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                    sys.stdout.write(progress)
                    sys.stdout.flush()
                    percent += 1./progSlots


                _BDT       = event.BDT
            
                _weightA   = event.weightA
                _weightB   = event.weightB
                _weightC   = event.weightC
                _weightD   = event.weightD


                _weight = 0

                if RunA:
                    _weight = _weight + _weightA
                if RunB:
                    _weight = _weight + _weightB
                if RunC:
                    _weight = _weight + _weightC
                if RunD:
                    _weight = _weight + _weightD


                _ptjet               = var.ptjet                   
                _ht                  = var.ht                      
                _msys                = var.msys                    
                _mjll                = var.mjll                    
                _ptsys               = var.ptsys                   
                _ptjll               = var.ptjll                   
                _ptsys_ht            = var.ptsys_ht                
                _htleps_ht           = var.htleps_ht               
                _NlooseJet20Central  = var.NlooseJet20Central      
                _NlooseJet20         = var.NlooseJet20             
                _NbtaggedlooseJet20  = var.NbtaggedlooseJet20      
                _met                 = var.met                     
                _loosejetPt          = var.loosejetPt              
                _centralityJLL       = var.centralityJLL           



                if useNNLOTTbar and "TTbar" in file:
                    _weight *= 245./234.


                _weightDown = _weight
                _weightUp = _weight

                if useZJetSF:
                    if "ZJets" in file:
                        _ZjetSF = ZjetSF(_met, chan)
                        _weight = _weight*_ZjetSF
                        _weightUp = 2.*_weight-_weightDown


                if "DATA" in file:
                    _weight = 1.

                if 'TTbar' in file:
                    if useTopPtReweight:
                        _topPTSF =  var.weightTopPt - 1.
                        _weight = _weight*(1+_topPTSF)


                if useZJetSF:
                    HistoLists[chan][reg][fileNum]['BDT14'][1]['ZjetSF'][0].Fill(                _BDT                , _weightUp )
                    HistoLists[chan][reg][fileNum]['BDT21'][1]['ZjetSF'][0].Fill(                _BDT                , _weightUp )
                    HistoLists[chan][reg][fileNum]['BDT28'][1]['ZjetSF'][0].Fill(                _BDT                , _weightUp )
                    HistoLists[chan][reg][fileNum]['BDT35'][1]['ZjetSF'][0].Fill(                _BDT                , _weightUp )

                    HistoLists[chan][reg][fileNum]['BDT14'][1]['ZjetSF'][1].Fill(                _BDT                , _weightDown )
                    HistoLists[chan][reg][fileNum]['BDT21'][1]['ZjetSF'][1].Fill(                _BDT                , _weightDown )
                    HistoLists[chan][reg][fileNum]['BDT28'][1]['ZjetSF'][1].Fill(                _BDT                , _weightDown )
                    HistoLists[chan][reg][fileNum]['BDT35'][1]['ZjetSF'][1].Fill(                _BDT                , _weightDown )

                    

                HistoLists[chan][reg][fileNum]['BDT14'][0].Fill(                      _BDT                      , _weight )
                HistoLists[chan][reg][fileNum]['BDT21'][0].Fill(                      _BDT                      , _weight )
                HistoLists[chan][reg][fileNum]['BDT28'][0].Fill(                      _BDT                      , _weight )
                HistoLists[chan][reg][fileNum]['BDT35'][0].Fill(                      _BDT                      , _weight )


            SystList = Systs[:]
            if "TTbar" in file:
                SystList += ExtraTTbarSysts
            if "DATA" in file:
                SystList = []

            for s in range(len(SystList)):
                syst = SystList[s]

                vartree = TChain(Folder[chan]+'/'+regions[reg])
                tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])

                fileName = file.replace('.ro','_'+syst+'Up_Output.ro')
                systfile = file.replace('.ro','_'+syst+'Up.ro')

                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                vartree.Add('../tmvaFiles/'+directory+'/'+systfile)


                nEvents = tree.GetEntries()*1.

                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
                for event,var in itertools.izip(tree,vartree):
                    evtCount += 1.
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots



                    _BDT                        = event.BDT                   
            
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

                    _ptjet               = var.ptjet                   
                    _ht                  = var.ht                      
                    _msys                = var.msys                    
                    _mjll                = var.mjll                    
                    _ptsys               = var.ptsys                   
                    _ptjll               = var.ptjll                   
                    _ptsys_ht            = var.ptsys_ht                
                    _htleps_ht           = var.htleps_ht               
                    _NlooseJet20Central  = var.NlooseJet20Central      
                    _NlooseJet20         = var.NlooseJet20             
                    _NbtaggedlooseJet20  = var.NbtaggedlooseJet20      
                    _met                 = var.met                     
                    _loosejetPt          = var.loosejetPt              
                    _centralityJLL       = var.centralityJLL           

                    if 'TTbar' in file:
                        if useTopPtReweight:
                            _topPTSF =  var.weightTopPt - 1.
                            _weight = _weight*(1+_topPTSF)

                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF

                    if useNNLOTTbar and "TTbar" in file:
                        _weight *= 245./234.

                    HistoLists[chan][reg][fileNum]['BDT14'][1][syst][0].Fill(                _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['BDT21'][1][syst][0].Fill(                _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['BDT28'][1][syst][0].Fill(                _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['BDT35'][1][syst][0].Fill(                _BDT                , _weight )


                print

                vartree = TChain(Folder[chan]+'/'+regions[reg])
                tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])

                fileName = file.replace('.ro','_'+syst+'Down_Output.ro')
                systfile = file.replace('.ro','_'+syst+'Down.ro')

                tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                vartree.Add('../tmvaFiles/'+directory+'/'+systfile)


                nEvents = tree.GetEntries()*1.

                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
                for event,var in itertools.izip(tree,vartree):
                    evtCount += 1.
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots



                    _BDT                        = event.BDT                   
            
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

                    _ptjet               = var.ptjet                   
                    _ht                  = var.ht                      
                    _msys                = var.msys                    
                    _mjll                = var.mjll                    
                    _ptsys               = var.ptsys                   
                    _ptjll               = var.ptjll                   
                    _ptsys_ht            = var.ptsys_ht                
                    _htleps_ht           = var.htleps_ht               
                    _NlooseJet20Central  = var.NlooseJet20Central      
                    _NlooseJet20         = var.NlooseJet20             
                    _NbtaggedlooseJet20  = var.NbtaggedlooseJet20      
                    _met                 = var.met                     
                    _loosejetPt          = var.loosejetPt              
                    _centralityJLL       = var.centralityJLL           

                    if 'TTbar' in file:
                        if useTopPtReweight:
                            _topPTSF =  var.weightTopPt - 1.
                            _weight = _weight*(1+_topPTSF)
                            
                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF

                    if useNNLOTTbar and "TTbar" in file:
                        _weight *= 245./234.

                    HistoLists[chan][reg][fileNum]['BDT14'][1][syst][1].Fill(                _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['BDT21'][1][syst][1].Fill(                _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['BDT28'][1][syst][1].Fill(                _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['BDT35'][1][syst][1].Fill(                _BDT                , _weight )


                print

                
            if "TWChannel" in file:
                SpecSysts = ['DS','Q2Up','Q2Down','TopMassUp','TopMassDown']
                systSpot = ['DRDS','Q2','Q2','TopMass','TopMass']
                systUpDown = [0,0,1,0,1]
                
                
                for i in range(len(SpecSysts)):
                    syst = SpecSysts[i]

                    vartree = TChain(Folder[chan]+'/'+regions[reg])
                    tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])

                    fileName = 'TWChannel_'+syst+'_Output_'+ChanName[chan]+'_'+regions[reg]+'.root'
                    systfile = 'TWChannel_'+syst+'.root'

                    tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/'+fileName)
                    vartree.Add('../tmvaFiles/'+directory+'/'+systfile)

                    nEvents = tree.GetEntries()*1.

                    evtCount = 0.
                    percent = 0.0
                    progSlots = 25.    
            
                    for event,var in itertools.izip(tree,vartree):
                        evtCount += 1.
                        if evtCount/nEvents > percent:
                            k = int(percent*progSlots)
                            progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                            sys.stdout.write(progress)
                            sys.stdout.flush()
                            percent += 1./progSlots



                        _BDT                        = event.BDT                   
            
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


                        _ptjet               = var.ptjet                   
                        _ht                  = var.ht                      
                        _msys                = var.msys                    
                        _mjll                = var.mjll                    
                        _ptsys               = var.ptsys                   
                        _ptjll               = var.ptjll                   
                        _ptsys_ht            = var.ptsys_ht                
                        _htleps_ht           = var.htleps_ht               
                        _NlooseJet20Central  = var.NlooseJet20Central      
                        _NlooseJet20         = var.NlooseJet20             
                        _NbtaggedlooseJet20  = var.NbtaggedlooseJet20      
                        _met                 = var.met                     
                        _loosejetPt          = var.loosejetPt              
                        _centralityJLL       = var.centralityJLL           


                        syst = systSpot[i]
                        
                        HistoLists[chan][reg][fileNum]['BDT14'][1][syst][systUpDown[i]].Fill(                _BDT                , _weight )
                        HistoLists[chan][reg][fileNum]['BDT21'][1][syst][systUpDown[i]].Fill(                _BDT                , _weight )
                        HistoLists[chan][reg][fileNum]['BDT28'][1][syst][systUpDown[i]].Fill(                _BDT                , _weight )
                        HistoLists[chan][reg][fileNum]['BDT35'][1][syst][systUpDown[i]].Fill(                _BDT                , _weight )



                print

                HistoLists[chan][reg][fileNum]['BDT14'][1]['DRDS'][1]               = HistoLists[chan][reg][fileNum]['BDT14'][0].Clone()   
                HistoLists[chan][reg][fileNum]['BDT21'][1]['DRDS'][1]               = HistoLists[chan][reg][fileNum]['BDT21'][0].Clone()   
                HistoLists[chan][reg][fileNum]['BDT28'][1]['DRDS'][1]               = HistoLists[chan][reg][fileNum]['BDT28'][0].Clone()   
                HistoLists[chan][reg][fileNum]['BDT35'][1]['DRDS'][1]               = HistoLists[chan][reg][fileNum]['BDT35'][0].Clone()   
                    
        print



#outFile = TFile('HistogramFile/test.root','RECREATE')
outFile = TFile('HistogramFile/testAdaBoostBDT'+runs+'.root','RECREATE')

for chan in HistoLists:
    for reg in chan:
        for sample in reg:
            for plot in sample:
                sample[plot][0].Write()

for chan in HistoLists:
    for reg in chan:
        for sample in reg:
            for plot in sample:
                if len(sample[plot]) > 1:
                    for s in sample[plot][1]:
                        syst = sample[plot][1][s]
                        syst[0].Write()
                        syst[1].Write()
                        

                    
