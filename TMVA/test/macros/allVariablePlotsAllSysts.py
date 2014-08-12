#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )

from ROOT import *

from array import *

import itertools

import os

from ZjetSF import *

RunA = False
RunB = False
RunC = False
RunD = False
runPicked = False

doProgBar = False
# BDT = 'Bagging2000TreesMET50'
# #BDT = 'AdaBoostDefault_NewTest'

plotInfo = [['ptjet',27,30,300, 'P_{T} leading jet [GeV]','Events / 10 GeV'],
            ['ht',53,70,600, 'H_{T} [GeV]','Events / 10 GeV'],
            ['msys',60,0,600, 'Mass-system [GeV]','Events / 10 GeV'],
            ['ptsys',50,0,200, 'P_{T} system [GeV]','Events / 4 GeV'],
            ['ptjll',30,0,300, 'P_{T}-jll [GeV]','Events / 10 GeV'],
            ['ptsys_ht',40,0,1, 'P_{T} system / H_{T}','Events'],
            ['htleps_ht',40,0,1, 'H_{T} leptons / H_{T}','Events'],
            ['NlooseJet20Central',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| < 2.4','Events'],
            ['NlooseJet20',10,0,10, 'Number of loose jets, P_{T} > 20','Events'],
            ['NbtaggedlooseJet20',4,0,4, 'Number of b-tagged loose jets, P_{T} > 20','Events'],
            ['met', 60, 0, 300,'MET [GeV]','Events / 5 GeV'],
            ['loosejetPt', 60, 0, 300, 'P_{T} of loose jet [GeV]','Events / 5 GeV'],
            ['centralityJLL',40,0,1,'Centrality - jll','Events'],
#             ['BDT',50,-1.01,1.01,'BDT Discriminant','Events'],
#             ['BDTBinned',5,-1.01,1.01,'BDT Discriminant','Events'],
#             ['BDTReBinned',5,0.0,1.0,'BDT Discriminant','Events'],

            ]

useDS = True
useZJetSF = True

useNNLOTTbar = False

directory = "ManyRegions_v4/"

i=0

ExtraNames = ""

doZpeakCuts = False

doMETcut = False


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
    elif '1BinCR' in arg:
        _1BinCR=True
    elif 'UnEvenBins' in arg:
        UnEvenBins = True
    elif '-n' in arg:
        i+=1
        ExtraNames+=sys.argv[i]
    elif '-metCut' in arg:
        doMETcut = True
        ExtraNames+='WithMETcut'
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

                   
regions = ['1j1t','2j1t','2j2t','1j0t','2j0t']
vFolder = ['ManyRegions_v2',
           'ManyRegions_v2',
           'ManyRegions_v2',
           'ManyRegions_v2',
           'ManyRegions_v2',
           ]



newBins = array('d',[-1.001,-0.995,-0.7,0.7,0.995,1.001])
                

HistoLists = list()
for chan in ChanName:
    chanList = list()

    HistoMode = list()
    for r in range(len(regions)):
#    for reg in regions:
        HistoRegion = list()
        reg = regions[r]
#         directory = vFolder[r]

        for i in range(len(fileList)):                        
            Histos = dict()

            fileName = fileList[i].split('.')[0]
            
            for plot in plotInfo:
                Histos[plot[0]] = list()
                Histos[plot[0]].append(TH1F(plot[0]+fileName+chan+reg," ",plot[1],plot[2],plot[3]))
                Histos[plot[0]][0].Sumw2()
#                 if plot[0] == 'BDTBinned':
#                     Histos['BDTBinned'][0] = TH1F('BDTBinned'+fileName+chan+reg," ",5,newBins)
#                     Histos['BDTBinned'][0].Sumw2()

                Histos[plot[0]].append(dict()) #list of systematics
                for syst in Systs + ['ZjetSF']:
                    upDown = list()
                    upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                    upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))
