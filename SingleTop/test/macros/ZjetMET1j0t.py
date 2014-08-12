#! /usr/bin/env python

from ROOT import *

from ZjetSF import *

import sys

#f = TFile("tmvaFiles/ZjetMETchecks/ZJets.root",'r')
f = "tmvaFiles/ZjetMETchecks/ZJets.root"

channels = ['emu','mumu','ee']

region = '1j0tNoMETmllCut'

histogram = [TH1F("metemu","",60,0,300),
             TH1F("metmumu","",60,0,300),            
             TH1F("metee","",60,0,300)]
histogramMllCut = [TH1F("metemuMll","",60,0,300),
                   TH1F("metmumuMll","",60,0,300),            
                   TH1F("meteeMll","",60,0,300)]
histogramBeforeReweight = [TH1F("metemuNoRew","",60,0,300),
                           TH1F("metmumuNoRew","",60,0,300),            
                           TH1F("meteeNoRew","",60,0,300)]


for mode in range(3):

    c = channels[mode]
    
    tree = TChain(c+'Channel/'+region)
    tree.Add(f)



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

        _met       = event.met
        _mll       = event.mll
        _weightA   = event.weightA
        _weightB   = event.weightB
        _weightC   = event.weightC


        _weight = _weightA+_weightB+_weightC
        
        histogramBeforeReweight[mode].Fill(_met,_weight)

        _weight *= ZjetSF(_met, mode)

        histogram[mode].Fill(_met,_weight)

        if mode == 0:
            histogramMllCut[mode].Fill(_met,_weight)
        elif _mll < 81 or _mll > 101:
            histogramMllCut[mode].Fill(_met,_weight)

histogram[0].SetLineColor(kRed)
histogram[1].SetLineColor(kGreen+2)
histogram[2].SetLineColor(kBlue)

histogramMllCut[0].SetLineColor(kRed)
histogramMllCut[1].SetLineColor(kGreen+2)
histogramMllCut[2].SetLineColor(kBlue)

histogramBeforeReweight[0].SetLineColor(kRed)
histogramBeforeReweight[1].SetLineColor(kGreen+2)
histogramBeforeReweight[2].SetLineColor(kBlue)


histogram[0].SetLineWidth(2)
histogram[1].SetLineWidth(2)
histogram[2].SetLineWidth(2)

histogramMllCut[0].SetLineWidth(2)
histogramMllCut[1].SetLineWidth(2)
histogramMllCut[2].SetLineWidth(2)

histogramBeforeReweight[0].SetLineWidth(2)
histogramBeforeReweight[1].SetLineWidth(2)
histogramBeforeReweight[2].SetLineWidth(2)

