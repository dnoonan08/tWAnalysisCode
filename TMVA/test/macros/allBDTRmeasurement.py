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
    plotInfo = [
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

directory = "ManyRegions_v4"

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
            'TWChannel_T.root',
            'TWChannel_Tbar.root',
            'TTbarNew.root',
            'TChannel.root',
            'SChannel.root',
            'ZJets.root',
            'WJets.root',
            'WW.root',
            'WZ.root',
            'ZZ.root',
            'TWDilepton_New.root',
            'DATA'
            ]


DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
Systs = ['JER','JES','UnclusteredMET','LES','PDF','BtagSF','PU']

ExtraTWSysts = ['TopMass','Q2']

ExtraTTbarSysts = ['TopMass', 'Q2','Matching']

                   
regions = ['1j1t','2j1t','2j2t']
regions = ['1j1t','2j1t','2j2t','1j0t','2j0t']
# regions = ['1j1t','1j0t']

vFolder = {'1j1t':'ManyRegions_v4',
           '2j1t':'ManyRegions_v4',
           '2j2t':'ManyRegions_v4',
           '1j0t':'ManyRegions_v4',
           '2j0t':'ManyRegions_v4',
           }


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


                __lepJetPt[0]               = var.lepJetPt_PosLep          
                __lepPt[0]                  = var.lepPt_PosLep             
                __lepJetDR[0]               = var.lepJetDR_PosLep          
                __lepJetDPhi[0]             = var.lepJetDPhi_PosLep        
                __lepJetDEta[0]             = var.lepJetDEta_PosLep        
                __lepJetM[0]                = var.lepJetM_PosLep           
                __lepPtRelJet[0]            = var.lepPtRelJet_PosLep       
                __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_PosLep
                __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_PosLep

                positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                
                __lepJetPt[0]               = var.lepJetPt_NegLep          
                __lepPt[0]                  = var.lepPt_NegLep             
                __lepJetDR[0]               = var.lepJetDR_NegLep          
                __lepJetDPhi[0]             = var.lepJetDPhi_NegLep        
                __lepJetDEta[0]             = var.lepJetDEta_NegLep        
                __lepJetM[0]                = var.lepJetM_NegLep           
                __lepPtRelJet[0]            = var.lepPtRelJet_NegLep       
                __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_NegLep
                __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_NegLep

                negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                if positiveLepBDT > negativeLepBDT:  lepPick = 'BDT35_plus' 
                if negativeLepBDT > positiveLepBDT: lepPick = 'BDT35_minus'

                maxBDT = positiveLepBDT
                minBDT = negativeLepBDT
                if negativeLepBDT > positiveLepBDT:
                    maxBDT = negativeLepBDT
                    minBDT = positiveLepBDT
                    

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
                    HistoLists[chan][reg][fileNum]['BDT35'][1]['ZjetSF'][0].Fill( _BDT   , _weightUp )
                    HistoLists[chan][reg][fileNum][lepPick][1]['ZjetSF'][0].Fill( _BDT   , _weightUp )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1]['ZjetSF'][0].Fill( positiveLepBDT   , _weightUp )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1]['ZjetSF'][0].Fill( negativeLepBDT   , _weightUp )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_max'][1]['ZjetSF'][0].Fill( maxBDT   , _weightUp )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_min'][1]['ZjetSF'][0].Fill( minBDT   , _weightUp )

                    HistoLists[chan][reg][fileNum]['BDT35'][1]['ZjetSF'][1].Fill( _BDT   , _weightDown )
                    HistoLists[chan][reg][fileNum][lepPick][1]['ZjetSF'][1].Fill( _BDT   , _weightDown )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1]['ZjetSF'][1].Fill( positiveLepBDT   , _weightDown )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1]['ZjetSF'][1].Fill( negativeLepBDT   , _weightDown )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_max'][1]['ZjetSF'][1].Fill( maxBDT   , _weightDown )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_min'][1]['ZjetSF'][1].Fill( minBDT   , _weightDown )

                    
                HistoLists[chan][reg][fileNum]['BDT35'][0].Fill(  _BDT      , _weight )
                HistoLists[chan][reg][fileNum][lepPick][0].Fill(  _BDT      , _weight )
                HistoLists[chan][reg][fileNum]['tWSepBDT'][0].Fill( positiveLepBDT   , _weight )
                HistoLists[chan][reg][fileNum]['tWSepBDT'][0].Fill( negativeLepBDT   , _weight )
                HistoLists[chan][reg][fileNum]['tWSepBDT_max'][0].Fill( maxBDT   , _weight )
                HistoLists[chan][reg][fileNum]['tWSepBDT_min'][0].Fill( minBDT   , _weight )


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

                    __lepJetPt[0]               = var.lepJetPt_PosLep          
                    __lepPt[0]                  = var.lepPt_PosLep             
                    __lepJetDR[0]               = var.lepJetDR_PosLep          
                    __lepJetDPhi[0]             = var.lepJetDPhi_PosLep        
                    __lepJetDEta[0]             = var.lepJetDEta_PosLep        
                    __lepJetM[0]                = var.lepJetM_PosLep           
                    __lepPtRelJet[0]            = var.lepPtRelJet_PosLep       
                    __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_PosLep
                    __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_PosLep
                    
                    positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                    
                    __lepJetPt[0]               = var.lepJetPt_NegLep          
                    __lepPt[0]                  = var.lepPt_NegLep             
                    __lepJetDR[0]               = var.lepJetDR_NegLep          
                    __lepJetDPhi[0]             = var.lepJetDPhi_NegLep        
                    __lepJetDEta[0]             = var.lepJetDEta_NegLep        
                    __lepJetM[0]                = var.lepJetM_NegLep           
                    __lepPtRelJet[0]            = var.lepPtRelJet_NegLep       
                    __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_NegLep
                    __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_NegLep
                    
                    negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                    
                    if positiveLepBDT > negativeLepBDT: lepPick = 'BDT35_plus'
                    if negativeLepBDT > positiveLepBDT: lepPick = 'BDT35_minus'

                    maxBDT = positiveLepBDT
                    minBDT = negativeLepBDT
                    if negativeLepBDT > positiveLepBDT:
                        maxBDT = negativeLepBDT
                        minBDT = positiveLepBDT

                    if 'TTbar' in file:
                        if useTopPtReweight:
                            _topPTSF =  var.weightTopPt - 1.
                            _weight = _weight*(1+_topPTSF)

                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF


                    HistoLists[chan][reg][fileNum]['BDT35'][1][syst][0].Fill( _BDT                , _weight )
                    HistoLists[chan][reg][fileNum][lepPick][1][syst][0].Fill( _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1][syst][0].Fill( positiveLepBDT   , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1][syst][0].Fill( negativeLepBDT   , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_max'][1][syst][0].Fill( maxBDT   , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_min'][1][syst][0].Fill( minBDT   , _weight )


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
                    
                    __lepJetPt[0]               = var.lepJetPt_PosLep          
                    __lepPt[0]                  = var.lepPt_PosLep             
                    __lepJetDR[0]               = var.lepJetDR_PosLep          
                    __lepJetDPhi[0]             = var.lepJetDPhi_PosLep        
                    __lepJetDEta[0]             = var.lepJetDEta_PosLep        
                    __lepJetM[0]                = var.lepJetM_PosLep           
                    __lepPtRelJet[0]            = var.lepPtRelJet_PosLep       
                    __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_PosLep
                    __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_PosLep
                    
                    positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                    
                    __lepJetPt[0]               = var.lepJetPt_NegLep          
                    __lepPt[0]                  = var.lepPt_NegLep             
                    __lepJetDR[0]               = var.lepJetDR_NegLep          
                    __lepJetDPhi[0]             = var.lepJetDPhi_NegLep        
                    __lepJetDEta[0]             = var.lepJetDEta_NegLep        
                    __lepJetM[0]                = var.lepJetM_NegLep           
                    __lepPtRelJet[0]            = var.lepPtRelJet_NegLep       
                    __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_NegLep
                    __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_NegLep
                    
                    negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                    
                    if positiveLepBDT > negativeLepBDT: lepPick = 'BDT35_plus'
                    if negativeLepBDT > positiveLepBDT: lepPick = 'BDT35_minus'

                    maxBDT = positiveLepBDT
                    minBDT = negativeLepBDT
                    if negativeLepBDT > positiveLepBDT:
                        maxBDT = negativeLepBDT
                        minBDT = positiveLepBDT

                    if 'TTbar' in file:
                        if useTopPtReweight:
                            _topPTSF =  var.weightTopPt - 1.
                            _weight = _weight*(1+_topPTSF)
                            
                    if useZJetSF:
                        if "ZJets" in file:
                            _ZjetSF = ZjetSF(_met, chan)
                            _weight = _weight*_ZjetSF


                    HistoLists[chan][reg][fileNum]['BDT35'][1][syst][1].Fill( _BDT                , _weight )
                    HistoLists[chan][reg][fileNum][lepPick][1][syst][1].Fill( _BDT                , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1][syst][1].Fill( positiveLepBDT   , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT'][1][syst][1].Fill( negativeLepBDT   , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_max'][1][syst][1].Fill( maxBDT   , _weight )
                    HistoLists[chan][reg][fileNum]['tWSepBDT_min'][1][syst][1].Fill( minBDT   , _weight )


                print

                
            if "TWChannel" in file:
                SpecSysts = ['DS','Q2Up','Q2Down','TopMassUp','TopMassDown']
                systSpot = ['DRDS','Q2','Q2','TopMass','TopMass']
                systUpDown = [0,0,1,0,1]
                
                tWName = file[:-5]
                
                for i in range(len(SpecSysts)):
                    syst = SpecSysts[i]

                    vartree = TChain(Folder[chan]+'/'+regions[reg])
                    tree = TChain(BDT + '_' + ChanName[chan] + '_' + regions[reg])

                    fileName = tWName+'_'+syst+'_Output_'+ChanName[chan]+'_'+regions[reg]+'.root'
                    systfile = tWName+'_'+syst+'.root'

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

                        __lepJetPt[0]               = var.lepJetPt_PosLep          
                        __lepPt[0]                  = var.lepPt_PosLep             
                        __lepJetDR[0]               = var.lepJetDR_PosLep          
                        __lepJetDPhi[0]             = var.lepJetDPhi_PosLep        
                        __lepJetDEta[0]             = var.lepJetDEta_PosLep        
                        __lepJetM[0]                = var.lepJetM_PosLep           
                        __lepPtRelJet[0]            = var.lepPtRelJet_PosLep       
                        __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_PosLep
                        __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_PosLep
                        
                        positiveLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                        
                        __lepJetPt[0]               = var.lepJetPt_NegLep          
                        __lepPt[0]                  = var.lepPt_NegLep             
                        __lepJetDR[0]               = var.lepJetDR_NegLep          
                        __lepJetDPhi[0]             = var.lepJetDPhi_NegLep        
                        __lepJetDEta[0]             = var.lepJetDEta_NegLep        
                        __lepJetM[0]                = var.lepJetM_NegLep           
                        __lepPtRelJet[0]            = var.lepPtRelJet_NegLep       
                        __lepPtRelJetSameLep[0]     = var.lepPtRelJetSameLep_NegLep
                        __lepJetCosTheta_boosted[0] = var.lepJetCosTheta_boosted_NegLep
                        
                        negativeLepBDT = reader_tW_tbarW.EvaluateMVA("BDT")
                        
                        if positiveLepBDT > negativeLepBDT: lepPick = 'BDT35_plus'
                        if negativeLepBDT > positiveLepBDT: lepPick = 'BDT35_minus'

                        maxBDT = positiveLepBDT
                        minBDT = negativeLepBDT
                        if negativeLepBDT > positiveLepBDT:
                            maxBDT = negativeLepBDT
                            minBDT = positiveLepBDT


                        syst = systSpot[i]
                        
                        HistoLists[chan][reg][fileNum]['BDT35'][1][syst][systUpDown[i]].Fill( _BDT                , _weight )
                        HistoLists[chan][reg][fileNum][lepPick][1][syst][systUpDown[i]].Fill( _BDT                , _weight )
                        HistoLists[chan][reg][fileNum]['tWSepBDT'][1][syst][systUpDown[i]].Fill( positiveLepBDT   , _weight )
                        HistoLists[chan][reg][fileNum]['tWSepBDT'][1][syst][systUpDown[i]].Fill( negativeLepBDT   , _weight )
                        HistoLists[chan][reg][fileNum]['tWSepBDT_max'][1][syst][systUpDown[i]].Fill( maxBDT   , _weight )
                        HistoLists[chan][reg][fileNum]['tWSepBDT_min'][1][syst][systUpDown[i]].Fill( minBDT   , _weight )



                print

                HistoLists[chan][reg][fileNum]['BDT35'][1]['DRDS'][1]       = HistoLists[chan][reg][fileNum]['BDT35'][0].Clone() 
                HistoLists[chan][reg][fileNum]['BDT35_plus'][1]['DRDS'][1]  = HistoLists[chan][reg][fileNum]['BDT35_plus'][0].Clone() 
                HistoLists[chan][reg][fileNum]['BDT35_minus'][1]['DRDS'][1] = HistoLists[chan][reg][fileNum]['BDT35_minus'][0].Clone()
                HistoLists[chan][reg][fileNum]['tWSepBDT'][1]['DRDS'][1]     = HistoLists[chan][reg][fileNum]['tWSepBDT'][0].Clone()
                HistoLists[chan][reg][fileNum]['tWSepBDT_max'][1]['DRDS'][1] = HistoLists[chan][reg][fileNum]['tWSepBDT_max'][0].Clone()
                HistoLists[chan][reg][fileNum]['tWSepBDT_min'][1]['DRDS'][1] = HistoLists[chan][reg][fileNum]['tWSepBDT_min'][0].Clone()

                    
            print



outFile = TFile('HistogramFile/'+BDT+'_BDTRmeasurement_v2_New'+runs+'.root','RECREATE')

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
                        

                    
