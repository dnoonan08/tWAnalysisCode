#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array

import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

AllowedRegions = ['1j0t','1j1t','1jNoTagging','2j0t','2j1t','2j2t','2jNoTagging','3plusjNoTagging','1j1tZpeak','ZpeakLepSel']

region = '1j1t'
runPicked = False
RunA = False
RunB = False
RunC = False

TotalLumi = 0.

channelPicked = False
emuChan = False
mumuChan = False
eeChan = False
combinedChan = False

versionPicked = False

specialName = ''

noPlots = False

totals = list()
errors = list()
#for i in range(1,len(sys.argv)):
i = 1
while i < len(sys.argv):
    arg=sys.argv[i]
    if arg == '-b':
        i += 1
        continue
    elif 'plotVariables.p' in arg:
        i += 1
        continue
    elif arg in AllowedRegions:
        region = arg
    elif arg == 'A':
        RunA = True
        runPicked = True
    elif arg == 'B':
        RunB = True
        runPicked = True
    elif arg == 'C':
        RunC = True
        runPicked = True
    elif arg == 'emu':
        emuChan = True
        channelPicked = True
    elif arg == 'mumu':
        mumuChan = True
        channelPicked = True
    elif arg == 'ee':
        eeChan = True
        channelPicked = True        
    elif arg == '-v':
        i += 1
        versionPicked = True
        vFolder = sys.argv[i]
    elif arg == '-special':
        i+= 1
        specialName = sys.argv[i]        
        if not specialName[-1] == '/':
            specialName = specialName + '/'
    elif arg == 'noPlots':
        noPlots = True
    elif arg == 'help':
        print "------------------------"
        print "Help Menu"
        print "------------------------"
        print "Allowed arguments"
        print "   One of the following regions:"
        print "     ",AllowedRegions
        print "   'A' - use Run A"
        print "   'B' - use Run B"
        print "   'C' - use Run C"
        print "   'emu'  - do emu channel"
        print "   'mumu' - do mumu channel"
        print "   'ee'   - do ee channel"
        print "   '-v Folder' - specify the version folder inside tmvaFiles to be used"
        print "Default mode:"
        print " 1j1t region, using Runs A, B, & C, all three channels"
        exit()
    else:
        print "Unknown argument", arg," will be ignored"
    i += 1

        
if not runPicked:
    RunA = True
    RunB = True
    RunC = True
    RunD = True

if not channelPicked:
    emuChan = True
    mumuChan = True
    eeChan = True
    combinedChan = True

if not versionPicked:
    vFolder='v11_MET50'
    vFolder='v3_Rmeasurement'
    vFolder='ManyRegions_v2'
#     versionList = glob.glob("tmvaFiles/v*")
#     versionList.sort(key=lambda a:int(a.split('/v')[-1]))
#     vFolder = versionList[-1].split('/')[-1]    
#     print vFolder

if RunA:
    TotalLumi = TotalLumi + 876
if RunB:
    TotalLumi = TotalLumi + 4412.
if RunC:
    TotalLumi = TotalLumi + 7055.
if RunD:
    TotalLumi = TotalLumi + 7369.

runs = ''

if RunA and RunB and RunC and RunD:
    runs=''
else:
    runs='_'
    if RunA:
        runs+='A'
    if RunB:
        runs+='B'
    if RunC:
        runs+='C'
    if RunD:
        runs+='D'

TotalLumi = TotalLumi/1000.

labelcms = TPaveText(0.1,0.88,0.6,0.92,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.045);
labelcms.SetFillColor(kWhite);
labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
labelcms.SetBorderSize(0);



doChannel = [emuChan, mumuChan, eeChan, combinedChan]
    