#                     if plot[0] == 'BDTBinned':
#                         upDown[0] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",5,newBins)
#                         upDown[1] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",5,newBins)

                    Histos[plot[0]][1][syst] = upDown

                if 'TWChannel' in fileName:
                    for syst in ExtraTWSysts+['DRDS']:
                        upDown = list()
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))
#                         if plot[0] == 'BDTBinned':
#                             upDown[0] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",5,newBins)
#                             upDown[1] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",5,newBins)

                        Histos[plot[0]][1][syst] = upDown

                if 'TTbar' in fileName:
                    for syst in ExtraTTbarSysts:
                        upDown = list()
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))
#                         if plot[0] == 'BDTBinned':
#                             upDown[0] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",5,newBins)
#                             upDown[1] = TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",5,newBins)

                        Histos[plot[0]][1][syst] = upDown
                        
            HistoRegion.append(Histos)

        HistoMode.append(HistoRegion)

    HistoLists.append(HistoMode)


########
# START GOING THROUGH SAMPLES
########

for chan in range(3):
    for reg in range(len(regions)):
        region = regions[reg]
        if '1j1tZpeak' in region:
            region = 'tree1j1tNomllMetCut'

        if 'Zpeak' in regions[reg]:
            doZpeakCuts = True
        else:
            doZpeakCuts = False            

        for fileNum in range(len(fileList)):
            
            file = fileList[fileNum]



            vartree = TChain(Folder[chan]+'/'+region)

            

            if file == 'DATA':
#                 tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012A_Output.root")
#                 tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012B_Output.root")
#                 tree.Add('../tmvaFiles/'+directory+'/'+BDT+'/Data_'+DataChannel[chan]+"_Run2012C_Output.root")
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012A.root')
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012B.root')
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012C.root')
                vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012D.root')
                
            else:
                print '../tmvaFiles/'+directory+'/'+file
                vartree.Add('../tmvaFiles/'+directory+'/'+file)
                

            nEvents = vartree.GetEntries()*1.

            print nEvents
            print ChanName[chan], regions[reg], file
            
            evtCount = 0.
            percent = 0.0
            progSlots = 25.    
            
#            for event,var in itertools.izip(tree,vartree):
            for var in vartree:
                evtCount += 1.
                if doProgBar:
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots


#                _BDT       = var.BDT
            
                _weightA   = var.weightA
                _weightB   = var.weightB
                _weightC   = var.weightC
                _weightD   = var.weightD


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
                _mll                 = var.mll                    
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




                _weightDown = _weight
                _weightUp = _weight

                if useZJetSF:
                    if "ZJets" in file:
                        _ZjetSF = ZjetSF(_met, chan)
                        _weight = _weight*_ZjetSF
                        _weightUp = 2.*_weight-_weightDown

                if doZpeakCuts:
                    if _mll < 81 or _mll > 101 or chan == 0:
                        continue

                if doMETcut:
                    if chan > 0 and _met < 50:
                        continue

                if "DATA" in file:
                    _weight = 1.


                if useZJetSF:
                    HistoLists[chan][reg][fileNum]['ptjet'][1]['ZjetSF'][0].Fill(              _ptjet              , _weightUp )
                    HistoLists[chan][reg][fileNum]['ht'][1]['ZjetSF'][0].Fill(                 _ht                 , _weightUp )
                    HistoLists[chan][reg][fileNum]['msys'][1]['ZjetSF'][0].Fill(               _msys               , _weightUp )
                    HistoLists[chan][reg][fileNum]['ptsys'][1]['ZjetSF'][0].Fill(              _ptsys              , _weightUp )
                    HistoLists[chan][reg][fileNum]['ptjll'][1]['ZjetSF'][0].Fill(              _ptjll              , _weightUp )
                    HistoLists[chan][reg][fileNum]['ptsys_ht'][1]['ZjetSF'][0].Fill(           _ptsys_ht           , _weightUp )
                    HistoLists[chan][reg][fileNum]['htleps_ht'][1]['ZjetSF'][0].Fill(          _htleps_ht          , _weightUp )
                    HistoLists[chan][reg][fileNum]['NlooseJet20Central'][1]['ZjetSF'][0].Fill( _NlooseJet20Central , _weightUp )
                    HistoLists[chan][reg][fileNum]['NlooseJet20'][1]['ZjetSF'][0].Fill(        _NlooseJet20        , _weightUp )
                    HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][1]['ZjetSF'][0].Fill( _NbtaggedlooseJet20 , _weightUp )
                    HistoLists[chan][reg][fileNum]['met'][1]['ZjetSF'][0].Fill(                _met                , _weightUp )
                    HistoLists[chan][reg][fileNum]['loosejetPt'][1]['ZjetSF'][0].Fill(         _loosejetPt         , _weightUp )
                    HistoLists[chan][reg][fileNum]['centralityJLL'][1]['ZjetSF'][0].Fill(      _centralityJLL      , _weightUp )
