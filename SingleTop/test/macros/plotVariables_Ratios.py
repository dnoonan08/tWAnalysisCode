#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array
from ZjetSF import *
from errorLists import *
import ROOT

import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

AllowedRegions = ['1j0t','1j1t','1jNoTagging','2j0t','2j1t','2j2t','2jNoTagging','3plusjNoTagging','1j1tZpeak','ZpeakLepSel','2plusjets1plustag','3plusjets1plustag','tree1j1tNomllMetCut', '1j0tNoMETmllCut']

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

useNNLOTTbar = True

specialName = ''

noPlots = False

useZjetsSF = True

doZpeakCuts = False

#doMETcut = False
doMETcut = True

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
    combinedChan = True

if not versionPicked:
    vFolder = 'TestDir_v3'
#     versionList = glob.glob("tmvaFiles/v*")
#     versionList.sort(key=lambda a:int(a.split('/v')[-1].split('_')[0]))
#     vFolder = versionList[-1].split('/')[-1]    
    print vFolder

if RunA:
    TotalLumi = TotalLumi + 808.472+82.136
if RunB:
    TotalLumi = TotalLumi + 4429.
if RunC:
    TotalLumi = TotalLumi + 495.003+6383.

runs = ''

if RunA and RunB and RunC:
    runs=''
else:
    runs='_'
    if RunA:
        runs+='A'
    if RunB:
        runs+='B'
    if RunC:
        runs+='C'


TotalLumi = TotalLumi/1000.

labelcms = TPaveText(0.12,0.7,0.6,0.92,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.045);
labelcms.SetFillColor(kWhite);
labelcms.SetFillStyle(0);
labelcms.SetBorderSize(0);

#gStyle.SetLabelSize(0.045,"x")
gStyle.SetLabelSize(0.035,"xy")


doChannel = [emuChan, mumuChan, eeChan, combinedChan]
    

if 'Zpeak' in region:
    doZpeakCuts = True
    doChannel[0] = False


plotInfo = [['ptjet',27,30,300, 'P_{T} leading jet [GeV]','Events / 10 GeV'],
            ['ptlep0',28,20,300, 'P_{T} lepton-0 [GeV]','Events / 10 GeV'],
            ['ptlep1',28,20,300, 'P_{T} lepton-1 [GeV]','Events / 10 GeV'],
            ['ht',53,70,600, 'H_{T} [GeV]','Events / 10 GeV'],
            ['msys',60,0,600, 'Mass-system [GeV]','Events / 10 GeV'],
#            ['mll',60,0,600, 'Mass-leptons [GeV]','Events / 10 GeV'],
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

            ]

fileList = ['TWChannel.root',
            'TTbar.root',
            'TChannel.root',
            'SChannel.root',
            'ZJets.root',
            'WJets.root',
            'WW.root',
            'WZ.root',
            'ZZ.root',
            'DATA']