plotInfo = [['ptjet',27,30,300, 'P_{T} leading jet [GeV]'],
            ['ht',60,0,600, 'H_{T} [GeV]'],
            ['msys',60,0,600, 'Mass-system [GeV]'],
            ['ptsys',50,0,200, 'P_{T} system [GeV]'],
            ['ptjll',30,0,300, 'P_{T}-jll [GeV]'],
            ['ptsys_ht',40,0,1, 'P_{T} system / H_{T}'],
            ['htleps_ht',40,0,1, 'H_{T} leptons / H_{T}'],
            ['NlooseJet20Central',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| < 2.4'],
            ['NlooseJet20Forward',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| > 2.4'],
            ['NlooseJet20',10,0,10, 'Number of loose jets, P_{T} > 20'],
            ['NlooseJet15Central',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| < 2.4'],
            ['NlooseJet15Forward',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| > 2.4'],
            ['NlooseJet15',10,0,10, 'Number of loose jets, P_{T} > 15'],
            ['NlooseJet25Central',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| < 2.4'],
            ['NlooseJet25Forward',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| > 2.4'],
            ['NlooseJet25',10,0,10, 'Number of loose jets, P_{T} > 25'],
            ['NbtaggedlooseJet15',4,0,4, 'Number of b-tagged loose jets, P_{T} > 15'],
            ['NbtaggedlooseJet20',4,0,4, 'Number of b-tagged loose jets, P_{T} > 20'],
            ['NbtaggedlooseJet25',4,0,4, 'Number of b-tagged loose jets, P_{T} > 25'],
            ['met', 60, 0, 300,'MET [GeV]'],
            ['loosejetPt', 60, 0, 300, 'P_{T} ofvloose jet [GeV]'],
            ['centralityJLL',40,0,1,'Centrality - jll']
            ]


fileList = ['TWChannel.root',
            'TTbar.root'
            ]

systList = ['BtagSF',
            'JER',
            'JES',
            'LES',
            'LepSF',
            'PDF',
            'PU',
            'Q2',
            'TopMass',            
            'UnclusteredMET']

# systList = ['Q2'
#             ]


DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee','3chan']
ChanLabels = [', e#mu channel',', #mu#mu channel',', ee channel', 'e#mu/#mu#mu/ee channels']
lumiLabel = "%.1f fb^{-1}" % TotalLumi

# DataRun = ['Run2012A','Run2012B','Run2012C']

HistoLists = list()

for mode in range(len(ChanName)):

    HistoMode = list()

    for i in range(len(fileList)):
        Histos = dict()

        fileName = fileList[i].split('.')[0]
        for plot in plotInfo:
            Histos[plot[0]] = list()
            Histos[plot[0]].append(TH1F(plot[0]+fileName+ChanName[mode]," ",plot[1],plot[2],plot[3]))
            Histos[plot[0]][0].SetLineColor(kBlack)
            Histos[plot[0]][0].SetLineWidth(2)
#            Histos[plot[0]][0].Sumw2()
            systematics = list()
            for s in systList:
                thisSyst = list()

                thisSyst.append(TH1F(plot[0]+fileName+ChanName[mode]+s+"Up"," ",plot[1],plot[2],plot[3]))
                thisSyst[0].SetLineColor(kBlue)
                thisSyst[0].SetLineWidth(2)
                thisSyst.append(TH1F(plot[0]+fileName+ChanName[mode]+s+"Down"," ",plot[1],plot[2],plot[3]))
                thisSyst[1].SetLineColor(kRed)
                thisSyst[1].SetLineWidth(2)

                systematics.append(thisSyst)

            if 'TWChannel' in fileName:
                thisSyst = list()

                thisSyst.append(TH1F(plot[0]+fileName+ChanName[mode]+"DRDSUp"," ",plot[1],plot[2],plot[3]))
                thisSyst[0].SetLineColor(kBlue)
                thisSyst[0].SetLineWidth(2)
                thisSyst.append(TH1F(plot[0]+fileName+ChanName[mode]+"DRDSDown"," ",plot[1],plot[2],plot[3]))
                thisSyst[1].SetLineColor(kRed)
                thisSyst[1].SetLineWidth(2)
                
                systematics.append(thisSyst)

            if 'TTbar' in fileName:
                thisSyst = list()

                thisSyst.append(TH1F(plot[0]+fileName+ChanName[mode]+"MatchingUp"," ",plot[1],plot[2],plot[3]))
                thisSyst[0].SetLineColor(kBlue)
                thisSyst[0].SetLineWidth(2)
                thisSyst.append(TH1F(plot[0]+fileName+ChanName[mode]+"MatchingDown"," ",plot[1],plot[2],plot[3]))
                thisSyst[1].SetLineColor(kRed)
                thisSyst[1].SetLineWidth(2)
                
                systematics.append(thisSyst)

            

            Histos[plot[0]].append(systematics)

        HistoMode.append(Histos)

    HistoLists.append(HistoMode)


systList.append('')
for mode in range(3):

    if not doChannel[mode]:
        continue

    for i in range(len(fileList)):

        print fileList[i]

        tree = TChain(Folder[mode]+'/'+region)

        tree.Add('tmvaFiles/'+vFolder+'/'+fileList[i])

        nEvents = tree.GetEntries()*1.

#        print nEvents

        evtCount = 0.
        percent = 0.0
        progSlots = 25.    

        for event in tree:
            evtCount += 1.
            if evtCount/nEvents > percent:
                k = int(percent*progSlots)
                progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                sys.stdout.write(progress)
                sys.stdout.flush()
                percent += 1./progSlots



            _ptjet                     = event.ptjet                   
            _ht                        = event.ht                      
            _msys                      = event.msys                    
            _ptsys                     = event.ptsys                   
            _ptjll                     = event.ptjll                   
            _ptsys_ht                  = event.ptsys_ht                
            _htleps_ht                 = event.htleps_ht               
            _NlooseJet15Central        = event.NlooseJet15Central      
            _NlooseJet15Forward        = event.NlooseJet15Forward      
            _NlooseJet15               = event.NlooseJet15             
            _NbtaggedlooseJet15        = event.NbtaggedlooseJet15      
            _NlooseJet20Central        = event.NlooseJet20Central      
            _NlooseJet20Forward        = event.NlooseJet20Forward      
            _NlooseJet20               = event.NlooseJet20             
            _NbtaggedlooseJet20        = event.NbtaggedlooseJet20      
            _NlooseJet25Central        = event.NlooseJet25Central      
            _NlooseJet25Forward        = event.NlooseJet25Forward      
            _NlooseJet25               = event.NlooseJet25             
            _NbtaggedlooseJet25        = event.NbtaggedlooseJet25      
            _met                       = event.met                     
            _loosejetPt                = event.loosejetPt              
            _centralityJLL             = event.centralityJLL           
            
            _weightA                    = event.weightA
            _weightB                    = event.weightB
            _weightC                    = event.weightC
            _weightD                    = event.weightD

            _weight = 0            


            _btagSF = 1.

#             if int(vFolder.split('v')[-1]) == 2:
#                 _btagSF = event.weightBtagSF
            
                

            if RunA:
                _weight = _weight + _weightA
            if RunB:
                _weight = _weight + _weightB
            if RunC:
                _weight = _weight + _weightC
            if RunD:
                _weight = _weight + _weightD

            _weight = _weight*_btagSF            


            #EXTRA CUTS


            HistoLists[mode][i]['ptjet'][0].Fill(                    _ptjet                    , _weight )
            HistoLists[mode][i]['ht'][0].Fill(                       _ht                       , _weight )
            HistoLists[mode][i]['msys'][0].Fill(                     _msys                     , _weight )
            HistoLists[mode][i]['ptsys'][0].Fill(                    _ptsys                    , _weight )
            HistoLists[mode][i]['ptjll'][0].Fill(                    _ptjll                    , _weight )
            HistoLists[mode][i]['ptsys_ht'][0].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[mode][i]['htleps_ht'][0].Fill(                _htleps_ht                , _weight )
            HistoLists[mode][i]['NlooseJet15Central'][0].Fill(       _NlooseJet15Central       , _weight )
            HistoLists[mode][i]['NlooseJet15Forward'][0].Fill(       _NlooseJet15Forward       , _weight )
            HistoLists[mode][i]['NlooseJet15'][0].Fill(              _NlooseJet15              , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet15'][0].Fill(       _NbtaggedlooseJet15       , _weight )
            HistoLists[mode][i]['NlooseJet20Central'][0].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[mode][i]['NlooseJet20Forward'][0].Fill(       _NlooseJet20Forward       , _weight )
            HistoLists[mode][i]['NlooseJet20'][0].Fill(              _NlooseJet20              , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet20'][0].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[mode][i]['NlooseJet25Central'][0].Fill(       _NlooseJet25Central       , _weight )
            HistoLists[mode][i]['NlooseJet25Forward'][0].Fill(       _NlooseJet25Forward       , _weight )
            HistoLists[mode][i]['NlooseJet25'][0].Fill(              _NlooseJet25              , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet25'][0].Fill(       _NbtaggedlooseJet25       , _weight )
            HistoLists[mode][i]['met'][0].Fill(                      _met                      , _weight )
            HistoLists[mode][i]['loosejetPt'][0].Fill(               _loosejetPt               , _weight )
            HistoLists[mode][i]['centralityJLL'][0].Fill(            _centralityJLL            , _weight )


            HistoLists[-1][i]['ptjet'][0].Fill(                    _ptjet                    , _weight )
            HistoLists[-1][i]['ht'][0].Fill(                       _ht                       , _weight )
            HistoLists[-1][i]['msys'][0].Fill(                     _msys                     , _weight )
            HistoLists[-1][i]['ptsys'][0].Fill(                    _ptsys                    , _weight )
            HistoLists[-1][i]['ptjll'][0].Fill(                    _ptjll                    , _weight )
            HistoLists[-1][i]['ptsys_ht'][0].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[-1][i]['htleps_ht'][0].Fill(                _htleps_ht                , _weight )
            HistoLists[-1][i]['NlooseJet15Central'][0].Fill(       _NlooseJet15Central       , _weight )
            HistoLists[-1][i]['NlooseJet15Forward'][0].Fill(       _NlooseJet15Forward       , _weight )
            HistoLists[-1][i]['NlooseJet15'][0].Fill(              _NlooseJet15              , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet15'][0].Fill(       _NbtaggedlooseJet15       , _weight )
            HistoLists[-1][i]['NlooseJet20Central'][0].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[-1][i]['NlooseJet20Forward'][0].Fill(       _NlooseJet20Forward       , _weight )
            HistoLists[-1][i]['NlooseJet20'][0].Fill(              _NlooseJet20              , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet20'][0].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[-1][i]['NlooseJet25Central'][0].Fill(       _NlooseJet25Central       , _weight )
            HistoLists[-1][i]['NlooseJet25Forward'][0].Fill(       _NlooseJet25Forward       , _weight )
            HistoLists[-1][i]['NlooseJet25'][0].Fill(              _NlooseJet25              , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet25'][0].Fill(       _NbtaggedlooseJet25       , _weight )
            HistoLists[-1][i]['met'][0].Fill(                      _met                      , _weight )
            HistoLists[-1][i]['loosejetPt'][0].Fill(               _loosejetPt               , _weight )
            HistoLists[-1][i]['centralityJLL'][0].Fill(            _centralityJLL            , _weight )

        print

        if 'TWChannel' in fileList[i]:
            systList[-1] = 'DRDS'
        if 'TTbar' in fileList[i]:
            systList[-1] = 'Matching'

        for s in range(len(systList)):
            tree = TChain(Folder[mode]+'/'+region)

            fName = 'tmvaFiles/'+vFolder+'/'+fileList[i]
            print fName.replace('.root','_'+systList[s]+'Up.root')
            tree.Add(fName.replace('.root','_'+systList[s]+'Up.root'))

            nEvents = tree.GetEntries()*1.

#            print nEvents

            evtCount = 0.
            percent = 0.0
            progSlots = 25.    
            
            for event in tree:
                evtCount += 1.
                if evtCount/nEvents > percent:
                    k = int(percent*progSlots)
                    progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                    sys.stdout.write(progress)
                    sys.stdout.flush()
                    percent += 1./progSlots
                    


                _ptjet                     = event.ptjet                   
                _ht                        = event.ht                      
                _msys                      = event.msys                    
                _ptsys                     = event.ptsys                   
                _ptjll                     = event.ptjll                   
                _ptsys_ht                  = event.ptsys_ht                
                _htleps_ht                 = event.htleps_ht               
                _NlooseJet15Central        = event.NlooseJet15Central      
                _NlooseJet15Forward        = event.NlooseJet15Forward      
                _NlooseJet15               = event.NlooseJet15             
                _NbtaggedlooseJet15        = event.NbtaggedlooseJet15      
                _NlooseJet20Central        = event.NlooseJet20Central      
                _NlooseJet20Forward        = event.NlooseJet20Forward      
                _NlooseJet20               = event.NlooseJet20             
                _NbtaggedlooseJet20        = event.NbtaggedlooseJet20      
                _NlooseJet25Central        = event.NlooseJet25Central      
                _NlooseJet25Forward        = event.NlooseJet25Forward      
                _NlooseJet25               = event.NlooseJet25             
                _NbtaggedlooseJet25        = event.NbtaggedlooseJet25      
                _met                       = event.met                     
                _loosejetPt                = event.loosejetPt              
                _centralityJLL             = event.centralityJLL           
                
                _weightA                    = event.weightA
                _weightB                    = event.weightB
                _weightC                    = event.weightC
                _weightD                    = event.weightD
                
                _weight = 0            
                
                
                _btagSF = 1.
                
#                 if int(vFolder.split('v')[-1]) == 2:
#                     _btagSF = event.weightBtagSF
                
                    
                
                if RunA:
                    _weight = _weight + _weightA
                if RunB:
                    _weight = _weight + _weightB
                if RunC:
                    _weight = _weight + _weightC
                if RunD:
                    _weight = _weight + _weightD
                
                _weight = _weight*_btagSF            
                
                
                #EXTRA CUTS
                
                
                HistoLists[mode][i]['ptjet'][1][s][0].Fill(                    _ptjet                    , _weight )
                HistoLists[mode][i]['ht'][1][s][0].Fill(                       _ht                       , _weight )
                HistoLists[mode][i]['msys'][1][s][0].Fill(                     _msys                     , _weight )
                HistoLists[mode][i]['ptsys'][1][s][0].Fill(                    _ptsys                    , _weight )
                HistoLists[mode][i]['ptjll'][1][s][0].Fill(                    _ptjll                    , _weight )
                HistoLists[mode][i]['ptsys_ht'][1][s][0].Fill(                 _ptsys_ht                 , _weight )
                HistoLists[mode][i]['htleps_ht'][1][s][0].Fill(                _htleps_ht                , _weight )
                HistoLists[mode][i]['NlooseJet15Central'][1][s][0].Fill(       _NlooseJet15Central       , _weight )
                HistoLists[mode][i]['NlooseJet15Forward'][1][s][0].Fill(       _NlooseJet15Forward       , _weight )
                HistoLists[mode][i]['NlooseJet15'][1][s][0].Fill(              _NlooseJet15              , _weight )
                HistoLists[mode][i]['NbtaggedlooseJet15'][1][s][0].Fill(       _NbtaggedlooseJet15       , _weight )
                HistoLists[mode][i]['NlooseJet20Central'][1][s][0].Fill(       _NlooseJet20Central       , _weight )
                HistoLists[mode][i]['NlooseJet20Forward'][1][s][0].Fill(       _NlooseJet20Forward       , _weight )
                HistoLists[mode][i]['NlooseJet20'][1][s][0].Fill(              _NlooseJet20              , _weight )
                HistoLists[mode][i]['NbtaggedlooseJet20'][1][s][0].Fill(       _NbtaggedlooseJet20       , _weight )
                HistoLists[mode][i]['NlooseJet25Central'][1][s][0].Fill(       _NlooseJet25Central       , _weight )
                HistoLists[mode][i]['NlooseJet25Forward'][1][s][0].Fill(       _NlooseJet25Forward       , _weight )
                HistoLists[mode][i]['NlooseJet25'][1][s][0].Fill(              _NlooseJet25              , _weight )
                HistoLists[mode][i]['NbtaggedlooseJet25'][1][s][0].Fill(       _NbtaggedlooseJet25       , _weight )
                HistoLists[mode][i]['met'][1][s][0].Fill(                      _met                      , _weight )
                HistoLists[mode][i]['loosejetPt'][1][s][0].Fill(               _loosejetPt               , _weight )
                HistoLists[mode][i]['centralityJLL'][1][s][0].Fill(            _centralityJLL            , _weight )

                HistoLists[-1][i]['ptjet'][1][s][0].Fill(                    _ptjet                    , _weight )
                HistoLists[-1][i]['ht'][1][s][0].Fill(                       _ht                       , _weight )
                HistoLists[-1][i]['msys'][1][s][0].Fill(                     _msys                     , _weight )
                HistoLists[-1][i]['ptsys'][1][s][0].Fill(                    _ptsys                    , _weight )
                HistoLists[-1][i]['ptjll'][1][s][0].Fill(                    _ptjll                    , _weight )
                HistoLists[-1][i]['ptsys_ht'][1][s][0].Fill(                 _ptsys_ht                 , _weight )
                HistoLists[-1][i]['htleps_ht'][1][s][0].Fill(                _htleps_ht                , _weight )
                HistoLists[-1][i]['NlooseJet15Central'][1][s][0].Fill(       _NlooseJet15Central       , _weight )
                HistoLists[-1][i]['NlooseJet15Forward'][1][s][0].Fill(       _NlooseJet15Forward       , _weight )
                HistoLists[-1][i]['NlooseJet15'][1][s][0].Fill(              _NlooseJet15              , _weight )
                HistoLists[-1][i]['NbtaggedlooseJet15'][1][s][0].Fill(       _NbtaggedlooseJet15       , _weight )
                HistoLists[-1][i]['NlooseJet20Central'][1][s][0].Fill(       _NlooseJet20Central       , _weight )
                HistoLists[-1][i]['NlooseJet20Forward'][1][s][0].Fill(       _NlooseJet20Forward       , _weight )
                HistoLists[-1][i]['NlooseJet20'][1][s][0].Fill(              _NlooseJet20              , _weight )
                HistoLists[-1][i]['NbtaggedlooseJet20'][1][s][0].Fill(       _NbtaggedlooseJet20       , _weight )
                HistoLists[-1][i]['NlooseJet25Central'][1][s][0].Fill(       _NlooseJet25Central       , _weight )
                HistoLists[-1][i]['NlooseJet25Forward'][1][s][0].Fill(       _NlooseJet25Forward       , _weight )
                HistoLists[-1][i]['NlooseJet25'][1][s][0].Fill(              _NlooseJet25              , _weight )
                HistoLists[-1][i]['NbtaggedlooseJet25'][1][s][0].Fill(       _NbtaggedlooseJet25       , _weight )
                HistoLists[-1][i]['met'][1][s][0].Fill(                      _met                      , _weight )
                HistoLists[-1][i]['loosejetPt'][1][s][0].Fill(               _loosejetPt               , _weight )
                HistoLists[-1][i]['centralityJLL'][1][s][0].Fill(            _centralityJLL            , _weight )

            print

            tree = TChain(Folder[mode]+'/'+region)

            fName = 'tmvaFiles/'+vFolder+'/'+fileList[i]
            print fName.replace('.root','_'+systList[s]+'Down.root')
            tree.Add(fName.replace('.root','_'+systList[s]+'Down.root'))


            nEvents = tree.GetEntries()*1.

#            print nEvents

            evtCount = 0.
            percent = 0.0
            progSlots = 25.    
            
            for event in tree:
                evtCount += 1.
                if evtCount/nEvents > percent:
                    k = int(percent*progSlots)
                    progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                    sys.stdout.write(progress)
                    sys.stdout.flush()
                    percent += 1./progSlots
                    


                _ptjet                     = event.ptjet                   
                _ht                        = event.ht                      
                _msys                      = event.msys                    
                _ptsys                     = event.ptsys                   
                _ptjll                     = event.ptjll                   
                _ptsys_ht                  = event.ptsys_ht                
                _htleps_ht                 = event.htleps_ht               
                _NlooseJet15Central        = event.NlooseJet15Central      
                _NlooseJet15Forward        = event.NlooseJet15Forward      
                _NlooseJet15               = event.NlooseJet15             
                _NbtaggedlooseJet15        = event.NbtaggedlooseJet15      
                _NlooseJet20Central        = event.NlooseJet20Central      
                _NlooseJet20Forward        = event.NlooseJet20Forward      
                _NlooseJet20               = event.NlooseJet20             
                _NbtaggedlooseJet20        = event.NbtaggedlooseJet20      
                _NlooseJet25Central        = event.NlooseJet25Central      
                _NlooseJet25Forward        = event.NlooseJet25Forward      
                _NlooseJet25               = event.NlooseJet25             
                _NbtaggedlooseJet25        = event.NbtaggedlooseJet25      
                _met                       = event.met                     
                _loosejetPt                = event.loosejetPt              
                _centralityJLL             = event.centralityJLL           
                
                _weightA                    = event.weightA
                _weightB                    = event.weightB
                _weightC                    = event.weightC
                _weightD                    = event.weightD
                
                _weight = 0            
                
                
                _btagSF = 1.
                
#                 if int(vFolder.split('v')[-1]) == 2:
#                     _btagSF = event.weightBtagSF
                
                    
                
                if RunA:
                    _weight = _weight + _weightA
                if RunB:
                    _weight = _weight + _weightB
                if RunC:
                    _weight = _weight + _weightC
                if RunD:
                    _weight = _weight + _weightD
                
                _weight = _weight*_btagSF            
                
                
                #EXTRA CUTS
                
                
                HistoLists[mode][i]['ptjet'][1][s][1].Fill(                    _ptjet                    , _weight )
                HistoLists[mode][i]['ht'][1][s][1].Fill(                       _ht                       , _weight )
                HistoLists[mode][i]['msys'][1][s][1].Fill(                     _msys                     , _weight )
                HistoLists[mode][i]['ptsys'][1][s][1].Fill(                    _ptsys                    , _weight )
                HistoLists[mode][i]['ptjll'][1][s][1].Fill(                    _ptjll                    , _weight )
                HistoLists[mode][i]['ptsys_ht'][1][s][1].Fill(                 _ptsys_ht                 , _weight )
                HistoLists[mode][i]['htleps_ht'][1][s][1].Fill(                _htleps_ht                , _weight )
                HistoLists[mode][i]['NlooseJet15Central'][1][s][1].Fill(       _NlooseJet15Central       , _weight )
                HistoLists[mode][i]['NlooseJet15Forward'][1][s][1].Fill(       _NlooseJet15Forward       , _weight )
                HistoLists[mode][i]['NlooseJet15'][1][s][1].Fill(              _NlooseJet15              , _weight )
                HistoLists[mode][i]['NbtaggedlooseJet15'][1][s][1].Fill(       _NbtaggedlooseJet15       , _weight )
                HistoLists[mode][i]['NlooseJet20Central'][1][s][1].Fill(       _NlooseJet20Central       , _weight )
                HistoLists[mode][i]['NlooseJet20Forward'][1][s][1].Fill(       _NlooseJet20Forward       , _weight )
                HistoLists[mode][i]['NlooseJet20'][1][s][1].Fill(              _NlooseJet20              , _weight )
                HistoLists[mode][i]['NbtaggedlooseJet20'][1][s][1].Fill(       _NbtaggedlooseJet20       , _weight )
                HistoLists[mode][i]['NlooseJet25Central'][1][s][1].Fill(       _NlooseJet25Central       , _weight )
                HistoLists[mode][i]['NlooseJet25Forward'][1][s][1].Fill(       _NlooseJet25Forward       , _weight )
                HistoLists[mode][i]['NlooseJet25'][1][s][1].Fill(              _NlooseJet25              , _weight )
                HistoLists[mode][i]['NbtaggedlooseJet25'][1][s][1].Fill(       _NbtaggedlooseJet25       , _weight )
                HistoLists[mode][i]['met'][1][s][1].Fill(                      _met                      , _weight )
                HistoLists[mode][i]['loosejetPt'][1][s][1].Fill(               _loosejetPt               , _weight )
                HistoLists[mode][i]['centralityJLL'][1][s][1].Fill(            _centralityJLL            , _weight )

                HistoLists[-1][i]['ptjet'][1][s][1].Fill(                    _ptjet                    , _weight )
                HistoLists[-1][i]['ht'][1][s][1].Fill(                       _ht                       , _weight )
                HistoLists[-1][i]['msys'][1][s][1].Fill(                     _msys                     , _weight )
                HistoLists[-1][i]['ptsys'][1][s][1].Fill(                    _ptsys                    , _weight )
                HistoLists[-1][i]['ptjll'][1][s][1].Fill(                    _ptjll                    , _weight )
                HistoLists[-1][i]['ptsys_ht'][1][s][1].Fill(                 _ptsys_ht                 , _weight )
                HistoLists[-1][i]['htleps_ht'][1][s][1].Fill(                _htleps_ht                , _weight )
                HistoLists[-1][i]['NlooseJet15Central'][1][s][1].Fill(       _NlooseJet15Central       , _weight )
                HistoLists[-1][i]['NlooseJet15Forward'][1][s][1].Fill(       _NlooseJet15Forward       , _weight )
                HistoLists[-1][i]['NlooseJet15'][1][s][1].Fill(              _NlooseJet15              , _weight )
                HistoLists[-1][i]['NbtaggedlooseJet15'][1][s][1].Fill(       _NbtaggedlooseJet15       , _weight )
                HistoLists[-1][i]['NlooseJet20Central'][1][s][1].Fill(       _NlooseJet20Central       , _weight )
                HistoLists[-1][i]['NlooseJet20Forward'][1][s][1].Fill(       _NlooseJet20Forward       , _weight )
                HistoLists[-1][i]['NlooseJet20'][1][s][1].Fill(              _NlooseJet20              , _weight )
                HistoLists[-1][i]['NbtaggedlooseJet20'][1][s][1].Fill(       _NbtaggedlooseJet20       , _weight )
                HistoLists[-1][i]['NlooseJet25Central'][1][s][1].Fill(       _NlooseJet25Central       , _weight )
                HistoLists[-1][i]['NlooseJet25Forward'][1][s][1].Fill(       _NlooseJet25Forward       , _weight )
                HistoLists[-1][i]['NlooseJet25'][1][s][1].Fill(              _NlooseJet25              , _weight )
                HistoLists[-1][i]['NbtaggedlooseJet25'][1][s][1].Fill(       _NbtaggedlooseJet25       , _weight )
                HistoLists[-1][i]['met'][1][s][1].Fill(                      _met                      , _weight )
                HistoLists[-1][i]['loosejetPt'][1][s][1].Fill(               _loosejetPt               , _weight )
                HistoLists[-1][i]['centralityJLL'][1][s][1].Fill(            _centralityJLL            , _weight )

            print



leg = TLegend(0.66,0.66,0.94,0.94)
leg.SetFillStyle(1)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.AddEntry(HistoLists[0][0]['ptjet'][0], "Standard", "l")
leg.AddEntry(HistoLists[0][0]['ptjet'][1][0][0], "Syst Up", "l")
leg.AddEntry(HistoLists[0][0]['ptjet'][1][0][1], "Syst Down", "l")




# for mode in range(len(ChanName)):

#     if not doChannel[mode]:
#         continue

#     labelcms2 = TPaveText(0.1,0.82,0.6,0.88,"NDCBR");
#     labelcms2.SetTextAlign(12);
#     labelcms2.SetTextSize(0.045);
#     labelcms2.SetFillColor(kWhite);
#     labelcms2.AddText("tW " + ChanLabels[mode] + region)
#     labelcms2.SetBorderSize(0);

    
#     for plot in plotInfo:

#         standardMax = HistoLists[mode][0][plot[0]][0].GetMaximum()

#         systList[-1] = 'DRDS'
#         for s in range(len(systList)):
#             c1 = TCanvas()
#             max1_ = max(HistoLists[mode][0][plot[0]][1][s][0].GetMaximum(),HistoLists[mode][0][plot[0]][1][s][1].GetMaximum())
#             max_ = max(standardMax,max1_)
#             HistoLists[mode][0][plot[0]][0].Draw()
#             HistoLists[mode][0][plot[0]][0].SetMaximum(max_*1.5)
#             HistoLists[mode][0][plot[0]][0].SetMinimum(0)
            
#             HistoLists[mode][0][plot[0]][0].GetYaxis().SetTitle("Events")
#             HistoLists[mode][0][plot[0]][0].GetYaxis().CenterTitle()
#             HistoLists[mode][0][plot[0]][0].GetXaxis().SetTitle(plot[4])
            
#             HistoLists[mode][0][plot[0]][1][s][0].Draw("same")
#             HistoLists[mode][0][plot[0]][1][s][1].Draw("same")
            
#             leg.Draw()        
#             labelcms.Draw()
#             labelcms2.Draw()
             
#             if not os.path.exists("SystematicsPlots/"+vFolder):
#                 command = "mkdir SystematicsPlots/"+vFolder
#                 os.system(command)
#             if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName):
#                 command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName
#                 os.system(command)
#             if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName + region):
#                 command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName+region
#                 os.system(command)
            
#             channel = "_" + ChanName[mode]

        
#             c1.SaveAs("SystematicsPlots/"+vFolder+"/"+specialName+region+"/"+plot[0]+"_tW_"+region+channel+runs+systList[s]+".png")


#     labelcms2 = TPaveText(0.1,0.82,0.6,0.88,"NDCBR");
#     labelcms2.SetTextAlign(12);
#     labelcms2.SetTextSize(0.045);
#     labelcms2.SetFillColor(kWhite);
#     labelcms2.AddText("t#bar{t} " + ChanLabels[mode] + region)
#     labelcms2.SetBorderSize(0);

    
#     for plot in plotInfo:
#         standardMax = HistoLists[mode][1][plot[0]][0].GetMaximum()

#         systList[-1] = 'Matching'

#         for s in range(len(systList)):
#             c1 = TCanvas()
#             max1_ = max(HistoLists[mode][1][plot[0]][1][s][0].GetMaximum(),HistoLists[mode][1][plot[0]][1][s][1].GetMaximum())
#             max_ = max(standardMax,max1_)
#             HistoLists[mode][1][plot[0]][0].Draw()
#             HistoLists[mode][1][plot[0]][0].SetMaximum(max_*1.5)
#             HistoLists[mode][1][plot[0]][0].SetMinimum(0)
            
#             HistoLists[mode][1][plot[0]][0].GetYaxis().SetTitle("Events")
#             HistoLists[mode][1][plot[0]][0].GetYaxis().CenterTitle()
#             HistoLists[mode][1][plot[0]][0].GetXaxis().SetTitle(plot[4])
            
#             HistoLists[mode][1][plot[0]][1][s][0].Draw("same")
#             HistoLists[mode][1][plot[0]][1][s][1].Draw("same")
            
#             leg.Draw()        
#             labelcms.Draw()
#             labelcms2.Draw()
            
#             if not os.path.exists("SystematicsPlots/"+vFolder):
#                 command = "mkdir SystematicsPlots/"+vFolder
#                 os.system(command)
#             if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName):
#                 command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName
#                 os.system(command)
#             if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName + region):
#                 command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName+region
#                 os.system(command)
            
#             channel = "_" + ChanName[mode]

        
#             c1.SaveAs("SystematicsPlots/"+vFolder+"/"+specialName+region+"/"+plot[0]+"_tt_"+region+channel+runs+systList[s]+".png")


mode = -1

labelcms2 = TPaveText(0.1,0.82,0.6,0.88,"NDCBR");
labelcms2.SetTextAlign(12);
labelcms2.SetTextSize(0.045);
labelcms2.SetFillColor(kWhite);
labelcms2.AddText("tW " + ChanLabels[mode] + region)
labelcms2.SetBorderSize(0);


for plot in plotInfo:

    standardMax = HistoLists[mode][0][plot[0]][0].GetMaximum()

    systList[-1] = 'DRDS'
    for s in range(len(systList)):
        c1 = TCanvas()
        max1_ = max(HistoLists[mode][0][plot[0]][1][s][0].GetMaximum(),HistoLists[mode][0][plot[0]][1][s][1].GetMaximum())
        max_ = max(standardMax,max1_)
        HistoLists[mode][0][plot[0]][0].Draw()
        HistoLists[mode][0][plot[0]][0].SetMaximum(max_*1.5)
        HistoLists[mode][0][plot[0]][0].SetMinimum(0)
        
        HistoLists[mode][0][plot[0]][0].GetYaxis().SetTitle("Events")
        HistoLists[mode][0][plot[0]][0].GetYaxis().CenterTitle()
        HistoLists[mode][0][plot[0]][0].GetXaxis().SetTitle(plot[4])
        
        HistoLists[mode][0][plot[0]][1][s][0].Draw("same")
        HistoLists[mode][0][plot[0]][1][s][1].Draw("same")
        
        leg.Draw()        
        labelcms.Draw()
        labelcms2.Draw()
         
        if not os.path.exists("SystematicsPlots/"):
            command = "mkdir SystematicsPlots/"
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder):
            command = "mkdir SystematicsPlots/"+vFolder
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName):
            command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName + region):
            command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName+region
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName + region+"/"+systList[s]):
            command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName+region+"/"+systList[s]
            os.system(command)
        
        channel = "_"

    
        c1.SaveAs("SystematicsPlots/"+vFolder+"/"+specialName+region+"/"+systList[s]+"/"+plot[0]+"_tW_"+region+channel+runs+systList[s]+".png")


labelcms2 = TPaveText(0.1,0.82,0.6,0.88,"NDCBR");
labelcms2.SetTextAlign(12);
labelcms2.SetTextSize(0.045);
labelcms2.SetFillColor(kWhite);
labelcms2.AddText("t#bar{t} " + ChanLabels[mode] + region)
labelcms2.SetBorderSize(0);


for plot in plotInfo:
    standardMax = HistoLists[mode][1][plot[0]][0].GetMaximum()

    systList[-1] = 'Matching'

    for s in range(len(systList)):
        c1 = TCanvas()
        max1_ = max(HistoLists[mode][1][plot[0]][1][s][0].GetMaximum(),HistoLists[mode][1][plot[0]][1][s][1].GetMaximum())
        max_ = max(standardMax,max1_)
        HistoLists[mode][1][plot[0]][0].Draw()
        HistoLists[mode][1][plot[0]][0].SetMaximum(max_*1.5)
        HistoLists[mode][1][plot[0]][0].SetMinimum(0)
        
        HistoLists[mode][1][plot[0]][0].GetYaxis().SetTitle("Events")
        HistoLists[mode][1][plot[0]][0].GetYaxis().CenterTitle()
        HistoLists[mode][1][plot[0]][0].GetXaxis().SetTitle(plot[4])
        
        HistoLists[mode][1][plot[0]][1][s][0].Draw("same")
        HistoLists[mode][1][plot[0]][1][s][1].Draw("same")
        
        leg.Draw()        
        labelcms.Draw()
        labelcms2.Draw()
        
        if not os.path.exists("SystematicsPlots/"):
            command = "mkdir SystematicsPlots/"
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder):
            command = "mkdir SystematicsPlots/"+vFolder
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName):
            command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName + region):
            command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName+region
            os.system(command)
        if not os.path.exists("SystematicsPlots/"+vFolder+"/"+specialName + region+"/"+systList[s]):
            command = "mkdir SystematicsPlots/"+vFolder+"/"+specialName+region+"/"+systList[s]
            os.system(command)
        
        channel = "_" 

    
        c1.SaveAs("SystematicsPlots/"+vFolder+"/"+specialName+region+"/"+systList[s]+"/"+plot[0]+"_tt_"+region+channel+runs+systList[s]+".png")