#                    HistoLists[chan][reg][fileNum]['BDT'][1]['ZjetSF'][0].Fill(                _BDT                , _weightUp )
#                    HistoLists[chan][reg][fileNum]['BDTBinned'][1]['ZjetSF'][0].Fill(         _BDT                , _weightUp )
#                     if _BDT < -0.995:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][0].Fill( 0.1  , _weightUp )
#                     elif _BDT < -0.7:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][0].Fill( 0.3  , _weightUp )
#                     elif _BDT < 0.7:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][0].Fill( 0.5   , _weightUp )
#                     elif _BDT < 0.995:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][0].Fill( 0.7   , _weightUp )
#                     elif _BDT < 1.01:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][0].Fill( 0.9   , _weightUp )

                    HistoLists[chan][reg][fileNum]['ptjet'][1]['ZjetSF'][1].Fill(              _ptjet              , _weightDown )
                    HistoLists[chan][reg][fileNum]['ht'][1]['ZjetSF'][1].Fill(                 _ht                 , _weightDown )
                    HistoLists[chan][reg][fileNum]['msys'][1]['ZjetSF'][1].Fill(               _msys               , _weightDown )
                    HistoLists[chan][reg][fileNum]['ptsys'][1]['ZjetSF'][1].Fill(              _ptsys              , _weightDown )
                    HistoLists[chan][reg][fileNum]['ptjll'][1]['ZjetSF'][1].Fill(              _ptjll              , _weightDown )
                    HistoLists[chan][reg][fileNum]['ptsys_ht'][1]['ZjetSF'][1].Fill(           _ptsys_ht           , _weightDown )
                    HistoLists[chan][reg][fileNum]['htleps_ht'][1]['ZjetSF'][1].Fill(          _htleps_ht          , _weightDown )
                    HistoLists[chan][reg][fileNum]['NlooseJet20Central'][1]['ZjetSF'][1].Fill( _NlooseJet20Central , _weightDown )
                    HistoLists[chan][reg][fileNum]['NlooseJet20'][1]['ZjetSF'][1].Fill(        _NlooseJet20        , _weightDown )
                    HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][1]['ZjetSF'][1].Fill( _NbtaggedlooseJet20 , _weightDown )
                    HistoLists[chan][reg][fileNum]['met'][1]['ZjetSF'][1].Fill(                _met                , _weightDown )
                    HistoLists[chan][reg][fileNum]['loosejetPt'][1]['ZjetSF'][1].Fill(         _loosejetPt         , _weightDown )
                    HistoLists[chan][reg][fileNum]['centralityJLL'][1]['ZjetSF'][1].Fill(      _centralityJLL      , _weightDown )
