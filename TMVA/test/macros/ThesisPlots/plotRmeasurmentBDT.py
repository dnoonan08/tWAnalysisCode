#!/usr/bin/env python

import sys
if not '-b' in sys.argv:
    sys.argv.append( '-b' )
    
from ROOT import *
from setTDRStyle import *
from array import array
#from errorLists import *
import ROOT

import itertools
import glob
import os

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()
gStyle.SetErrorX(0.5)

regions = ['1j1t','2j1t','2j2t']
regions = ['1j1t','2j1t','2j2t','1j0t','2j0t']
regions = ['1j1t','1j0t']

ChanName = ['emu','mumu','ee']
#ChanName = ['emu']

file = TFile('../HistogramFile/AdaBoostDefault_NewTests_BDTRmeasurement_v2.root','r')

#KU Colors
colortw = kOrange-2
colortt = kRed+1
colorother = kGreen+2
colorzjet = kAzure-6

Colors = [colortw,
          colortt,
          colorother,
          colorother,
          colorzjet,
          colorother,
          colorother,
          colorother,
          colorother,
          kBlack]



BDT = 'AdaBoost'

samples = ['TWChannel',
           'TTbarNew',
           'TChannel',
           'SChannel',
           'ZJets',
           'WJets',
           'WW',
           'WZ',
           'ZZ',
           'DATA']


TotalLumi = 12200.

specialName = 'InputVariableBins'

totals = list()
errors = list()

        

RunA = True
RunB = True
RunC = True

binNames = ['-1 to -0.995', '-0.995 to -0.7','-0.7 to 0.7','0.7 to 0.995','0.995 to 1.']

emuChan = True
mumuChan = True
eeChan = True
combinedChan = True


oneLine = TH1F("_line","",1,-1,1)
oneLine.Fill(0)
oneLine.SetLineColor(kBlack)
oneLine.SetLineWidth(5)


TotalLumi = 808.472+82.136 + 4429. + 495.003+6383.
TotalLumi = 876.+4412.+7055.+7369.

TotalLumi = TotalLumi/1000.

#labelcms = TPaveText(0.14,0.76,0.6,0.92,"NDCBR")
labelcms = TPaveText(0.1,0.9,0.9,0.98,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.06);
labelcms.SetFillColor(kWhite);
labelcms.SetFillStyle(0);
labelcms.SetBorderSize(0);
labelcms.SetTextFont(42);

#gStyle.SetLabelSize(0.045,"x")
gStyle.SetLabelSize(0.035,"xy")


doChannel = [emuChan, mumuChan, eeChan, combinedChan]
    
doZpeakCuts = False

plots =  [
#     'ptjet',
#     'ht',
#     'msys','ptsys',
#     'ptjll',
#     'ptsys_ht',
#     'htleps_ht',
#     'NlooseJet20Central',
#     'NlooseJet20',
#     'NbtaggedlooseJet20',          
#     'met',
#     'loosejetPt', 
#     'centralityJLL',
#     'BDT14',
#     'BDT21',
#     'BDT28',
    'BDT35',
    'BDT35_plus',
    'BDT35_minus',
    'tWSepBDT',
    'tWSepBDT_max',
    'tWSepBDT_min',
#     'BDTBinned',
#     'BDTReBinned',
    
    ]


l_data = TH1F('a','',1,0,1)
l_data.SetMarkerStyle(20)
l_data.SetMarkerSize(1.2)
l_data.SetMarkerColor(kBlack)
l_data.SetLineColor(kBlack)
l_tw   = TH1F('b','',1,0,1)
l_tw.SetFillColor(Colors[0])
l_tt   = TH1F('c','',1,0,1)
l_tt.SetFillColor(Colors[1])
l_zjet = TH1F('d','',1,0,1)
l_zjet.SetFillColor(Colors[4])
l_oth  = TH1F('e','',1,0,1)
l_oth.SetFillColor(Colors[2])
l_syst = TH1F('f','',1,0,1)
l_syst.SetFillColor(kBlack)
l_syst.SetFillStyle(3354)        


leg = TLegend(0.68,0.6,0.94,0.89)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.SetTextFont(42)
leg.AddEntry(l_data, "Data", "p")
leg.AddEntry(l_tw  , "#it{tW}", "f")
leg.AddEntry(l_tt  , "#lower[-0.1]{#it{t#bar{t}}}", "f")
leg.AddEntry(l_zjet, "#lower[0.18]{#it{Z/#gamma*}+jets}", "f")
leg.AddEntry(l_oth , "Other", "f")
leg.AddEntry(l_syst, "Uncertainty", "f")


