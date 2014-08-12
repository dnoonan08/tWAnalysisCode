#!/usr/bin/env python                                                                                                                  

#Uses random numbers for btagging scale factors

from ROOT import *

import sys

from EventShapeVariables import *        
from BtagSF import *
from ZjetSF import *
from fileLoadDict_storeUser import fileLists

import random
import os

quickRun = False
if '-short' in sys.argv:
    quickRun = True
    sys.argv.remove('-short')
    
if len(sys.argv) == 2:
    ChanName = sys.argv[1]
    if not ChanName in fileLists:
        print 'Unknown Channel, please check list in fileLoadDict.py'
        sys.exit(0)
    systName = "noSyst"
elif len(sys.argv) == 3:
    ChanName = sys.argv[1]
    if not ChanName in fileLists:
        print 'Unknown Channel, please check list in fileLoadDict.py'
        sys.exit(0)
    systName = sys.argv[2]
    if not systName in allowedSystNames:
        print 'Unknown Systematic:', systName
        sys.exit(0)
else:
    print 'Please specificy a channel as the arguement'
    sys.exit(0)

RunA = True
RunB = True
RunC = True

numJets = 1
numBtags = 1

#fileVersion = 'v8_CSVL'
fileVersion = 'v10'

useLeptonSF = True

#Input actual luminosities for runA, B, C, and D for each channel from data

isData = False

SFsyst = ''

if 'Data' in ChanName:
    SFsyst = 'Data'
    isData = True


TrueLumis = [[876.,4412.,7055.,7360.],
             [876.,4412.,7017.,7369.],
             [876.,4412.,7055.,7369.]]


#The values used from SingleTopPSetsSummer_tW for the luminosities of run A, B, C, and D
UsedLumis = [15000.,15000.,15000.,15000.]

#Lepton Scale Factors
lepSF = [0.916,0.963,0.903]
#lepSF = [0.936,0.962,0.950]
lepSFUnc = [0.011,0.012,0.014]
        

#Branch variables for TMVA tree



temp = ''

if 'SF' in systName:
    temp = systName
    systName = 'noSyst'

if 'PDF' in systName:
    temp = systName
    systName = 'noSyst'

fchain = TChain('TreesDileptontW/'+fileLists[ChanName][0]+'_'+systName)

fchain.SetCacheSize(20*1024*1024)

if 'SF' in temp:
    systName = temp    

if 'PDF' in temp:
    systName = temp    

for file in fileLists[ChanName][1]:
    fchain.Add(file)

Channel = ['emu', 'mumu', 'ee']

evtCount = 0.
percent = 0.0
progSlots = 25.
nEvents = fchain.GetEntries()*1.

print nEvents

#Bins 0-LepSel, 1-LepVeto, 2-mll, 3-MET, 4-jet, 5-bjet, 6-loosejetVeto, 7-ptsys, 8-ht

CutflowHists = [[TH1F("emuCutflow1j1t","",10,-1,9), TH1F("mumuCutflow1j1t","",10,-1,9), TH1F("eeCutflow1j1t","",10,-1,9)],
                [TH1F("emuCutflow2j1t","",10,-1,9), TH1F("mumuCutflow2j1t","",10,-1,9), TH1F("eeCutflow2j1t","",10,-1,9)],
                [TH1F("emuCutflow2j2t","",10,-1,9), TH1F("mumuCutflow2j2t","",10,-1,9), TH1F("eeCutflow2j2t","",10,-1,9)],
                [TH1F("emuCutflow0j","",10,-1,9),   TH1F("mumuCutflow0j","",10,-1,9),   TH1F("eeCutflow0j","",10,-1,9)],
                [TH1F("emuCutflow3j","",10,-1,9),   TH1F("mumuCutflow3j","",10,-1,9),   TH1F("eeCutflow3j","",10,-1,9)]]

#CutflowHists = [TH1F("emuCutflow1j1t","",10,-1,9), TH1F("mumuCutflow1j1t","",10,-1,9), TH1F("eeCutflow1j1t","",10,-1,9)]

for a in CutflowHists:
    for b in a:
        b.Sumw2()

