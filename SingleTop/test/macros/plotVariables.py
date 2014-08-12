#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array
from ZjetSF_3 import *
# from ZjetSF import *
from errorLists import *


import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

AllowedRegions = ['1j0t','1j1t','1jNoTagging','2j0t','2j1t','2j2t','2jNoTagging','3plusjNoTagging','1j1tZpeak','ZpeakLepSel','2plusjets1plustag','3plusjets1plustag','tree1j1tNomllMetCut','3j0t','3j1t','3j2t','3j3t']

region = '1j1t'
runPicked = False
RunA = False
RunB = False
RunC = False
RunD = False

TotalLumi = 0.

channelPicked = False
emuChan = False
mumuChan = False
eeChan = False
combinedChan = False

versionPicked = False

#specialName = 'NewTTbarFiles'
# specialName = 'ZjetSF3'
#specialName = 'OldTTbarTest'
specialName = ''

noPlots = False

useZjetsSF = True

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
    elif arg == 'noPlots':
        noPlots = True
    elif arg == 'noZjetSF':
        useZjetsSF = False
        specialName += 'NoZjetSF'
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

if noPlots:
    print "Not Making Plots"
        
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
    versionList = glob.glob("tmvaFiles/v*")
    versionList.sort(key=lambda a:int(a.split('/v')[-1].split('_')[0]))
    vFolder = versionList[-1].split('/')[-1]    
    print vFolder

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

doZpeakCuts = False

if '1j1tZpeak' in region:
    doZpeakCuts = True

TotalLumi = TotalLumi/1000.

labelcms = TPaveText(0.12,0.88,0.6,0.92,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.045);
labelcms.SetFillColor(kWhite);
labelcms.SetFillStyle(0);
labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
labelcms.SetBorderSize(0);

#gStyle.SetLabelSize(0.045,"x")
gStyle.SetLabelSize(0.035,"xy")


doChannel = [emuChan, mumuChan, eeChan, combinedChan]

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
            'jetCSV',
            'etajet',
            ]
    
