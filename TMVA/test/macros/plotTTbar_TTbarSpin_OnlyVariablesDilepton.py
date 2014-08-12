#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array
from errorLists import *

import itertools
import ROOT
import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

AllowedRegions = ['1j0t','1j1t','1jNoTagging','2j0t','2j1t','2j2t','2jNoTagging','3plusjNoTagging','1j1tZpeak','ZpeakLepSel','2plusjets1plustag','3plusjets1plustag','tree1j1tNomllMetCut']

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

specialName = 'TTbarSpinComparisonDilepton'

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

if not channelPicked:
    emuChan = True
    mumuChan = True
    eeChan = True
    combinedChan = True

if not versionPicked:
    vFolder = 'TestDir_v3'
#    vFolder = 'v11_MET50'

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

doZpeakCuts = False


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
    
plotInfo = [['ptjet',27,30,300, 'P_{T} leading jet [GeV]','Events / 10 GeV'],
            ['ptlep0',56,20,300, 'P_{T} leading lepton [GeV]','Events / 10 GeV'],
            ['ptlep1',56,20,300, 'P_{T} second lepton [GeV]','Events / 10 GeV'],
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
            ['dPhileps',30,0,3.142,'delta phi leptons','Events'],
            ['mll',40,0,200,'delta phi leptons','Events'],
            ]

fileList = ['TTbarDilepton.root',
            'TTbarSpin.root'
            ]


Colors = [kAzure-2,
          kRed+1,
          ]


DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
ChanLabels = [', e#mu channel',', #mu#mu channel',', ee channel', 'e#mu/#mu#mu/ee channels']
lumiLabel = "%.1f fb^{-1}" % TotalLumi

if 'ZpeakLepSel' in region:
    ChanLabels[3] = 'ee/#mu#mu channels'
#    doChannel[0] = False
if '1j1tZpeak' in region:
    ChanLabels[3] = 'ee/#mu#mu channels'

HistoLists = list()

newBins = array('d',[-1.001,-0.995,-0.7,0.7,0.995,1.001])

for mode in range(3):


    HistoMode = list()

    for i in range(len(fileList)):
        Histos = dict()

        fileName = fileList[i].split('.')[0]
        for plot in plotInfo:
            Histos[plot[0]] = TH1F(plot[0]+fileName+ChanName[mode]," ",plot[1],plot[2],plot[3])
            Histos[plot[0]].SetLineColor(Colors[i])
            Histos[plot[0]].SetLineWidth(3)
            Histos[plot[0]].SetMarkerSize(0.0001)
            Histos[plot[0]].Sumw2()
        HistoMode.append(Histos)


    HistoLists.append(HistoMode)

HistoMode = list()

for i in range(len(fileList)):
    Histos = dict()

    fileName = fileList[i].split('.')[0]
    for plot in plotInfo:
        Histos[plot[0]] = TH1F(plot[0]+fileName," ",plot[1],plot[2],plot[3])
        Histos[plot[0]].SetLineColor(Colors[i])
        Histos[plot[0]].SetLineWidth(3)
        Histos[plot[0]].SetMarkerSize(0.0001)
        Histos[plot[0]].Sumw2()
    HistoMode.append(Histos)


HistoLists.append(HistoMode)



