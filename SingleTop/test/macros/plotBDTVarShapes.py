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

AllowedRegions = ['1j0t','1j1t','1jNoTagging','2j0t','2j1t','2j2t','2jNoTagging','3plusjNoTagging','1j1tZpeak','ZpeakLepSel','2plusjets1plustag','3plusjets1plustag','tree1j1tNomllMetCut','3j0t','3j1t','3j2t','3j3t']

region = '1j1t'
runPicked = False

channelPicked = False
emuChan = False
mumuChan = False
eeChan = False
combinedChan = False

versionPicked = False

#specialName = 'NewTTbarFiles'
# specialName = 'OriginalZjetSF/OldTTbar'
specialName = ''

fast = False

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
    elif arg == 'D':
        RunD = True
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
    elif arg == 'noZjetSF':
        useZjetsSF = False
        specialName += 'NoZjetSF'
    elif arg == "fast":
        fast = True
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
        print "   'D' - use Run D"
        print "   'emu'  - do emu channel"
        print "   'mumu' - do mumu channel"
        print "   'ee'   - do ee channel"
        print "   '-v Folder' - specify the version folder inside tmvaFiles to be used"
        print "Default mode:"
        print " 1j1t region, using Runs A, B, C, & D, all three channels"
        exit()
    else:
        print "Unknown argument", arg," will be ignored"
    i += 1


if not channelPicked:
    emuChan = True
    mumuChan = True
    eeChan = True
    combinedChan = True

if not versionPicked:
    vFolder = "ManyRegions_v2"
#     versionList = glob.glob("tmvaF/v*")
#     versionList.sort(key=lambda a:int(a.split('/v')[-1].split('_')[0]))
#     vFolder = versionList[-1].split('/')[-1]    
#     print vFolder

doZpeakCuts = False

labelcms = TPaveText(0.1,0.9,0.9,0.98,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.045);
labelcms.SetFillColor(kWhite);
labelcms.SetFillStyle(0);
labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV, "+region);
labelcms.SetBorderSize(0);

#gStyle.SetLabelSize(0.045,"x")
gStyle.SetLabelSize(0.035,"xy")

bdtPlots = ['lepJetPt_PosLep',
            'lepPt_PosLep',
            'lepJetDR_PosLep',
            'lepJetDPhi_PosLep',
            'lepJetDEta_PosLep',
            'lepJetM_PosLep',
            'lepPtRelJet_PosLep',
            'jetPtRelLep_PosLep',
            'lepPtRelJetSameLep_PosLep',
            'lepPtRelJetOtherLep_PosLep',
            'lepJetMt_PosLep',
            'lepJetCosTheta_boosted_PosLep',
            'lepJetPt_NegLep',
            'lepPt_NegLep',
            'lepJetDR_NegLep',
            'lepJetDPhi_NegLep',
            'lepJetDEta_NegLep',
            'lepJetM_NegLep',
            'lepPtRelJet_NegLep',
            'jetPtRelLep_NegLep',
            'lepPtRelJetSameLep_NegLep',
            'lepPtRelJetOtherLep_NegLep',
            'lepJetMt_NegLep',
            'lepJetCosTheta_boosted_NegLep',
            'ptjet',
            'ptsys',
            'ht',
            'NlooseJet20',
            'NlooseJet20Central',
            'NbtaggedlooseJet20',
            'centralityJLL',
            'loosejetPt',
            'ptsys_ht',
            'msys',
            'htleps_ht',
            'ptjll',
            'met',
            ]
    