plotInfo = [['ptjet',27,30,300, 'P_{T} leading jet [GeV]','Events / 10 GeV'],
            ['ptlep0',28,20,300, 'P_{T} lepton-0 [GeV]','Events / 10 GeV'],
            ['ptlep1',28,20,300, 'P_{T} lepton-1 [GeV]','Events / 10 GeV'],
            ['jetCSV',100,0,1, 'Jet CSV','Events'],
            ['ht',60,0,600, 'H_{T} [GeV]','Events / 10 GeV'],
            ['htNoMet',60,0,600, 'H_{T} - no MET [GeV]','Events / 10 GeV'],
            ['msys',60,0,600, 'Mass-system [GeV]','Events / 10 GeV'],
            ['mll',60,0,600, 'Mass-leptons [GeV]','Events / 10 GeV'],
            ['mjll',60,0,600, 'Mass-jll [GeV]','Events / 10 GeV'],
            ['mjl0',60,0,600, 'Mass-jl0 [GeV]','Events / 10 GeV'],
            ['mjl1',60,0,600, 'Mass-jl1 [GeV]','Events / 10 GeV'],
            ['ptsys',50,0,200, 'P_{T} system [GeV]','Events / 4 GeV'],
            ['ptjll',30,0,300, 'P_{T}-jll [GeV]','Events / 10 GeV'],
            ['ptjl0',30,0,300, 'P_{T}-jl_{0} [GeV]','Events / 10 GeV'],
            ['ptjl1',30,0,300, 'P_{T}-jl_{1} [GeV]','Events / 10 GeV'],
            ['ptjl0met',30,0,300, 'P_{T}-jl_{0}MET [GeV]','Events / 10 GeV'],
            ['ptjl1met',30,0,300, 'P_{T}-jl_{1}MET [GeV]','Events / 10 GeV'],
            ['ptjlmetmin',30,0,300, 'P_{T}-jlMETmin [GeV]','Events / 10 GeV'],
            ['ptjlmetmax',30,0,300, 'P_{T}-jlMETmax [GeV]','Events / 10 GeV'],
            ['ptjlmin',30,0,300, 'P_{T}-jlmin [GeV]','Events / 10 GeV'],
            ['ptjlmax',30,0,300, 'P_{T}-jlmax [GeV]','Events / 10 GeV'],
            ['mjl0met',50,0,500, 'Mass-jl_{0}MET [GeV]','Events / 10 GeV'],
            ['mjl1met',50,0,500, 'Mass-jl_{1}MET [GeV]','Events / 10 GeV'],
            ['mjlmetmin',50,0,500, 'Mass-jlMETmin [GeV]','Events / 10 GeV'],
            ['mjlmetmax',50,0,500, 'Mass-jlMETmax [GeV]','Events / 10 GeV'],
            ['mjlmin',30,0,300, 'Mass-jlmin [GeV]','Events / 10 GeV'],
            ['mjlmax',30,0,300, 'Mass-jlmax [GeV]','Events / 10 GeV'],
            ['ptleps',30,0,300, 'P_{T}-leptons [GeV]','Events / 10 GeV'],
            ['htleps',30,0,300, 'H_{T}-leptons [GeV]','Events / 10 GeV'],
            ['ptsys_ht',40,0,1, 'P_{T} system / H_{T}','Events'],
            ['ptjet_ht',40,0,1, 'P_{T} jet / H_{T}','Events'],
            ['ptlep0_ht',40,0,1, 'P_{T} l_{0} / H_{T}','Events'],
            ['ptlep1_ht',40,0,1, 'P_{T} l_{1} / H_{T}','Events'],
            ['ptleps_ht',40,0,1, 'P_{T} leptons / H_{T}','Events'],
            ['htleps_ht',40,0,1, 'H_{T} leptons / H_{T}','Events'],
            ['NlooseJet15Central',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| < 2.4','Events'],
            ['NlooseJet15Forward',10,0,10, 'Number of loose jets, P_{T} > 15, |#eta| > 2.4','Events'],
            ['NlooseJet20Central',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| < 2.4','Events'],
            ['NlooseJet20Forward',10,0,10, 'Number of loose jets, P_{T} > 20, |#eta| > 2.4','Events'],
            ['NlooseJet25Central',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| < 2.4','Events'],
            ['NlooseJet25Forward',10,0,10, 'Number of loose jets, P_{T} > 25, |#eta| > 2.4','Events'],
            ['NtightJetForward',10,0,10, 'Number of loose jets, P_{T} > 30, |#eta| > 2.4','Events'],            
            ['NlooseJet15',10,0,10, 'Number of loose jets, P_{T} > 15','Events'],
            ['NlooseJet20',10,0,10, 'Number of loose jets, P_{T} > 20','Events'],
            ['NlooseJet25',10,0,10, 'Number of loose jets, P_{T} > 25','Events'],
            ['NbtaggedlooseJet15',4,0,4, 'Number of b-tagged loose jets, P_{T} > 15','Events'],
            ['NbtaggedlooseJet20',4,0,4, 'Number of b-tagged loose jets, P_{T} > 20','Events'],
            ['NbtaggedlooseJet25',4,0,4, 'Number of b-tagged loose jets, P_{T} > 25','Events'],
            ['unweightedEta_Avg', 30,0,15,'unweightedEta_Avg','Events'],
            ['unweightedEta_Vecjll', 60,0,30,'unweightedEta_Vecjll','Events'],
            ['unweightedEta_Vecsys', 60,0,30,'unweightedEta_Vecsys','Events'],
            ['unweightedPhi_Avg', 40,0,20,'unweightedPhi_Avg','Events'],
            ['unweightedPhi_Vecjll', 40,0,20,'unweightedPhi_Vecjll','Events'],
            ['unweightedPhi_Vecsys', 40,0,20,'unweightedPhi_Vecsys','Events'],
            ['avgEta', 50,0,2.5,'Average #eta','Events'],
            ['sysEta', 40, 0,5,'#eta of system','Events'],
            ['jllEta', 40, 0,5,'#eta of jll','Events'],
            ['dRleps', 60, 0,6,'#Delta R leptons','Events'],
            ['dRjlmin', 60, 0,6,'#Delta R(jet,closest lepton)','Events'],
            ['dRjlmax', 60, 0,6,'#Delta R(jet,farthest lepton)','Events'],
            ['dEtaleps', 25, 0,5,'#Delta #eta leptons','Events'],
            ['dEtajlmin', 25, 0,5,'#Delta #eta (jet,closest lepton)','Events'],
            ['dEtajlmax', 25, 0,5,'#Delta #eta (jet,farthest lepton)','Events'],
            ['dPhileps', 25, 0,3.15,'#Delta #phi leptons','Events'],
            ['dPhijlmin', 25, 0,3.15,'#Delta #phi (jet,closest lepton)','Events'],
            ['dPhijlmax', 25, 0,3.15,'#Delta #phi (jet,farthest lepton)','Events'],
            ['dPhimetlmin',25,0,3.15,'#Delta #phi (MET,closest lepton)','Events'],
            ['dPhimetlmax',25,0,3.15,'#Delta #phi (MET,farthest lepton)','Events'],
            ['dPhijmet',25,0,3.15,'#Delta #phi (jet,MET)','Events'],
            ['met', 60, 0, 300,'MET [GeV]','Events / 5 GeV'],
            ['etajet', 24, 0, 2.4, '#eta jet','Events'],
            ['etalep0', 25, 0, 2.5, '#eta lepton-0','Events'],
            ['etalep1', 25, 0, 2.5, '#eta lepton-1','Events'],
            ['phijet', 40, -3.15, 3.15, '#phi jet','Events'],
            ['philep0', 40, -3.15, 3.15, '#phi lepton-0','Events'],
            ['philep1', 40, -3.15, 3.15, '#phi lepton-1','Events'],
            ['phimet', 40, -3.15, 3.15, '#phi MET','Events'],
            ['sumeta2', 40, 0, 15, '#Sigma #eta^{2}','Events'],
            ['loosejetPt', 60, 0, 300, 'P_{T} of loose jet [GeV]','Events / 5 GeV'],
            ['loosejetCSV', 55, -0.1, 1.0, 'CSV of loose jet','Events'],
            ['centralityJLL',40,0,1,'Centrality - jll','Events'],
            ['centralityJLLM',40,0,1,'Centrality of system','Events'],
            ['centralityJLLWithLoose',40,0,1,'Centrality - jll + loose jets','Events'],
            ['centralityJLLMWithLoose',40,0,1,'Centrality - system + loose jets','Events'],
            ['sphericityJLL',40,0,1,'Sphericity - jll','Events'],
            ['sphericityJLLM',40,0,1,'Sphericity - system','Events'],
            ['sphericityJLLWithLoose',40,0,1,'Sphericity - jll + loose jets','Events'],
            ['sphericityJLLMWithLoose',40,0,1,'Sphericity - system + loose jets','Events'],
            ['aplanarityJLL',40,0,.5,'Aplanarity - jll','Events'],
            ['aplanarityJLLM',40,0,.5,'Aplanarity - system','Events'],
            ['aplanarityJLLWithLoose',40,0,.5,'Aplanarity - jll + loose jets','Events'],
            ['aplanarityJLLMWithLoose',40,0,.5,'Aplanarity - system + loost jets','Events'],
            ['lepJetPt_PosLep',40,0,300,'P_{T} jet & positive-lepton','Events'],
            ['lepPt_PosLep',40,0,300,'P_{T} positive-lepton','Events'],
            ['lepJetDR_PosLep',40,0,6,'#Delta R(jet,positive-lepton)','Events'],
            ['lepJetDPhi_PosLep',40,0,3.2,'#Delta #phi (jet,positive-lepton)','Events'],
            ['lepJetDEta_PosLep',40,0,5,'#Delta #eta (jet,positive-lepton)','Events'],
            ['lepJetM_PosLep',40,0,300,'Mass of jet & positive-lepton','Events'],
            ['lepPtRelJet_PosLep',40,0,200,'P_{T} positive-lepton relative to jet','Events'],
            ['jetPtRelLep_PosLep',40,0,200,'P_{T} jet relative to positive-lepton','Events'],
            ['lepPtRelJetSameLep_PosLep',40,0,200,'P_{T} pos-lepton relative to jet & pos-lep','Events'],
            ['lepPtRelJetOtherLep_PosLep',40,0,200,'P_{T} pos-lepton relative to jet & neg-lep','Events'],
            ['lepJetMt_PosLep',40,0,300,'M_{T} jet & positive-lepton','Events'],
            ['lepJetCosTheta_boosted_PosLep',40,-1.,1.,'Cos #theta (positive-lepton,jet)','Events'],
            ['lepJetPt_NegLep',40,0,300,'P_{T} jet & negative-lepton','Events'],
            ['lepPt_NegLep',40,0,300,'P_{T} negative-lepton','Events'],
            ['lepJetDR_NegLep',40,0,6,'#Delta R(jet,negative-lepton)','Events'],
            ['lepJetDPhi_NegLep',40,0,3.2,'#Delta #phi (jet,negative-lepton)','Events'],
            ['lepJetDEta_NegLep',40,0,5,'#Delta #eta (jet,negative-lepton)','Events'],
            ['lepJetM_NegLep',40,0,300,'Mass of jet & negative-lepton','Events'],
            ['lepPtRelJet_NegLep',40,0,200,'P_{T} negative-lepton relative to jet','Events'],
            ['jetPtRelLep_NegLep',40,0,200,'P_{T} jet relative to negative-lepton','Events'],
            ['lepPtRelJetSameLep_NegLep',40,0,200,'P_{T} neg-lepton relative to jet & neg-lep','Events'],
            ['lepPtRelJetOtherLep_NegLep',40,0,200,'P_{T} neg-lepton relative to jet & pos-lep','Events'],
            ['lepJetMt_NegLep',40,0,300,'M_{T} jet & negative-lepton','Events'],
            ['lepJetCosTheta_boosted_NegLep',40,-1.,1.,'Cos #theta (negative-lepton,jet)','Events'],
            ]

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

Colors = [kOrange-2,
          kRed+1,
          kGreen+2,
          kGreen+2,
          kAzure-6,
          kGreen+2,
          kGreen+2,
          kGreen+2,
          kGreen+2,
          kBlack]

ChannelErrors = [tWErrors,
                 ttErrors,
                 otherErrors,
                 otherErrors,
                 otherErrors,
                 otherErrors,
                 otherErrors,
                 otherErrors,
                 otherErrors]


DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
ChanLabels = [', e#mu channel',', #mu#mu channel',', ee channel', 'e#mu/#mu#mu/ee channels']
lumiLabel = "%.1f fb^{-1}" % TotalLumi

if 'ZpeakLepSel' in region or '1j1tZpeak' in region:
    ChanLabels[3] = 'ee/#mu#mu channels'
    doChannel[0] = False

HistoLists = list()

for mode in range(3):


    HistoMode = list()

    for i in range(len(fileList)):
        Histos = dict()

        fileName = fileList[i].split('.')[0]
        for plot in plotInfo:
            Histos[plot[0]] = TH1F(plot[0]+fileName+ChanName[mode]," ",plot[1],plot[2],plot[3])
            Histos[plot[0]].SetFillColor(Colors[i])
            Histos[plot[0]].SetLineColor(kBlack)
            Histos[plot[0]].SetLineWidth(1)
            Histos[plot[0]].SetMarkerSize(0.0001)
            Histos[plot[0]].Sumw2()
        HistoMode.append(Histos)

    for plot in plotInfo:
        HistoMode[-1][plot[0]].SetMarkerStyle(20)
        HistoMode[-1][plot[0]].SetMarkerSize(1.2)
        HistoMode[-1][plot[0]].SetLineWidth(2)
        HistoMode[-1][plot[0]].SetMarkerColor(kBlack)
        HistoMode[-1][plot[0]].SetLineColor(kBlack)

    HistoLists.append(HistoMode)

HistoMode = list()

for i in range(len(fileList)):
    Histos = dict()

    fileName = fileList[i].split('.')[0]
    for plot in plotInfo:
        Histos[plot[0]] = TH1F(plot[0]+fileName," ",plot[1],plot[2],plot[3])
        Histos[plot[0]].SetFillColor(Colors[i])
        Histos[plot[0]].SetLineColor(kBlack)
        Histos[plot[0]].SetLineWidth(1)
        Histos[plot[0]].SetMarkerSize(0.0001)
        Histos[plot[0]].Sumw2()
    HistoMode.append(Histos)

    for plot in plotInfo:
        HistoMode[-1][plot[0]].SetMarkerStyle(20)
        HistoMode[-1][plot[0]].SetMarkerSize(1.2)
        HistoMode[-1][plot[0]].SetLineWidth(2)
        HistoMode[-1][plot[0]].SetMarkerColor(kBlack)
        HistoMode[-1][plot[0]].SetLineColor(kBlack)

HistoLists.append(HistoMode)



for mode in range(3):

    if not doChannel[mode]:
        continue

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



            _ptjet                     = event.ptjet                   
            _ptlep0                    = event.ptlep0                  
            _ptlep1                    = event.ptlep1                  
            _jetCSV                    = event.jetCSV                  
            _ht                        = event.ht                      
            _htNoMet                   = event.htNoMet                 
            _msys                      = event.msys                    
            if 'TestDir_v3' in vFolder:
                _mll                   = event.mll
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


            _lepJetPt_PosLep            = event.lepJetPt_PosLep           
            _lepPt_PosLep               = event.lepPt_PosLep              
            _lepJetDR_PosLep            = event.lepJetDR_PosLep           
            _lepJetDPhi_PosLep          = event.lepJetDPhi_PosLep         
            _lepJetDEta_PosLep          = event.lepJetDEta_PosLep         
            _lepJetM_PosLep             = event.lepJetM_PosLep            
            _lepPtRelJet_PosLep         = event.lepPtRelJet_PosLep        
            _jetPtRelLep_PosLep         = event.jetPtRelLep_PosLep        
            _lepPtRelJetSameLep_PosLep  = event.lepPtRelJetSameLep_PosLep 
            _lepPtRelJetOtherLep_PosLep = event.lepPtRelJetOtherLep_PosLep
            _lepJetMt_PosLep            = event.lepJetMt_PosLep           
            _lepJetPt_NegLep            = event.lepJetPt_NegLep           
            _lepPt_NegLep               = event.lepPt_NegLep              
            _lepJetDR_NegLep            = event.lepJetDR_NegLep           
            _lepJetDPhi_NegLep          = event.lepJetDPhi_NegLep         
            _lepJetDEta_NegLep          = event.lepJetDEta_NegLep         
            _lepJetM_NegLep             = event.lepJetM_NegLep            
            _lepPtRelJet_NegLep         = event.lepPtRelJet_NegLep        
            _jetPtRelLep_NegLep         = event.jetPtRelLep_NegLep        
            _lepPtRelJetSameLep_NegLep  = event.lepPtRelJetSameLep_NegLep 
            _lepPtRelJetOtherLep_NegLep = event.lepPtRelJetOtherLep_NegLep
            _lepJetMt_NegLep            = event.lepJetMt_NegLep           


            
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

            if fileList[i] == 'DATA':
                _weight = 1.


            if 'ZJets' in fileList[i] and useZjetsSF:
                _weight *= ZjetSF(_met, mode)



            #EXTRA CUTS

            if doZpeakCuts:
                if mode == 0:
                    continue
                else:
                    if _mll < 81 or _mll > 101:
                        continue                    
            elif mode > 0 and _met < 50:
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
#            HistoLists[mode][i]['mll'].Fill(                      _mll                      , _weight )
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

            HistoLists[mode][i]['lepJetPt_PosLep'].Fill(            _lepJetPt_PosLep           , _weight )
            HistoLists[mode][i]['lepPt_PosLep'].Fill(               _lepPt_PosLep              , _weight )
            HistoLists[mode][i]['lepJetDR_PosLep'].Fill(            _lepJetDR_PosLep           , _weight )
            HistoLists[mode][i]['lepJetDPhi_PosLep'].Fill(          _lepJetDPhi_PosLep         , _weight )
            HistoLists[mode][i]['lepJetDEta_PosLep'].Fill(          _lepJetDEta_PosLep         , _weight )
            HistoLists[mode][i]['lepJetM_PosLep'].Fill(             _lepJetM_PosLep            , _weight )
            HistoLists[mode][i]['lepPtRelJet_PosLep'].Fill(         _lepPtRelJet_PosLep        , _weight )
            HistoLists[mode][i]['jetPtRelLep_PosLep'].Fill(         _jetPtRelLep_PosLep        , _weight )
            HistoLists[mode][i]['lepPtRelJetSameLep_PosLep'].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
            HistoLists[mode][i]['lepPtRelJetOtherLep_PosLep'].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
            HistoLists[mode][i]['lepJetMt_PosLep'].Fill(            _lepJetMt_PosLep           , _weight )
            HistoLists[mode][i]['lepJetPt_NegLep'].Fill(            _lepJetPt_NegLep           , _weight )
            HistoLists[mode][i]['lepPt_NegLep'].Fill(               _lepPt_NegLep              , _weight )
            HistoLists[mode][i]['lepJetDR_NegLep'].Fill(            _lepJetDR_NegLep           , _weight )
            HistoLists[mode][i]['lepJetDPhi_NegLep'].Fill(          _lepJetDPhi_NegLep         , _weight )
            HistoLists[mode][i]['lepJetDEta_NegLep'].Fill(          _lepJetDEta_NegLep         , _weight )
            HistoLists[mode][i]['lepJetM_NegLep'].Fill(             _lepJetM_NegLep            , _weight )
            HistoLists[mode][i]['lepPtRelJet_NegLep'].Fill(         _lepPtRelJet_NegLep        , _weight )
            HistoLists[mode][i]['jetPtRelLep_NegLep'].Fill(         _jetPtRelLep_NegLep        , _weight )
            HistoLists[mode][i]['lepPtRelJetSameLep_NegLep'].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
            HistoLists[mode][i]['lepPtRelJetOtherLep_NegLep'].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
            HistoLists[mode][i]['lepJetMt_NegLep'].Fill(            _lepJetMt_NegLep           , _weight )







            HistoLists[-1][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[-1][i]['ptlep0'].Fill(                   _ptlep0                   , _weight )
            HistoLists[-1][i]['ptlep1'].Fill(                   _ptlep1                   , _weight )
            HistoLists[-1][i]['jetCSV'].Fill(                   _jetCSV                   , _weight )
            HistoLists[-1][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[-1][i]['htNoMet'].Fill(                  _htNoMet                  , _weight )
            HistoLists[-1][i]['msys'].Fill(                     _msys                     , _weight )
#            HistoLists[-1][i]['mll'].Fill(                      _mll                      , _weight )
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

            HistoLists[-1][i]['lepJetPt_PosLep'].Fill(            _lepJetPt_PosLep           , _weight )
            HistoLists[-1][i]['lepPt_PosLep'].Fill(               _lepPt_PosLep              , _weight )
            HistoLists[-1][i]['lepJetDR_PosLep'].Fill(            _lepJetDR_PosLep           , _weight )
            HistoLists[-1][i]['lepJetDPhi_PosLep'].Fill(          _lepJetDPhi_PosLep         , _weight )
            HistoLists[-1][i]['lepJetDEta_PosLep'].Fill(          _lepJetDEta_PosLep         , _weight )
            HistoLists[-1][i]['lepJetM_PosLep'].Fill(             _lepJetM_PosLep            , _weight )
            HistoLists[-1][i]['lepPtRelJet_PosLep'].Fill(         _lepPtRelJet_PosLep        , _weight )
            HistoLists[-1][i]['jetPtRelLep_PosLep'].Fill(         _jetPtRelLep_PosLep        , _weight )
            HistoLists[-1][i]['lepPtRelJetSameLep_PosLep'].Fill(  _lepPtRelJetSameLep_PosLep , _weight )
            HistoLists[-1][i]['lepPtRelJetOtherLep_PosLep'].Fill( _lepPtRelJetOtherLep_PosLep, _weight )
            HistoLists[-1][i]['lepJetMt_PosLep'].Fill(            _lepJetMt_PosLep           , _weight )
            HistoLists[-1][i]['lepJetPt_NegLep'].Fill(            _lepJetPt_NegLep           , _weight )
            HistoLists[-1][i]['lepPt_NegLep'].Fill(               _lepPt_NegLep              , _weight )
            HistoLists[-1][i]['lepJetDR_NegLep'].Fill(            _lepJetDR_NegLep           , _weight )
            HistoLists[-1][i]['lepJetDPhi_NegLep'].Fill(          _lepJetDPhi_NegLep         , _weight )
            HistoLists[-1][i]['lepJetDEta_NegLep'].Fill(          _lepJetDEta_NegLep         , _weight )
            HistoLists[-1][i]['lepJetM_NegLep'].Fill(             _lepJetM_NegLep            , _weight )
            HistoLists[-1][i]['lepPtRelJet_NegLep'].Fill(         _lepPtRelJet_NegLep        , _weight )
            HistoLists[-1][i]['jetPtRelLep_NegLep'].Fill(         _jetPtRelLep_NegLep        , _weight )
            HistoLists[-1][i]['lepPtRelJetSameLep_NegLep'].Fill(  _lepPtRelJetSameLep_NegLep , _weight )
            HistoLists[-1][i]['lepPtRelJetOtherLep_NegLep'].Fill( _lepPtRelJetOtherLep_NegLep, _weight )
            HistoLists[-1][i]['lepJetMt_NegLep'].Fill(            _lepJetMt_NegLep           , _weight )



        print


errorHistTemp = TH1F("tempErr","tempErr",10,0,10)
errorHistTemp.SetFillColor(kBlack)
errorHistTemp.SetFillStyle(3013)
#errorHistTemp.SetFillColor(kGray+3)
#errorHistTemp.SetFillStyle(3140)

    
leg = TLegend(0.7,0.66,0.94,0.94)
#leg.SetFillStyle(1)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.AddEntry(HistoLists[0][-1]['ptjet'], "Data", "p")
leg.AddEntry(HistoLists[0][0]['ptjet'], "tW", "f")
leg.AddEntry(HistoLists[0][1]['ptjet'], "t#bar{t}", "f")
leg.AddEntry(HistoLists[0][4]['ptjet'], "Z/#gamma*+jets", "f")
leg.AddEntry(HistoLists[0][2]['ptjet'], "Other", "f")
leg.AddEntry(errorHistTemp, "Syst", "f")


for mode in range(3):
    tot = list()
    err = list()

    for i in range(len(fileList)):
        tot.append(HistoLists[mode][i]['NbtaggedlooseJet15'].Integral())
        tempErr = 0
        for bin in range(1,plotInfo[0][1]+1):
            tempErr = tempErr + pow(HistoLists[mode][i]['NbtaggedlooseJet15'].GetBinError(bin),2)
        err.append(sqrt(tempErr))
    totals.append(tot)
    errors.append(err)




for mode in range(4):

    if noPlots:
        continue

    if not doChannel[mode]:
        continue


    labelcms2 = TPaveText(0.12,0.82,0.6,0.88,"NDCBR");
    labelcms2.SetTextAlign(12);
    labelcms2.SetTextSize(0.045);
    labelcms2.SetFillColor(kWhite);
    labelcms2.SetFillStyle(0);
    labelcms2.AddText(lumiLabel + ChanLabels[mode])
    labelcms2.SetBorderSize(0);



    labelKStest = TPaveText(0.12,0.7,0.6,0.74,"NDCBR");
    labelKStest.SetTextAlign(12);
    labelKStest.SetTextSize(0.045);
    labelKStest.SetFillColor(kWhite);
    labelKStest.SetBorderSize(0);
    

#     if region == 'ZpeakLepSel':
#         bins = array('d',[0,5,10,15,20,25,30,40,50,75,100,150,200,300])
#         plotInfo.append(['metBinned',1,0,1,'MET [GeV]'])
#         for i in range(len(HistoLists)):            
#             HistoLists[mode][i]['metBinned'] = HistoLists[mode][i]['met'].Rebin(13,'metBinned',bins)

    chanNum = mode
    if mode > 2:
        chanNum = 0
    


    startSample = 1
    for plot in plotInfo:
        errorBand = HistoLists[mode][startSample][plot[0]].Clone()
        errorBand.SetMarkerSize(0)
        for i in range(startSample+1,len(HistoLists[mode])-1):
            errorBand.Add(HistoLists[mode][i][plot[0]])
        for bin in range(errorBand.GetNbinsX()):
            binStatError2 = 0
            binSystError2 = 0
            regionTemp = region
            if region == 'tree1j1tNomllMetCut' or '1j1tZpeak' in region:
                regionTemp = '1j1t'
            if region == 'ZpeakLepSel':
                regionTemp = 'NoSyst'
            for i in range(startSample ,len(HistoLists[mode])-1):
                binStatError2 = binStatError2 + pow(HistoLists[mode][i][plot[0]].GetBinError(bin),2)
                binSystError2 = binSystError2 + pow(HistoLists[mode][i][plot[0]].GetBinContent(bin)*ChannelErrors[i][regionTemp][chanNum],2)
            error = sqrt(binStatError2 + binSystError2)
            errorBand.SetBinError(bin,error)

        errorBand.SetFillColor(kBlack)
        errorBand.SetFillStyle(3013)        
        #         errorBand.SetFillColor(kGray+3)
        #         errorBand.SetFillStyle(3140)        

        
        ksResult = errorBand.KolmogorovTest(HistoLists[mode][-1][plot[0]])
        labelKStest.Clear()
        labelKStest.AddText("Kolmogorov: %.2f" %ksResult)
        
#         if firstPlot:
#             firstPlot = False
#             print "Channel: ", ChanName[mode]
#             signal = 0.
#             bkg = 0.
#             for i in range(len(HistoLists)):                
#                 print fileList[i].split('.roo')[0], "\t", HistoList[i][plot[0]].Integral()
#                 if i == 0:
#                     signal = signal + HistoList[i][plot[0]].Integral()
#                 elif not fileList[i] =='DATA':
#                     bkg = bkg + HistoList[i][plot[0]].Integral()
        
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][3][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][5][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][6][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][7][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][8][plot[0]])
        
        hStack = THStack(plot[0],plot[0])
        hStack.Add(HistoLists[mode][2][plot[0]])
        hStack.Add(HistoLists[mode][4][plot[0]])
        hStack.Add(HistoLists[mode][1][plot[0]])
        hStack.Add(HistoLists[mode][0][plot[0]])


#         dataVal = HistoLists[mode][-1][plot[0]].Integral()
#         mcVal = errorBand.Integral()
        

        labelcms3 = TPaveText(0.12,0.74,0.6,0.82,"NDCBR");
        labelcms3.SetTextAlign(12);
        labelcms3.SetTextSize(0.045);
        labelcms3.SetFillColor(kWhite);
        labelcms3.SetFillStyle(0);
#        labelcms3.AddText("%s Data: %.2f MC: %.2f" %(region, dataVal, mcVal))
        labelcms3.AddText(region)
        labelcms3.SetBorderSize(0);

        
        c1 = TCanvas()
        gPad.SetLeftMargin(0.12)
        max_ = max(hStack.GetMaximum(),HistoLists[mode][-1][plot[0]].GetMaximum())
        hStack.Draw("histo")
        hStack.SetMaximum(max_*1.5)
        hStack.SetMinimum(0)

#        errorBand.Draw("e2 same")
        hStack.GetYaxis().SetTitle(plot[5])
        hStack.GetYaxis().CenterTitle()
        hStack.GetYaxis().SetTitleOffset(1.28)
        hStack.GetYaxis().SetTitleSize(0.05)
        hStack.GetXaxis().SetTitle(plot[4])
        hStack.GetXaxis().SetTitleSize(0.05)
        HistoLists[mode][-1][plot[0]].Draw("e x0, same")
        leg.Draw()        
        labelcms.Draw()
        labelcms2.Draw()
        labelcms3.Draw()
#        labelKStest.Draw()
        if not os.path.exists("VariablePlots/"):
            command = "mkdir VariablePlots/"
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder):
            command = "mkdir VariablePlots/"+vFolder
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName +"/" + region):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+'/'+region
            os.system(command)

        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName +"/bdtPlots"):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+'/bdtPlots'
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName +"/bdtPlots/" + region):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+'/bdtPlots/'+region
            os.system(command)

        channel = ""
        if mode < 3:
            channel = "_" + ChanName[mode]

        
