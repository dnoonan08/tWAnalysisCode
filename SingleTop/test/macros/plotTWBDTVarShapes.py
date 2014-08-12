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

bdtPlots = ['lepJetPt',
            'lepPt',
            'lepJetDR',
            'lepJetDPhi',
            'lepJetDEta',
            'lepJetM',
            'lepPtRelJet',
            'jetPtRelLep',
            'lepPtRelJetSameLep',
            'lepPtRelJetOtherLep',
            'lepJetMt',
            'lepJetCosTheta_boosted',
            ]
    
plotInfo = [
            ['lepJetPt',40,0,300,'P_{T} jet & lepton','Events'],
            ['lepPt',40,0,300,'P_{T} lepton','Events'],
            ['lepJetDR',40,0,6,'#Delta R(jet,lepton)','Events'],
            ['lepJetDPhi',40,0,3.2,'#Delta #phi (jet,lepton)','Events'],
            ['lepJetDEta',40,0,5,'#Delta #eta (jet,lepton)','Events'],
            ['lepJetM',40,0,300,'Mass of jet & lepton','Events'],
            ['lepPtRelJet',40,0,200,'P_{T} lepton relative to jet','Events'],
            ['jetPtRelLep',40,0,200,'P_{T} jet relative to lepton','Events'],
            ['lepPtRelJetSameLep',40,0,200,'P_{T} lepton relative to jet & same lepton','Events'],
            ['lepPtRelJetOtherLep',40,0,200,'P_{T} lepton relative to jet & other lepton','Events'],
            ['lepJetMt',40,0,300,'M_{T} jet & lepton','Events'],
            ['lepJetCosTheta_boosted',40,-1.,1.,'Cos #theta (lepton,jet)','Events'],
            ]


