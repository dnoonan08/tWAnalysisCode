#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array

from ZjetSF import *
from ZjetSF_3 import *

import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

AllowedRegions = ['ZpeakLepSel','Zpeak0jets','Zpeak1jets','Zpeak2jets']

region = 'ZpeakLepSel'
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

versionPicked = False

specialName = 'ZjetMET_Original/'

noPlots = False

totals = list()
errors = list()

i = 1
while i < len(sys.argv):
    arg=sys.argv[i]
    if arg == '-b':
        i += 1
        continue
    elif 'ZjetMETClosurePlots.p' in arg:
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
        specialName = specialName + sys.argv[i]        
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

if not versionPicked:
    vFolder = 'ZpeakRegion'

if RunA:
    TotalLumi = TotalLumi + 876
if RunB:
    TotalLumi = TotalLumi + 4412.
if RunC:
    TotalLumi = TotalLumi + 7055.
if RunD:
    TotalLumi = TotalLumi + 7369.

TotalLumi = TotalLumi/1000.

labelcms = TPaveText(0.12,0.88,0.6,0.92,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.045);
labelcms.SetFillColor(kWhite);
labelcms.SetFillStyle(0);
labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
labelcms.SetBorderSize(0);

#gStyle.SetLabelSize(0.045,"y")
gStyle.SetLabelSize(0.035,"xy")


doChannel = [emuChan, mumuChan, eeChan]
    