for mode in range(3):

    if not doChannel[mode]:
        continue

    for i in range(len(fileList)):

        print fileList[i]
        file = fileList[i]

        regiontemp = region

        if '1j1tZpeak' in region:
            regiontemp = 'tree1j1tNomllMetCut'


        tree = TChain(Folder[mode]+'/'+regiontemp)

        tree.Add('../tmvaFiles/'+vFolder+'/'+fileList[i])

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
            _ht                        = event.ht                      
            _msys                      = event.msys                    
            _mll                       = event.mll
            _mjll                      = event.mjll                    
            _ptsys                     = event.ptsys                   
            _ptjll                     = event.ptjll                   
            _ptsys_ht                  = event.ptsys_ht                
            _htleps_ht                 = event.htleps_ht               
            _NlooseJet20Central        = event.NlooseJet20Central      
            _NlooseJet20               = event.NlooseJet20             
            _NbtaggedlooseJet20        = event.NbtaggedlooseJet20      
            _met                       = event.met                     
            _loosejetPt                = event.loosejetPt              
            _centralityJLL             = event.centralityJLL           
            _dPhileps                  = event.dPhileps
            
            _weightA                    = event.weightA
            _weightB                    = event.weightB
            _weightC                    = event.weightC

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

            _weight = _weight*_btagSF            

            if fileList[i] == 'DATA':
                _weight = 1.


            if 'ZJets' in fileList[i]:
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
            HistoLists[mode][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[mode][i]['mll'].Fill(                      _mll                      , _weight )
            HistoLists[mode][i]['msys'].Fill(                     _msys                     , _weight )
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
            HistoLists[mode][i]['dPhileps'].Fill(                 _dPhileps                 , _weight )

            HistoLists[-1][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[-1][i]['ptlep0'].Fill(                   _ptlep0                   , _weight )
            HistoLists[-1][i]['ptlep1'].Fill(                   _ptlep1                   , _weight )
            HistoLists[-1][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[-1][i]['msys'].Fill(                     _msys                     , _weight )
            HistoLists[-1][i]['mll'].Fill(                      _mll                      , _weight )
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
            HistoLists[-1][i]['dPhileps'].Fill(                 _dPhileps                 , _weight )



        print


    
leg = TLegend(0.7,0.66,0.94,0.94)
#leg.SetFillStyle(1)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
#leg.AddEntry(HistoLists[0][-1]['ptjet'], "Data", "p")
#leg.AddEntry(HistoLists[0][0]['ptjet'], "tW", "f")
leg.AddEntry(HistoLists[0][0]['ptjet'], "t#bar{t}", "l")
leg.AddEntry(HistoLists[0][1]['ptjet'], "t#bar{t} With Spin", "l")
# leg.AddEntry(HistoLists[0][4]['ptjet'], "Z/#gamma*+jets", "f")
# leg.AddEntry(HistoLists[0][2]['ptjet'], "Other", "f")
# leg.AddEntry(errorHistTemp, "Syst", "f")



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
    



    labelcms3 = TPaveText(0.12,0.74,0.6,0.82,"NDCBR");
    labelcms3.SetTextAlign(12);
    labelcms3.SetTextSize(0.045);
    labelcms3.SetFillColor(kWhite);
    labelcms3.SetFillStyle(0);
    #        labelcms3.AddText("%s Data: %.2f MC: %.2f" %(region, dataVal, mcVal))
    labelcms3.AddText(region)
    labelcms3.SetBorderSize(0);

    for plot in plotInfo:
        
        c1 = TCanvas()
        c1.cd()
        t1 = TPad("t1", "t1", 0.0,0.0,1.,0.25)
        ROOT.SetOwnership(t1,0)
        t1.Draw()
        t1.cd()
        t1.SetTopMargin(0.01)
        t1.SetBottomMargin(0.3)

        h_ratio = HistoLists[mode][0][plot[0]].Clone()        
        h_ratio.Divide(HistoLists[mode][1][plot[0]])

        h_ratio.SetMinimum(0.8)
        h_ratio.SetMaximum(1.2)
        h_ratio.SetMarkerStyle(20)
        h_ratio.SetMarkerSize(1.2)
        h_ratio.SetLineColor(kBlack)
        h_ratio.GetYaxis().SetTitle("#frac{TTbar}{TTbarSpin}")
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

        t1.SetGrid(0,1)
        h_ratio.Draw("e x0")
        
        c1.cd()
        t2 = TPad("t2", "t1", 0.,.25,1.,1.)
        ROOT.SetOwnership(t2,0)
        t2.Draw()
        t2.cd()
        t2.SetBottomMargin(0.01)

        
#        Ratio = HistoLists[mode][0][plot[0]].Integral()/HistoLists[mode][1][plot[0]].Integral()
        labelcms3.Clear()
        labelcms3.AddText(region)
        ksTest = HistoLists[mode][0][plot[0]].KolmogorovTest(HistoLists[mode][1][plot[0]])
        ksLabel = "Kolmogorov Test: %.3f" % (ksTest)
        labelcms3.AddText(ksLabel)


        gPad.SetLeftMargin(0.12)
        max_ = max(HistoLists[mode][0][plot[0]].GetMaximum(),HistoLists[mode][1][plot[0]].GetMaximum())        
        HistoLists[mode][0][plot[0]].Draw()
        HistoLists[mode][0][plot[0]].SetMaximum(max_*1.5)
        HistoLists[mode][0][plot[0]].SetMinimum(0)
        HistoLists[mode][0][plot[0]].GetYaxis().SetTitle(plot[5])
        HistoLists[mode][0][plot[0]].GetYaxis().CenterTitle()
        HistoLists[mode][0][plot[0]].GetYaxis().SetTitleOffset(1.28)
        HistoLists[mode][0][plot[0]].GetYaxis().SetTitleSize(0.05)
#         HistoLists[mode][0][plot[0]].GetXaxis().SetTitle(plot[4])
#         HistoLists[mode][0][plot[0]].GetXaxis().SetTitleSize(0.05)
        HistoLists[mode][0][plot[0]].GetXaxis().SetLabelSize(0)
        HistoLists[mode][1][plot[0]].Draw("same")
        leg.Draw()        
        labelcms.Draw()
        labelcms2.Draw()
        labelcms3.Draw()


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
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+"/"+region
            os.system(command)
            
        channel = ""
        if mode < 3:
            channel = "_" + ChanName[mode]

        
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".pdf")
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+".png")


        t1.Clear()
        t2.Clear()


