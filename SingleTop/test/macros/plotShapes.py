#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *

import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
# gStyle.SetCanvasBorderMode(0)
# gStyle.SetCanvasColor(kWhite)
# gStyle.SetCanvasDefH(600)
# gStyle.SetCanvasDefW(600)
# gStyle.SetCanvasDefX(0)
# gStyle.SetCanvasDefY(0)

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

versionPicked = False

specialName = ''

noPlots = False

totals = list()

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

if not channelPicked:
    emuChan = True
    mumuChan = True
    eeChan = True

if not versionPicked:
    versionList = glob.glob("tmvaFiles/v*")
    versionList.sort(key=lambda a:int(a.split('/v')[-1]))
    vFolder = versionList[-1].split('/')[-1]    
    print vFolder

if RunA:
    TotalLumi = TotalLumi + 808.472+82.136
if RunB:
    TotalLumi = TotalLumi + 4429.
if RunC:
    TotalLumi = TotalLumi + 495.003+6383.

TotalLumi = TotalLumi/1000.

labelcms = TPaveText(0.12,0.88,0.6,0.92,"NDCBR")
labelcms.SetTextAlign(12)
labelcms.SetTextSize(0.045)
labelcms.SetFillColor(kWhite)
labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV")
labelcms.SetBorderSize(0)



doChannel = [emuChan, mumuChan, eeChan]
    