plotInfo = [['met', 60, 0, 300,'E_{T}^{miss} [GeV]'],
            ['mll', 20, 81, 101,'m_{ll} [GeV]'],
            ['ptlep0',28,20,300, 'P_{T} lepton-0 [GeV]','Events / 10 GeV'],
            ['ptlep1',28,20,300, 'P_{T} lepton-1 [GeV]','Events / 10 GeV'],

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



DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
ChanLabels = [', e#mu channel',', #mu#mu channel',', ee channel']
lumiLabel = "%.1f fb^{-1}" % TotalLumi

# DataRun = ['Run2012A','Run2012B','Run2012C']


for mode in range(1,3):

    if not doChannel[mode]:
        continue

    HistoLists = list()

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
        HistoLists.append(Histos)

    for plot in plotInfo:
        HistoLists[-1][plot[0]].SetMarkerStyle(20)
        HistoLists[-1][plot[0]].SetMarkerSize(1.2)
        HistoLists[-1][plot[0]].SetLineWidth(2)
        HistoLists[-1][plot[0]].SetMarkerColor(kBlack)
        HistoLists[-1][plot[0]].SetLineColor(kBlack)
    
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



            _met                       = event.met
            _mll                       = event.mll
            _ptlep0                    = event.ptlep0
            _ptlep1                    = event.ptlep1 

            
            _weightA                    = event.weightA
            _weightB                    = event.weightB
            _weightC                    = event.weightC
            _weightD                    = event.weightD

            _weight = 0            


#             if _met < 50:
#                 continue

            if RunA:
                _weight = _weight + _weightA
            if RunB:
                _weight = _weight + _weightB
            if RunC:
                _weight = _weight + _weightC
            if RunD:
                _weight = _weight + _weightD

            if fileList[i] == 'DATA':
                _weight = 1.

            if 'ZJets.ro' in fileList[i]:
                _weight *= ZjetSF(_met, mode)

            HistoLists[i]['met'].Fill(    _met    , _weight )
            HistoLists[i]['mll'].Fill(    _mll    , _weight )
            HistoLists[i]['ptlep0'].Fill( _ptlep0 , _weight )
            HistoLists[i]['ptlep1'].Fill( _ptlep1 , _weight )

        print

    errorHistTemp = TH1F("tempErr","tempErr",10,0,10)
    errorHistTemp.SetFillColor(kBlack)
    errorHistTemp.SetFillStyle(3003)
    
    leg = TLegend(0.7,0.66,0.94,0.94)
#    leg.SetFillStyle(1)
    leg.SetFillColor(kWhite)
    leg.SetBorderSize(1)
    leg.AddEntry(HistoLists[-1]['met'], "Data", "p")
    leg.AddEntry(HistoLists[0]['met'], "tW", "f")
    leg.AddEntry(HistoLists[1]['met'], "t#bar{t}", "f")
    leg.AddEntry(HistoLists[4]['met'], "Z/#gamma*+jets", "f")
    leg.AddEntry(HistoLists[2]['met'], "Other", "f")
    leg.AddEntry(errorHistTemp, "Syst", "f")

    tot = list()
    err = list()

    for i in range(len(fileList)):
        tot.append(HistoLists[i]['met'].Integral())
        tempErr = 0
        for bin in range(1,plotInfo[0][1]+1):
            tempErr = tempErr + pow(HistoLists[i]['met'].GetBinError(bin),2)
        err.append(sqrt(tempErr))
    totals.append(tot)
    errors.append(err)


    if noPlots:
        continue

    labelcms2 = TPaveText(0.12,0.82,0.6,0.88,"NDCBR");
    labelcms2.SetTextAlign(12);
    labelcms2.SetTextSize(0.045);
    labelcms2.SetFillColor(kWhite);
    labelcms2.SetFillStyle(0);
    labelcms2.AddText(lumiLabel + ChanLabels[mode])
    labelcms2.SetBorderSize(0);

    labelcms3 = TPaveText(0.12,0.74,0.6,0.82,"NDCBR");
    labelcms3.SetTextAlign(12);
    labelcms3.SetTextSize(0.045);
    labelcms3.SetFillColor(kWhite);
    labelcms3.SetFillStyle(0);
    labelcms3.AddText(region)
    labelcms3.SetBorderSize(0);

    firstPlot = True


#     bins = array('d',[0,5,10,15,20,25,30,40,50,75,100,150,200,300])
#     bins = array('d',[0,5,10,15,20,25,30,40,50,75,300])
#     bins = array('d',[0,10,20,30,40,50,60,100,300])
    bins = array('d',[0,10,20,30,40,50,60,70,80,100,300])
    plotInfo.append(['metBinned',1,0,1,'MET [GeV]'])
    for i in range(len(HistoLists)):            
        HistoLists[i]['metBinned'] = HistoLists[i]['met'].Rebin(len(bins)-1,'metBinned',bins)
        

    for plot in plotInfo:
        errorBand = HistoLists[0][plot[0]].Clone()
        for i in range(1,len(HistoLists)-1):
            errorBand.Add(HistoLists[i][plot[0]])
        for bin in range(errorBand.GetNbinsX()):
            error2 = 0
            for i in range(len(HistoLists)-1):
                error2 = error2 + pow(HistoLists[i][plot[0]].GetBinError(bin),2)
            error = sqrt(error2)
            errorBand.SetBinError(bin,error)
            
        errorBand.SetFillColor(kBlack)
        errorBand.SetFillStyle(3003)

        
        HistoLists[2][plot[0]].Add(HistoLists[3][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[5][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[6][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[7][plot[0]])
        HistoLists[2][plot[0]].Add(HistoLists[8][plot[0]])
        
        hStack = THStack(plot[0],plot[0])
        hStack.Add(HistoLists[2][plot[0]])
        hStack.Add(HistoLists[4][plot[0]])
        hStack.Add(HistoLists[1][plot[0]])
        hStack.Add(HistoLists[0][plot[0]])
        
        c1 = TCanvas()
        gPad.SetLeftMargin(0.12)
        max_ = max(hStack.GetMaximum(),HistoLists[-1][plot[0]].GetMaximum())
        hStack.Draw("histo")
        hStack.SetMaximum(max_*1.5)
        hStack.SetMinimum(0)
        errorBand.Draw("e2 same")
        hStack.GetYaxis().SetTitle("Events")
        hStack.GetYaxis().CenterTitle()
        hStack.GetYaxis().SetTitleOffset(1.28)
        hStack.GetYaxis().SetTitleSize(0.05)
        hStack.GetXaxis().SetTitle(plot[4])
        hStack.GetXaxis().SetTitleSize(0.05)
        HistoLists[-1][plot[0]].Draw("e x0, same")
        leg.Draw()        
        labelcms.Draw()
        labelcms2.Draw()
        labelcms3.Draw()

        if not os.path.exists("VariablePlots/"+specialName):
            command = "mkdir VariablePlots/"+specialName
            os.system(command)
        if not os.path.exists("VariablePlots/"+specialName + region):
            command = "mkdir VariablePlots/"+specialName+region
            os.system(command)
            
        
        c1.SaveAs("VariablePlots/"+specialName+region+"/ClosureTest_"+plot[0]+"_"+region+"_"+ChanName[mode]+".pdf")
        c1.SaveAs("VariablePlots/"+specialName+region+"/ClosureTest_"+plot[0]+"_"+region+"_"+ChanName[mode]+".png")
        c1.SetLogy()
        hStack.SetMaximum(max_*150.)
        hStack.SetMinimum(1.)
        
        c1.SaveAs("VariablePlots/"+specialName+region+"/ClosureTest_"+plot[0]+"_"+region+"_"+ChanName[mode]+"_log.pdf")
        c1.SaveAs("VariablePlots/"+specialName+region+"/ClosureTest_"+plot[0]+"_"+region+"_"+ChanName[mode]+"_log.png")