plotInfo = {'ptjet':['P_{T} leading jet [GeV]','Events / 10 GeV'],
            'ht':['H_{T} [GeV]','Events / 10 GeV'],
            'msys':['Mass-system [GeV]','Events / 10 GeV'],
            'ptsys':['P_{T} system [GeV]','Events / 4 GeV'],
            'ptjll':['P_{T}-jll [GeV]','Events / 10 GeV'],
            'ptsys_ht':['P_{T} system / H_{T}','Events'],
            'htleps_ht':['H_{T} leptons / H_{T}','Events'],
            'NlooseJet20Central':['Number of loose jets, P_{T} > 20 GeV, |#eta| < 2.4','Events'],
            'NlooseJet20':['Number of loose jets, P_{T} > 20 GeV','Events'],
            'NbtaggedlooseJet20':['Number of b-tagged loose jets, P_{T} > 20 GeV','Events'],
            'met':['MET [GeV]','Events / 5 GeV'],
            'loosejetPt':['P_{T} of loose jet [GeV]','Events / 5 GeV'],
            'centralityJLL':['Centrality - jll','Events'],
            'BDT':['BDT discriminant','Events'],
            'BDTBinned':['BDT discriminant','Events'],
            'BDTReBinned':['BDT discriminant','Events'],
            'BDT14':['BDT discriminant','Events'],
            'BDT21':['BDT discriminant','Events'],
            'BDT28':['BDT discriminant','Events'],
            'BDT35':['BDT discriminant','Events'],
            'BDT35_plus':['BDT discriminant','Events'],
            'BDT35_minus':['BDT discriminant','Events'],
            'tWSepBDT':['tW Reconstruction BDT discriminant','Events'],
            'tWSepBDT_max':['tW Reconstruction BDT discriminant','Events'],
            'tWSepBDT_min':['tW Reconstruction BDT discriminant','Events'],
            
            }



DataChannel = ['MuEG','DoubleMu','DoubleElectron']
Folder = ['emuChannel','mumuChannel','eeChannel']

ChanLabels = {'emu'  : ', #it{e#mu} channel',
              'mumu' : ', #it{#mu#mu} channel',
              'ee'   : ', #it{ee} channel',
              ' '    : '',
#              ' '    : ', ee/e#it{#mu}/#it{#mu#mu} channels',
#              ' '    : ', ee/e#mu/#mu#mu channels',
#              ' '    : ', #it{ee}/#it{e#mu}/#it{#mu#mu} channels',
#               ' '    : ', #it{e#mu}/#it{#mu#mu}/#it{ee} channels',
              }

lumiLabel = "L=%.1f fb^{-1}" % TotalLumi


Systs = ['JER','JES','UnclusteredMET','LES','PDF','BtagSF','PU']
ExtraTWSysts = ['TopMass','Q2','DRDS']
ExtraTTbarSysts = ['TopMass', 'Q2','Matching']


SampleSysts = {'TWChannel' : Systs[:]+ExtraTWSysts[:],
               'TTbarNew'     : Systs[:]+ExtraTTbarSysts[:],
               'TChannel'  : Systs[:],
               'SChannel'  : Systs[:],
               'ZJets'     : Systs[:] + ['ZjetSF'],
               'WJets'     : Systs[:],
               'WW'        : Systs[:],
               'WZ'        : Systs[:],
               'ZZ'        : Systs[:],
               'DATA'      : [],
               }

lineAtOne = TH1F("line","",1,-0.4,0.3)
lineAtOne.SetBinContent(1,1)
lineAtOne.SetBinError(1,0.0)
lineAtOne.SetLineColor(kBlack)
lineAtOne.SetLineWidth(1)


for plot in plots:
    for reg in regions:
        regionTotals = list()
        regionErrors = list()
        regionHistTots = list()
        
        for mode in ChanName:



            hists = list()
            SystUp = list()
            SystDown = list()

#            print plot, mode, reg
            error = file.Get(plot+"TWChannel"+mode+reg).Clone("errorBand")
            histTot = file.Get(plot+"TWChannel"+mode+reg).Clone("histTot")

            error.SetMarkerSize(0)
            error.SetLineWidth(1)