#                     HistoLists[chan][reg][fileNum]['BDT'][1]['ZjetSF'][1].Fill(                _BDT                , _weightDown )
#                     HistoLists[chan][reg][fileNum]['BDTBinned'][1]['ZjetSF'][1].Fill(         _BDT                , _weightDown )
#                     if _BDT < -0.995:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][1].Fill( 0.1  , _weightDown )
#                     elif _BDT < -0.7:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][1].Fill( 0.3  , _weightDown )
#                     elif _BDT < 0.7:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][1].Fill( 0.5   , _weightDown )
#                     elif _BDT < 0.995:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][1].Fill( 0.7   , _weightDown )
#                     elif _BDT < 1.01:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['ZjetSF'][1].Fill( 0.9   , _weightDown )
                    


                HistoLists[chan][reg][fileNum]['ptjet'][0].Fill(                    _ptjet                    , _weight )
                HistoLists[chan][reg][fileNum]['ht'][0].Fill(                       _ht                       , _weight )
                HistoLists[chan][reg][fileNum]['msys'][0].Fill(                     _msys                     , _weight )
                HistoLists[chan][reg][fileNum]['ptsys'][0].Fill(                    _ptsys                    , _weight )
                HistoLists[chan][reg][fileNum]['ptjll'][0].Fill(                    _ptjll                    , _weight )
                HistoLists[chan][reg][fileNum]['ptsys_ht'][0].Fill(                 _ptsys_ht                 , _weight )
                HistoLists[chan][reg][fileNum]['htleps_ht'][0].Fill(                _htleps_ht                , _weight )
                HistoLists[chan][reg][fileNum]['NlooseJet20Central'][0].Fill(       _NlooseJet20Central       , _weight )
                HistoLists[chan][reg][fileNum]['NlooseJet20'][0].Fill(              _NlooseJet20              , _weight )
                HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][0].Fill(       _NbtaggedlooseJet20       , _weight )
                HistoLists[chan][reg][fileNum]['met'][0].Fill(                      _met                      , _weight )
                HistoLists[chan][reg][fileNum]['loosejetPt'][0].Fill(               _loosejetPt               , _weight )
                HistoLists[chan][reg][fileNum]['centralityJLL'][0].Fill(            _centralityJLL            , _weight )
#                 HistoLists[chan][reg][fileNum]['BDT'][0].Fill(                      _BDT                      , _weight )
#                 HistoLists[chan][reg][fileNum]['BDTBinned'][0].Fill(               _BDT                      , _weight )
#                 if _BDT < -0.995:
#                     HistoLists[chan][reg][fileNum]['BDTReBinned'][0].Fill( 0.1  , _weight )
#                 elif _BDT < -0.7:
#                     HistoLists[chan][reg][fileNum]['BDTReBinned'][0].Fill( 0.3  , _weight )
#                 elif _BDT < 0.7:
#                     HistoLists[chan][reg][fileNum]['BDTReBinned'][0].Fill( 0.5   , _weight )
#                 elif _BDT < 0.995:
#                     HistoLists[chan][reg][fileNum]['BDTReBinned'][0].Fill( 0.7   , _weight )
#                 elif _BDT < 1.01:
#                     HistoLists[chan][reg][fileNum]['BDTReBinned'][0].Fill( 0.9   , _weight )


            SystList = Systs[:]
            if "TTbar" in file:
                SystList += ExtraTTbarSysts
            if "DATA" in file:
                SystList = []

            for s in range(len(SystList)):
                syst = SystList[s]

                vartree = TChain(Folder[chan]+'/'+region)

                systfile = file.replace('.ro','_'+syst+'Up.ro')

                vartree.Add('../tmvaFiles/'+directory+'/'+systfile)


                nEvents = vartree.GetEntries()*1.

                print nEvents
            
                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
#                for event,var in itertools.izip(tree,vartree):
                for var in vartree:
                    evtCount += 1.
                    if doProgBar:
                        if evtCount/nEvents > percent:
                            k = int(percent*progSlots)
                            progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                            sys.stdout.write(progress)
                            sys.stdout.flush()
                            percent += 1./progSlots
                            


#                    _BDT                        = var.BDT                   
            
                    _weightA                    = var.weightA
                    _weightB                    = var.weightB
                    _weightC                    = var.weightC
                    _weightD                    = var.weightD
                    
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


                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF

                    if useNNLOTTbar and "TTbar" in file:
                        _weight *= 245./234.

                    HistoLists[chan][reg][fileNum]['ptjet'][1][syst][0].Fill(              _ptjet              , _weight )
                    HistoLists[chan][reg][fileNum]['ht'][1][syst][0].Fill(                 _ht                 , _weight )
                    HistoLists[chan][reg][fileNum]['msys'][1][syst][0].Fill(               _msys               , _weight )
                    HistoLists[chan][reg][fileNum]['ptsys'][1][syst][0].Fill(              _ptsys              , _weight )
                    HistoLists[chan][reg][fileNum]['ptjll'][1][syst][0].Fill(              _ptjll              , _weight )
                    HistoLists[chan][reg][fileNum]['ptsys_ht'][1][syst][0].Fill(           _ptsys_ht           , _weight )
                    HistoLists[chan][reg][fileNum]['htleps_ht'][1][syst][0].Fill(          _htleps_ht          , _weight )
                    HistoLists[chan][reg][fileNum]['NlooseJet20Central'][1][syst][0].Fill( _NlooseJet20Central , _weight )
                    HistoLists[chan][reg][fileNum]['NlooseJet20'][1][syst][0].Fill(        _NlooseJet20        , _weight )
                    HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][1][syst][0].Fill( _NbtaggedlooseJet20 , _weight )
                    HistoLists[chan][reg][fileNum]['met'][1][syst][0].Fill(                _met                , _weight )
                    HistoLists[chan][reg][fileNum]['loosejetPt'][1][syst][0].Fill(         _loosejetPt         , _weight )
                    HistoLists[chan][reg][fileNum]['centralityJLL'][1][syst][0].Fill(      _centralityJLL      , _weight )