#         c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".pdf")
#         c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".png")


        if plot[0] in bdtPlots:
            c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".pdf")
            c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".png")
            

        c1.SetLogy()
        hStack.SetMaximum(max_*30)
        hStack.SetMinimum(1.)
        
#         c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+"_log.pdf")
#         c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+"_log.png")

        if plot[0] in bdtPlots:
            c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+"_log.pdf")
            c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+"_log.png")


signal = [0.,0.,0.]
bkg = [0.,0.,0.]
sigErr = [0.,0.,0.]
bkgErr = [0.,0.,0.]

print
print "\\begin{tabular}{| l | c | c | c | c |}"
print "\\hline"
print "Channel & $e\\mu$ & $\\mu\\mu$ & $ee$ & Combined \\\\"
print "\\hline"

for i in range(len(fileList) - 1):
    print fileList[i],"&","%.1f" % totals[0][i],"$\pm$","%.1f" % errors[0][i],"&","%.1f" % totals[1][i],"$\pm$","%.1f" % errors[1][i],"&","%.1f" % totals[2][i],"$\pm$","%.1f" % errors[2][i],"&","%.1f" % (totals[0][i]+totals[1][i]+totals[2][i]),"$\pm$","%.1f" % sqrt(pow(errors[0][i],2)+pow(errors[1][i],2)+pow(errors[2][i],2)),"\\\\"
    if i == 0:
        signal[0] += totals[0][i]
        signal[1] += totals[1][i]
        signal[2] += totals[2][i]
        sigErr[0] = sqrt(pow(sigErr[0],2) + pow(errors[0][i],2))
        sigErr[1] = sqrt(pow(sigErr[1],2) + pow(errors[1][i],2))
        sigErr[2] = sqrt(pow(sigErr[2],2) + pow(errors[2][i],2))
    else:
        bkg[0] += totals[0][i]
        bkg[1] += totals[1][i]
        bkg[2] += totals[2][i]
        bkgErr[0] = sqrt(pow(bkgErr[0],2) + pow(errors[0][i],2))
        bkgErr[1] = sqrt(pow(bkgErr[1],2) + pow(errors[1][i],2))
        bkgErr[2] = sqrt(pow(bkgErr[2],2) + pow(errors[2][i],2))
        