#            error.SetFillColor(kGray+1)
            error.SetFillColor(kBlack)
            error.SetFillStyle(3354)        

            file.cd()
            
            for i in range(len(samples)):
                sample = samples[i]
                hists.append(file.Get(plot+sample+mode+reg))
                hists[i].SetFillColor(Colors[i])
                hists[i].SetLineColor(kBlack)
                hists[i].SetLineWidth(1)
                hists[i].SetMarkerSize(0.0001)

                systHistsUp = list()
                systHistsDown = list()
                systs = SampleSysts[sample]
                for s in systs:
                    systHistsUp.append(file.Get(plot+sample+mode+reg+'_'+s+'Up'))
                    if 'DRDS' in s:
                        systHistsDown.append(file.Get(plot+sample+mode+reg))
                    else:
                        systHistsDown.append(file.Get(plot+sample+mode+reg+'_'+s+'Down'))

                SystUp.append(systHistsUp)
                SystDown.append(systHistsDown)

            hists[-1].SetMarkerSize(1.2)
            hists[-1].SetMarkerStyle(20)
            hists[-1].SetLineWidth(2)
            hists[-1].SetMarkerColor(kBlack)
            hists[-1].SetLineColor(kBlack)

            

            for bin in range(1,hists[i].GetNbinsX()+1):
                SystDict = {'JER'            : [0.,0.],
                            'JES'            : [0.,0.],
                            'UnclusteredMET' : [0.,0.],
                            'LES'            : [0.,0.],
                            'PDF'            : [0.,0.],
                            'BtagSF'         : [0.,0.],
                            'PU'             : [0.,0.],
                            'TopMass'        : [0.,0.],
                            'Q2'             : [0.,0.],
                            'DRDS'           : [0.,0.],
                            'Matching'       : [0.,0.],
                            'ZjetSF'         : [0.,0.],
                            'lepSF'          : [0.,0.],
                            'lumi'           : [0.,0.],
                            'ttxs'           : [0.,0.],
                            'Stat'           : [0.,0.],
                            }
                error.SetBinContent(bin,0.)
                histTot.SetBinContent(bin,0.)
                histTot.SetBinError(bin,0.)

                binTot = 0
                for i in range(len(samples)-1):

                    sample = samples[i]
                    central = hists[i].GetBinContent(bin)
                    binTot += central
                    
                    systs = SampleSysts[sample]

                    for s in range(len(systs)):
                        syst = systs[s]
                        sUp = SystUp[i]
                        sDown = SystDown[i]

                        SystDict[syst][0] += sUp[s].GetBinContent(bin)-central
                        SystDict[syst][1] += sDown[s].GetBinContent(bin)-central
                    
                    SystDict['Stat'][0] = sqrt(pow(SystDict['Stat'][0],2) + pow(hists[i].GetBinError(bin),2))
                    SystDict['lumi'][0] = sqrt(pow(SystDict['lumi'][0],2) + pow(central*0.044,2))
                    SystDict['lepSF'][0] = sqrt(pow(SystDict['lepSF'][0],2) + pow(central*0.02,2))

                    SystDict['Stat'][1] = sqrt(pow(SystDict['Stat'][1],2) + pow(hists[i].GetBinError(bin),2))
                    SystDict['lumi'][1] = sqrt(pow(SystDict['lumi'][1],2) + pow(central*0.044,2))
                    SystDict['lepSF'][1] = sqrt(pow(SystDict['lepSF'][1],2) + pow(central*0.02,2))

                    if 'TTbar' in sample:
                        SystDict['ttxs'][0] = sqrt(pow(SystDict['ttxs'][0],2) + pow(central*0.067,2))
                        SystDict['ttxs'][1] = sqrt(pow(SystDict['ttxs'][1],2) + pow(central*0.067,2))
                        

                up = 0.
                down = 0.
                for s in SystDict:
                    high = max(SystDict[s][0],SystDict[s][1])
                    low = max(SystDict[s][0],SystDict[s][1])
                    
                    up += high*high
                    down += low*low
                up = sqrt(up)
                down = sqrt(down)
                binUp = binTot + up
                binDown = binTot - down

                error.SetBinContent(bin,(binUp+binDown)/2.)
                error.SetBinError(bin,(binUp-binDown)/2.)
                histTot.SetBinContent(bin,binTot)
                
            hists[2].Add(hists[3])
            hists[2].Add(hists[5])
            hists[2].Add(hists[6])
            hists[2].Add(hists[7])
            hists[2].Add(hists[8])


            regionTotals.append(hists)
            regionErrors.append(error)
            regionHistTots.append(histTot)
            
            hStack = THStack(plot,plot)
            hStack.Add(hists[2])
            hStack.Add(hists[4])
            hStack.Add(hists[1])
            hStack.Add(hists[0])


            histTot2 = hists[0].Clone("histTot2")
            histTot2.Add(hists[1])
            histTot2.Add(hists[2])
            histTot2.Add(hists[4])

