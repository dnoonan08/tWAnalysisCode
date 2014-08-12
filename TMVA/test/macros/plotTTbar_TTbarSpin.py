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

BDT = 'Bagging2000TreesMET50'

TotalLumi = 0.

channelPicked = False
emuChan = False
mumuChan = False
eeChan = False
combinedChan = False

versionPicked = False

useNNLOTTbar = True

specialName = 'TTbarSpinComparison'

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
    vFolder = 'v11_MET50'
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
            ['BDT',50,-1.01,1.01,'BDT Discriminant','Events'],
            ['BDT-Binned',5,-1.01,1.01,'BDT Discriminant','Events'],

            ]

fileList = ['TTbar.root',
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

if 'ZpeakLepSel' in region or '1j1tZpeak' in region:
    ChanLabels[3] = 'ee/#mu#mu channels'
#    doChannel[0] = False

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

        Histos['BDT-Binned'] = TH1F('BDT-Binned'+fileName+ChanName[mode]," ",5,newBins)
        Histos['BDT-Binned'].SetLineColor(Colors[i])
        Histos['BDT-Binned'].SetLineWidth(3)
        Histos['BDT-Binned'].SetMarkerSize(0.0001)
        Histos['BDT-Binned'].Sumw2()

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

    Histos['BDT-Binned'] = TH1F('BDT-Binned'+fileName+ChanName[mode]," ",5,newBins)
    Histos['BDT-Binned'].SetLineColor(Colors[i])
    Histos['BDT-Binned'].SetLineWidth(3)
    Histos['BDT-Binned'].SetMarkerSize(0.0001)
    Histos['BDT-Binned'].Sumw2()

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

        BDTtree = TChain(BDT + '_' + ChanName[mode] + '_' + region)

        fileName = file.replace('.ro','_Output.ro')

        if 'TTbarSpin' in file:
            fileName = 'TTbarSpin_Output_'+ChanName[mode]+'_'+region+'.root'

        BDTtree.Add('../tmvaFiles/'+vFolder+'/'+BDT+'/'+fileName)

        tree = TChain(Folder[mode]+'/'+regiontemp)

        tree.Add('../tmvaFiles/'+vFolder+'/'+fileList[i])

        nEvents = tree.GetEntries()*1.
        nEvents2 = BDTtree.GetEntries()*1.

        print nEvents, nEvents2

        evtCount = 0.
        percent = 0.0
        progSlots = 25.    

        for event,bdtevt in itertools.izip(tree,BDTtree):
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
            if 'TestDir_v3' in vFolder:
                _mll                   = event.mll
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
            
            _weightA                    = event.weightA
            _weightB                    = event.weightB
            _weightC                    = event.weightC

            _BDT                        = bdtevt.BDT
            
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
            HistoLists[mode][i]['BDT'].Fill(                      _BDT                      , _weight )
            HistoLists[mode][i]['BDT-Binned'].Fill(               _BDT                      , _weight )

            HistoLists[-1][i]['ptjet'].Fill(                    _ptjet                    , _weight )
            HistoLists[-1][i]['ht'].Fill(                       _ht                       , _weight )
            HistoLists[-1][i]['msys'].Fill(                     _msys                     , _weight )
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
            HistoLists[-1][i]['BDT'].Fill(                      _BDT                      , _weight )
            HistoLists[-1][i]['BDT-Binned'].Fill(               _BDT                      , _weight )



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

#         c1.SetLogy()
#         HistoLists[mode][0][plot[0]].SetMaximum(max_*30)
#         HistoLists[mode][0][plot[0]].SetMinimum(1.)
        
#         c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+"_log.pdf")
#         c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/"+region+"/"+plot[0]+"_"+region+channel+runs+"_log.png")

        t1.Clear()
        t2.Clear()


# signal = [0.,0.,0.]
# bkg = [0.,0.,0.]
# sigErr = [0.,0.,0.]
# bkgErr = [0.,0.,0.]

# print
# print "\\begin{tabular}{| l | c | c | c | c |}"
# print "\\hline"
# print "Channel & $e\\mu$ & $\\mu\\mu$ & $ee$ & Combined \\\\"
# print "\\hline"

# for i in range(len(fileList) - 1):
#     print fileList[i],"&","%.1f" % totals[0][i],"$\pm$","%.1f" % errors[0][i],"&","%.1f" % totals[1][i],"$\pm$","%.1f" % errors[1][i],"&","%.1f" % totals[2][i],"$\pm$","%.1f" % errors[2][i],"&","%.1f" % (totals[0][i]+totals[1][i]+totals[2][i]),"$\pm$","%.1f" % sqrt(pow(errors[0][i],2)+pow(errors[1][i],2)+pow(errors[2][i],2)),"\\\\"
#     if i == 0:
#         signal[0] += totals[0][i]
#         signal[1] += totals[1][i]
#         signal[2] += totals[2][i]
#         sigErr[0] = sqrt(pow(sigErr[0],2) + pow(errors[0][i],2))
#         sigErr[1] = sqrt(pow(sigErr[1],2) + pow(errors[1][i],2))
#         sigErr[2] = sqrt(pow(sigErr[2],2) + pow(errors[2][i],2))
#     else:
#         bkg[0] += totals[0][i]
#         bkg[1] += totals[1][i]
#         bkg[2] += totals[2][i]
#         bkgErr[0] = sqrt(pow(bkgErr[0],2) + pow(errors[0][i],2))
#         bkgErr[1] = sqrt(pow(bkgErr[1],2) + pow(errors[1][i],2))
#         bkgErr[2] = sqrt(pow(bkgErr[2],2) + pow(errors[2][i],2))
        
# print "\\hline"
# print "Signal &","%.1f" % signal[0],"$\pm$","%.1f" % sigErr[0],"&","%.1f" % signal[1],"$\pm$","%.1f" % sigErr[1],"&","%.1f" % signal[2],"$\pm$","%.1f" % sigErr[2],"&","%.1f" % (signal[0]+signal[1]+signal[2]),"$\pm$","%.1f" % sqrt(pow(sigErr[0],2)+pow(sigErr[1],2)+pow(sigErr[2],2)), " \\\\"
# print "Background &","%.1f" % bkg[0],"$\pm$","%.1f" % bkgErr[0],"&","%.1f" % bkg[1],"$\pm$","%.1f" % bkgErr[1],"&","%.1f" % bkg[2],"$\pm$","%.1f" % bkgErr[2],"&","%.1f" % (bkg[0]+bkg[1]+bkg[2]),"$\pm$","%.1f" % sqrt(pow(bkgErr[0],2)+pow(bkgErr[1],2)+pow(bkgErr[2],2)), " \\\\"
# print "Data &","%.1f" % totals[0][-1],"$\pm$","%.1f" % errors[0][-1],"&","%.1f" % totals[1][-1],"$\pm$","%.1f" % errors[1][-1],"&","%.1f" % totals[2][-1],"$\pm$","%.1f" % errors[2][-1],"&","%.1f" % (totals[0][-1]+totals[1][-1]+totals[2][-1]),"$\pm$","%.1f" % sqrt(pow(errors[0][-1],2)+pow(errors[1][-1],2)+pow(errors[2][-1],2)), " \\\\"
# print "Sum All MC &","%.1f" % (signal[0]+bkg[0]),"$\pm$","%.1f" % sqrt(pow(sigErr[0],2)+pow(bkgErr[0],2)),"&","%.1f" % (signal[1]+bkg[1]),"$\pm$","%.1f" % sqrt(pow(sigErr[1],2)+pow(bkgErr[1],2)),"&","%.1f" % (signal[2]+bkg[2]),"$\pm$","%.1f" % sqrt(pow(sigErr[2],2)+pow(bkgErr[2],2)),"&","%.1f" % (signal[0]+signal[1]+signal[2]+bkg[0]+bkg[1]+bkg[2]),"$\pm$","%.1f" % sqrt(pow(sigErr[0],2)+pow(sigErr[1],2)+pow(sigErr[2],2)+pow(bkgErr[0],2)+pow(bkgErr[1],2)+pow(bkgErr[2],2)), " \\\\"


# # print "Background &","%.1f" % bkg[0],"&","%.1f" % bkg[1],"&","%.1f" % bkg[2],"&","%.1f" % (bkg[0]+bkg[1]+bkg[2]), " \\\\"
# # print "Data &","%.1f" % totals[0][-1],"&","%.1f" % totals[1][-1],"&","%.1f" % totals[2][-1],"&","%.1f" % (totals[0][-1]+totals[1][-1]+totals[2][-1]), " \\\\"
# print "\\hline"
# for i in range(3):
#     if signal[i] == 0 and bkg[i] == 0:
#         bkg[i] = 1.
# print "S/B &","%.4f" % (signal[0]/bkg[0]),"&","%.4f" % (signal[1]/bkg[1]),"&","%.4f" % (signal[2]/bkg[2]),"&","%.4f" % ((signal[0]+signal[1]+signal[2])/(bkg[0]+bkg[1]+bkg[2])), " \\\\"
# print "$S/\\sqrt{B}$ &","%.2f" % (signal[0]/sqrt(bkg[0])),"&","%.2f" % (signal[1]/sqrt(bkg[1])),"&","%.2f" % (signal[2]/sqrt(bkg[2])),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2])), " \\\\"
# print "\\hline"
# print "$S/\\sqrt{B+dB^2}$ (5\\%) &","%.2f" % (signal[0]/sqrt(bkg[0]+pow(0.05*bkg[0],2))),"&","%.2f" % (signal[1]/sqrt(bkg[1]+pow(0.05*bkg[1],2))),"&","%.2f" % (signal[2]/sqrt(bkg[2]+pow(0.05*bkg[2],2))),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2]+pow((bkg[0]+bkg[1]+bkg[2])*0.05,2))), " \\\\"
# print "$S/\\sqrt{B+dB^2}$ (10\\%) &","%.2f" % (signal[0]/sqrt(bkg[0]+pow(0.1*bkg[0],2))),"&","%.2f" % (signal[1]/sqrt(bkg[1]+pow(0.1*bkg[1],2))),"&","%.2f" % (signal[2]/sqrt(bkg[2]+pow(0.1*bkg[2],2))),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2]+pow((bkg[0]+bkg[1]+bkg[2])*0.1,2))), " \\\\"
# print "$S/\\sqrt{B+dB^2}$ (15\\%) &","%.2f" % (signal[0]/sqrt(bkg[0]+pow(0.15*bkg[0],2))),"&","%.2f" % (signal[1]/sqrt(bkg[1]+pow(0.15*bkg[1],2))),"&","%.2f" % (signal[2]/sqrt(bkg[2]+pow(0.15*bkg[2],2))),"&","%.2f" % ((signal[0]+signal[1]+signal[2])/sqrt(bkg[0]+bkg[1]+bkg[2]+pow((bkg[0]+bkg[1]+bkg[2])*0.15,2))), " \\\\"
# print "\\hline"
# print "\\end{tabular}"