print "\\hline"
print "Signal &","%.1f" % signal[0],"$\pm$","%.1f" % sigErr[0],"&","%.1f" % signal[1],"$\pm$","%.1f" % sigErr[1],"&","%.1f" % signal[2],"$\pm$","%.1f" % sigErr[2],"&","%.1f" % (signal[0]+signal[1]+signal[2]),"$\pm$","%.1f" % sqrt(pow(sigErr[0],2)+pow(sigErr[1],2)+pow(sigErr[2],2)), " \\\\"
print "Background &","%.1f" % bkg[0],"$\pm$","%.1f" % bkgErr[0],"&","%.1f" % bkg[1],"$\pm$","%.1f" % bkgErr[1],"&","%.1f" % bkg[2],"$\pm$","%.1f" % bkgErr[2],"&","%.1f" % (bkg[0]+bkg[1]+bkg[2]),"$\pm$","%.1f" % sqrt(pow(bkgErr[0],2)+pow(bkgErr[1],2)+pow(bkgErr[2],2)), " \\\\"
print "Data &","%.1f" % totals[0][-1],"$\pm$","%.1f" % errors[0][-1],"&","%.1f" % totals[1][-1],"$\pm$","%.1f" % errors[1][-1],"&","%.1f" % totals[2][-1],"$\pm$","%.1f" % errors[2][-1],"&","%.1f" % (totals[0][-1]+totals[1][-1]+totals[2][-1]),"$\pm$","%.1f" % sqrt(pow(errors[0][-1],2)+pow(errors[1][-1],2)+pow(errors[2][-1],2)), " \\\\"
print "Sum All MC &","%.1f" % (signal[0]+bkg[0]),"$\pm$","%.1f" % sqrt(pow(sigErr[0],2)+pow(bkgErr[0],2)),"&","%.1f" % (signal[1]+bkg[1]),"$\pm$","%.1f" % sqrt(pow(sigErr[1],2)+pow(bkgErr[1],2)),"&","%.1f" % (signal[2]+bkg[2]),"$\pm$","%.1f" % sqrt(pow(sigErr[2],2)+pow(bkgErr[2],2)),"&","%.1f" % (signal[0]+signal[1]+signal[2]+bkg[0]+bkg[1]+bkg[2]),"$\pm$","%.1f" % sqrt(pow(sigErr[0],2)+pow(sigErr[1],2)+pow(sigErr[2],2)+pow(bkgErr[0],2)+pow(bkgErr[1],2)+pow(bkgErr[2],2)), " \\\\"