#             labelcms.Clear()
#             labelcms.AddText("CMS, #sqrt{s} = 8 TeV, " + lumiLabel);
#             labelcms.AddText(reg + ChanLabels[mode])
            labelcms.SetTextSize(0.05);
            labelcms.Clear()
            labelcms.AddText("CMS, #sqrt{s} = 8 TeV, " + lumiLabel + ", " + reg + ChanLabels[mode])
            
#             labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
#             labelcms.AddText(lumiLabel + " " +ChanLabels[mode])
#             labelcms.AddText(reg)
#             ksTest = error.KolmogorovTest(hists[-1])
#             ksLabel = "Kolmogorov Test: %.3f" % (ksTest)
#             labelcms.AddText(ksLabel)

            
            c1 = TCanvas("","",600,520)
            ROOT.SetOwnership(c1,0)

#             t1 = TPad("t1", "t1", 0.0,0.0,1.,0.25)
#             ROOT.SetOwnership(t1,0)
#             t1.Draw()
#             t1.cd()
#             t1.SetTopMargin(0.0)
#             t1.SetBottomMargin(0.35)
#             t1.SetLeftMargin(0.13)
            
#             dataRatio = hists[-1].Clone('dataRat')
#             dataRatio.Divide(histTot)

#             errorRatio = error.Clone('errorRat'+plot+reg+mode)
#             errorRatio.Divide(histTot)

# #             errorFile.cd()
# #             errorRatio.Write()

#             dataRatio.GetYaxis().SetLabelSize(0.06)

#             if 'BDTReBinned' in plot:
#                 dataRatio.GetXaxis().SetLabelSize(1.)
#                 for b in range(1,dataRatio.GetNbinsX()+1):
#                     dataRatio.GetXaxis().SetBinLabel(b, binNames[b-1])


#             dataRatio.SetMinimum(0.2)
#             dataRatio.SetMaximum(1.8)
#             dataRatio.GetYaxis().SetTitle("#frac{Data}{MC}")
#             dataRatio.GetYaxis().CenterTitle()
#             dataRatio.GetYaxis().SetTitleSize(0.18)
#             dataRatio.GetYaxis().SetTitleOffset(0.32)

#             dataRatio.GetXaxis().SetTitle(plotInfo[plot][0])
#             dataRatio.GetXaxis().SetTitleSize(0.2)
#             dataRatio.GetXaxis().SetTitleOffset(.85)

#             dataRatio.GetXaxis().SetLabelSize(0.16)
#             dataRatio.GetYaxis().SetLabelSize(0.16)
#             dataRatio.SetNdivisions(5,"Y")

#             dataRatioOver = dataRatio.Clone("dataRatioOver")
#             dataRatioUnder = dataRatio.Clone("dataRatioUnder")

#             dataRatioOver.Reset()
#             dataRatioUnder.Reset()
#             dataRatioOver.SetMarkerStyle(22)
#             dataRatioUnder.SetMarkerStyle(23)
#             for bin in range(1,dataRatio.GetNbinsX()+1):
#                 max_ = dataRatio.GetMaximum()
#                 min_ = dataRatio.GetMinimum()
#                 delta = (max_-min_)/15.
#                 dataRatioOver.SetBinError(bin,0.)
#                 dataRatioUnder.SetBinError(bin,0.)
#                 if dataRatio.GetBinContent(bin) > max_:
#                     dataRatioOver.SetBinContent(bin,max_-delta)                
#                 else:                
#                     dataRatioOver.SetBinContent(bin,min_-1.)
    
#                 if dataRatio.GetBinContent(bin) < min_ and not dataRatio.GetBinContent(bin) == 0:
#                     dataRatioUnder.SetBinContent(bin,min_+delta)
#                 else:
#                     dataRatioUnder.SetBinContent(bin,min_-1.)