#                     HistoLists[chan][reg][fileNum]['BDT'][1][syst][0].Fill(                _BDT                , _weight )
#                     HistoLists[chan][reg][fileNum]['BDTBinned'][1][syst][0].Fill(         _BDT                , _weight )
#                     if _BDT < -0.995:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][0].Fill( 0.1  , _weight )
#                     elif _BDT < -0.7:                                
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][0].Fill( 0.3  , _weight )
#                     elif _BDT < 0.7:                                 
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][0].Fill( 0.5   , _weight )
#                     elif _BDT < 0.995:                               
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][0].Fill( 0.7   , _weight )
#                     elif _BDT < 1.01:                                
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][0].Fill( 0.9   , _weight )


                print

                vartree = TChain(Folder[chan]+'/'+region)

                systfile = file.replace('.ro','_'+syst+'Down.ro')

                vartree.Add('../tmvaFiles/'+directory+'/'+systfile)


                nEvents = vartree.GetEntries()*1.

                evtCount = 0.
                percent = 0.0
                progSlots = 25.    
            
#                for event,var in itertools.izip(tree,vartree):
                for var in vartree:
                    evtCount += 1.
                    if doProgBar:
                        if evtCount/nEvents > percent:
                            k = int(percent*progSlots)
                            progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                            sys.stdout.write(progress)
                            sys.stdout.flush()
                            percent += 1./progSlots



#                    _BDT                        = var.BDT                   
            
                    _weightA                    = var.weightA
                    _weightB                    = var.weightB
                    _weightC                    = var.weightC 
                    _weightD                    = var.weightD
                   
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

                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF

                    if useNNLOTTbar and "TTbar" in file:
                        _weight *= 245./234.

                    HistoLists[chan][reg][fileNum]['ptjet'][1][syst][1].Fill(              _ptjet              , _weight )
                    HistoLists[chan][reg][fileNum]['ht'][1][syst][1].Fill(                 _ht                 , _weight )
                    HistoLists[chan][reg][fileNum]['msys'][1][syst][1].Fill(               _msys               , _weight )
                    HistoLists[chan][reg][fileNum]['ptsys'][1][syst][1].Fill(              _ptsys              , _weight )
                    HistoLists[chan][reg][fileNum]['ptjll'][1][syst][1].Fill(              _ptjll              , _weight )
                    HistoLists[chan][reg][fileNum]['ptsys_ht'][1][syst][1].Fill(           _ptsys_ht           , _weight )
                    HistoLists[chan][reg][fileNum]['htleps_ht'][1][syst][1].Fill(          _htleps_ht          , _weight )
                    HistoLists[chan][reg][fileNum]['NlooseJet20Central'][1][syst][1].Fill( _NlooseJet20Central , _weight )
                    HistoLists[chan][reg][fileNum]['NlooseJet20'][1][syst][1].Fill(        _NlooseJet20        , _weight )
                    HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][1][syst][1].Fill( _NbtaggedlooseJet20 , _weight )
                    HistoLists[chan][reg][fileNum]['met'][1][syst][1].Fill(                _met                , _weight )
                    HistoLists[chan][reg][fileNum]['loosejetPt'][1][syst][1].Fill(         _loosejetPt         , _weight )
                    HistoLists[chan][reg][fileNum]['centralityJLL'][1][syst][1].Fill(      _centralityJLL      , _weight )