plotInfo = [['ptjet',27,30,300, 'P_{T} leading jet [GeV]'],
            ['ptlep0',28,20,300, 'P_{T} lepton-0 [GeV]'],
            ['ptlep1',28,20,300, 'P_{T} lepton-1 [GeV]'],
            ['jetCSV',100,0,1, 'Jet CSV'],
            ['ht',60,0,600, 'H_{T} [GeV]'],
            ['htNoMet',60,0,600, 'H_{T} - no MET [GeV]'],
            ['msys',60,0,600, 'Mass-system [GeV]'],
            ['mjll',60,0,600, 'Mass-jll [GeV]'],
            ['mjl0',60,0,600, 'Mass-jl0 [GeV]'],
            ['mjl1',60,0,600, 'Mass-jl1 [GeV]'],
            ['ptsys',50,0,200, 'P_{T} system [GeV]'],
            ['ptjll',30,0,300, 'P_{T}-jll [GeV]'],
            ['ptjl0',30,0,300, 'P_{T}-jl_{0} [GeV]'],
            ['ptjl1',30,0,300, 'P_{T}-jl_{1} [GeV]'],
            ['ptjl0met',30,0,300, 'P_{T}-jl_{0}MET [GeV]'],
            ['ptjl1met',30,0,300, 'P_{T}-jl_{1}MET [GeV]'],
            ['ptjlmetmin',30,0,300, 'P_{T}-jlMETmin [GeV]'],
            ['ptjlmetmax',30,0,300, 'P_{T}-jlMETmax [GeV]'],
            ['ptjlmin',30,0,300, 'P_{T}-jlmin [GeV]'],
            ['ptjlmax',30,0,300, 'P_{T}-jlmax [GeV]'],
            ['mjl0met',50,0,500, 'Mass-jl_{0}MET [GeV]'],
            ['mjl1met',50,0,500, 'Mass-jl_{1}MET [GeV]'],
            ['mjlmetmin',50,0,500, 'Mass-jlMETmin [GeV]'],
            ['mjlmetmax',50,0,500, 'Mass-jlMETmax [GeV]'],
            ['mjlmin',30,0,300, 'Mass-jlmin [GeV]'],
            ['mjlmax',30,0,300, 'Mass-jlmax [GeV]'],
            ['ptleps',30,0,300, 'P_{T}-leptons [GeV]'],
            ['htleps',30,0,300, 'H_{T}-leptons [GeV]'],
            ['ptsys_ht',40,0,1, 'P_{T} system / H_{T}'],
            ['ptjet_ht',40,0,1, 'P_{T} jet / H_{T}'],
            ['ptlep0_ht',40,0,1, 'P_{T} l_{0} / H_{T}'],
            ['ptlep1_ht',40,0,1, 'P_{T} l_{1} / H_{T}'],
            ['ptleps_ht',40,0,1, 'P_{T} leptons / H_{T}'],
            ['htleps_ht',40,0,1, 'H_{T} leptons / H_{T}'],
            ['NlooseJet15Central',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| < 2.4'],
            ['NlooseJet15Forward',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| > 2.4'],
            ['NlooseJet20Central',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| < 2.4'],
            ['NlooseJet20Forward',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| > 2.4'],
            ['NlooseJet25Central',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| < 2.4'],
            ['NlooseJet25Forward',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| > 2.4'],
            ['NtightJetForward',10,0,10, 'Number of loose jets, P_{T} > 30, |#eta| > 2.4'],            
            ['NlooseJet15',10,0,10, 'Number of loose jets, P_{T} > 15'],
            ['NlooseJet20',10,0,10, 'Number of loose jets, P_{T} > 20'],
            ['NlooseJet25',10,0,10, 'Number of loose jets, P_{T} > 25'],
            ['NbtaggedlooseJet15',4,0,4, 'Number of b-tagged loose jets, P_{T} > 15'],
            ['NbtaggedlooseJet20',4,0,4, 'Number of b-tagged loose jets, P_{T} > 20'],
            ['NbtaggedlooseJet25',4,0,4, 'Number of b-tagged loose jets, P_{T} > 25'],
            ['unweightedEta_Avg', 30,0,15,'unweightedEta_Avg'],
            ['unweightedEta_Vecjll', 60,0,30,'unweightedEta_Vecjll'],
            ['unweightedEta_Vecsys', 60,0,30,'unweightedEta_Vecsys'],
            ['unweightedPhi_Avg', 40,0,20,'unweightedPhi_Avg'],
            ['unweightedPhi_Vecjll', 40,0,20,'unweightedPhi_Vecjll'],
            ['unweightedPhi_Vecsys', 40,0,20,'unweightedPhi_Vecsys'],
            ['avgEta', 50,0,2.5,'Average #eta'],
            ['sysEta', 40, 0,5,'#eta of system'],
            ['jllEta', 40, 0,5,'#eta of jll'],
            ['dRleps', 60, 0,6,'#Delta R leptons'],
            ['dRjlmin', 60, 0,6,'#Delta R(jet,closest lepton)'],
            ['dRjlmax', 60, 0,6,'#Delta R(jet,farthest lepton)'],
            ['dEtaleps', 25, 0,5,'#Delta #eta leptons'],
            ['dEtajlmin', 25, 0,5,'#Delta #eta (jet,closest lepton)'],
            ['dEtajlmax', 25, 0,5,'#Delta #eta (jet,farthest lepton)'],
            ['dPhileps', 25, 0,3.15,'#Delta #phi leptons'],
            ['dPhijlmin', 25, 0,3.15,'#Delta #phi (jet,closest lepton)'],
            ['dPhijlmax', 25, 0,3.15,'#Delta #phi (jet,farthest lepton)'],
            ['dPhimetlmin',25,0,3.15,'#Delta #phi (MET,closest lepton)'],
            ['dPhimetlmax',25,0,3.15,'#Delta #phi (MET,farthest lepton)'],
            ['dPhijmet',25,0,3.15,'#Delta #phi (jet,MET)'],
            ['met', 60, 0, 300,'MET [GeV]'],
            ['etajet', 24, 0, 2.4, '#eta jet'],
            ['etalep0', 25, 0, 2.5, '#eta lepton-0'],
            ['etalep1', 25, 0, 2.5, '#eta lepton-1'],
            ['phijet', 40, -3.15, 3.15, '#phi jet'],
            ['philep0', 40, -3.15, 3.15, '#phi lepton-0'],
            ['philep1', 40, -3.15, 3.15, '#phi lepton-1'],
            ['phimet', 40, -3.15, 3.15, '#phi MET'],
            ['sumeta2', 40, 0, 15, '#Sigma #eta^{2}'],
            ['loosejetPt', 60, 0, 300, 'P_{T} ofvloose jet [GeV]'],
            ['loosejetCSV', 55, -0.1, 1.0, 'CSV of loose jet'],
            ['centralityJLL',40,0,1,'Centrality - jll'],
            ['centralityJLLM',40,0,1,'Centrality of system'],
            ['centralityJLLWithLoose',40,0,1,'Centrality - jll + loose jets'],
            ['centralityJLLMWithLoose',40,0,1,'Centrality - system + loose jets'],
            ['sphericityJLL',40,0,1,'Sphericity - jll'],
            ['sphericityJLLM',40,0,1,'Sphericity - system'],
            ['sphericityJLLWithLoose',40,0,1,'Sphericity - jll + loose jets'],
            ['sphericityJLLMWithLoose',40,0,1,'Sphericity - system + loose jets'],
            ['aplanarityJLL',40,0,.5,'Aplanarity - jll'],
            ['aplanarityJLLM',40,0,.5,'Aplanarity - system'],
            ['aplanarityJLLWithLoose',40,0,.5,'Aplanarity - jll + loose jets'],
            ['aplanarityJLLMWithLoose',40,0,.5,'Aplanarity - system + loost jets'],

            ]

drawZ = False
if 'Zpeak' in region:
    drawZ = True

fileList = ['TWChannel.root',
            'TTbar.root'
            ]

if drawZ:
    fileList.append('ZJets.root')

Colors = [kAzure-3,
          kRed+1,
          kGreen-3
          ]


Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
ChanLabels = [', e#mu channel',', #mu#mu channel',', ee channel', ', e#mu/#mu#mu/ee channels']


HistoLists = list()

for mode in range(3):

    if not doChannel[mode]:
        continue

    HistoMode = list()

    for i in range(len(fileList)):
        Histos = dict()

        fileName = fileList[i].split('.')[0]
        for plot in plotInfo:
            Histos[plot[0]] = TH1F(plot[0]+fileName+ChanName[mode]," ",plot[1],plot[2],plot[3])
            Histos[plot[0]].SetLineColor(Colors[i])
            Histos[plot[0]].SetLineWidth(2)
        HistoMode.append(Histos)
    HistoLists.append(HistoMode)

HistoMode = list()

for i in range(len(fileList)):
    Histos = dict()
    
    fileName = fileList[i].split('.')[0]
    for plot in plotInfo:
        Histos[plot[0]] = TH1F(plot[0]+fileName," ",plot[1],plot[2],plot[3])
        Histos[plot[0]].SetLineColor(Colors[i])
        Histos[plot[0]].SetLineWidth(2)
    HistoMode.append(Histos)

HistoLists.append(HistoMode)


for mode in range(3):

    if not doChannel[mode]:
        continue
    
    for i in range(len(fileList)):

        print fileList[i]

        tree = TChain(Folder[mode]+'/'+region)

        if fileList[i] == 'DATA':
            if RunA:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012A.root')
            if RunB:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012B.root')
            if RunC:
                tree.Add('tmvaFiles/'+vFolder+'/Data_'+DataChannel[mode]+'_Run2012C.root')

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



            _ptjet                     = event.ptjet                   
            _ptlep0                    = event.ptlep0                  
            _ptlep1                    = event.ptlep1                  
            _jetCSV                    = event.jetCSV                  
            _ht                        = event.ht                      
            _htNoMet                   = event.htNoMet                 
            _msys                      = event.msys                    
            _mjll                      = event.mjll                    
            _mjl0                      = event.mjl0                    
            _mjl1                      = event.mjl1                    
            _ptsys                     = event.ptsys                   
            _ptjll                     = event.ptjll                   
            _ptjl0                     = event.ptjl0                   
            _ptjl1                     = event.ptjl1
            _ptjl0met                  = event.ptjl0met
            _ptjl1met                  = event.ptjl1met         
            _ptjlmetmin                = event.ptjlmetmin
            _ptjlmetmax                = event.ptjlmetmax
            _ptjlmin                   = event.ptjlmin
            _ptjlmax                   = event.ptjlmax
            _mjl0met                   = event.mjl0met
            _mjl1met                   = event.mjl1met         
            _mjlmetmin                 = event.mjlmetmin
            _mjlmetmax                 = event.mjlmetmax
            _mjlmin                    = event.mjlmin
            _mjlmax                    = event.mjlmax            
            _ptleps                    = event.ptleps                  
            _htleps                    = event.htleps                  
            _ptsys_ht                  = event.ptsys_ht                
            _ptjet_ht                  = event.ptjet_ht                
            _ptlep0_ht                 = event.ptlep0_ht               
            _ptlep1_ht                 = event.ptlep1_ht               
            _ptleps_ht                 = event.ptleps_ht               
            _htleps_ht                 = event.htleps_ht               
            _NlooseJet15Central        = event.NlooseJet15Central      
            _NlooseJet15Forward        = event.NlooseJet15Forward      
            _NlooseJet20Central        = event.NlooseJet20Central      
            _NlooseJet20Forward        = event.NlooseJet20Forward      
            _NlooseJet25Central        = event.NlooseJet25Central      
            _NlooseJet25Forward        = event.NlooseJet25Forward      
            _NtightJetForward          = event.NtightJetForward        
            _NlooseJet15               = event.NlooseJet15             
            _NlooseJet20               = event.NlooseJet20             
            _NlooseJet25               = event.NlooseJet25             
            _NbtaggedlooseJet15        = event.NbtaggedlooseJet15      
            _NbtaggedlooseJet20        = event.NbtaggedlooseJet20      
            _NbtaggedlooseJet25        = event.NbtaggedlooseJet25      
            _unweightedEta_Avg         = event.unweightedEta_Avg       
            _unweightedEta_Vecjll      = event.unweightedEta_Vecjll    
            _unweightedEta_Vecsys      = event.unweightedEta_Vecsys    
            _unweightedPhi_Avg         = event.unweightedPhi_Avg       
            _unweightedPhi_Vecjll      = event.unweightedPhi_Vecjll    
            _unweightedPhi_Vecsys      = event.unweightedPhi_Vecsys    
            _avgEta                    = event.avgEta                  
            _sysEta                    = event.sysEta                  
            _jllEta                    = event.jllEta                  
            _dRleps                    = event.dRleps                  
            _dRjlmin                   = event.dRjlmin                 
            _dRjlmax                   = event.dRjlmax                 
            _dEtaleps                  = event.dEtaleps                
            _dEtajlmin                 = event.dEtajlmin               
            _dEtajlmax                 = event.dEtajlmax               
            _dPhileps                  = event.dPhileps                
            _dPhijlmin                 = event.dPhijlmin               
            _dPhijlmax                 = event.dPhijlmax               
            _dPhimetlmin               = event.dPhimetlmin             
            _dPhimetlmax               = event.dPhimetlmax             
            _dPhijmet                  = event.dPhijmet                
            _met                       = event.met                     
            _etajet                    = event.etajet                  
            _etalep0                   = event.etalep0                 
            _etalep1                   = event.etalep1                 
            _phijet                    = event.phijet                  
            _philep0                   = event.philep0                 
            _philep1                   = event.philep1                 
            _phimet                    = event.phimet                  
            _sumeta2                   = event.sumeta2                 
            _loosejetPt                = event.loosejetPt              
            _loosejetCSV               = event.loosejetCSV             
            _centralityJLL             = event.centralityJLL           
            _centralityJLLM            = event.centralityJLLM          
            _centralityJLLWithLoose    = event.centralityJLLWithLoose  
            _centralityJLLMWithLoose   = event.centralityJLLMWithLoose 
            _sphericityJLL             = event.sphericityJLL           
            _sphericityJLLM            = event.sphericityJLLM          
            _sphericityJLLWithLoose    = event.sphericityJLLWithLoose  
            _sphericityJLLMWithLoose   = event.sphericityJLLMWithLoose 
            _aplanarityJLL             = event.aplanarityJLL           
            _aplanarityJLLM            = event.aplanarityJLLM          
            _aplanarityJLLWithLoose    = event.aplanarityJLLWithLoose  
            _aplanarityJLLMWithLoose   = event.aplanarityJLLMWithLoose 
            
            _weightA                    = event.weightA
            _weightB                    = event.weightB
            _weightC                    = event.weightC

            _weight = 0            


            _btagSF = 1.

            if int(vFolder.split('v')[-1]) > 1:
                _btagSF = event.weightBtagSF
            
                

            if RunA:
                _weight = _weight + _weightA
            if RunB:
                _weight = _weight + _weightB
            if RunC:
                _weight = _weight + _weightC

            _weight = _weight*_btagSF            

            if fileList[i] == 'DATA':
                _weight = 1.

            #EXTRA CUTS

            if mode > 0 and _met < 50:
                continue
            
            #             if _met < 30:
            #                 continue
            
#             if _NbtaggedlooseJet20 > 0:
#                 continue
#             if _NlooseJet15 > 0:
#                 continue
            
#             if _ptsys > 50:
#                 continue
            
#             if mode== 0 and _ht < 160:
#                 continue

            HistoLists[mode][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[mode][i]['ptlep0'].Fill(                   _ptlep0                   , _weight )
            HistoLists[mode][i]['ptlep1'].Fill(                   _ptlep1                   , _weight )
            HistoLists[mode][i]['jetCSV'].Fill(                   _jetCSV                   , _weight )
            HistoLists[mode][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[mode][i]['htNoMet'].Fill(                  _htNoMet                  , _weight )
            HistoLists[mode][i]['msys'].Fill(                     _msys                     , _weight )
            HistoLists[mode][i]['mjll'].Fill(                     _mjll                     , _weight )
            HistoLists[mode][i]['mjl0'].Fill(                     _mjl0                     , _weight )
            HistoLists[mode][i]['mjl1'].Fill(                     _mjl1                     , _weight )
            HistoLists[mode][i]['ptsys'].Fill(                    _ptsys                    , _weight )
            HistoLists[mode][i]['ptjll'].Fill(                    _ptjll                    , _weight )
            HistoLists[mode][i]['ptjl0'].Fill(                    _ptjl0                    , _weight )
            HistoLists[mode][i]['ptjl1'].Fill(                    _ptjl1                    , _weight )
            HistoLists[mode][i]['ptjl0met'].Fill(                 _ptjl0met                 , _weight )
            HistoLists[mode][i]['ptjl1met'].Fill(                 _ptjl1met                 , _weight )
            HistoLists[mode][i]['ptjlmetmin'].Fill(               _ptjlmetmin               , _weight )
            HistoLists[mode][i]['ptjlmetmax'].Fill(               _ptjlmetmax               , _weight )
            HistoLists[mode][i]['ptjlmin'].Fill(                  _ptjlmin                  , _weight )
            HistoLists[mode][i]['ptjlmax'].Fill(                  _ptjlmax                  , _weight )
            HistoLists[mode][i]['mjl0met'].Fill(                  _mjl0met                  , _weight )
            HistoLists[mode][i]['mjl1met'].Fill(                  _mjl1met                  , _weight )
            HistoLists[mode][i]['mjlmetmin'].Fill(                _mjlmetmin                , _weight )
            HistoLists[mode][i]['mjlmetmax'].Fill(                _mjlmetmax                , _weight )
            HistoLists[mode][i]['mjlmin'].Fill(                   _mjlmin                   , _weight )
            HistoLists[mode][i]['mjlmax'].Fill(                   _mjlmax                   , _weight )
            HistoLists[mode][i]['ptleps'].Fill(                   _ptleps                   , _weight )
            HistoLists[mode][i]['htleps'].Fill(                   _htleps                   , _weight )
            HistoLists[mode][i]['ptsys_ht'].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[mode][i]['ptjet_ht'].Fill(                 _ptjet_ht                 , _weight )
            HistoLists[mode][i]['ptlep0_ht'].Fill(                _ptlep0_ht                , _weight )
            HistoLists[mode][i]['ptlep1_ht'].Fill(                _ptlep1_ht                , _weight )
            HistoLists[mode][i]['ptleps_ht'].Fill(                _ptleps_ht                , _weight )
            HistoLists[mode][i]['htleps_ht'].Fill(                _htleps_ht                , _weight )
            HistoLists[mode][i]['NlooseJet15Central'].Fill(       _NlooseJet15Central       , _weight )
            HistoLists[mode][i]['NlooseJet15Forward'].Fill(       _NlooseJet15Forward       , _weight )
            HistoLists[mode][i]['NlooseJet20Central'].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[mode][i]['NlooseJet20Forward'].Fill(       _NlooseJet20Forward       , _weight )
            HistoLists[mode][i]['NlooseJet25Central'].Fill(       _NlooseJet25Central       , _weight )
            HistoLists[mode][i]['NlooseJet25Forward'].Fill(       _NlooseJet25Forward       , _weight )
            HistoLists[mode][i]['NtightJetForward'].Fill(         _NtightJetForward         , _weight )
            HistoLists[mode][i]['NlooseJet15'].Fill(              _NlooseJet15              , _weight )
            HistoLists[mode][i]['NlooseJet20'].Fill(              _NlooseJet20              , _weight )
            HistoLists[mode][i]['NlooseJet25'].Fill(              _NlooseJet25              , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet15'].Fill(       _NbtaggedlooseJet15       , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet20'].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet25'].Fill(       _NbtaggedlooseJet25       , _weight )
            HistoLists[mode][i]['unweightedEta_Avg'].Fill(        _unweightedEta_Avg        , _weight )
            HistoLists[mode][i]['unweightedEta_Vecjll'].Fill(     _unweightedEta_Vecjll     , _weight )
            HistoLists[mode][i]['unweightedEta_Vecsys'].Fill(     _unweightedEta_Vecsys     , _weight )
            HistoLists[mode][i]['unweightedPhi_Avg'].Fill(        _unweightedPhi_Avg        , _weight )
            HistoLists[mode][i]['unweightedPhi_Vecjll'].Fill(     _unweightedPhi_Vecjll     , _weight )
            HistoLists[mode][i]['unweightedPhi_Vecsys'].Fill(     _unweightedPhi_Vecsys     , _weight )
            HistoLists[mode][i]['avgEta'].Fill(                   _avgEta                   , _weight )
            HistoLists[mode][i]['sysEta'].Fill(                   _sysEta                   , _weight )
            HistoLists[mode][i]['jllEta'].Fill(                   _jllEta                   , _weight )
            HistoLists[mode][i]['dRleps'].Fill(                   _dRleps                   , _weight )
            HistoLists[mode][i]['dRjlmin'].Fill(                  _dRjlmin                  , _weight )
            HistoLists[mode][i]['dRjlmax'].Fill(                  _dRjlmax                  , _weight )
            HistoLists[mode][i]['dEtaleps'].Fill(                 _dEtaleps                 , _weight )
            HistoLists[mode][i]['dEtajlmin'].Fill(                _dEtajlmin                , _weight )
            HistoLists[mode][i]['dEtajlmax'].Fill(                _dEtajlmax                , _weight )
            HistoLists[mode][i]['dPhileps'].Fill(                 _dPhileps                 , _weight )
            HistoLists[mode][i]['dPhijlmin'].Fill(                _dPhijlmin                , _weight )
            HistoLists[mode][i]['dPhijlmax'].Fill(                _dPhijlmax                , _weight )
            HistoLists[mode][i]['dPhimetlmin'].Fill(              _dPhimetlmin              , _weight )
            HistoLists[mode][i]['dPhimetlmax'].Fill(              _dPhimetlmax              , _weight )
            HistoLists[mode][i]['dPhijmet'].Fill(                 _dPhijmet                 , _weight )
            HistoLists[mode][i]['met'].Fill(                      _met                      , _weight )
            HistoLists[mode][i]['etajet'].Fill(                   _etajet                   , _weight )
            HistoLists[mode][i]['etalep0'].Fill(                  _etalep0                  , _weight )
            HistoLists[mode][i]['etalep1'].Fill(                  _etalep1                  , _weight )
            HistoLists[mode][i]['phijet'].Fill(                   _phijet                   , _weight )
            HistoLists[mode][i]['philep0'].Fill(                  _philep0                  , _weight )
            HistoLists[mode][i]['philep1'].Fill(                  _philep1                  , _weight )
            HistoLists[mode][i]['phimet'].Fill(                   _phimet                   , _weight )
            HistoLists[mode][i]['sumeta2'].Fill(                  _sumeta2                  , _weight )
            HistoLists[mode][i]['loosejetPt'].Fill(               _loosejetPt               , _weight )
            HistoLists[mode][i]['loosejetCSV'].Fill(              _loosejetCSV              , _weight )
            HistoLists[mode][i]['centralityJLL'].Fill(            _centralityJLL            , _weight )
            HistoLists[mode][i]['centralityJLLM'].Fill(           _centralityJLLM           , _weight )
            HistoLists[mode][i]['centralityJLLWithLoose'].Fill(   _centralityJLLWithLoose   , _weight )
            HistoLists[mode][i]['centralityJLLMWithLoose'].Fill(  _centralityJLLMWithLoose  , _weight )
            HistoLists[mode][i]['sphericityJLL'].Fill(            _sphericityJLL            , _weight )
            HistoLists[mode][i]['sphericityJLLM'].Fill(           _sphericityJLLM           , _weight )
            HistoLists[mode][i]['sphericityJLLWithLoose'].Fill(   _sphericityJLLWithLoose   , _weight )
            HistoLists[mode][i]['sphericityJLLMWithLoose'].Fill(  _sphericityJLLMWithLoose  , _weight )
            HistoLists[mode][i]['aplanarityJLL'].Fill(            _aplanarityJLL            , _weight )
            HistoLists[mode][i]['aplanarityJLLM'].Fill(           _aplanarityJLLM           , _weight )
            HistoLists[mode][i]['aplanarityJLLWithLoose'].Fill(   _aplanarityJLLWithLoose   , _weight )
            HistoLists[mode][i]['aplanarityJLLMWithLoose'].Fill(  _aplanarityJLLMWithLoose  , _weight )




            HistoLists[-1][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[-1][i]['ptlep0'].Fill(                   _ptlep0                   , _weight )
            HistoLists[-1][i]['ptlep1'].Fill(                   _ptlep1                   , _weight )
            HistoLists[-1][i]['jetCSV'].Fill(                   _jetCSV                   , _weight )
            HistoLists[-1][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[-1][i]['htNoMet'].Fill(                  _htNoMet                  , _weight )
            HistoLists[-1][i]['msys'].Fill(                     _msys                     , _weight )
            HistoLists[-1][i]['mjll'].Fill(                     _mjll                     , _weight )
            HistoLists[-1][i]['mjl0'].Fill(                     _mjl0                     , _weight )
            HistoLists[-1][i]['mjl1'].Fill(                     _mjl1                     , _weight )
            HistoLists[-1][i]['ptsys'].Fill(                    _ptsys                    , _weight )
            HistoLists[-1][i]['ptjll'].Fill(                    _ptjll                    , _weight )
            HistoLists[-1][i]['ptjl0'].Fill(                    _ptjl0                    , _weight )
            HistoLists[-1][i]['ptjl1'].Fill(                    _ptjl1                    , _weight )
            HistoLists[-1][i]['ptjl0met'].Fill(                 _ptjl0met                 , _weight )
            HistoLists[-1][i]['ptjl1met'].Fill(                 _ptjl1met                 , _weight )
            HistoLists[-1][i]['ptjlmetmin'].Fill(               _ptjlmetmin               , _weight )
            HistoLists[-1][i]['ptjlmetmax'].Fill(               _ptjlmetmax               , _weight )
            HistoLists[-1][i]['ptjlmin'].Fill(                  _ptjlmin                  , _weight )
            HistoLists[-1][i]['ptjlmax'].Fill(                  _ptjlmax                  , _weight )
            HistoLists[-1][i]['mjl0met'].Fill(                  _mjl0met                  , _weight )
            HistoLists[-1][i]['mjl1met'].Fill(                  _mjl1met                  , _weight )
            HistoLists[-1][i]['mjlmetmin'].Fill(                _mjlmetmin                , _weight )
            HistoLists[-1][i]['mjlmetmax'].Fill(                _mjlmetmax                , _weight )
            HistoLists[-1][i]['mjlmin'].Fill(                   _mjlmin                   , _weight )
            HistoLists[-1][i]['mjlmax'].Fill(                   _mjlmax                   , _weight )
            HistoLists[-1][i]['ptleps'].Fill(                   _ptleps                   , _weight )
            HistoLists[-1][i]['htleps'].Fill(                   _htleps                   , _weight )
            HistoLists[-1][i]['ptsys_ht'].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[-1][i]['ptjet_ht'].Fill(                 _ptjet_ht                 , _weight )
            HistoLists[-1][i]['ptlep0_ht'].Fill(                _ptlep0_ht                , _weight )
            HistoLists[-1][i]['ptlep1_ht'].Fill(                _ptlep1_ht                , _weight )
            HistoLists[-1][i]['ptleps_ht'].Fill(                _ptleps_ht                , _weight )
            HistoLists[-1][i]['htleps_ht'].Fill(                _htleps_ht                , _weight )
            HistoLists[-1][i]['NlooseJet15Central'].Fill(       _NlooseJet15Central       , _weight )
            HistoLists[-1][i]['NlooseJet15Forward'].Fill(       _NlooseJet15Forward       , _weight )
            HistoLists[-1][i]['NlooseJet20Central'].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[-1][i]['NlooseJet20Forward'].Fill(       _NlooseJet20Forward       , _weight )
            HistoLists[-1][i]['NlooseJet25Central'].Fill(       _NlooseJet25Central       , _weight )
            HistoLists[-1][i]['NlooseJet25Forward'].Fill(       _NlooseJet25Forward       , _weight )
            HistoLists[-1][i]['NtightJetForward'].Fill(         _NtightJetForward         , _weight )
            HistoLists[-1][i]['NlooseJet15'].Fill(              _NlooseJet15              , _weight )
            HistoLists[-1][i]['NlooseJet20'].Fill(              _NlooseJet20              , _weight )
            HistoLists[-1][i]['NlooseJet25'].Fill(              _NlooseJet25              , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet15'].Fill(       _NbtaggedlooseJet15       , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet20'].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet25'].Fill(       _NbtaggedlooseJet25       , _weight )
            HistoLists[-1][i]['unweightedEta_Avg'].Fill(        _unweightedEta_Avg        , _weight )
            HistoLists[-1][i]['unweightedEta_Vecjll'].Fill(     _unweightedEta_Vecjll     , _weight )
            HistoLists[-1][i]['unweightedEta_Vecsys'].Fill(     _unweightedEta_Vecsys     , _weight )
            HistoLists[-1][i]['unweightedPhi_Avg'].Fill(        _unweightedPhi_Avg        , _weight )
            HistoLists[-1][i]['unweightedPhi_Vecjll'].Fill(     _unweightedPhi_Vecjll     , _weight )
            HistoLists[-1][i]['unweightedPhi_Vecsys'].Fill(     _unweightedPhi_Vecsys     , _weight )
            HistoLists[-1][i]['avgEta'].Fill(                   _avgEta                   , _weight )
            HistoLists[-1][i]['sysEta'].Fill(                   _sysEta                   , _weight )
            HistoLists[-1][i]['jllEta'].Fill(                   _jllEta                   , _weight )
            HistoLists[-1][i]['dRleps'].Fill(                   _dRleps                   , _weight )
            HistoLists[-1][i]['dRjlmin'].Fill(                  _dRjlmin                  , _weight )
            HistoLists[-1][i]['dRjlmax'].Fill(                  _dRjlmax                  , _weight )
            HistoLists[-1][i]['dEtaleps'].Fill(                 _dEtaleps                 , _weight )
            HistoLists[-1][i]['dEtajlmin'].Fill(                _dEtajlmin                , _weight )
            HistoLists[-1][i]['dEtajlmax'].Fill(                _dEtajlmax                , _weight )
            HistoLists[-1][i]['dPhileps'].Fill(                 _dPhileps                 , _weight )
            HistoLists[-1][i]['dPhijlmin'].Fill(                _dPhijlmin                , _weight )
            HistoLists[-1][i]['dPhijlmax'].Fill(                _dPhijlmax                , _weight )
            HistoLists[-1][i]['dPhimetlmin'].Fill(              _dPhimetlmin              , _weight )
            HistoLists[-1][i]['dPhimetlmax'].Fill(              _dPhimetlmax              , _weight )
            HistoLists[-1][i]['dPhijmet'].Fill(                 _dPhijmet                 , _weight )
            HistoLists[-1][i]['met'].Fill(                      _met                      , _weight )
            HistoLists[-1][i]['etajet'].Fill(                   _etajet                   , _weight )
            HistoLists[-1][i]['etalep0'].Fill(                  _etalep0                  , _weight )
            HistoLists[-1][i]['etalep1'].Fill(                  _etalep1                  , _weight )
            HistoLists[-1][i]['phijet'].Fill(                   _phijet                   , _weight )
            HistoLists[-1][i]['philep0'].Fill(                  _philep0                  , _weight )
            HistoLists[-1][i]['philep1'].Fill(                  _philep1                  , _weight )
            HistoLists[-1][i]['phimet'].Fill(                   _phimet                   , _weight )
            HistoLists[-1][i]['sumeta2'].Fill(                  _sumeta2                  , _weight )
            HistoLists[-1][i]['loosejetPt'].Fill(               _loosejetPt               , _weight )
            HistoLists[-1][i]['loosejetCSV'].Fill(              _loosejetCSV              , _weight )
            HistoLists[-1][i]['centralityJLL'].Fill(            _centralityJLL            , _weight )
            HistoLists[-1][i]['centralityJLLM'].Fill(           _centralityJLLM           , _weight )
            HistoLists[-1][i]['centralityJLLWithLoose'].Fill(   _centralityJLLWithLoose   , _weight )
            HistoLists[-1][i]['centralityJLLMWithLoose'].Fill(  _centralityJLLMWithLoose  , _weight )
            HistoLists[-1][i]['sphericityJLL'].Fill(            _sphericityJLL            , _weight )
            HistoLists[-1][i]['sphericityJLLM'].Fill(           _sphericityJLLM           , _weight )
            HistoLists[-1][i]['sphericityJLLWithLoose'].Fill(   _sphericityJLLWithLoose   , _weight )
            HistoLists[-1][i]['sphericityJLLMWithLoose'].Fill(  _sphericityJLLMWithLoose  , _weight )
            HistoLists[-1][i]['aplanarityJLL'].Fill(            _aplanarityJLL            , _weight )
            HistoLists[-1][i]['aplanarityJLLM'].Fill(           _aplanarityJLLM           , _weight )
            HistoLists[-1][i]['aplanarityJLLWithLoose'].Fill(   _aplanarityJLLWithLoose   , _weight )
            HistoLists[-1][i]['aplanarityJLLMWithLoose'].Fill(  _aplanarityJLLMWithLoose  , _weight )


        print

leg = TLegend(0.82,0.78,0.94,0.94)
leg.SetFillStyle(1)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(0.045)
leg.AddEntry(HistoLists[0][0]['ptjet'], "tW", "l")
leg.AddEntry(HistoLists[0][1]['ptjet'], "t#bar{t}", "l")
if drawZ:
    leg.AddEntry(HistoLists[0][2]['ptjet'], "Z/#gamma*+jets", "l")


for mode in range(4):

    labelcms2 = TPaveText(0.12,0.82,0.6,0.88,"NDCBR")
    labelcms2.SetTextAlign(12)
    labelcms2.SetTextSize(0.045)
    labelcms2.SetFillColor(kWhite)
    labelcms2.AddText(region+ChanLabels[mode]) 
    labelcms2.SetBorderSize(0)
    
    for plot in plotInfo:
        
        c1 = TCanvas()
        tW = HistoLists[mode][0][plot[0]]
        tt = HistoLists[mode][1][plot[0]]
        tWmax = tW.GetMaximum()/tW.Integral()
        ttmax = tt.GetMaximum()/tt.Integral()
        Zmax = 0
        if drawZ:
            Z = HistoLists[mode][2][plot[0]]
            Zmax = Z.GetMaximum()/Z.Integral()
        max_ = max(tWmax, ttmax)
        if drawZ:
            max_ = max(max_,Zmax)
        
        frame = TH1F(plot[0]+"frame"+str(mode),"",plot[1],plot[2],plot[3])
        frame.SetMaximum(max_*1.25)
        frame.SetMinimum(0)
        frame.Draw()
        tW.DrawNormalized("same")
        tt.DrawNormalized("same")
        if drawZ:
            Z.DrawNormalized("same")
        frame.GetYaxis().SetTitle("Normalized Events")
        frame.GetYaxis().CenterTitle()
        frame.GetXaxis().SetTitle(plot[4])
        

        leg.Draw()        
        labelcms.Draw()
        labelcms2.Draw()
        
        if not os.path.exists("ShapePlots/"+specialName):
            command = "mkdir ShapePlots/"+specialName
            os.system(command)
        if not os.path.exists("ShapePlots/"+specialName + region):
            command = "mkdir ShapePlots/"+specialName+region
            os.system(command)

        channel = ""
        if mode < 3:
            channel = "_" + ChanName[mode]
        c1.SaveAs("ShapePlots/"+specialName+region+"/"+plot[0]+"_"+region+channel+".pdf")