jetPtHists = [[[TH1F("emuJetPt1j_j1","",100,0.,200.), TH1F("mumuJetPt1j_j1","",100,0.,200.), TH1F("eeJetPt1j_j1","",100,0.,200.)],
               [TH1F("emuJetPt1j_j2","",100,0.,200.), TH1F("mumuJetPt1j_j2","",100,0.,200.), TH1F("eeJetPt1j_j2","",100,0.,200.)],
               [TH1F("emuJetPt1j_j3","",100,0.,200.), TH1F("mumuJetPt1j_j3","",100,0.,200.), TH1F("eeJetPt1j_j3","",100,0.,200.)]],
              [[TH1F("emuJetPt2j_j1","",100,0.,200.), TH1F("mumuJetPt2j_j1","",100,0.,200.), TH1F("eeJetPt2j_j1","",100,0.,200.)],
               [TH1F("emuJetPt2j_j2","",100,0.,200.), TH1F("mumuJetPt2j_j2","",100,0.,200.), TH1F("eeJetPt2j_j2","",100,0.,200.)],
               [TH1F("emuJetPt2j_j3","",100,0.,200.), TH1F("mumuJetPt2j_j3","",100,0.,200.), TH1F("eeJetPt2j_j3","",100,0.,200.)]]
              ]



for a in jetPtHists:
    for b in a:
        for c in b:
            c.Sumw2()


leptonPtHists = [[TH1F("emuJetPt_lep1","",100,0.,200.), TH1F("mumuJetPt_lep1","",100,0.,200.), TH1F("eeJetPt_lep1","",100,0.,200.)],
                 [TH1F("emuJetPt_lep2","",100,0.,200.), TH1F("mumuJetPt_lep2","",100,0.,200.), TH1F("eeJetPt_lep2","",100,0.,200.)],
                 ]


for a in leptonPtHists:
    for b in a:
        b.Sumw2()

leptonWParentHists = [TH1F("emuLepWParents","",3,0.,3.), TH1F("mumuLepWParents","",3,0.,3.), TH1F("eeLepWParents","",3,0.,3.)]


for a in leptonWParentHists:
    a.Sumw2()


jetEtaHists = [[[TH1F("emuJetEta1j_j1","",50,-5.,5.), TH1F("mumuJetEta1j_j1","",50,-5.,5.), TH1F("eeJetEta1j_j1","",50,-5.,5.)],
                [TH1F("emuJetEta1j_j2","",50,-5.,5.), TH1F("mumuJetEta1j_j2","",50,-5.,5.), TH1F("eeJetEta1j_j2","",50,-5.,5.)],
                [TH1F("emuJetEta1j_j3","",50,-5.,5.), TH1F("mumuJetEta1j_j3","",50,-5.,5.), TH1F("eeJetEta1j_j3","",50,-5.,5.)]],
               [[TH1F("emuJetEta2j_j1","",50,-5.,5.), TH1F("mumuJetEta2j_j1","",50,-5.,5.), TH1F("eeJetEta2j_j1","",50,-5.,5.)],
                [TH1F("emuJetEta2j_j2","",50,-5.,5.), TH1F("mumuJetEta2j_j2","",50,-5.,5.), TH1F("eeJetEta2j_j2","",50,-5.,5.)],
                [TH1F("emuJetEta2j_j3","",50,-5.,5.), TH1F("mumuJetEta2j_j3","",50,-5.,5.), TH1F("eeJetEta2j_j3","",50,-5.,5.)]],
               ]

for a in jetEtaHists:
    for b in a:
        for c in b:
            c.Sumw2()

jetsPassingIDHists = [TH1F("emuJetId","",40,0.,40.), TH1F("mumuJetId","",40,0.,40.), TH1F("eeJetId","",40,0.,40.)]

for a in jetsPassingIDHists:
    a.Sumw2()

nJetsHists = [TH1F("emuNJets","",6,0.,6.), TH1F("mumuNJets","",6,0.,6.), TH1F("eeNJets","",6,0.,6.)]

for a in jetsPassingIDHists:
    a.Sumw2()

