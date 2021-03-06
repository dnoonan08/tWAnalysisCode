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

doProgBar = True
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
            ['lepJetPt',40,0,300,'P_{T} jet & lepton','Events'],
            ['lepPt',40,0,300,'P_{T} lepton','Events'],
            ['lepJetDR',40,0,6,'#Delta R(jet,lepton)','Events'],
            ['lepJetDPhi',40,0,3.2,'#Delta #phi (jet,lepton)','Events'],
            ['lepJetDEta',40,0,5,'#Delta #eta (jet,lepton)','Events'],
            ['lepJetM',40,0,300,'Mass of jet & lepton','Events'],
            ['lepPtRelJet',40,0,200,'P_{T} lepton relative to jet','Events'],
            ['jetPtRelLep',40,0,200,'P_{T} jet relative to lepton','Events'],
            ['lepPtRelJetSameLep',40,0,200,'P_{T} lepton relative to jet & lep','Events'],
            ['lepPtRelJetOtherLep',40,0,200,'P_{T} lepton relative to jet & other lep','Events'],
            ['lepJetMt',40,0,300,'M_{T} jet & lepton','Events'],
            ['lepJetCosTheta_boosted',40,-1.,1.,'Cos #theta (lepton,jet)','Events'],
            ['BDT35',35,-0.4,0.3,'BDT Discriminant','Events'],
            ['BDT35_plus',35,-0.4,0.3,'BDT Discriminant','Events'],
            ['BDT35_minus',35,-0.4,0.3,'BDT Discriminant','Events'],
            ['tWSepBDT',50,-1.,1.,'BDT Discriminant','Events'],
            ['tWSepBDT_max',50,-1.,1.,'BDT Discriminant','Events'],
            ['tWSepBDT_min',50,-1.,1.,'BDT Discriminant','Events'],
            ]

useDS = True
useZJetSF = True

useTopPtReweight = False

directory = "ManyRegions_v3/"

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
    elif 'TopPtReweight' in arg:
        useTopPtReweight = True
        ExtraNames += "TopPtReweight"
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


reader_Main = TMVA.Reader( "!Color:!Silent" )

__ptjet               = array('f',[0])
__ptsys               = array('f',[0])
__ht                  = array('f',[0])
__NlooseJet20         = array('f',[0])
__NlooseJet20Central  = array('f',[0])
__NbtaggedlooseJet20  = array('f',[0])
__centralityJLL       = array('f',[0])
__loosejetPt          = array('f',[0])
__ptsys_ht            = array('f',[0])
__msys                = array('f',[0])
__htleps_ht           = array('f',[0])
__ptjll               = array('f',[0])
__met                 = array('f',[0])



reader_Main.AddVariable ("ptjet"              , __ptjet               )
reader_Main.AddVariable ("ptsys"              , __ptsys               )
reader_Main.AddVariable ("ht"                 , __ht                  )
reader_Main.AddVariable ("NlooseJet20"        , __NlooseJet20         )
reader_Main.AddVariable ("NlooseJet20Central" , __NlooseJet20Central  )
reader_Main.AddVariable ("NbtaggedlooseJet20" , __NbtaggedlooseJet20  )
reader_Main.AddVariable ("centralityJLL"      , __centralityJLL       )
reader_Main.AddVariable ("loosejetPt"         , __loosejetPt          )
reader_Main.AddVariable ("ptsys_ht"           , __ptsys_ht            )
reader_Main.AddVariable ("msys"               , __msys                )
reader_Main.AddVariable ("htleps_ht"          , __htleps_ht           )
reader_Main.AddVariable ("ptjll"              , __ptjll               )
reader_Main.AddVariable ("met"                , __met                 )