#                     HistoLists[chan][reg][fileNum]['BDT'][1][syst][1].Fill(                _BDT                , _weight )
#                     HistoLists[chan][reg][fileNum]['BDTBinned'][1][syst][1].Fill(         _BDT                , _weight )
#                     if _BDT < -0.995:
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][1].Fill( 0.1  , _weight )
#                     elif _BDT < -0.7:                                
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][1].Fill( 0.3  , _weight )
#                     elif _BDT < 0.7:                                 
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][1].Fill( 0.5   , _weight )
#                     elif _BDT < 0.995:                               
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][1].Fill( 0.7   , _weight )
#                     elif _BDT < 1.01:                                
#                         HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][1].Fill( 0.9   , _weight )


                print

                
            if "TWChannel" in file:
                SpecSysts = ['DS','Q2Up','Q2Down','TopMassUp','TopMassDown']
                systSpot = ['DRDS','Q2','Q2','TopMass','TopMass']
                systUpDown = [0,0,1,0,1]
                
                
                for i in range(len(SpecSysts)):
                    syst = SpecSysts[i]

                    vartree = TChain(Folder[chan]+'/'+region)

                    systfile = 'TWChannel_'+syst+'.root'

                    vartree.Add('../tmvaFiles/'+directory+'/'+systfile)

                    nEvents = vartree.GetEntries()*1.

                    evtCount = 0.
                    percent = 0.0
                    progSlots = 25.    
            
#                    for event,var in itertools.izip(tree,vartree):
                    for var in vartree:
                        evtCount += 1.
                        if doProgBar:
                            if evtCount/nEvents > percent:
                                k = int(percent*progSlots)
                                progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                                sys.stdout.write(progress)
                                sys.stdout.flush()
                                percent += 1./progSlots
                                


#                        _BDT                        = var.BDT                   
            
                        _weightA                    = var.weightA
                        _weightB                    = var.weightB
                        _weightC                    = var.weightC
                        _weightD                    = var.weightD
                    
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
                        
                        HistoLists[chan][reg][fileNum]['ptjet'][1][syst][systUpDown[i]].Fill(              _ptjet              , _weight )
                        HistoLists[chan][reg][fileNum]['ht'][1][syst][systUpDown[i]].Fill(                 _ht                 , _weight )
                        HistoLists[chan][reg][fileNum]['msys'][1][syst][systUpDown[i]].Fill(               _msys               , _weight )
                        HistoLists[chan][reg][fileNum]['ptsys'][1][syst][systUpDown[i]].Fill(              _ptsys              , _weight )
                        HistoLists[chan][reg][fileNum]['ptjll'][1][syst][systUpDown[i]].Fill(              _ptjll              , _weight )
                        HistoLists[chan][reg][fileNum]['ptsys_ht'][1][syst][systUpDown[i]].Fill(           _ptsys_ht           , _weight )
                        HistoLists[chan][reg][fileNum]['htleps_ht'][1][syst][systUpDown[i]].Fill(          _htleps_ht          , _weight )
                        HistoLists[chan][reg][fileNum]['NlooseJet20Central'][1][syst][systUpDown[i]].Fill( _NlooseJet20Central , _weight )
                        HistoLists[chan][reg][fileNum]['NlooseJet20'][1][syst][systUpDown[i]].Fill(        _NlooseJet20        , _weight )
                        HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][1][syst][systUpDown[i]].Fill( _NbtaggedlooseJet20 , _weight )
                        HistoLists[chan][reg][fileNum]['met'][1][syst][systUpDown[i]].Fill(                _met                , _weight )
                        HistoLists[chan][reg][fileNum]['loosejetPt'][1][syst][systUpDown[i]].Fill(         _loosejetPt         , _weight )
                        HistoLists[chan][reg][fileNum]['centralityJLL'][1][syst][systUpDown[i]].Fill(      _centralityJLL      , _weight )