jetPtHists_Aftermll = [[TH1F("emuJetPt_j1","",100,0.,200.), TH1F("mumuJetPt_j1","",100,0.,200.), TH1F("eeJetPt_j1","",100,0.,200.)],
                       [TH1F("emuJetPt_j2","",100,0.,200.), TH1F("mumuJetPt_j2","",100,0.,200.), TH1F("eeJetPt_j2","",100,0.,200.)],
                       [TH1F("emuJetPt_j3","",100,0.,200.), TH1F("mumuJetPt_j3","",100,0.,200.), TH1F("eeJetPt_j3","",100,0.,200.)],
                       ]

for a in jetPtHists_Aftermll:
    for b in a:
        b.Sumw2()


jetEtaHists_Aftermll = [[TH1F("emuJetEta_j1","",50,-5.,5.), TH1F("mumuJetEta_j1","",50,-5.,5.), TH1F("eeJetEta_j1","",50,-5.,5.)],
                        [TH1F("emuJetEta_j2","",50,-5.,5.), TH1F("mumuJetEta_j2","",50,-5.,5.), TH1F("eeJetEta_j2","",50,-5.,5.)],
                        [TH1F("emuJetEta_j3","",50,-5.,5.), TH1F("mumuJetEta_j3","",50,-5.,5.), TH1F("eeJetEta_j3","",50,-5.,5.)],
                        ]

for a in jetEtaHists_Aftermll:
    for b in a:
        b.Sumw2()


jetCSVHists = [[TH1F("emuJetCSV1j","",100,-1.,1.), TH1F("mumuJetCSV1j","",100,-1.,1.), TH1F("eeJetCSV1j","",100,-1.,1.)],
               [TH1F("emuJetCSV2jfirst","",100,-1.,1.), TH1F("mumuJetCSV2jfirst","",100,-1.,1.), TH1F("eeJetCSV2jfirst","",100,-1.,1.)],
               [TH1F("emuJetCSV2jsecond","",100,-1.,1.), TH1F("mumuJetCSV2jsecond","",100,-1.,1.), TH1F("eeJetCSV2jsecond","",100,-1.,1.)]]

for a in jetCSVHists:
    for b in a:
        b.Sumw2()

jetTCHPHists = [[TH1F("emuJetTCHP1j","",100,0.,50.), TH1F("mumuJetTCHP1j","",100,0.,50.), TH1F("eeJetTCHP1j","",100,0.,50.)],
               [TH1F("emuJetTCHP2jfirst","",100,0.,50.), TH1F("mumuJetTCHP2jfirst","",100,0.,50.), TH1F("eeJetTCHP2jfirst","",100,0.,50.)],
               [TH1F("emuJetTCHP2jsecond","",100,0.,50.), TH1F("mumuJetTCHP2jsecond","",100,0.,50.), TH1F("eeJetTCHP2jsecond","",100,0.,50.)]]

for a in jetTCHPHists:
    for b in a:
        b.Sumw2()