#             dataRatio.Draw("e x0 pz")
#             errorRatio.Draw("e2 same")
#             dataRatioOver.Draw("ep same")
#             dataRatioUnder.Draw("ep same")
#             lineAtOne.Draw("e same")


            c1.cd()
            t2 = TPad("t2", "t1", 0.,0.,1.,1.)
            
            ROOT.SetOwnership(t2,0)
            t2.Draw()
            t2.cd()
            t2.SetBottomMargin(0.1)
            t2.SetTopMargin(0.1)
            t2.SetLeftMargin(0.13)

            max_ = max(hStack.GetMaximum(),hists[-1])
            if '1j0t' in reg:
                max_ *= 1.1
            hStack.Draw("histo")
            hStack.SetMaximum(max_*1.5)
            hStack.SetMinimum(0)
            hists[-1].Draw("e x0, same")
            error.Draw("e2 same")


            hStack.GetYaxis().SetTitle(plotInfo[plot][1])
            hStack.GetXaxis().SetTitle(plotInfo[plot][0])
            hStack.GetYaxis().CenterTitle()
            hStack.GetYaxis().SetTitleOffset(0.9)
            hStack.GetYaxis().SetTitleSize(0.07)
            hStack.GetYaxis().SetLabelSize(0.05)
            hStack.GetXaxis().SetTitleSize(0.06)
            hStack.GetXaxis().SetTitleOffset(0.8)
            hStack.GetXaxis().SetLabelSize(0.05)


            leg.Draw()
            labelcms.Draw()

            if not os.path.exists("plots2/"):
                command = "mkdir plots2/"
                os.system(command)
            if not os.path.exists("plots2/"+BDT):
                command = "mkdir plots2/"+BDT+"/"
                os.system(command)
            if not os.path.exists("plots2/"+BDT+"/"+reg):
                command = "mkdir plots2/"+BDT+"/"+reg
                os.system(command)

            c1.SaveAs("plots2/"+BDT+"/"+reg+"/"+plot+"_"+reg+"_"+mode+".pdf")
            c1.SaveAs("plots2/"+BDT+"/"+reg+"/"+plot+"_"+reg+"_"+mode+".png")

#            t1.Clear()
            t2.Clear()


        for i in range(len(regionTotals[0])):
            regionTotals[0][i].Add(regionTotals[1][i])
            regionTotals[0][i].Add(regionTotals[2][i])
            
        regionErrors[0].Add(regionErrors[1])
        regionErrors[0].Add(regionErrors[2])

        regionHistTots[0].Add(regionHistTots[1])
        regionHistTots[0].Add(regionHistTots[2])



        histTot2 = regionTotals[0][0].Clone("histTot2")
        histTot2.Add(regionTotals[0][1])
        histTot2.Add(regionTotals[0][2])
        histTot2.Add(regionTotals[0][4])

#         labelcms.Clear()
#         labelcms.AddText("CMS, #sqrt{s} = 8 TeV, " + lumiLabel);
#         labelcms.AddText(reg +ChanLabels[' '])
        labelcms.SetTextSize(0.06);
        labelcms.Clear()
        labelcms.AddText("CMS, #sqrt{s} = 8 TeV, " + lumiLabel + ", " + reg +ChanLabels[' '])

#         labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
#         labelcms.AddText(lumiLabel + " " +ChanLabels[' '])
#         labelcms.AddText(reg)
#         ksTest = regionErrors[0].KolmogorovTest(regionTotals[0][-1])
#         ksLabel = "Kolmogorov Test: %.3f" % (ksTest)
#         labelcms.AddText(ksLabel)



        hStack = THStack(plot,plot)
        hStack.Add(regionTotals[0][2])
        hStack.Add(regionTotals[0][4])
        hStack.Add(regionTotals[0][1])
        hStack.Add(regionTotals[0][0])


        c1 = TCanvas("","",600,520)
        ROOT.SetOwnership(c1,0)

#         t1 = TPad("t1", "t1", 0.0,0.0,1.,0.25)
#         ROOT.SetOwnership(t1,0)
#         t1.Draw()
#         t1.cd()
#         t1.SetTopMargin(0.0)
#         t1.SetBottomMargin(0.35)
#         t1.SetLeftMargin(0.13)

#         dataRatio = regionTotals[0][-1].Clone('dataRat')
#         dataRatio.Divide(regionHistTots[0])