#                         HistoLists[chan][reg][fileNum]['BDT'][1][syst][systUpDown[i]].Fill(                _BDT                , _weight )
#                         HistoLists[chan][reg][fileNum]['BDTBinned'][1][syst][systUpDown[i]].Fill(         _BDT                , _weight )
#                         if _BDT < -0.995:
#                             HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][systUpDown[i]].Fill( 0.1  , _weight )
#                         elif _BDT < -0.7:                                
#                             HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][systUpDown[i]].Fill( 0.3  , _weight )
#                         elif _BDT < 0.7:                                 
#                             HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][systUpDown[i]].Fill( 0.5   , _weight )
#                         elif _BDT < 0.995:                               
#                             HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][systUpDown[i]].Fill( 0.7   , _weight )
#                         elif _BDT < 1.01:                                
#                             HistoLists[chan][reg][fileNum]['BDTReBinned'][1][syst][systUpDown[i]].Fill( 0.9   , _weight )



                print

                HistoLists[chan][reg][fileNum]['ptjet'][1]['DRDS'][1]             = HistoLists[chan][reg][fileNum]['ptjet'][0].Clone()      
                HistoLists[chan][reg][fileNum]['ht'][1]['DRDS'][1]                = HistoLists[chan][reg][fileNum]['ht'][0].Clone()
                HistoLists[chan][reg][fileNum]['msys'][1]['DRDS'][1]              = HistoLists[chan][reg][fileNum]['msys'][0].Clone()
                HistoLists[chan][reg][fileNum]['ptsys'][1]['DRDS'][1]             = HistoLists[chan][reg][fileNum]['ptsys'][0].Clone()
                HistoLists[chan][reg][fileNum]['ptjll'][1]['DRDS'][1]             = HistoLists[chan][reg][fileNum]['ptjll'][0].Clone()  
                HistoLists[chan][reg][fileNum]['ptsys_ht'][1]['DRDS'][1]          = HistoLists[chan][reg][fileNum]['ptsys_ht'][0].Clone()
                HistoLists[chan][reg][fileNum]['htleps_ht'][1]['DRDS'][1]         = HistoLists[chan][reg][fileNum]['htleps_ht'][0].Clone()
                HistoLists[chan][reg][fileNum]['NlooseJet20Central'][1]['DRDS'][1]= HistoLists[chan][reg][fileNum]['NlooseJet20Central'][0].Clone()
                HistoLists[chan][reg][fileNum]['NlooseJet20'][1]['DRDS'][1]       = HistoLists[chan][reg][fileNum]['NlooseJet20'][0].Clone()
                HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][1]['DRDS'][1]= HistoLists[chan][reg][fileNum]['NbtaggedlooseJet20'][0].Clone()
                HistoLists[chan][reg][fileNum]['met'][1]['DRDS'][1]               = HistoLists[chan][reg][fileNum]['met'][0].Clone() 
                HistoLists[chan][reg][fileNum]['loosejetPt'][1]['DRDS'][1]        = HistoLists[chan][reg][fileNum]['loosejetPt'][0].Clone() 
                HistoLists[chan][reg][fileNum]['centralityJLL'][1]['DRDS'][1]     = HistoLists[chan][reg][fileNum]['centralityJLL'][0].Clone()
#                 HistoLists[chan][reg][fileNum]['BDT'][1]['DRDS'][1]               = HistoLists[chan][reg][fileNum]['BDT'][0].Clone()   
#                 HistoLists[chan][reg][fileNum]['BDTBinned'][1]['DRDS'][1]         = HistoLists[chan][reg][fileNum]['BDTBinned'][0].Clone() 
#                 HistoLists[chan][reg][fileNum]['BDTReBinned'][1]['DRDS'][1]       = HistoLists[chan][reg][fileNum]['BDTReBinned'][0].Clone() 
                    
        print




if not os.path.exists('HistogramFile'):
    command = 'mkdir HistogramFile'
    os.system(command)
if not os.path.exists('HistogramFile/'+ExtraNames):
    command = 'mkdir HistogramFile/'+ExtraNames
    os.system(command)

outFile = TFile('HistogramFile/'+ExtraNames+'/variablePlots'+runs+'.root','RECREATE')



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
                        

                    
