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

fast = False

i = 1
while i < len(sys.argv):
    arg=sys.argv[i]
    if arg == '-b':
        i += 1
        continue
    else:
        print "Unknown argument", arg," will be ignored"
    i += 1


labelcms = TPaveText(0.1,0.9,0.9,0.98,"NDCBR")
labelcms.SetTextAlign(12);
labelcms.SetTextSize(0.045);
labelcms.SetFillColor(kWhite);
labelcms.SetFillStyle(0);
labelcms.AddText("CMS Preliminary, #sqrt{s} = 8 TeV");
labelcms.SetBorderSize(0);

#gStyle.SetLabelSize(0.045,"x")
gStyle.SetLabelSize(0.035,"xy")



BDT_Train = [TH1F('BDTTrainSig','',40,-1.,1.), TH1F('BDTTrainBkg','',40,-1.,1.)]
BDT_Test  = [TH1F('BDTTestSig','',40,-1.,1.),  TH1F('BDTTestBkg','',40,-1.,1.)]


Colors = [TColor.GetColor( "#7d99d1" ),
          TColor.GetColor( "#ff0000" ),
          ]

Style = [1001,
         3554,
         ]

Lines = [TColor.GetColor( "#0000ee" ),
         TColor.GetColor( "#ff0000" ),
         ]


for i in range(2):
    BDT_Train[i].SetFillColor(Colors[i])
    BDT_Train[i].SetFillStyle(Style[i])
    BDT_Train[i].SetLineColor(Lines[i])
    BDT_Train[i].SetLineWidth(2)
    BDT_Train[i].SetMarkerSize(0.)
#     BDT_Train[i].Sumw2()

    BDT_Test[i].SetFillColor(Colors[i])
    BDT_Test[i].SetFillStyle(Style[i])
    BDT_Test[i].SetLineColor(Lines[i])
    BDT_Test[i].SetLineWidth(2)
    BDT_Test[i].SetMarkerSize(0.)
    BDT_Test[i].Sumw2()


Traintree = TChain('TrainTree')
Testtree = TChain('TestTree')

Traintree.Add('../trainrootfiles/test_tW_tbarW_tW_tbarW_April15.root')
Testtree.Add('../trainrootfiles/test_tW_tbarW_tW_tbarW_April15.root')



for event in Traintree:
    classID = event.classID
    BDT = event.tW_tbarW_April15GradBoost500Trees

    BDT_Train[classID].Fill(BDT)

for event in Testtree:
    classID = event.classID
    BDT = event.tW_tbarW_April15GradBoost500Trees

    BDT_Test[classID].Fill(BDT)


leg = TLegend(0.13,0.75,0.41,0.89)
leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.AddEntry(BDT_Train[0], "Top Lepton", "f")
leg.AddEntry(BDT_Train[1], "W Lepton", "f")

c1 = TCanvas()
gPad.SetLeftMargin(0.12)
gPad.SetTopMargin(0.1)

m0_ = BDT_Train[0].GetMaximum()
m1_ = BDT_Train[1].GetMaximum()


max_ = max(m0_, m1_)
BDT_Train[0].DrawNormalized("h")
BDT_Train[0].SetMaximum(max_*1.3)
BDT_Train[0].SetMinimum(0.)
BDT_Train[0].GetYaxis().SetTitle("Normalized to 1")
BDT_Train[0].GetYaxis().CenterTitle()
BDT_Train[0].GetYaxis().SetTitleOffset(1.28)
BDT_Train[0].GetYaxis().SetTitleSize(0.05)
BDT_Train[0].GetXaxis().SetTitle('tW Reconstruction BDT Discriminant')
BDT_Train[0].GetXaxis().SetTitleSize(0.05)

BDT_Train[0].DrawNormalized("h")
BDT_Train[1].DrawNormalized("h,same")

labelcms.Draw()
leg.Draw()

c1.Update()
c1.SaveAs("BDTshape_2.pdf")

leg2 = TLegend(0.13,0.75,0.69,0.89)
leg2.SetFillColor(kWhite)
leg2.SetBorderSize(1)
leg2.SetNColumns(2)
leg2.AddEntry(BDT_Train[0], "Signal Train", "f")
leg2.AddEntry(BDT_Test[0], "Signal Test", "lep")
leg2.AddEntry(BDT_Train[1], "Background Train", "f")
leg2.AddEntry(BDT_Test[1], "Background Test", "lep")

BDT_Test[0].DrawNormalized("e,same")
BDT_Test[1].DrawNormalized("e,same")

leg2.Draw()

c1.Update()
c1.SaveAs("BDTshape_overtraining_2.pdf")

print "Kolmogorov Smirnov"
print "Signal", BDT_Train[0].KolmogorovTest(BDT_Test[0])
print "Background", BDT_Train[1].KolmogorovTest(BDT_Test[1])

print "Signal", BDT_Train[0].Chi2Test(BDT_Test[0])
print "Background", BDT_Train[1].Chi2Test(BDT_Test[1])


print