for event in fchain:

    evtCount += 1.
    if evtCount/nEvents > percent:
        i = int(percent*progSlots)
        progress = '0%[' + '-' * i + ' ' * (int(progSlots)-i) + ']100%\r'
        sys.stdout.write(progress)
        sys.stdout.flush()
        percent += 1./progSlots

    if quickRun:
        if evtCount/nEvents > .02:
            break

    evtWeightA = event.weightA
    evtWeightB = event.weightB
    evtWeightC = event.weightC
    evtWeightD = event.weightD
    evtPUWeightA = event.PUWeightA
    evtPUWeightB = event.PUWeightB
    evtPUWeightC = event.PUWeightC
    evtPUWeightD = event.PUWeightD


    if isData:
        weight = 1.

    #Get Muon objects
    muonPt = event.muonPt
    muonEta = event.muonEta
    muonPhi = event.muonPhi
    muonE = event.muonE
    muonCharge = event.muonCharge
    muonRelIso = event.muonRelIso
    muonDeltaCorrectedRelIso = event.muonDeltaCorrectedRelIso
    if not isData:
        muonHasTParent = event.muonHasTParent
        muonHasWParent = event.muonHasWParent

    #Get Electron objects
    electronPt = event.electronPt
    electronEta = event.electronEta
    electronPhi = event.electronPhi
    electronE = event.electronE
    electronCharge = event.electronCharge
    electronRelIso = event.electronRelIso
    electronRhoCorrectedRelIso = event.electronRhoCorrectedRelIso
    electronDeltaCorrectedRelIso = event.electronDeltaCorrectedRelIso
    electronPVDz = event.electronPVDz
    electronPVDxy = event.electronPVDxy
    electronDB = event.electronDB
    electronMVATrigV0 = event.electronMVATrigV0
    electronMVANonTrigV0 = event.electronMVANonTrigV0
    electronTrackerExpectedInnerHits = event.electronTrackerExpectedInnerHits
    electronSuperClusterEta = event.electronSuperClusterEta
    electronECALPt = event.electronECALPt
    electronPassConversionVeto = event.electronPassConversionVeto
    if not isData:
        electronHasTParent = event.electronHasTParent
        electronHasWParent = event.electronHasWParent

    goodMuonidx = list()
    goodEleidx = list()
    looseMuonidx = list()
    looseEleidx = list()


    MetPt = event.MetPt
    MetPhi = event.MetPhi


    extraMultipliers = 1

    weightA      = extraMultipliers*evtWeightA*evtPUWeightA*TrueLumis[0][0]/UsedLumis[0]

    weightB      = extraMultipliers*evtWeightB*evtPUWeightB*TrueLumis[0][1]/UsedLumis[1]

    weightC      = extraMultipliers*evtWeightC*evtPUWeightC*TrueLumis[0][2]/UsedLumis[2]

    weightD      = extraMultipliers*evtWeightD*evtPUWeightD*TrueLumis[0][3]/UsedLumis[3]

    weight = weightA + weightB + weightC + weightD

    if isData:
        weight = 1.


    CutflowHists[0][0].Fill(-0.5,weight)
    CutflowHists[1][0].Fill(-0.5,weight)
    CutflowHists[2][0].Fill(-0.5,weight)
    CutflowHists[3][0].Fill(-0.5,weight)
    CutflowHists[4][0].Fill(-0.5,weight)

    CutflowHists[0][1].Fill(-0.5,weight)
    CutflowHists[1][1].Fill(-0.5,weight)
    CutflowHists[2][1].Fill(-0.5,weight)
    CutflowHists[3][1].Fill(-0.5,weight)
    CutflowHists[4][1].Fill(-0.5,weight)

    CutflowHists[0][2].Fill(-0.5,weight)
    CutflowHists[1][2].Fill(-0.5,weight)
    CutflowHists[2][2].Fill(-0.5,weight)
    CutflowHists[3][2].Fill(-0.5,weight)
    CutflowHists[4][2].Fill(-0.5,weight)


    for i in range(len(muonPt)):
        isTightMuon = False
        if muonPt[i] > 20:
            if abs(muonEta[i]) < 2.4:
                if muonDeltaCorrectedRelIso[i] < 0.2:
                    goodMuonidx.append(i)
                    isTightMuon = True
        if not isTightMuon:
            if muonPt[i] > 10:
                if abs(muonEta[i]) < 2.5:
                    if muonDeltaCorrectedRelIso[i] < 0.2:
                        looseMuonidx.append(i)

    for i in range(len(electronPt)):
        isTightElectron = False
        if electronPassConversionVeto[i]:
            if electronPt[i] > 20:
                if abs(electronEta[i]) < 2.5:
                    if abs(electronPVDxy[i]) < 0.04:
                        if electronMVATrigV0[i] >= 0.5 and electronMVATrigV0[i] <= 1.0:
                            if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                                if electronTrackerExpectedInnerHits[i] <= 1:
                                    goodEleidx.append(i)
                                    isTightElectron = True
        if not isTightElectron:
            if electronPt[i] > 15:
                if abs(electronEta[i]) < 2.5:
                    if electronMVATrigV0[i] >= 0.5 and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                        if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                            looseEleidx.append(i)
    nLooseLeptons = len(looseEleidx) + len(looseMuonidx)

    ModeIdx = -1

    lepton0 = TLorentzVector()
    lepton1 = TLorentzVector()

    totalWParents = 0

    if len(goodMuonidx) == 1 and len(goodEleidx) == 1:
        ModeIdx = 0
        i = goodMuonidx[0]
        j = goodEleidx[0]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = muonCharge[i]+electronCharge[j]
        chargeMult = muonCharge[i]*electronCharge[j]
        if not isData:
            if abs(muonHasWParent[i]) == 1:
                totalWParents += 1.
            if abs(electronHasWParent[j]) == 1:
                totalWParents += 1.            
    elif len(goodMuonidx) == 2 and len(goodEleidx) == 0:
        ModeIdx = 1
        i = goodMuonidx[0]
        j = goodMuonidx[1]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(muonPt[j],muonEta[j],muonPhi[j],muonE[j])
        totalCharge = muonCharge[i]+muonCharge[j]
        chargeMult = muonCharge[i]*muonCharge[j]
        if not isData:
            if muonHasWParent[i] == 1:
                totalWParents += 1.
            if muonHasWParent[j] == 1:
                totalWParents += 1.            
    elif len(goodMuonidx) == 0 and len(goodEleidx) == 2:
        ModeIdx = 2
        i = goodEleidx[0]
        j = goodEleidx[1]
        lepton0.SetPtEtaPhiE(electronPt[i],electronEta[i],electronPhi[i],electronE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = electronCharge[i]+electronCharge[j]
        chargeMult = electronCharge[i]*electronCharge[j]
        if not isData:
            if electronHasWParent[i] == 1:
                totalWParents += 1.
            if electronHasWParent[j] == 1:
                totalWParents += 1.            
    else: 
        continue  

    if chargeMult > 0:
        continue

    ZmetSF = 1.
    if 'ZJets' in ChanName:
        ZmetSF = ZjetSF(MetPt, ModeIdx)


    extraMultipliers = lepSF[ModeIdx] * ZmetSF

    weightA      = extraMultipliers*evtWeightA*evtPUWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]

    weightB      = extraMultipliers*evtWeightB*evtPUWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]

    weightC      = extraMultipliers*evtWeightC*evtPUWeightC*TrueLumis[ModeIdx][2]/UsedLumis[2]

    weightD      = extraMultipliers*evtWeightD*evtPUWeightD*TrueLumis[ModeIdx][3]/UsedLumis[3]

    weight = weightA + weightB + weightC + weightD

    if isData:
        weight = 1.


    leptonPtHists[0][ModeIdx].Fill(lepton0.Pt(),weight)
    leptonPtHists[1][ModeIdx].Fill(lepton1.Pt(),weight)

    leptonWParentHists[ModeIdx].Fill(totalWParents,weight)    

    CutflowHists[0][ModeIdx].Fill(0.5,weight)
    CutflowHists[1][ModeIdx].Fill(0.5,weight)
    CutflowHists[2][ModeIdx].Fill(0.5,weight)
    CutflowHists[3][ModeIdx].Fill(0.5,weight)
    CutflowHists[4][ModeIdx].Fill(0.5,weight)

    if totalCharge != 0:
        print "Charge Issue???"
        continue

    if nLooseLeptons != 0:
        continue

    CutflowHists[0][ModeIdx].Fill(1.5,weight)
    CutflowHists[1][ModeIdx].Fill(1.5,weight)
    CutflowHists[2][ModeIdx].Fill(1.5,weight)
    CutflowHists[3][ModeIdx].Fill(1.5,weight)
    CutflowHists[4][ModeIdx].Fill(1.5,weight)


    mll = (lepton0 + lepton1).M()

    if mll < 20:
        continue



    inZpeak = False
    if ModeIdx > 0:
        if mll < 101 and mll > 81:
            continue

    CutflowHists[0][ModeIdx].Fill(2.5,weight)
    CutflowHists[1][ModeIdx].Fill(2.5,weight)
    CutflowHists[2][ModeIdx].Fill(2.5,weight)
    CutflowHists[3][ModeIdx].Fill(2.5,weight)
    CutflowHists[4][ModeIdx].Fill(2.5,weight)


    if ModeIdx>0 and MetPt<50:
        continue

    CutflowHists[0][ModeIdx].Fill(3.5,weight)
    CutflowHists[1][ModeIdx].Fill(3.5,weight)
    CutflowHists[2][ModeIdx].Fill(3.5,weight)
    CutflowHists[3][ModeIdx].Fill(3.5,weight)
    CutflowHists[4][ModeIdx].Fill(3.5,weight)


    MET = TLorentzVector()
    MET.SetPtEtaPhiE(MetPt, 0, MetPhi, MetPt)

    jetPt = event.jetPt
    jetPhi = event.jetPhi
    jetEta = event.jetEta
    jetE = event.jetE
    jetCSV = event.jetCSV
    jetTCHP = event.jetTCHP
    jetNumDaughters = event.jetNumDaughters
    jetCHEmEn = event.jetCHEmEn
    jetCHHadEn = event.jetCHHadEn
    jetCHMult = event.jetCHMult
    jetNeuEmEn = event.jetNeuEmEn
    jetNeuHadEn = event.jetNeuHadEn


    goodJetIdx = list()
    btaggedTightJetIdx = list()
    looseJet20Idx = list()
    btaggedLooseJet20Idx = list()

    jetsPassingID = 0
    jetIDCount = 0
    jetIDCount_2 = 0

    for i in range(len(jetPt)):
        isTightJet = False
        jetID = False        
        btagSF_ = BtagSF(jetPt[i],SFsyst)
        if btagSF_ > 1:
            print btagSF_, jetPt[i]
        if jetNumDaughters[i] > 1:
            if jetNeuHadEn[i] < 0.99:
                if jetNeuEmEn[i] < 0.99:
                    if abs(jetEta[i]) > 2.4:
                        jetID = True
                    else:
                        if jetCHEmEn[i] < 0.99:
                            if jetCHHadEn[i] > 0:
                                if jetCHMult[i] > 0:
                                    jetID = True
        if jetID:
            jetsPassingID += 1
            if jetIDCount_2 == 3: jetIDCount_2 = 2 
            jetPtHists_Aftermll[jetIDCount_2][ModeIdx].Fill(jetPt[i],weight)
            jetEtaHists_Aftermll[jetIDCount_2][ModeIdx].Fill(jetEta[i],weight)
            jetIDCount_2 += 1
        if jetPt[i] > 30:
            if abs(jetEta[i]) < 2.4:
                if jetID:
                    tJet = TLorentzVector()
                    tJet.SetPtEtaPhiE(jetPt[i],jetEta[i],jetPhi[i],jetE[i])
                    if min(lepton0.DeltaR(tJet),lepton1.DeltaR(tJet)) > 0.3:
                        goodJetIdx.append(i)
                        isTightJet = True
                        #                        if jetCSV[i] > 0.244:
                        if jetCSV[i] > 0.679:
                            if random.random() < btagSF_ or isData:
                                btaggedTightJetIdx.append(i)

        if not isTightJet:
            if jetID:
                if jetPt[i] > 20:
                    if abs(jetEta[i]) < 2.4:
                        looseJet20Idx.append(i)
                        #                        if jetCSV[i] > 0.244:
                        if jetCSV[i] > 0.679:
                            if random.random() < btagSF_ or isData:
                                btaggedLooseJet20Idx.append(i)

        jetsPassingIDHists[ModeIdx].Fill(jetsPassingID,weight)

    nJetsHists[ModeIdx].Fill(len(goodJetIdx),weight)

    if len(goodJetIdx) == 1:
        CutflowHists[0][ModeIdx].Fill(4.5,weight)
        jetCSVHists[0][ModeIdx].Fill(jetCSV[ goodJetIdx[0] ],weight)
        jetTCHPHists[0][ModeIdx].Fill(jetTCHP[ goodJetIdx[0] ],weight)        
    elif len(goodJetIdx) == 2:
        CutflowHists[1][ModeIdx].Fill(4.5,weight)
        CutflowHists[2][ModeIdx].Fill(4.5,weight)
        jetCSVHists[1][ModeIdx].Fill(jetCSV[ goodJetIdx[0] ],weight)
        jetCSVHists[2][ModeIdx].Fill(jetCSV[ goodJetIdx[1] ],weight)
        jetTCHPHists[1][ModeIdx].Fill(jetTCHP[ goodJetIdx[0] ],weight)
        jetTCHPHists[2][ModeIdx].Fill(jetTCHP[ goodJetIdx[1] ],weight)
    elif len(goodJetIdx) == 0:
        CutflowHists[3][ModeIdx].Fill(4.5,weight)
    elif len(goodJetIdx) == 3:
        CutflowHists[4][ModeIdx].Fill(4.5,weight)
    else:
        continue

    
    nJets = len(goodJetIdx)-1
    jetIDCount = 0
    if nJets == 0 or nJets == 1:
        for i in range(len(jetPt)):
            isTightJet = False
            jetID = False        
            if jetNumDaughters[i] > 1:
                if jetNeuHadEn[i] < 0.99:
                    if jetNeuEmEn[i] < 0.99:
                        if abs(jetEta[i]) > 2.4:
                            jetID = True
                        else:
                            if jetCHEmEn[i] < 0.99:
                                if jetCHHadEn[i] > 0:
                                    if jetCHMult[i] > 0:
                                        jetID = True
            if jetID:
                if jetIDCount == 3: jetIDCount = 2
                jetPtHists[nJets][jetIDCount][ModeIdx].Fill(jetPt[i],weight)
                jetEtaHists[nJets][jetIDCount][ModeIdx].Fill(jetEta[i],weight)
                jetIDCount += 1
    


    region = -1
    if len(btaggedTightJetIdx) == 1:
        if len(goodJetIdx) == 1:
            CutflowHists[0][ModeIdx].Fill(5.5,weight)
            region = 0
            print totalWParents
        elif len(goodJetIdx) == 2:
            CutflowHists[1][ModeIdx].Fill(5.5,weight)
            region = 1
        else:
            continue
    elif len(btaggedTightJetIdx) == 2:
        if len(goodJetIdx) == 2:
            CutflowHists[2][ModeIdx].Fill(5.5,weight)
            region = 2
        else:
            continue
    else:
        continue

    if len(btaggedLooseJet20Idx) > 0.:
        continue

    CutflowHists[region][ModeIdx].Fill(6.5,weight)

    jetIdx = goodJetIdx[0]

    jet = TLorentzVector()
    jet.SetPtEtaPhiE(jetPt[jetIdx],jetEta[jetIdx], jetPhi[jetIdx], jetE[jetIdx])

    system = lepton0 + lepton1 + MET + jet 
    Ht = lepton0.Pt() + lepton1.Pt() + MET.Pt() + jet.Pt()

    if system.Pt() > 30:
        continue

    CutflowHists[region][ModeIdx].Fill(7.5,weight)

    if ModeIdx==0 and Ht < 160:
        continue

    CutflowHists[region][ModeIdx].Fill(8.5,weight)

    