reader_Main.BookMVA("BDT", "../weights/test_tw_00_AdaBoostDefault_NewTests_2.weights.xml")




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

                Histos[plot[0]].append(dict()) #list of systematics
                for syst in Systs + ['ZjetSF']:
                    upDown = list()
                    upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                    upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))

                    Histos[plot[0]][1][syst] = upDown

                if 'TWChannel' in fileName:
                    for syst in ExtraTWSysts+['DRDS']:
                        upDown = list()
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))

                        Histos[plot[0]][1][syst] = upDown

                if 'TTbar' in fileName:
                    for syst in ExtraTTbarSysts:
                        upDown = list()
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Up'," ",plot[1],plot[2],plot[3]))
                        upDown.append(TH1F(plot[0]+fileName+chan+reg+'_'+syst+'Down'," ",plot[1],plot[2],plot[3]))

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
                if RunA: vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012A.root')
                if RunB: vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012B.root')
                if RunC: vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012C.root')
                if RunD: vartree.Add('../tmvaFiles/'+directory+'/Data_'+DataChannel[chan]+'_Run2012D.root')
                
            else:
                print '../tmvaFiles/'+directory+'/'+file
                vartree.Add('../tmvaFiles/'+directory+'/'+file)
                

            nEvents = vartree.GetEntries()*1.

            print nEvents
            print ChanName[chan], regions[reg], file
            
            evtCount = 0.
            percent = 0.0
            progSlots = 25.    
            
            for var in vartree:
                evtCount += 1.
                if doProgBar:
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots


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

                _lepJetPt_PosLep            = var.lepJetPt_PosLep           
                _lepPt_PosLep               = var.lepPt_PosLep              
                _lepJetDR_PosLep            = var.lepJetDR_PosLep           
                _lepJetDPhi_PosLep          = var.lepJetDPhi_PosLep         
                _lepJetDEta_PosLep          = var.lepJetDEta_PosLep         
                _lepJetM_PosLep             = var.lepJetM_PosLep            
                _lepPtRelJet_PosLep         = var.lepPtRelJet_PosLep        
                _jetPtRelLep_PosLep         = var.jetPtRelLep_PosLep        
                _lepPtRelJetSameLep_PosLep  = var.lepPtRelJetSameLep_PosLep 
                _lepPtRelJetOtherLep_PosLep = var.lepPtRelJetOtherLep_PosLep
                _lepJetMt_PosLep            = var.lepJetMt_PosLep           
                _lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep           
                _lepJetPt_NegLep            = var.lepJetPt_NegLep           
                _lepPt_NegLep               = var.lepPt_NegLep              
                _lepJetDR_NegLep            = var.lepJetDR_NegLep           
                _lepJetDPhi_NegLep          = var.lepJetDPhi_NegLep         
                _lepJetDEta_NegLep          = var.lepJetDEta_NegLep         
                _lepJetM_NegLep             = var.lepJetM_NegLep            
                _lepPtRelJet_NegLep         = var.lepPtRelJet_NegLep        
                _jetPtRelLep_NegLep         = var.jetPtRelLep_NegLep        
                _lepPtRelJetSameLep_NegLep  = var.lepPtRelJetSameLep_NegLep 
                _lepPtRelJetOtherLep_NegLep = var.lepPtRelJetOtherLep_NegLep
                _lepJetMt_NegLep            = var.lepJetMt_NegLep           
                _lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep           
                
            
                __lepJetPt[0]               = _lepJetPt_PosLep          
                __lepPt[0]                  = _lepPt_PosLep             
                __lepJetDR[0]               = _lepJetDR_PosLep          
                __lepJetDPhi[0]             = _lepJetDPhi_PosLep        
                __lepJetDEta[0]             = _lepJetDEta_PosLep        
                __lepJetM[0]                = _lepJetM_PosLep           
                __lepPtRelJet[0]            = _lepPtRelJet_PosLep       
                __lepPtRelJetSameLep[0]     = _lepPtRelJetSameLep_PosLep
                __lepJetCosTheta_boosted[0] = _lepJetCosTheta_boosted_PosLep
                
                positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                
                __lepJetPt[0]               = _lepJetPt_NegLep          
                __lepPt[0]                  = _lepPt_NegLep             
                __lepJetDR[0]               = _lepJetDR_NegLep          
                __lepJetDPhi[0]             = _lepJetDPhi_NegLep        
                __lepJetDEta[0]             = _lepJetDEta_NegLep        
                __lepJetM[0]                = _lepJetM_NegLep           
                __lepPtRelJet[0]            = _lepPtRelJet_NegLep       
                __lepPtRelJetSameLep[0]     = _lepPtRelJetSameLep_NegLep
                __lepJetCosTheta_boosted[0] = _lepJetCosTheta_boosted_NegLep
                
                negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")

                __ptjet[0]               = _ptjet               
                __ptsys[0]               = _ptsys               
                __ht[0]                  = _ht                  
                __NlooseJet20[0]         = _NlooseJet20         
                __NlooseJet20Central[0]  = _NlooseJet20Central  
                __NbtaggedlooseJet20[0]  = _NbtaggedlooseJet20  
                __centralityJLL[0]       = _centralityJLL       
                __loosejetPt[0]          = _loosejetPt          
                __ptsys_ht[0]            = _ptsys_ht            
                __msys[0]                = _msys                
                __htleps_ht[0]           = _htleps_ht           
                __ptjll[0]               = _ptjll               
                __met[0]                 = _met                 

                _BDT = reader_Main.EvaluateMVA("BDT")                

                _weightDown = _weight
                _weightUp = _weight

                if 'TTbar' in file:
                    if useTopPtReweight:
                        _topPTSF =  var.weightTopPt - 1.
                        _weight = _weight*(1+_topPTSF)

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

                    HistoLists[chan][reg][fileNum]['lepJetPt'][1]['ZjetSF'][0].Fill(            _lepJetPt_PosLep           , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPt'][1]['ZjetSF'][0].Fill(               _lepPt_PosLep              , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1]['ZjetSF'][0].Fill(            _lepJetDR_PosLep           , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1]['ZjetSF'][0].Fill(          _lepJetDPhi_PosLep         , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1]['ZjetSF'][0].Fill(          _lepJetDEta_PosLep         , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1]['ZjetSF'][0].Fill(             _lepJetM_PosLep            , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1]['ZjetSF'][0].Fill(         _lepPtRelJet_PosLep        , _weightUp )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1]['ZjetSF'][0].Fill(         _jetPtRelLep_PosLep        , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1]['ZjetSF'][0].Fill(  _lepPtRelJetSameLep_PosLep , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1]['ZjetSF'][0].Fill( _lepPtRelJetOtherLep_PosLep, _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1]['ZjetSF'][0].Fill(            _lepJetMt_PosLep           , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1]['ZjetSF'][0].Fill(            _lepJetCosTheta_boosted_PosLep           , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetPt'][1]['ZjetSF'][0].Fill(            _lepJetPt_NegLep           , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPt'][1]['ZjetSF'][0].Fill(               _lepPt_NegLep              , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1]['ZjetSF'][0].Fill(            _lepJetDR_NegLep           , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1]['ZjetSF'][0].Fill(          _lepJetDPhi_NegLep         , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1]['ZjetSF'][0].Fill(          _lepJetDEta_NegLep         , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1]['ZjetSF'][0].Fill(             _lepJetM_NegLep            , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1]['ZjetSF'][0].Fill(         _lepPtRelJet_NegLep        , _weightUp )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1]['ZjetSF'][0].Fill(         _jetPtRelLep_NegLep        , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1]['ZjetSF'][0].Fill(  _lepPtRelJetSameLep_NegLep , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1]['ZjetSF'][0].Fill( _lepPtRelJetOtherLep_NegLep, _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1]['ZjetSF'][0].Fill(            _lepJetMt_NegLep           , _weightUp )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1]['ZjetSF'][0].Fill(            _lepJetCosTheta_boosted_NegLep           , _weightUp )




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

                    HistoLists[chan][reg][fileNum]['lepJetPt'][1]['ZjetSF'][1].Fill(            _lepJetPt_PosLep           , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPt'][1]['ZjetSF'][1].Fill(               _lepPt_PosLep              , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1]['ZjetSF'][1].Fill(            _lepJetDR_PosLep           , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1]['ZjetSF'][1].Fill(          _lepJetDPhi_PosLep         , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1]['ZjetSF'][1].Fill(          _lepJetDEta_PosLep         , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1]['ZjetSF'][1].Fill(             _lepJetM_PosLep            , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1]['ZjetSF'][1].Fill(         _lepPtRelJet_PosLep        , _weightDown )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1]['ZjetSF'][1].Fill(         _jetPtRelLep_PosLep        , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1]['ZjetSF'][1].Fill(  _lepPtRelJetSameLep_PosLep , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1]['ZjetSF'][1].Fill( _lepPtRelJetOtherLep_PosLep, _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1]['ZjetSF'][1].Fill(            _lepJetMt_PosLep           , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1]['ZjetSF'][1].Fill(            _lepJetCosTheta_boosted_PosLep           , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetPt'][1]['ZjetSF'][1].Fill(            _lepJetPt_NegLep           , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPt'][1]['ZjetSF'][1].Fill(               _lepPt_NegLep              , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1]['ZjetSF'][1].Fill(            _lepJetDR_NegLep           , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1]['ZjetSF'][1].Fill(          _lepJetDPhi_NegLep         , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1]['ZjetSF'][1].Fill(          _lepJetDEta_NegLep         , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1]['ZjetSF'][1].Fill(             _lepJetM_NegLep            , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1]['ZjetSF'][1].Fill(         _lepPtRelJet_NegLep        , _weightDown )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1]['ZjetSF'][1].Fill(         _jetPtRelLep_NegLep        , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1]['ZjetSF'][1].Fill(  _lepPtRelJetSameLep_NegLep , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1]['ZjetSF'][1].Fill( _lepPtRelJetOtherLep_NegLep, _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1]['ZjetSF'][1].Fill(            _lepJetMt_NegLep           , _weightDown )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1]['ZjetSF'][1].Fill(            _lepJetCosTheta_boosted_PosLep           , _weightDown )


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

                HistoLists[chan][reg][fileNum]['lepJetPt'][0].Fill(            _lepJetPt_PosLep           , _weight )
                HistoLists[chan][reg][fileNum]['lepPt'][0].Fill(               _lepPt_PosLep              , _weight )
                HistoLists[chan][reg][fileNum]['lepJetDR'][0].Fill(            _lepJetDR_PosLep           , _weight )
                HistoLists[chan][reg][fileNum]['lepJetDPhi'][0].Fill(          _lepJetDPhi_PosLep         , _weight )
                HistoLists[chan][reg][fileNum]['lepJetDEta'][0].Fill(          _lepJetDEta_PosLep         , _weight )
                HistoLists[chan][reg][fileNum]['lepJetM'][0].Fill(             _lepJetM_PosLep            , _weight )
                HistoLists[chan][reg][fileNum]['lepPtRelJet'][0].Fill(         _lepPtRelJet_PosLep        , _weight )
                HistoLists[chan][reg][fileNum]['jetPtRelLep'][0].Fill(         _jetPtRelLep_PosLep        , _weight )
                HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][0].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
                HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][0].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
                HistoLists[chan][reg][fileNum]['lepJetMt'][0].Fill(            _lepJetMt_PosLep           , _weight )
                HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][0].Fill( _lepJetCosTheta_boosted_PosLep           , _weight )
                HistoLists[chan][reg][fileNum]['lepJetPt'][0].Fill(            _lepJetPt_NegLep           , _weight )
                HistoLists[chan][reg][fileNum]['lepPt'][0].Fill(               _lepPt_NegLep              , _weight )
                HistoLists[chan][reg][fileNum]['lepJetDR'][0].Fill(            _lepJetDR_NegLep           , _weight )
                HistoLists[chan][reg][fileNum]['lepJetDPhi'][0].Fill(          _lepJetDPhi_NegLep         , _weight )
                HistoLists[chan][reg][fileNum]['lepJetDEta'][0].Fill(          _lepJetDEta_NegLep         , _weight )
                HistoLists[chan][reg][fileNum]['lepJetM'][0].Fill(             _lepJetM_NegLep            , _weight )
                HistoLists[chan][reg][fileNum]['lepPtRelJet'][0].Fill(         _lepPtRelJet_NegLep        , _weight )
                HistoLists[chan][reg][fileNum]['jetPtRelLep'][0].Fill(         _jetPtRelLep_NegLep        , _weight )
                HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][0].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
                HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][0].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
                HistoLists[chan][reg][fileNum]['lepJetMt'][0].Fill(            _lepJetMt_NegLep           , _weight )
                HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][0].Fill( _lepJetCosTheta_boosted_NegLep           , _weight )


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

                    _lepJetPt_PosLep            = var.lepJetPt_PosLep           
                    _lepPt_PosLep               = var.lepPt_PosLep              
                    _lepJetDR_PosLep            = var.lepJetDR_PosLep           
                    _lepJetDPhi_PosLep          = var.lepJetDPhi_PosLep         
                    _lepJetDEta_PosLep          = var.lepJetDEta_PosLep         
                    _lepJetM_PosLep             = var.lepJetM_PosLep            
                    _lepPtRelJet_PosLep         = var.lepPtRelJet_PosLep        
                    _jetPtRelLep_PosLep         = var.jetPtRelLep_PosLep        
                    _lepPtRelJetSameLep_PosLep  = var.lepPtRelJetSameLep_PosLep 
                    _lepPtRelJetOtherLep_PosLep = var.lepPtRelJetOtherLep_PosLep
                    _lepJetMt_PosLep            = var.lepJetMt_PosLep           
                    _lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep           
                    _lepJetPt_NegLep            = var.lepJetPt_NegLep           
                    _lepPt_NegLep               = var.lepPt_NegLep              
                    _lepJetDR_NegLep            = var.lepJetDR_NegLep           
                    _lepJetDPhi_NegLep          = var.lepJetDPhi_NegLep         
                    _lepJetDEta_NegLep          = var.lepJetDEta_NegLep         
                    _lepJetM_NegLep             = var.lepJetM_NegLep            
                    _lepPtRelJet_NegLep         = var.lepPtRelJet_NegLep        
                    _jetPtRelLep_NegLep         = var.jetPtRelLep_NegLep        
                    _lepPtRelJetSameLep_NegLep  = var.lepPtRelJetSameLep_NegLep 
                    _lepPtRelJetOtherLep_NegLep = var.lepPtRelJetOtherLep_NegLep
                    _lepJetMt_NegLep            = var.lepJetMt_NegLep           
                    _lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep           
                    
                    if 'TTbar' in file:
                        if useTopPtReweight:
                            _topPTSF =  var.weightTopPt - 1.
                            _weight = _weight*(1+_topPTSF)
                            
                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF


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

                    HistoLists[chan][reg][fileNum]['lepJetPt'][1][syst][0].Fill(            _lepJetPt_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepPt'][1][syst][0].Fill(               _lepPt_PosLep              , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1][syst][0].Fill(            _lepJetDR_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1][syst][0].Fill(          _lepJetDPhi_PosLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1][syst][0].Fill(          _lepJetDEta_PosLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1][syst][0].Fill(             _lepJetM_PosLep            , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1][syst][0].Fill(         _lepPtRelJet_PosLep        , _weight )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1][syst][0].Fill(         _jetPtRelLep_PosLep        , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1][syst][0].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1][syst][0].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1][syst][0].Fill(            _lepJetMt_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1][syst][0].Fill( _lepJetCosTheta_boosted_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetPt'][1][syst][0].Fill(            _lepJetPt_NegLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepPt'][1][syst][0].Fill(               _lepPt_NegLep              , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1][syst][0].Fill(            _lepJetDR_NegLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1][syst][0].Fill(          _lepJetDPhi_NegLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1][syst][0].Fill(          _lepJetDEta_NegLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1][syst][0].Fill(             _lepJetM_NegLep            , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1][syst][0].Fill(         _lepPtRelJet_NegLep        , _weight )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1][syst][0].Fill(         _jetPtRelLep_NegLep        , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1][syst][0].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1][syst][0].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1][syst][0].Fill(            _lepJetMt_NegLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1][syst][0].Fill( _lepJetCosTheta_boosted_NegLep           , _weight )


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

                    _lepJetPt_PosLep            = var.lepJetPt_PosLep           
                    _lepPt_PosLep               = var.lepPt_PosLep              
                    _lepJetDR_PosLep            = var.lepJetDR_PosLep           
                    _lepJetDPhi_PosLep          = var.lepJetDPhi_PosLep         
                    _lepJetDEta_PosLep          = var.lepJetDEta_PosLep         
                    _lepJetM_PosLep             = var.lepJetM_PosLep            
                    _lepPtRelJet_PosLep         = var.lepPtRelJet_PosLep        
                    _jetPtRelLep_PosLep         = var.jetPtRelLep_PosLep        
                    _lepPtRelJetSameLep_PosLep  = var.lepPtRelJetSameLep_PosLep 
                    _lepPtRelJetOtherLep_PosLep = var.lepPtRelJetOtherLep_PosLep
                    _lepJetMt_PosLep            = var.lepJetMt_PosLep           
                    _lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep           
                    _lepJetPt_NegLep            = var.lepJetPt_NegLep           
                    _lepPt_NegLep               = var.lepPt_NegLep              
                    _lepJetDR_NegLep            = var.lepJetDR_NegLep           
                    _lepJetDPhi_NegLep          = var.lepJetDPhi_NegLep         
                    _lepJetDEta_NegLep          = var.lepJetDEta_NegLep         
                    _lepJetM_NegLep             = var.lepJetM_NegLep            
                    _lepPtRelJet_NegLep         = var.lepPtRelJet_NegLep        
                    _jetPtRelLep_NegLep         = var.jetPtRelLep_NegLep        
                    _lepPtRelJetSameLep_NegLep  = var.lepPtRelJetSameLep_NegLep 
                    _lepPtRelJetOtherLep_NegLep = var.lepPtRelJetOtherLep_NegLep
                    _lepJetMt_NegLep            = var.lepJetMt_NegLep           
                    _lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep           
                    
                    if 'TTbar' in file:
                        if useTopPtReweight:
                            _topPTSF =  var.weightTopPt - 1.
                            _weight = _weight*(1+_topPTSF)

                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF


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

                    HistoLists[chan][reg][fileNum]['lepJetPt'][1][syst][1].Fill(            _lepJetPt_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepPt'][1][syst][1].Fill(               _lepPt_PosLep              , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1][syst][1].Fill(            _lepJetDR_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1][syst][1].Fill(          _lepJetDPhi_PosLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1][syst][1].Fill(          _lepJetDEta_PosLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1][syst][1].Fill(             _lepJetM_PosLep            , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1][syst][1].Fill(         _lepPtRelJet_PosLep        , _weight )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1][syst][1].Fill(         _jetPtRelLep_PosLep        , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1][syst][1].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1][syst][1].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1][syst][1].Fill(            _lepJetMt_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1][syst][1].Fill( _lepJetCosTheta_boosted_PosLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetPt'][1][syst][1].Fill(            _lepJetPt_NegLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepPt'][1][syst][1].Fill(               _lepPt_NegLep              , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDR'][1][syst][1].Fill(            _lepJetDR_NegLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDPhi'][1][syst][1].Fill(          _lepJetDPhi_NegLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetDEta'][1][syst][1].Fill(          _lepJetDEta_NegLep         , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetM'][1][syst][1].Fill(             _lepJetM_NegLep            , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJet'][1][syst][1].Fill(         _lepPtRelJet_NegLep        , _weight )
                    HistoLists[chan][reg][fileNum]['jetPtRelLep'][1][syst][1].Fill(         _jetPtRelLep_NegLep        , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1][syst][1].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
                    HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1][syst][1].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
                    HistoLists[chan][reg][fileNum]['lepJetMt'][1][syst][1].Fill(            _lepJetMt_NegLep           , _weight )
                    HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1][syst][1].Fill( _lepJetCosTheta_boosted_NegLep           , _weight )


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
                        
                        _lepJetPt_PosLep            = var.lepJetPt_PosLep           
                        _lepPt_PosLep               = var.lepPt_PosLep              
                        _lepJetDR_PosLep            = var.lepJetDR_PosLep           
                        _lepJetDPhi_PosLep          = var.lepJetDPhi_PosLep         
                        _lepJetDEta_PosLep          = var.lepJetDEta_PosLep         
                        _lepJetM_PosLep             = var.lepJetM_PosLep            
                        _lepPtRelJet_PosLep         = var.lepPtRelJet_PosLep        
                        _jetPtRelLep_PosLep         = var.jetPtRelLep_PosLep        
                        _lepPtRelJetSameLep_PosLep  = var.lepPtRelJetSameLep_PosLep 
                        _lepPtRelJetOtherLep_PosLep = var.lepPtRelJetOtherLep_PosLep
                        _lepJetMt_PosLep            = var.lepJetMt_PosLep           
                        _lepJetCosTheta_boosted_PosLep = var.lepJetCosTheta_boosted_PosLep           
                        _lepJetPt_NegLep            = var.lepJetPt_NegLep           
                        _lepPt_NegLep               = var.lepPt_NegLep              
                        _lepJetDR_NegLep            = var.lepJetDR_NegLep           
                        _lepJetDPhi_NegLep          = var.lepJetDPhi_NegLep         
                        _lepJetDEta_NegLep          = var.lepJetDEta_NegLep         
                        _lepJetM_NegLep             = var.lepJetM_NegLep            
                        _lepPtRelJet_NegLep         = var.lepPtRelJet_NegLep        
                        _jetPtRelLep_NegLep         = var.jetPtRelLep_NegLep        
                        _lepPtRelJetSameLep_NegLep  = var.lepPtRelJetSameLep_NegLep 
                        _lepPtRelJetOtherLep_NegLep = var.lepPtRelJetOtherLep_NegLep
                        _lepJetMt_NegLep            = var.lepJetMt_NegLep           
                        _lepJetCosTheta_boosted_NegLep = var.lepJetCosTheta_boosted_NegLep           


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

                        HistoLists[chan][reg][fileNum]['lepJetPt'][1][syst][systUpDown[i]].Fill(            _lepJetPt_PosLep           , _weight )
                        HistoLists[chan][reg][fileNum]['lepPt'][1][syst][systUpDown[i]].Fill(               _lepPt_PosLep              , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetDR'][1][syst][systUpDown[i]].Fill(            _lepJetDR_PosLep           , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetDPhi'][1][syst][systUpDown[i]].Fill(          _lepJetDPhi_PosLep         , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetDEta'][1][syst][systUpDown[i]].Fill(          _lepJetDEta_PosLep         , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetM'][1][syst][systUpDown[i]].Fill(             _lepJetM_PosLep            , _weight )
                        HistoLists[chan][reg][fileNum]['lepPtRelJet'][1][syst][systUpDown[i]].Fill(         _lepPtRelJet_PosLep        , _weight )
                        HistoLists[chan][reg][fileNum]['jetPtRelLep'][1][syst][systUpDown[i]].Fill(         _jetPtRelLep_PosLep        , _weight )
                        HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1][syst][systUpDown[i]].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
                        HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1][syst][systUpDown[i]].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
                        HistoLists[chan][reg][fileNum]['lepJetMt'][1][syst][systUpDown[i]].Fill(            _lepJetMt_PosLep           , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1][syst][systUpDown[i]].Fill( _lepJetCosTheta_boosted_PosLep           , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetPt'][1][syst][systUpDown[i]].Fill(            _lepJetPt_NegLep           , _weight )
                        HistoLists[chan][reg][fileNum]['lepPt'][1][syst][systUpDown[i]].Fill(               _lepPt_NegLep              , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetDR'][1][syst][systUpDown[i]].Fill(            _lepJetDR_NegLep           , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetDPhi'][1][syst][systUpDown[i]].Fill(          _lepJetDPhi_NegLep         , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetDEta'][1][syst][systUpDown[i]].Fill(          _lepJetDEta_NegLep         , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetM'][1][syst][systUpDown[i]].Fill(             _lepJetM_NegLep            , _weight )
                        HistoLists[chan][reg][fileNum]['lepPtRelJet'][1][syst][systUpDown[i]].Fill(         _lepPtRelJet_NegLep        , _weight )
                        HistoLists[chan][reg][fileNum]['jetPtRelLep'][1][syst][systUpDown[i]].Fill(         _jetPtRelLep_NegLep        , _weight )
                        HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1][syst][systUpDown[i]].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
                        HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1][syst][systUpDown[i]].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
                        HistoLists[chan][reg][fileNum]['lepJetMt'][1][syst][systUpDown[i]].Fill(            _lepJetMt_NegLep           , _weight )
                        HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1][syst][systUpDown[i]].Fill( _lepJetCosTheta_boosted_NegLep           , _weight )



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

                HistoLists[chan][reg][fileNum]['lepJetPt'][1]['DRDS'][1]            = HistoLists[chan][reg][fileNum]['lepJetPt'][0].Clone()           
                HistoLists[chan][reg][fileNum]['lepPt'][1]['DRDS'][1]               = HistoLists[chan][reg][fileNum]['lepPt'][0].Clone()              
                HistoLists[chan][reg][fileNum]['lepJetDR'][1]['DRDS'][1]            = HistoLists[chan][reg][fileNum]['lepJetDR'][0].Clone()           
                HistoLists[chan][reg][fileNum]['lepJetDPhi'][1]['DRDS'][1]          = HistoLists[chan][reg][fileNum]['lepJetDPhi'][0].Clone()         
                HistoLists[chan][reg][fileNum]['lepJetDEta'][1]['DRDS'][1]          = HistoLists[chan][reg][fileNum]['lepJetDEta'][0].Clone()         
                HistoLists[chan][reg][fileNum]['lepJetM'][1]['DRDS'][1]             = HistoLists[chan][reg][fileNum]['lepJetM'][0].Clone()            
                HistoLists[chan][reg][fileNum]['lepPtRelJet'][1]['DRDS'][1]         = HistoLists[chan][reg][fileNum]['lepPtRelJet'][0].Clone()        
                HistoLists[chan][reg][fileNum]['jetPtRelLep'][1]['DRDS'][1]         = HistoLists[chan][reg][fileNum]['jetPtRelLep'][0].Clone()        
                HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][1]['DRDS'][1]  = HistoLists[chan][reg][fileNum]['lepPtRelJetSameLep'][0].Clone() 
                HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][1]['DRDS'][1] = HistoLists[chan][reg][fileNum]['lepPtRelJetOtherLep'][0].Clone() 
                HistoLists[chan][reg][fileNum]['lepJetMt'][1]['DRDS'][1]            = HistoLists[chan][reg][fileNum]['lepJetMt'][0].Clone()            
                HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][1]['DRDS'][1] = HistoLists[chan][reg][fileNum]['lepJetCosTheta_boosted'][0].Clone()            

                    
        print




if not os.path.exists('HistogramFile'):
    command = 'mkdir HistogramFile'
    os.system(command)
if not os.path.exists('HistogramFile/'+ExtraNames):
    command = 'mkdir HistogramFile/'+ExtraNames
    os.system(command)

outFile = TFile('HistogramFile/'+ExtraNames+'/FullVariablePlots'+runs+'.root','RECREATE')



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
                        

                    