Colors = [kWhite,
          kRed+1,
          kGreen-3,
          kGreen-3,
          kAzure-2,
          kGreen-3,
          kGreen-3,
          kGreen-3,
          kGreen-3,
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

if 'Zpeak' in region:
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
        else:
            print region
        
        tree = TChain(Folder[mode]+'/'+regiontemp)

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
            
            _weightA                    = event.weightA
            _weightB                    = event.weightB
            _weightC                    = event.weightC

            _weight = 0            


            _btagSF = 1.


            if RunA:
                _weight = _weight + _weightA
            if RunB:
                _weight = _weight + _weightB
            if RunC:
                _weight = _weight + _weightC

            _weight = _weight*_btagSF            

            if fileList[i] == 'DATA':
                _weight = 1.


            if 'ZJets' in fileList[i] and useZjetsSF:
                _weight *= ZjetSF(_met, mode)

            if useNNLOTTbar and 'TTbar' in fileList[i]:
                _weight *= 245./234.



            #EXTRA CUTS

            if doZpeakCuts:
                if mode == 0:
                    continue
                else:
                    if _mll < 81 or _mll > 101:                        
                        continue                    
            if doMETcut:
                if mode > 0 and _met < 50:
                    continue
            
            
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
            HistoLists[mode][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[mode][i]['msys'].Fill(                     _msys                     , _weight )
#            HistoLists[mode][i]['mll'].Fill(                      _mll                      , _weight )
            HistoLists[mode][i]['ptsys'].Fill(                    _ptsys                    , _weight )
            HistoLists[mode][i]['ptjll'].Fill(                    _ptjll                    , _weight )
            HistoLists[mode][i]['ptsys_ht'].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[mode][i]['htleps_ht'].Fill(                _htleps_ht                , _weight )
            HistoLists[mode][i]['NlooseJet20Central'].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[mode][i]['NlooseJet20'].Fill(              _NlooseJet20              , _weight )
            HistoLists[mode][i]['NbtaggedlooseJet20'].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[mode][i]['met'].Fill(                      _met                      , _weight )
            HistoLists[mode][i]['loosejetPt'].Fill(               _loosejetPt               , _weight )
            HistoLists[mode][i]['centralityJLL'].Fill(            _centralityJLL            , _weight )

            HistoLists[-1][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[-1][i]['ptlep0'].Fill(                   _ptlep0                   , _weight )
            HistoLists[-1][i]['ptlep1'].Fill(                   _ptlep1                   , _weight )
            HistoLists[-1][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[-1][i]['msys'].Fill(                     _msys                     , _weight )
#            HistoLists[-1][i]['mll'].Fill(                      _mll                      , _weight )
            HistoLists[-1][i]['ptsys'].Fill(                    _ptsys                    , _weight )
            HistoLists[-1][i]['ptjll'].Fill(                    _ptjll                    , _weight )
            HistoLists[-1][i]['ptsys_ht'].Fill(                 _ptsys_ht                 , _weight )
            HistoLists[-1][i]['htleps_ht'].Fill(                _htleps_ht                , _weight )
            HistoLists[-1][i]['NlooseJet20Central'].Fill(       _NlooseJet20Central       , _weight )
            HistoLists[-1][i]['NlooseJet20'].Fill(              _NlooseJet20              , _weight )
            HistoLists[-1][i]['NbtaggedlooseJet20'].Fill(       _NbtaggedlooseJet20       , _weight )
            HistoLists[-1][i]['met'].Fill(                      _met                      , _weight )
            HistoLists[-1][i]['loosejetPt'].Fill(               _loosejetPt               , _weight )
            HistoLists[-1][i]['centralityJLL'].Fill(            _centralityJLL            , _weight )

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



for mode in range(4):

    if noPlots:
        continue

    if not doChannel[mode]:
        continue

    chanNum = mode
    regionNum = 0
    if mode > 2:
        chanNum = 0
    if '1j1t' in region:
        regionNum = 0
    elif '2j1t' in region:
        regionNum = 1
    else:
        regionNum = 2

    


    startSample = 1
    for plot in plotInfo:
        labelcms.Clear()
        labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
        labelcms.AddText(lumiLabel + " " +ChanLabels[mode])
        labelcms.AddText(region)

        errorBand = HistoLists[mode][startSample][plot[0]].Clone()
        errorBand.SetMarkerSize(0)
        for i in range(startSample+1,len(HistoLists[mode])-1):
            errorBand.Add(HistoLists[mode][i][plot[0]])
        for bin in range(errorBand.GetNbinsX()):
            binStatError2 = 0
            binSystError2 = 0
            regionTemp = region
            #if region == 'tree1j1tNomllMetCut' or '1j1tZpeak' in region:
            if 'tree1j1tNomllMetCut' in region:
                regionTemp = '1j1t'
            if '1j0tNo' in region:
                regionTemp = '1j1t'
            if '1j1tZpeak' in region:
                regionTemp = '1j1t'
            if region == 'ZpeakLepSel':
                regionTemp = '1j1t'
            for i in range(startSample ,len(HistoLists[mode])-1):
                binStatError2 = binStatError2 + pow(HistoLists[mode][i][plot[0]].GetBinError(bin),2)
                binSystError2 = binSystError2 + pow(HistoLists[mode][i][plot[0]].GetBinContent(bin)*ChannelErrors[i][regionTemp][chanNum],2)
            error = sqrt(binStatError2 + binSystError2)
            errorBand.SetBinError(bin,error)

        errorBand.SetFillColor(kBlack)
        errorBand.SetFillStyle(3013)        
        #         errorBand.SetFillColor(kGray+3)
        #         errorBand.SetFillStyle(3140)        

        
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


        
        c1 = TCanvas()

        c1.cd()
        t1 = TPad("t1", "t1", 0.0,0.0,1.,0.25)
        ROOT.SetOwnership(t1,0)
        t1.Draw()
        t1.cd()
        t1.SetTopMargin(0.01)
        t1.SetBottomMargin(0.3)
#         t1.SetRightMargin(0.1)
#        t1.SetFillStyle(0)

        newError = errorBand.Clone()
        if startSample == 1:
            newError.Add(HistoLists[mode][0][plot[0]])
            
            for bin in range(newError.GetNbinsX()):
                regionTemp = region
                if region == 'tree1j1tNomllMetCut' or '1j1tZpeak' in region:
                    regionTemp = '1j1t'
                if region == 'ZpeakLepSel':
                    regionTemp = 'NoSyst'
                if '1j0tNo' in region:
                    regionTemp = '1j1t'

                binStatError = HistoLists[mode][i][plot[0]].GetBinError(bin)
                binSystError = HistoLists[mode][i][plot[0]].GetBinContent(bin)*ChannelErrors[i][regionTemp][chanNum]
                newErrorError = newError.GetBinError(bin)
                error = sqrt(pow(newErrorError,2) + pow(binSystError,2) + pow(binStatError,2))
                newError.SetBinError(bin,error)
        ksHist = newError.Clone()
        h_ratio = HistoLists[mode][-1][plot[0]].Clone()        
        h_ratio.Divide(newError)
        for bin in range(1,newError.GetNbinsX()+1):
            percentError = 0.
            if newError.GetBinContent(bin) > 0.:
                percentError = newError.GetBinError(bin)/newError.GetBinContent(bin)
            newError.SetBinError(bin, percentError)
            newError.SetBinContent(bin,1.)

        h_ratio.SetMinimum(0.)
        h_ratio.SetMaximum(2.)
        h_ratio.GetYaxis().SetTitle("#frac{Data}{MC}")
        h_ratio.GetYaxis().CenterTitle()
        h_ratio.GetYaxis().SetTitleSize(0.15)
        h_ratio.GetYaxis().SetTitleOffset(0.28)
        h_ratio.GetXaxis().SetTitle(plot[4])
        h_ratio.GetXaxis().SetTitleSize(0.15)
        h_ratio.GetXaxis().SetTitleOffset(.95)

        h_ratio.GetXaxis().SetLabelSize(0.1)
        h_ratio.GetYaxis().SetLabelSize(0.1)
#        h_ratio.GetYaxis().SetNdivisions(5)
        h_ratio.SetNdivisions(5,"Y")
#        h_ratio.SetNdivisions(5,"Y")

        h_ratioOver = h_ratio.Clone("h_ratioOver")
        h_ratioUnder = h_ratio.Clone("h_ratioUnder")

        h_ratioOver.Reset()
        h_ratioUnder.Reset()
        h_ratioOver.SetMarkerStyle(22)
        h_ratioUnder.SetMarkerStyle(23)
        for bin in range(1,h_ratio.GetNbinsX()+1):
            max_ = h_ratio.GetMaximum()
            min_ = h_ratio.GetMinimum()
            delta = (max_-min_)/15.
            h_ratioOver.SetBinError(bin,0.)
            h_ratioUnder.SetBinError(bin,0.)
            if h_ratio.GetBinContent(bin) > max_:
                h_ratioOver.SetBinContent(bin,max_-delta)                
            else:                
                h_ratioOver.SetBinContent(bin,min_-1.)

            if h_ratio.GetBinContent(bin) < min_ and h_ratio.GetBinContent(bin) > 0:
                h_ratioUnder.SetBinContent(bin,min_+delta)
            else:
                h_ratioUnder.SetBinContent(bin,min_-1.)


        h_ratio.Draw("e x0 pz")
        newError.Draw("e2 same")
        h_ratioOver.Draw("ep same")
        h_ratioUnder.Draw("ep same")
        
        c1.cd()
        t2 = TPad("t2", "t1", 0.,.25,1.,1.)
        ROOT.SetOwnership(t2,0)
        t2.Draw()
        t2.cd()
        t2.SetBottomMargin(0.01)

#         t2.SetTopMargin(0.1)
#         t2.SetBottomMargin(0.01)
#         t2.SetRightMargin(0.1)
#         t2.SetFillStyle(0)

        max_ = max(hStack.GetMaximum(),HistoLists[mode][-1][plot[0]].GetMaximum())
        hStack.Draw("histo")
        hStack.SetMaximum(max_*1.5)
        hStack.SetMinimum(0)

        errorBand.Draw("e2 same")

        hStack.GetYaxis().SetTitle(plot[5])
        hStack.GetYaxis().CenterTitle()
        hStack.GetYaxis().SetTitleOffset(1.)
        hStack.GetYaxis().SetTitleSize(0.05)
        hStack.GetXaxis().SetLabelSize(0)
#         hStack.GetXaxis().SetTitle(plot[4])
#         hStack.GetXaxis().SetTitleSize(0.05)

        HistoLists[mode][-1][plot[0]].Draw("e x0, same")

        ksTest = ksHist.KolmogorovTest(HistoLists[mode][-1][plot[0]])
        ksLabel = "Kolmogorov Test: %.3f" % (ksTest)
        labelcms.AddText(ksLabel)

        

        leg.Draw()        
        labelcms.Draw()
        #         labelcms2.Draw()
        #         labelcms3.Draw()
        #        labelKStest.Draw()

        if not os.path.exists("VariablePlots/WithRatios/"+vFolder):
            command = "mkdir VariablePlots/WithRatios/"+vFolder
            os.system(command)
        if not os.path.exists("VariablePlots/WithRatios/"+vFolder+"/"+specialName):
            command = "mkdir VariablePlots/WithRatios/"+vFolder+"/"+specialName
            os.system(command)
        if not os.path.exists("VariablePlots/WithRatios/"+vFolder+"/"+specialName +"/" + region):
            command = "mkdir VariablePlots/WithRatios/"+vFolder+"/"+specialName+'/'+region
            os.system(command)
            
        channel = ""
        if mode < 3:
            channel = "_" + ChanName[mode]

        
        c1.SaveAs("VariablePlots/WithRatios/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".pdf")
        c1.SaveAs("VariablePlots/WithRatios/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".png")


        t1.Clear()
        t2.Clear()
