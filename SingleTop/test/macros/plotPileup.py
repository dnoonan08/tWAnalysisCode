#!/usr/bin/env python

from ROOT import *

from setTDRStyle import *

gStyle.SetOptStat(0)
gStyle.SetOptTitle(0)
setTDRStyle()

import ROOT

_runA = TFile("../PileUpHistos/run2012A_Jan22ReReco.root")
_runB = TFile("../PileUpHistos/run2012B_Jan22ReReco.root")
_runC = TFile("../PileUpHistos/run2012C_Jan22ReReco.root")
_runD = TFile("../PileUpHistos/run2012D_Jan22ReReco.root")
_s10 = TFile("../PileUpHistos/pileUpDistrSummer12_53X.root")

runA=_runA.Get("pileup")
runB=_runB.Get("pileup")
runC=_runC.Get("pileup")
runD=_runD.Get("pileup")
s10=_s10.Get("pileup")

runA.SetLineWidth(2)
runB.SetLineWidth(2)
runC.SetLineWidth(2)
runD.SetLineWidth(2)
s10.SetLineWidth(2)

runA.SetLineColor(kRed)
runB.SetLineColor(kOrange-3)
runC.SetLineColor(kGreen+3)
runD.SetLineColor(kBlue)
s10.SetLineColor(kBlack)

runA.SetXTitle("Pileup interactions")
runA.SetYTitle("Normalized to 1")
runA.GetXaxis().SetTitleSize(0.05)
runA.GetYaxis().SetTitleSize(0.05)

s10.SetXTitle("Pileup interactions")
s10.SetYTitle("Normalized to 1")
s10.GetXaxis().SetTitleSize(0.05)
s10.GetYaxis().SetTitleSize(0.05)

c1 = TCanvas("1"," ",600,480)
t1 = TPad("t1", "t1", 0.,0.,1.,1.)
t1.Draw()
t1.cd()
t1.SetLeftMargin(0.14)

# c1.Draw()
# c1 = TCanvas()

gPad.SetLeftMargin(0.12)


runA.DrawNormalized()
runB.DrawNormalized("same")
runC.DrawNormalized("same")
runD.DrawNormalized("same")

leg = TLegend(0.6,0.6,0.93,0.9)

leg.AddEntry(runA,"Runs 2012 A")
leg.AddEntry(runB,"Runs 2012 B")
leg.AddEntry(runC,"Runs 2012 C")
leg.AddEntry(runD,"Runs 2012 D")

leg.SetFillColor(kWhite)
leg.SetBorderSize(1)
leg.SetTextSize(.04)

leg.Draw()

c1.SaveAs("dataPileup.pdf")

c2 = TCanvas("2"," ",600,480)
t2 = TPad("t1", "t1", 0.,0.,1.,1.)
t2.Draw()
t2.cd()
t2.SetLeftMargin(0.14)

s10.DrawNormalized()

leg2 = TLegend(0.6,0.8,0.93,0.9)

leg2.AddEntry(s10,"PU S10 scenario")
leg2.SetTextSize(.04)
leg2.SetFillColor(kWhite)
leg2.SetBorderSize(1)

leg2.Draw()

c2.SaveAs("mcPileup.pdf")