fileList = ['TWDilepton_T123.root',
            'TWDilepton_Tbar123.root',
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

histName = ['topLepton','WLepton']

for mode in range(3):


    HistoMode = list()

    for i in range(len(fileList)):
        Histos = dict()

        fileName = histName[i]
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

            _lepJetPt_PosLep               = event.lepJetPt_PosLep           
            _lepPt_PosLep                  = event.lepPt_PosLep              
            _lepJetDR_PosLep               = event.lepJetDR_PosLep           
            _lepJetDPhi_PosLep             = event.lepJetDPhi_PosLep         
            _lepJetDEta_PosLep             = event.lepJetDEta_PosLep         
            _lepJetM_PosLep                = event.lepJetM_PosLep            
            _lepPtRelJet_PosLep            = event.lepPtRelJet_PosLep        
            _jetPtRelLep_PosLep            = event.jetPtRelLep_PosLep        
            _lepPtRelJetSameLep_PosLep     = event.lepPtRelJetSameLep_PosLep 
            _lepPtRelJetOtherLep_PosLep    = event.lepPtRelJetOtherLep_PosLep
            _lepJetMt_PosLep               = event.lepJetMt_PosLep           
            _lepJetCosTheta_boosted_PosLep = event.lepJetCosTheta_boosted_PosLep
            _lepJetPt_NegLep               = event.lepJetPt_NegLep           
            _lepPt_NegLep                  = event.lepPt_NegLep              
            _lepJetDR_NegLep               = event.lepJetDR_NegLep           
            _lepJetDPhi_NegLep             = event.lepJetDPhi_NegLep         
            _lepJetDEta_NegLep             = event.lepJetDEta_NegLep         
            _lepJetM_NegLep                = event.lepJetM_NegLep            
            _lepPtRelJet_NegLep            = event.lepPtRelJet_NegLep        
            _jetPtRelLep_NegLep            = event.jetPtRelLep_NegLep        
            _lepPtRelJetSameLep_NegLep     = event.lepPtRelJetSameLep_NegLep 
            _lepPtRelJetOtherLep_NegLep    = event.lepPtRelJetOtherLep_NegLep
            _lepJetMt_NegLep               = event.lepJetMt_NegLep           
            _lepJetCosTheta_boosted_NegLep = event.lepJetCosTheta_boosted_NegLep


                
            _weight = 1.

            posNumber = 2
            negNumber = 2

            if i == 0:
                posNumber = 0
                negNumber = 1
            if i == 1:
                posNumber = 1
                negNumber = 0
                

            HistoLists[mode][posNumber]['lepJetPt'].Fill(               _lepJetPt_PosLep              , _weight )
            HistoLists[mode][posNumber]['lepPt'].Fill(                  _lepPt_PosLep                 , _weight )
            HistoLists[mode][posNumber]['lepJetDR'].Fill(               _lepJetDR_PosLep              , _weight )
            HistoLists[mode][posNumber]['lepJetDPhi'].Fill(             _lepJetDPhi_PosLep            , _weight )
            HistoLists[mode][posNumber]['lepJetDEta'].Fill(             _lepJetDEta_PosLep            , _weight )
            HistoLists[mode][posNumber]['lepJetM'].Fill(                _lepJetM_PosLep               , _weight )
            HistoLists[mode][posNumber]['lepPtRelJet'].Fill(            _lepPtRelJet_PosLep           , _weight )
            HistoLists[mode][posNumber]['jetPtRelLep'].Fill(            _jetPtRelLep_PosLep           , _weight )
            HistoLists[mode][posNumber]['lepPtRelJetSameLep'].Fill(     _lepPtRelJetSameLep_PosLep    , _weight )
            HistoLists[mode][posNumber]['lepPtRelJetOtherLep'].Fill(    _lepPtRelJetOtherLep_PosLep   , _weight )
            HistoLists[mode][posNumber]['lepJetMt'].Fill(               _lepJetMt_PosLep              , _weight )
            HistoLists[mode][posNumber]['lepJetCosTheta_boosted'].Fill( _lepJetCosTheta_boosted_PosLep, _weight )

            HistoLists[mode][negNumber]['lepJetPt'].Fill(               _lepJetPt_NegLep              , _weight )
            HistoLists[mode][negNumber]['lepPt'].Fill(                  _lepPt_NegLep                 , _weight )
            HistoLists[mode][negNumber]['lepJetDR'].Fill(               _lepJetDR_NegLep              , _weight )
            HistoLists[mode][negNumber]['lepJetDPhi'].Fill(             _lepJetDPhi_NegLep            , _weight )
            HistoLists[mode][negNumber]['lepJetDEta'].Fill(             _lepJetDEta_NegLep            , _weight )
            HistoLists[mode][negNumber]['lepJetM'].Fill(                _lepJetM_NegLep               , _weight )
            HistoLists[mode][negNumber]['lepPtRelJet'].Fill(            _lepPtRelJet_NegLep           , _weight )
            HistoLists[mode][negNumber]['jetPtRelLep'].Fill(            _jetPtRelLep_NegLep           , _weight )
            HistoLists[mode][negNumber]['lepPtRelJetSameLep'].Fill(     _lepPtRelJetSameLep_NegLep    , _weight )
            HistoLists[mode][negNumber]['lepPtRelJetOtherLep'].Fill(    _lepPtRelJetOtherLep_NegLep   , _weight )
            HistoLists[mode][negNumber]['lepJetMt'].Fill(               _lepJetMt_NegLep              , _weight )
            HistoLists[mode][negNumber]['lepJetCosTheta_boosted'].Fill( _lepJetCosTheta_boosted_NegLep, _weight )


            HistoLists[-1][posNumber]['lepJetPt'].Fill(               _lepJetPt_PosLep              , _weight )
            HistoLists[-1][posNumber]['lepPt'].Fill(                  _lepPt_PosLep                 , _weight )
            HistoLists[-1][posNumber]['lepJetDR'].Fill(               _lepJetDR_PosLep              , _weight )
            HistoLists[-1][posNumber]['lepJetDPhi'].Fill(             _lepJetDPhi_PosLep            , _weight )
            HistoLists[-1][posNumber]['lepJetDEta'].Fill(             _lepJetDEta_PosLep            , _weight )
            HistoLists[-1][posNumber]['lepJetM'].Fill(                _lepJetM_PosLep               , _weight )
            HistoLists[-1][posNumber]['lepPtRelJet'].Fill(            _lepPtRelJet_PosLep           , _weight )
            HistoLists[-1][posNumber]['jetPtRelLep'].Fill(            _jetPtRelLep_PosLep           , _weight )
            HistoLists[-1][posNumber]['lepPtRelJetSameLep'].Fill(     _lepPtRelJetSameLep_PosLep    , _weight )
            HistoLists[-1][posNumber]['lepPtRelJetOtherLep'].Fill(    _lepPtRelJetOtherLep_PosLep   , _weight )
            HistoLists[-1][posNumber]['lepJetMt'].Fill(               _lepJetMt_PosLep              , _weight )
            HistoLists[-1][posNumber]['lepJetCosTheta_boosted'].Fill( _lepJetCosTheta_boosted_PosLep, _weight )

            HistoLists[-1][negNumber]['lepJetPt'].Fill(               _lepJetPt_NegLep              , _weight )
            HistoLists[-1][negNumber]['lepPt'].Fill(                  _lepPt_NegLep                 , _weight )
            HistoLists[-1][negNumber]['lepJetDR'].Fill(               _lepJetDR_NegLep              , _weight )
            HistoLists[-1][negNumber]['lepJetDPhi'].Fill(             _lepJetDPhi_NegLep            , _weight )
            HistoLists[-1][negNumber]['lepJetDEta'].Fill(             _lepJetDEta_NegLep            , _weight )
            HistoLists[-1][negNumber]['lepJetM'].Fill(                _lepJetM_NegLep               , _weight )
            HistoLists[-1][negNumber]['lepPtRelJet'].Fill(            _lepPtRelJet_NegLep           , _weight )
            HistoLists[-1][negNumber]['jetPtRelLep'].Fill(            _jetPtRelLep_NegLep           , _weight )
            HistoLists[-1][negNumber]['lepPtRelJetSameLep'].Fill(     _lepPtRelJetSameLep_NegLep    , _weight )
            HistoLists[-1][negNumber]['lepPtRelJetOtherLep'].Fill(    _lepPtRelJetOtherLep_NegLep   , _weight )
            HistoLists[-1][negNumber]['lepJetMt'].Fill(               _lepJetMt_NegLep              , _weight )
            HistoLists[-1][negNumber]['lepJetCosTheta_boosted'].Fill( _lepJetCosTheta_boosted_NegLep, _weight )


leg = TLegend(0.66,0.75,0.94,0.89)
#leg.SetFillStyle(1)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.AddEntry(HistoLists[0][0]['lepJetPt'], "Top Lepton", "f")
leg.AddEntry(HistoLists[0][1]['lepJetPt'], "W Lepton", "f")

leg2 = TLegend(0.13,0.75,0.41,0.89)
leg2.SetFillColor(kWhite)
leg2.SetBorderSize(1)
leg2.AddEntry(HistoLists[0][0]['lepJetPt'], "Top Lepton", "f")
leg2.AddEntry(HistoLists[0][1]['lepJetPt'], "W Lepton", "f")


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
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName +"/normalizedPlots_2"):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+'/normalizedPlots_2'
            os.system(command)
        if not os.path.exists("VariablePlots/"+vFolder+"/"+specialName +"/normalizedPlots_2/" + region):
            command = "mkdir VariablePlots/"+vFolder+"/"+specialName+'/normalizedPlots_2/'+region
            os.system(command)

        channel = ""
        if mode < 3:
            channel = "_" + ChanName[mode]

        
        c1.SaveAs("VariablePlots/"+vFolder+"/"+specialName+"/normalizedPlots_2/"+region+"/"+plot[0]+"_"+region+channel+".pdf")
        

        print