plotInfo = [['ptjet',27,30,300, 'P_{T} leading jet [GeV]','Events / 10 GeV'],
            ['jetCSV',100,0,1, 'Jet CSV','Events'],
            ['ht',60,0,600, 'H_{T} [GeV]','Events / 10 GeV'],
            ['msys',60,0,600, 'Mass-system [GeV]','Events / 10 GeV'],
            ['ptsys',50,0,200, 'P_{T} system [GeV]','Events / 4 GeV'],
            ['ptjll',30,0,300, 'P_{T}-jll [GeV]','Events / 10 GeV'],
            ['ptsys_ht',40,0,1, 'P_{T} system / H_{T}','Events'],
            ['htleps_ht',40,0,1, 'H_{T} leptons / H_{T}','Events'],
            ['NlooseJet15Central',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| < 2.4','Events'],
            ['NlooseJet15Forward',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| > 2.4','Events'],
            ['NlooseJet20Central',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| < 2.4','Events'],
            ['NlooseJet20Forward',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| > 2.4','Events'],
            ['NlooseJet25Central',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| < 2.4','Events'],
            ['NlooseJet25Forward',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| > 2.4','Events'],
            ['NlooseJet15',10,0,10, 'Number of loose jets, P_{T} > 15','Events'],
            ['NlooseJet20',10,0,10, 'Number of loose jets, P_{T} > 20','Events'],
            ['NlooseJet25',10,0,10, 'Number of loose jets, P_{T} > 25','Events'],
            ['NbtaggedlooseJet15',4,0,4, 'Number of b-tagged loose jets, P_{T} > 15','Events'],
            ['NbtaggedlooseJet20',4,0,4, 'Number of b-tagged loose jets, P_{T} > 20','Events'],
            ['NbtaggedlooseJet25',4,0,4, 'Number of b-tagged loose jets, P_{T} > 25','Events'],
            ['met', 60, 0, 300,'MET [GeV]','Events / 5 GeV'],
            ['loosejetPt', 30, 0, 150, 'P_{} of loose jet [GeV]','Events / 5 GeV'],
            ['centralityJLL',40,0,1,'Centrality - jll','Events'],
#             ['lepJetPt_PosLep',40,0,300,'P_{T} jet & positive-lepton','Events'],
#             ['lepPt_PosLep',40,0,300,'P_{T} positive-lepton','Events'],
#             ['lepJetDR_PosLep',40,0,6,'#Delta R(jet,positive-lepton)','Events'],
#             ['lepJetDPhi_PosLep',40,0,3.2,'#Delta #phi (jet,positive-lepton)','Events'],
#             ['lepJetDEta_PosLep',40,0,5,'#Delta #eta (jet,positive-lepton)','Events'],
#             ['lepJetM_PosLep',40,0,300,'Mass of jet & positive-lepton','Events'],
#             ['lepPtRelJet_PosLep',40,0,200,'P_{T} positive-lepton relative to jet','Events'],
#             ['jetPtRelLep_PosLep',40,0,200,'P_{T} jet relative to positive-lepton','Events'],
#             ['lepPtRelJetSameLep_PosLep',40,0,200,'P_{T} pos-lepton relative to jet & pos-lep','Events'],
#             ['lepPtRelJetOtherLep_PosLep',40,0,200,'P_{T} pos-lepton relative to jet & neg-lep','Events'],
#             ['lepJetMt_PosLep',40,0,300,'M_{T} jet & positive-lepton','Events'],
#             ['lepJetCosTheta_boosted_PosLep',40,-1.,1.,'Cos #theta (positive-lepton,jet)','Events'],
#             ['lepJetPt_NegLep',40,0,300,'P_{T} jet & negative-lepton','Events'],
#             ['lepPt_NegLep',40,0,300,'P_{T} negative-lepton','Events'],
#             ['lepJetDR_NegLep',40,0,6,'#Delta R(jet,negative-lepton)','Events'],
#             ['lepJetDPhi_NegLep',40,0,3.2,'#Delta #phi (jet,negative-lepton)','Events'],
#             ['lepJetDEta_NegLep',40,0,5,'#Delta #eta (jet,negative-lepton)','Events'],
#             ['lepJetM_NegLep',40,0,300,'Mass of jet & negative-lepton','Events'],
#             ['lepPtRelJet_NegLep',40,0,200,'P_{T} negative-lepton relative to jet','Events'],
#             ['jetPtRelLep_NegLep',40,0,200,'P_{T} jet relative to negative-lepton','Events'],
#             ['lepPtRelJetSameLep_NegLep',40,0,200,'P_{T} neg-lepton relative to jet & neg-lep','Events'],
#             ['lepPtRelJetOtherLep_NegLep',40,0,200,'P_{T} neg-lepton relative to jet & pos-lep','Events'],
#             ['lepJetMt_NegLep',40,0,300,'M_{T} jet & negative-lepton','Events'],
#             ['lepJetCosTheta_boosted_NegLep',40,-1.,1.,'Cos #theta (negative-lepton,jet)','Events'],
            ]


fileList = ['TWDilepton_123.root',
            'TTbarDilepton.root',
            ]

Colors = [TColor.GetColor( "#7d99d1" ),
          TColor.GetColor( "#ff0000" ),
          ]

Style = [1001,
         3554,
         ]

Lines = [TColor.GetColor( "#0000ee" ),
         TColor.GetColor( "#ff0000" ),
         ]

         
         

ChanName = ['emu','mumu','ee']

Folder = ['emuChannel','mumuChannel','eeChannel']

HistoLists = list()


for mode in range(3):


    HistoMode = list()

    for i in range(len(fileList)):
        Histos = dict()

        fileName = fileList[i].split('.')[0]
        for plot in plotInfo:
            Histos[plot[0]] = TH1F(plot[0]+fileName+ChanName[mode]," ",plot[1],plot[2],plot[3])
            Histos[plot[0]].SetFillColor(Colors[i])
            Histos[plot[0]].SetFillStyle(Style[i])
            Histos[plot[0]].SetLineColor(Lines[i])
            Histos[plot[0]].SetLineWidth(4)
            Histos[plot[0]].SetMarkerSize(0.)
#             Histos[plot[0]].Sumw2()
        HistoMode.append(Histos)

    HistoLists.append(HistoMode)

HistoMode = list()

for i in range(len(fileList)):
    Histos = dict()

    fileName = fileList[i].split('.')[0]
    for plot in plotInfo:
        Histos[plot[0]] = TH1F(plot[0]+fileName," ",plot[1],plot[2],plot[3])
        Histos[plot[0]].SetFillColor(Colors[i])
        Histos[plot[0]].SetFillStyle(Style[i])
        Histos[plot[0]].SetLineColor(Lines[i])
        Histos[plot[0]].SetLineWidth(4)
        Histos[plot[0]].SetMarkerSize(0.)
#         Histos[plot[0]].Sumw2()
    HistoMode.append(Histos)


HistoLists.append(HistoMode)

for mode in range(3):


    for i in range(len(fileList)):

        print fileList[i]

        regiontemp = region

        if '1j1tZpeak' in region:
            regiontemp = 'tree1j1tNomllMetCut'

        tree = TChain(Folder[mode]+'/'+regiontemp)

        if fileList[i] == 'DATA':
            if RunA:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012A.root')
            if RunB:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012B.root')
            if RunC:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012C.root')
            if RunD:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012D.root')

        else:
            tree.Add('tmvaFiles/'+vFolder+'/'+fileList[i])

        nEvents = tree.GetEntries()*1.

        print nEvents

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


            if fast:
                if evtCount > 1000:
                    break

            _ptjet                     = event.ptjet                   
            _jetCSV                    = event.jetCSV                  
            _ht                        = event.ht                      
            _msys                      = event.msys                    
            _ptsys                     = event.ptsys                   
            _ptjll                     = event.ptjll                   
            _ptsys_ht                  = event.ptsys_ht                
            _htleps_ht                 = event.htleps_ht               
            _NlooseJet15Central        = event.NlooseJet15Central      
            _NlooseJet15Forward        = event.NlooseJet15Forward      
            _NlooseJet20Central        = event.NlooseJet20Central      
            _NlooseJet20Forward        = event.NlooseJet20Forward      
            _NlooseJet25Central        = event.NlooseJet25Central      
            _NlooseJet25Forward        = event.NlooseJet25Forward      
            _NlooseJet15               = event.NlooseJet15             
            _NlooseJet20               = event.NlooseJet20             
            _NlooseJet25               = event.NlooseJet25             
            _NbtaggedlooseJet15        = event.NbtaggedlooseJet15      
            _NbtaggedlooseJet20        = event.NbtaggedlooseJet20      
            _NbtaggedlooseJet25        = event.NbtaggedlooseJet25      
            _met                       = event.met                     
            _loosejetPt                = event.loosejetPt              
            _centralityJLL             = event.centralityJLL           

#             _lepJetPt_PosLep            = event.lepJetPt_PosLep           
#             _lepPt_PosLep               = event.lepPt_PosLep              
#             _lepJetDR_PosLep            = event.lepJetDR_PosLep           
#             _lepJetDPhi_PosLep          = event.lepJetDPhi_PosLep         
#             _lepJetDEta_PosLep          = event.lepJetDEta_PosLep         
#             _lepJetM_PosLep             = event.lepJetM_PosLep            
#             _lepPtRelJet_PosLep         = event.lepPtRelJet_PosLep        
#             _jetPtRelLep_PosLep         = event.jetPtRelLep_PosLep        
#             _lepPtRelJetSameLep_PosLep  = event.lepPtRelJetSameLep_PosLep 
#             _lepPtRelJetOtherLep_PosLep = event.lepPtRelJetOtherLep_PosLep
#             _lepJetMt_PosLep            = event.lepJetMt_PosLep           
#             _lepJetPt_NegLep            = event.lepJetPt_NegLep           
#             _lepPt_NegLep               = event.lepPt_NegLep              
#             _lepJetDR_NegLep            = event.lepJetDR_NegLep           
#             _lepJetDPhi_NegLep          = event.lepJetDPhi_NegLep         
#             _lepJetDEta_NegLep          = event.lepJetDEta_NegLep         
#             _lepJetM_NegLep             = event.lepJetM_NegLep            
#             _lepPtRelJet_NegLep         = event.lepPtRelJet_NegLep        
#             _jetPtRelLep_NegLep         = event.jetPtRelLep_NegLep        
#             _lepPtRelJetSameLep_NegLep  = event.lepPtRelJetSameLep_NegLep 
#             _lepPtRelJetOtherLep_NegLep = event.lepPtRelJetOtherLep_NegLep
#             _lepJetMt_NegLep            = event.lepJetMt_NegLep           


                
            _weight = 1.




            

            HistoLists[mode][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[mode][i]['jetCSV'].Fill(                   _jetCSV                   , _weight )
            HistoLists[mode][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[mode][i]['msys'].Fill(                     _msys                     , _weight )
            HistoLists[mode][i]['ptsys'].Fill(                    _ptsys                    , _weight )
            HistoLists[mode][i]['ptjll'].Fill(                    _ptjll                    , _weight )
            HistoLists[mode][i]['ptsys_ht'].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[mode][i]['htleps_ht'].Fill(                _htleps_ht                , _weight )
            HistoLists[mode][i]['NlooseJet15Central'].Fill(       _NlooseJet15Central       , _weight )
            HistoLists[mode][i]['NlooseJet15Forward'].Fill(       _NlooseJet15Forward       , _weight )
            HistoLists[mode][i]['NlooseJet20Central'].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[mode][i]['NlooseJet20Forward'].Fill(       _NlooseJet20Forward       , _weight )
            HistoLists[mode][i]['NlooseJet25Central'].Fill(       _NlooseJet25Central       , _weight )
            HistoLists[mode][i]['NlooseJet25Forward'].Fill(       _NlooseJet25Forward       , _weight )
            HistoLists[mode][i]['NlooseJet15'].Fill(              _NlooseJet15              , _weight )
            HistoLists[mode][i]['NlooseJet20'].Fill(              _NlooseJet20              , _weight )
            HistoLists[mode][i]['NlooseJet25'].Fill(              _NlooseJet25              , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet15'].Fill(       _NbtaggedlooseJet15       , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet20'].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet25'].Fill(       _NbtaggedlooseJet25       , _weight )
            HistoLists[mode][i]['met'].Fill(                      _met                      , _weight )
            HistoLists[mode][i]['loosejetPt'].Fill(               _loosejetPt               , _weight )
            HistoLists[mode][i]['centralityJLL'].Fill(            _centralityJLL            , _weight )

#             HistoLists[mode][i]['lepJetPt_PosLep'].Fill(            _lepJetPt_PosLep           , _weight )
#             HistoLists[mode][i]['lepPt_PosLep'].Fill(               _lepPt_PosLep              , _weight )
#             HistoLists[mode][i]['lepJetDR_PosLep'].Fill(            _lepJetDR_PosLep           , _weight )
#             HistoLists[mode][i]['lepJetDPhi_PosLep'].Fill(          _lepJetDPhi_PosLep         , _weight )
#             HistoLists[mode][i]['lepJetDEta_PosLep'].Fill(          _lepJetDEta_PosLep         , _weight )
#             HistoLists[mode][i]['lepJetM_PosLep'].Fill(             _lepJetM_PosLep            , _weight )
#             HistoLists[mode][i]['lepPtRelJet_PosLep'].Fill(         _lepPtRelJet_PosLep        , _weight )
#             HistoLists[mode][i]['jetPtRelLep_PosLep'].Fill(         _jetPtRelLep_PosLep        , _weight )
#             HistoLists[mode][i]['lepPtRelJetSameLep_PosLep'].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
#             HistoLists[mode][i]['lepPtRelJetOtherLep_PosLep'].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
#             HistoLists[mode][i]['lepJetMt_PosLep'].Fill(            _lepJetMt_PosLep           , _weight )
#             HistoLists[mode][i]['lepJetPt_NegLep'].Fill(            _lepJetPt_NegLep           , _weight )
#             HistoLists[mode][i]['lepPt_NegLep'].Fill(               _lepPt_NegLep              , _weight )
#             HistoLists[mode][i]['lepJetDR_NegLep'].Fill(            _lepJetDR_NegLep           , _weight )
#             HistoLists[mode][i]['lepJetDPhi_NegLep'].Fill(          _lepJetDPhi_NegLep         , _weight )
#             HistoLists[mode][i]['lepJetDEta_NegLep'].Fill(          _lepJetDEta_NegLep         , _weight )
#             HistoLists[mode][i]['lepJetM_NegLep'].Fill(             _lepJetM_NegLep            , _weight )
#             HistoLists[mode][i]['lepPtRelJet_NegLep'].Fill(         _lepPtRelJet_NegLep        , _weight )
#             HistoLists[mode][i]['jetPtRelLep_NegLep'].Fill(         _jetPtRelLep_NegLep        , _weight )
#             HistoLists[mode][i]['lepPtRelJetSameLep_NegLep'].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
#             HistoLists[mode][i]['lepPtRelJetOtherLep_NegLep'].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
#             HistoLists[mode][i]['lepJetMt_NegLep'].Fill(            _lepJetMt_NegLep           , _weight )







            HistoLists[-1][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[-1][i]['jetCSV'].Fill(                   _jetCSV                   , _weight )
            HistoLists[-1][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[-1][i]['msys'].Fill(                     _msys                     , _weight )
            HistoLists[-1][i]['ptsys'].Fill(                    _ptsys                    , _weight )
            HistoLists[-1][i]['ptjll'].Fill(                    _ptjll                    , _weight )
            HistoLists[-1][i]['ptsys_ht'].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[-1][i]['htleps_ht'].Fill(                _htleps_ht                , _weight )
            HistoLists[-1][i]['NlooseJet15Central'].Fill(       _NlooseJet15Central       , _weight )
            HistoLists[-1][i]['NlooseJet15Forward'].Fill(       _NlooseJet15Forward       , _weight )
            HistoLists[-1][i]['NlooseJet20Central'].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[-1][i]['NlooseJet20Forward'].Fill(       _NlooseJet20Forward       , _weight )
            HistoLists[-1][i]['NlooseJet25Central'].Fill(       _NlooseJet25Central       , _weight )
            HistoLists[-1][i]['NlooseJet25Forward'].Fill(       _NlooseJet25Forward       , _weight )
            HistoLists[-1][i]['NlooseJet15'].Fill(              _NlooseJet15              , _weight )
            HistoLists[-1][i]['NlooseJet20'].Fill(              _NlooseJet20              , _weight )
            HistoLists[-1][i]['NlooseJet25'].Fill(              _NlooseJet25              , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet15'].Fill(       _NbtaggedlooseJet15       , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet20'].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet25'].Fill(       _NbtaggedlooseJet25       , _weight )
            HistoLists[-1][i]['met'].Fill(                      _met                      , _weight )
            HistoLists[-1][i]['loosejetPt'].Fill(               _loosejetPt               , _weight )
            HistoLists[-1][i]['centralityJLL'].Fill(            _centralityJLL            , _weight )

#             HistoLists[-1][i]['lepJetPt_PosLep'].Fill(            _lepJetPt_PosLep           , _weight )
#             HistoLists[-1][i]['lepPt_PosLep'].Fill(               _lepPt_PosLep              , _weight )
#             HistoLists[-1][i]['lepJetDR_PosLep'].Fill(            _lepJetDR_PosLep           , _weight )
#             HistoLists[-1][i]['lepJetDPhi_PosLep'].Fill(          _lepJetDPhi_PosLep         , _weight )
#             HistoLists[-1][i]['lepJetDEta_PosLep'].Fill(          _lepJetDEta_PosLep         , _weight )
#             HistoLists[-1][i]['lepJetM_PosLep'].Fill(             _lepJetM_PosLep            , _weight )
#             HistoLists[-1][i]['lepPtRelJet_PosLep'].Fill(         _lepPtRelJet_PosLep        , _weight )
#             HistoLists[-1][i]['jetPtRelLep_PosLep'].Fill(         _jetPtRelLep_PosLep        , _weight )
#             HistoLists[-1][i]['lepPtRelJetSameLep_PosLep'].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
#             HistoLists[-1][i]['lepPtRelJetOtherLep_PosLep'].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
#             HistoLists[-1][i]['lepJetMt_PosLep'].Fill(            _lepJetMt_PosLep           , _weight )
#             HistoLists[-1][i]['lepJetPt_NegLep'].Fill(            _lepJetPt_NegLep           , _weight )
#             HistoLists[-1][i]['lepPt_NegLep'].Fill(               _lepPt_NegLep              , _weight )
#             HistoLists[-1][i]['lepJetDR_NegLep'].Fill(            _lepJetDR_NegLep           , _weight )
#             HistoLists[-1][i]['lepJetDPhi_NegLep'].Fill(          _lepJetDPhi_NegLep         , _weight )
#             HistoLists[-1][i]['lepJetDEta_NegLep'].Fill(          _lepJetDEta_NegLep         , _weight )
#             HistoLists[-1][i]['lepJetM_NegLep'].Fill(             _lepJetM_NegLep            , _weight )
#             HistoLists[-1][i]['lepPtRelJet_NegLep'].Fill(         _lepPtRelJet_NegLep        , _weight )
#             HistoLists[-1][i]['jetPtRelLep_NegLep'].Fill(         _jetPtRelLep_NegLep        , _weight )
#             HistoLists[-1][i]['lepPtRelJetSameLep_NegLep'].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
#             HistoLists[-1][i]['lepPtRelJetOtherLep_NegLep'].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
#             HistoLists[-1][i]['lepJetMt_NegLep'].Fill(            _lepJetMt_NegLep           , _weight )


leg = TLegend(0.66,0.75,0.94,0.89)
#leg.SetFillStyle(1)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.AddEntry(HistoLists[0][0]['ptjet'], "Signal: tW", "f")
leg.AddEntry(HistoLists[0][1]['ptjet'], "Background: t#bar{t}", "f")

leg2 = TLegend(0.13,0.75,0.41,0.89)
leg2.SetFillColor(kWhite)
leg2.SetBorderSize(1)
leg2.AddEntry(HistoLists[0][0]['ptjet'], "Signal: tW", "f")
leg2.AddEntry(HistoLists[0][1]['ptjet'], "Background: t#bar{t}", "f")


for mode in range(3,4):

    for plot in plotInfo:

        c1 = TCanvas()
        gPad.SetLeftMargin(0.12)
        gPad.SetTopMargin(0.1)

        m0_ = HistoLists[mode][0][plot[0]].GetMaximum()/HistoLists[mode][0][plot[0]].Integral()
        m1_ = HistoLists[mode][1][plot[0]].GetMaximum()/HistoLists[mode][1][plot[0]].Integral()

        m0_ = HistoLists[mode][0][plot[0]].GetMaximum()
        m1_ = HistoLists[mode][1][plot[0]].GetMaximum()


        max_ = max(m0_, m1_)
        print m0_, m1_, max_

        frame = TH1F("","",plot[1],plot[2],plot[3])
        frame.GetYaxis().SetRangeUser(0,max_*1.2)

        HistoLists[mode][0][plot[0]].DrawNormalized("h")


        if 'loosejetPt' in plot[0]:         HistoLists[mode][0][plot[0]].GetXaxis().SetRangeUser(0.,150.)
        HistoLists[mode][0][plot[0]].SetMaximum(max_*1.2)
        HistoLists[mode][0][plot[0]].SetMinimum(0.)
        HistoLists[mode][0][plot[0]].GetYaxis().SetTitle("Normalized to 1")
        HistoLists[mode][0][plot[0]].GetYaxis().CenterTitle()
        HistoLists[mode][0][plot[0]].GetYaxis().SetTitleOffset(1.28)
        HistoLists[mode][0][plot[0]].GetYaxis().SetTitleSize(0.05)
        HistoLists[mode][0][plot[0]].GetXaxis().SetTitle(plot[4])
        HistoLists[mode][0][plot[0]].GetXaxis().SetTitleSize(0.05)

        HistoLists[mode][0][plot[0]].DrawNormalized("h")
        HistoLists[mode][1][plot[0]].DrawNormalized("h,same")

        labelcms.Draw()
        if 'centrality' in plot[0]:
            leg2.Draw()
        else:
            leg.Draw()

        c1.Update()

        if not os.path.exists("VariablePlots/"):
            command = "mkdir VariablePlots/"
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder):
            command = "mkdir VariablePlots/"+vFolder
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName +"/normalizedPlots"):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+'/normalizedPlots'
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName +"/normalizedPlots/" + region):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+'/normalizedPlots/'+region
            os.system(command)

        channel = ""
        if mode < 3:
            channel = "_" + ChanName[mode]

        
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/normalizedPlots/"+region+"/"+plot[0]+"_"+region+channel+".pdf")
        

        print
