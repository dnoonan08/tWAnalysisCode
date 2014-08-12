#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array
from ZjetSF import *
from errorLists import *


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
#     print vFolder

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
            ]

fileList = ['TWChannel.root',
            'TTbar.root',
            'ZJets.root',
            'DATA']


DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']
ChanName = ['emu','mumu','ee']
ChanLabels = [', e#mu channel',', #mu#mu channel',', ee channel', 'e#mu/#mu#mu/ee channels']
lumiLabel = "%.1f fb^{-1}" % TotalLumi

if 'ZpeakLepSel' in region or '1j1tZpeak' in region:
    ChanLabels[3] = 'ee/#mu#mu channels'
    doChannel[0] = False

if not os.path.exists('correlations'):
    command = "mkdir correlations"
    os.system(command)
if not os.path.exists('correlations/'+region):
    command = "mkdir correlations/"+region
    os.system(command)




HistoLists = list()


for i in range(len(fileList)):
    Histos = dict()
    
    fileName = fileList[i].split('.')[0]
    for i in range(len(plotInfo)):
        plotI = plotInfo[i]
        for j in range(len(plotInfo)):
            plotJ = plotInfo[j]
            Histos[plotI[0]+plotJ[0]] = TH2F(plotI[0]+plotJ[0]+fileName," ",plotI[1],plotI[2],plotI[3],plotJ[1],plotJ[2],plotJ[3])
            Histos[plotI[0]+plotJ[0]].Sumw2()

    HistoLists.append(Histos)



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
            _ht                        = event.ht                      
            _msys                      = event.msys                    
            _mll                       = event.mll
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
                    
#             elif mode > 0 and _met < 50:
#                 continue

            
            Values = {
                'ptjet'              : _ptjet             ,
                'ht'                 : _ht                ,
                'msys'               : _msys              ,
                'ptsys'              : _ptsys             ,
                'ptjll'              : _ptjll             ,
                'ptsys_ht'           : _ptsys_ht          ,
                'htleps_ht'          : _htleps_ht         ,
                'NlooseJet20Central' : _NlooseJet20Central,
                'NlooseJet20'        : _NlooseJet20       ,
                'NbtaggedlooseJet20' : _NbtaggedlooseJet20,
                'met'                : _met               ,
                'loosejetPt'         : _loosejetPt        ,
                'centralityJLL'      : _centralityJLL     ,
                }



            for varx in plotInfo:
                varX = varx[0]
                for vary in plotInfo:
                    varY = vary[0]
                    HistoLists[i][varX+varY].Fill(  Values[varX], Values[varY], _weight)


        print


for i in range(len(fileList)):
    file = fileList[i].split('.')[0]
    hCorr = TH2F("correlation"+file,'',len(plotInfo),0,len(plotInfo),len(plotInfo),0,len(plotInfo))
    for x in range(len(plotInfo)):
        varX = plotInfo[x][0]
        for y in range(len(plotInfo)):
            varY = plotInfo[y][0]            
            hCorr.Fill(x,y,HistoLists[i][varX+varY].GetCorrelationFactor())

    for x in range(len(plotInfo)):
        var = plotInfo[x][0]
        hCorr.GetXaxis().SetBinLabel(x+1,var)
        hCorr.GetYaxis().SetBinLabel(x+1,var)
    c1 = TCanvas()
    gPad.SetLeftMargin(0.2)
    gPad.SetRightMargin(0.1)
    gPad.SetBottomMargin(0.1)
    gStyle.SetPaintTextFormat(".2f")
    gStyle.SetPalette(1)
    hCorr.SetMarkerSize(1.)
    hCorr.Draw("colz TEXT0")
    
    c1.SaveAs("correlations/"+region+"/"+file+".pdf")


hCorr = TH2F("correlation"+file,'',len(plotInfo),0,len(plotInfo),len(plotInfo),0,len(plotInfo))
for i in range(1,len(fileList)-1):
    file = fileList[i].split('.')[0]    
    for x in range(len(plotInfo)):
        varX = plotInfo[x][0]
        for y in range(len(plotInfo)):
            varY = plotInfo[y][0]            
            HistoLists[0][varX+varY].Add(HistoLists[i][varX+varY])

for x in range(len(plotInfo)):
    varX = plotInfo[x][0]
    for y in range(len(plotInfo)):
        varY = plotInfo[y][0]
        hCorr.Fill(x,y,HistoLists[0][varX+varY].GetCorrelationFactor())

for x in range(len(plotInfo)):
    var = plotInfo[x][0]
    hCorr.GetXaxis().SetBinLabel(x+1,var)
    hCorr.GetYaxis().SetBinLabel(x+1,var)
c1 = TCanvas()
gPad.SetLeftMargin(0.2)
gPad.SetRightMargin(0.1)
gPad.SetBottomMargin(0.1)
gStyle.SetPaintTextFormat(".2f")
gStyle.SetPalette(1)
hCorr.SetMarkerSize(1.)
hCorr.Draw("colz TEXT0")

c1.SaveAs("correlations/"+region+"/TotalMC.pdf")