if not os.path.exists('cutFlows/'):
    command = 'mkdir cutFlows/'
    os.system(command)
if not os.path.exists('cutFlows/'+fileVersion):
    command = 'mkdir cutFlows/'+fileVersion
    os.system(command)

outFileName = 'cutFlows/'+fileVersion+'/'+fileLists[ChanName][2]

print
print outFileName
outputFile = TFile(outFileName,"RECREATE")

DirCutflows = outputFile.mkdir("Cutflows","Cutflows")
DirCutflows.cd()
for a in CutflowHists:
    for b in a:
        b.Write()

DirJetPt = outputFile.mkdir("JetPt","JetPt")
DirJetPt.cd()
for a in jetPtHists:
    for b in a:
        for c in b:
            c.Write()

for a in jetPtHists_Aftermll:
    for b in a:
        b.Write()

DirJetEta = outputFile.mkdir("JetEta","JetEta")
DirJetEta.cd()
for a in jetEtaHists:
    for b in a:
        for c in b:
            c.Write()
for a in jetEtaHists_Aftermll:
    for b in a:
        b.Write()

DirJetCSV = outputFile.mkdir("JetCSV","JetCSV")
DirJetCSV.cd()
for a in jetCSVHists:
    for b in a:
        b.Write()

DirJetTCHP = outputFile.mkdir("JetTCHP","JetTCHP")
DirJetTCHP.cd()
for a in jetTCHPHists:
    for b in a:
        b.Write()

DirJetCount = outputFile.mkdir("JetCount","JetCount")
DirJetCount.cd()
for a in jetsPassingIDHists:
    a.Write()
for a in nJetsHists:
    a.Write()

DirLepInfo = outputFile.mkdir("LepInfo","LepInfo")
DirLepInfo.cd()
for a in leptonPtHists:
    for b in a:
        b.Write()
for a in leptonWParentHists:
    a.Write()