# print "Background &","%.1f" % bkg[0],"&","%.1f" % bkg[1],"&","%.1f" % bkg[2],"&","%.1f" % (bkg[0]+bkg[1]+bkg[2]), " \\\\"
# print "Data &","%.1f" % totals[0][-1],"&","%.1f" % totals[1][-1],"&","%.1f" % totals[2][-1],"&","%.1f" % (totals[0][-1]+totals[1][-1]+totals[2][-1]), " \\\\"
print "\\hline"
for i in range(3):
    if signal[i] == 0 and bkg[i] == 0:
        bkg[i] = 1.
print "S/B &","%.4f" % (signal[0]/bkg[0]),"&","%.4f" % (signal[1]/bkg[1]),"&","%.4f" % (signal[2]/bkg[2]),"&","%.4f" % ((signal[0]+signal[1]+signal[2])/(bkg[0]+bkg[1]+bkg[2])), " \\\\"
print "$S/\\sqrt{B}$ &","%.2f" % (signal[0]/sqrt(bkg[0])),"&","%.2f" % (signal[1]/sqrt(bkg[1])),"&","%.2f" % (signal[2]/sqrt(bkg[2])),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2])), " \\\\"
print "\\hline"
print "$S/\\sqrt{B+dB^2}$ (5\\%) &","%.2f" % (signal[0]/sqrt(bkg[0]+pow(0.05*bkg[0],2))),"&","%.2f" % (signal[1]/sqrt(bkg[1]+pow(0.05*bkg[1],2))),"&","%.2f" % (signal[2]/sqrt(bkg[2]+pow(0.05*bkg[2],2))),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2]+pow((bkg[0]+bkg[1]+bkg[2])*0.05,2))), " \\\\"
print "$S/\\sqrt{B+dB^2}$ (10\\%) &","%.2f" % (signal[0]/sqrt(bkg[0]+pow(0.1*bkg[0],2))),"&","%.2f" % (signal[1]/sqrt(bkg[1]+pow(0.1*bkg[1],2))),"&","%.2f" % (signal[2]/sqrt(bkg[2]+pow(0.1*bkg[2],2))),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2]+pow((bkg[0]+bkg[1]+bkg[2])*0.1,2))), " \\\\"
print "$S/\\sqrt{B+dB^2}$ (15\\%) &","%.2f" % (signal[0]/sqrt(bkg[0]+pow(0.15*bkg[0],2))),"&","%.2f" % (signal[1]/sqrt(bkg[1]+pow(0.15*bkg[1],2))),"&","%.2f" % (signal[2]/sqrt(bkg[2]+pow(0.15*bkg[2],2))),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2]+pow((bkg[0]+bkg[1]+bkg[2])*0.15,2))), " \\\\"
print "\\hline"
print "\\end{tabular}"

