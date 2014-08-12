#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array
from ZjetSF_2 import *
from errorLists import *


import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

verbose = False

#AllowedRegions = ['1j1t']
AllowedRegions = ['1j0t','1j1t','2j0t','2j1t','2j2t','3j0t','3j1t','3j2t','3j3t']

RegionNumber = {'1j0t':1,
                '1j1t':2,
                '2j0t':3,
                '2j1t':4,
                '2j2t':5,
                '3j0t':6,
                '3j1t':7,
                '3j2t':8,
                '3j3t':9,
                }



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

specialName = 'ZjetSF2/Notemu'

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
#     versionList = glob.glob("tmvaFiles/v*")
#     versionList.sort(key=lambda a:int(a.split('/v')[-1].split('_')[0]))
#     vFolder = versionList[-1].split('/')[-1]    
    vFolder = 'ManyRegions_v2'
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

    
plotInfo = [
            ['RegionCount',9,1,10,'','Events']
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


for region in AllowedRegions:
    
#     region = AllowedRegions[r]

    print '-------------------------'
    print region
    print '-------------------------'
    print

    for mode in range(3):    
        if not doChannel[mode]:
            continue
    
        for i in range(len(fileList)):
    
            print fileList[i]
    
            regiontemp = region
    
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
                if verbose:
                    evtCount += 1.
                    if evtCount/nEvents > percent:
                        k = int(percent*progSlots)
                        progress = '0%[' + '-' * k + ' ' * (int(progSlots)-k) + ']100%\r'
                        sys.stdout.write(progress)
                        sys.stdout.flush()
                        percent += 1./progSlots
    
                _met                    = event.met
    
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
                
                HistoLists[mode][i]['RegionCount'].Fill( RegionNumber[region]   , _weight )

                HistoLists[-1][i]['RegionCount'].Fill( RegionNumber[region]   , _weight )
    
    
            print
    
    
    
leg = TLegend(0.7,0.66,0.94,0.94)
#leg.SetFillStyle(1)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.AddEntry(HistoLists[0][-1]['RegionCount'], "Data", "p")
leg.AddEntry(HistoLists[0][0]['RegionCount'], "tW", "f")
leg.AddEntry(HistoLists[0][1]['RegionCount'], "t#bar{t}", "f")
leg.AddEntry(HistoLists[0][4]['RegionCount'], "Z/#gamma*+jets", "f")
leg.AddEntry(HistoLists[0][2]['RegionCount'], "Other", "f")




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
    labelcms2.AddText(lumiLabel +" "+ ChanLabels[mode])
    labelcms2.SetBorderSize(0);




    chanNum = mode
    if mode > 2:
        chanNum = 0
    


    startSample = 1
    for plot in plotInfo:
        
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][3][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][5][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][6][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][7][plot[0]])
        HistoLists[mode][2][plot[0]].Add(HistoLists[mode][8][plot[0]])

        for r in range(len(AllowedRegions)):
            HistoLists[mode][2][plot[0]].GetXaxis().SetBinLabel(r+1,AllowedRegions[r])

        hStack = THStack(plot[0],plot[0])
        hStack.Add(HistoLists[mode][2][plot[0]])
        hStack.Add(HistoLists[mode][4][plot[0]])
        hStack.Add(HistoLists[mode][1][plot[0]])
        hStack.Add(HistoLists[mode][0][plot[0]])


#         dataVal = HistoLists[mode][-1][plot[0]].Integral()
#         mcVal = errorBand.Integral()
        

#         labelcms3 = TPaveText(0.12,0.74,0.6,0.82,"NDCBR");
#         labelcms3.SetTextAlign(12);
#         labelcms3.SetTextSize(0.045);
#         labelcms3.SetFillColor(kWhite);
#         labelcms3.SetFillStyle(0);
# #        labelcms3.AddText("%s Data: %.2f MC: %.2f" %(region, dataVal, mcVal))
#         labelcms3.AddText(region)
#         labelcms3.SetBorderSize(0);


        
        c1 = TCanvas()
        gPad.SetLeftMargin(0.12)
        max_ = max(hStack.GetMaximum(),HistoLists[mode][-1][plot[0]].GetMaximum())
        hStack.Draw("histo")
        hStack.SetMaximum(max_*1.5)
        hStack.SetMinimum(0)

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
#         labelcms3.Draw()
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


        channel = ""
        if mode < 3:
            channel = "_" + ChanName[mode]

        
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+plot[0]+channel+runs+".pdf")
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+plot[0]+channel+runs+".png")


            

        c1.SetLogy()
        hStack.SetMaximum(max_*30)
        hStack.SetMinimum(1.)
        
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+plot[0]+channel+runs+"_log.pdf")
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+plot[0]+channel+runs+"_log.png")