#         errorRatio = regionErrors[0].Clone('errorRat'+plot+reg)
#         errorRatio.Divide(regionHistTots[0])

# #         errorFile.cd()
# #         errorRatio.Write()

#         if 'BDTReBinned' in plot:
#             for b in range(1,dataRatio.GetNbinsX()+1):
#                 dataRatio.GetXaxis().SetBinLabel(b, binNames[b-1])
                

#         dataRatio.SetMinimum(0.2)
#         dataRatio.SetMaximum(1.8)
#         dataRatio.GetYaxis().SetTitle("#frac{Data}{MC}")
#         dataRatio.GetYaxis().CenterTitle()
#         dataRatio.GetYaxis().SetTitleSize(0.18)
#         dataRatio.GetYaxis().SetTitleOffset(0.32)

#         dataRatio.GetXaxis().SetTitle(plotInfo[plot][0])
#         dataRatio.GetXaxis().SetTitleSize(0.2)
#         dataRatio.GetXaxis().SetTitleOffset(.85)

#         dataRatio.GetXaxis().SetLabelSize(0.16)
#         dataRatio.GetYaxis().SetLabelSize(0.16)
#         dataRatio.SetNdivisions(5,"Y")

#         dataRatioOver = dataRatio.Clone("dataRatioOver")
#         dataRatioUnder = dataRatio.Clone("dataRatioUnder")

#         dataRatioOver.Reset()
#         dataRatioUnder.Reset()
#         dataRatioOver.SetMarkerStyle(22)
#         dataRatioUnder.SetMarkerStyle(23)
#         for bin in range(1,dataRatio.GetNbinsX()+1):
#             max_ = dataRatio.GetMaximum()
#             min_ = dataRatio.GetMinimum()
#             delta = (max_-min_)/15.
#             dataRatioOver.SetBinError(bin,0.)
#             dataRatioUnder.SetBinError(bin,0.)
#             if dataRatio.GetBinContent(bin) > max_:
#                 dataRatioOver.SetBinContent(bin,max_-delta)                
#             else:                
#                 dataRatioOver.SetBinContent(bin,min_-1.)

#             if dataRatio.GetBinContent(bin) < min_ and not dataRatio.GetBinContent(bin) == 0:
#                 dataRatioUnder.SetBinContent(bin,min_+delta)
#             else:
#                 dataRatioUnder.SetBinContent(bin,min_-1.)




#         dataRatio.Draw("e x0 pz")
#         errorRatio.Draw("e2 same")
#         dataRatioOver.Draw("ep same")
#         dataRatioUnder.Draw("ep same")
#         lineAtOne.Draw("e same")


        c1.cd()
        t2 = TPad("t2", "t1", 0.,.0,1.,1.)
#        t2 = TPad("t2", "t1", 0.,.15,1.,1.)
        ROOT.SetOwnership(t2,0)
        t2.Draw()
        t2.cd()
        t2.SetTopMargin(0.1)
        t2.SetBottomMargin(0.1)
        t2.SetLeftMargin(0.13)

        max_ = max(hStack.GetMaximum(),regionTotals[0][-1])
        if '1j0t' in reg:
            max_ *= 1.1
        hStack.Draw("histo")
        hStack.SetMaximum(max_*1.5)
        hStack.SetMinimum(0)
        regionTotals[0][-1].Draw("e x0, same")
        regionErrors[0].Draw("e2 same")


        hStack.GetYaxis().SetTitle(plotInfo[plot][1])
        hStack.GetXaxis().SetTitle(plotInfo[plot][0])
        hStack.GetYaxis().CenterTitle()
        hStack.GetYaxis().SetTitleOffset(0.95)
        hStack.GetYaxis().SetTitleSize(0.07)
        hStack.GetYaxis().SetLabelSize(0.05)
        hStack.GetXaxis().SetTitleSize(0.06)
        hStack.GetXaxis().SetTitleOffset(0.8)
        hStack.GetXaxis().SetLabelSize(0.05)



        leg.Draw()
        labelcms.Draw()


        
        c1.SaveAs("plots2/"+BDT+"/"+reg+"/"+plot+"_"+reg+".pdf")
        c1.SaveAs("plots2/"+BDT+"/"+reg+"/"+plot+"_"+reg+".png")

#        t1.Clear()
        t2.Clear()

