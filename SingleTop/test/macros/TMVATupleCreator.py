#!/usr/bin/env python

#Uses random numbers for btagging scale factors

from ROOT import *

import sys

from EventShapeVariables import *
from BtagSF import *
from fileLoadDict_storeUser import fileLists

import random
import os

allowedSystNames = ['JESUp','JESDown','UnclusteredMETUp','UnclusteredMETDown','JERUp','JERDown','BtagSFUp','BtagSFDown','LepSFUp','LepSFDown','PDFUp','PDFDown','LESUp','LESDown','PUUp','PUDown']

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

fileVersion = 'v10_MET50'
#fileVersion = 'TestDir'

useLeptonSF = True

#Input actual luminosities for runA, B, Crereco, and Cprompt for each channel from data

isData = False

SFsyst = ''
if systName == 'BtagSFUp':
    SFsyst = 'Up'
if systName == 'BtagSFDown':
    SFsyst = 'Down'
if 'Data' in ChanName:
    SFsyst = 'Data'
    isData = True


TrueLumis = [[808.472+82.136,4398.,495.003,6397.],
             [808.472+82.136,4411.,495.003,6397.],
             [808.472+82.136,4446.,485.574,6397.]]


#The values used from SingleTopPSetsSummer_tW for the luminosities of run A, B, Crereco, and Cprompt
UsedLumis = [15000.,15000.,15000.,15000.]

#Lepton Scale Factors
#lepSF = [0.936,0.962,0.950]
lepSFUnc = [0.011,0.012,0.014]

lepSF = [0.916,0.963,0.903]
        
### a C/C++ structure is required, to allow memory based access
gROOT.ProcessLine(
    "struct eventInfo_t {\
    Int_t           RunNum;\
    Int_t           LumiNum;\
    Int_t           EventNum;\
    Double_t        weightA;\
    Double_t        weightNoPUA;\
    Double_t        weightB;\
    Double_t        weightNoPUB;\
    Double_t        weightC;\
    Double_t        weightNoPUC;\
    Double_t        weightBtagSF;\
    Double_t        ptjet;\
    Double_t        ptlep0;\
    Double_t        ptlep1;\
    Double_t        jetCSV;\
    Double_t        ht;\
    Double_t        htTot;\
    Double_t        htNoMet;\
    Double_t        msys;\
    Double_t        mjll;\
    Double_t        mjl0;\
    Double_t        mjl1;\
    Double_t        mjlmax;\
    Double_t        mjlmin;\
    Double_t        mjl0met;\
    Double_t        mjl1met;\
    Double_t        mjlmetmax;\
    Double_t        mjlmetmin;\
    Double_t        ptsys;\
    Double_t        ptsysTot;\
    Double_t        ptjll;\
    Double_t        ptjl0;\
    Double_t        ptjl1;\
    Double_t        ptjl0met;\
    Double_t        ptjl1met;\
    Double_t        ptjlmetmax;\
    Double_t        ptjlmetmin;\
    Double_t        ptjlmax;\
    Double_t        ptjlmin;\
    Double_t        ptleps;\
    Double_t        htleps;\
    Double_t        ptsys_ht;\
    Double_t        ptjet_ht;\
    Double_t        ptlep0_ht;\
    Double_t        ptlep1_ht;\
    Double_t        ptleps_ht;\
    Double_t        htleps_ht;\
    Int_t           NlooseJet15Central;\
    Int_t           NlooseJet15Forward;\
    Int_t           NlooseJet20Central;\
    Int_t           NlooseJet20Forward;\
    Int_t           NlooseJet25Central;\
    Int_t           NlooseJet25Forward;\
    Int_t           NtightJetForward;\
    Int_t           NlooseJet15;\
    Int_t           NlooseJet20;\
    Int_t           NlooseJet25;\
    Int_t           NbtaggedlooseJet15;\
    Int_t           NbtaggedlooseJet20;\
    Int_t           NbtaggedlooseJet25;\
    Double_t        unweightedEta_Avg;\
    Double_t        unweightedEta_Vecjll;\
    Double_t        unweightedEta_Vecsys;\
    Double_t        unweightedPhi_Avg;\
    Double_t        unweightedPhi_Vecjll;\
    Double_t        unweightedPhi_Vecsys;\
    Double_t        avgEta;\
    Double_t        sysEta;\
    Double_t        jllEta;\
    Double_t        dRleps;\
    Double_t        dRjlmin;\
    Double_t        dRjlmax;\
    Double_t        dEtaleps;\
    Double_t        dEtajlmin;\
    Double_t        dEtajlmax;\
    Double_t        dPhileps;\
    Double_t        dPhijlmin;\
    Double_t        dPhijlmax;\
    Double_t        dPhimetlmin;\
    Double_t        dPhimetlmax;\
    Double_t        dPhijmet;\
    Double_t        met;\
    Double_t        etajet;\
    Double_t        etalep0;\
    Double_t        etalep1;\
    Double_t        phijet;\
    Double_t        philep0;\
    Double_t        philep1;\
    Double_t        phimet;\
    Double_t        sumeta2;\
    Double_t        loosejetPt;\
    Double_t        loosejetCSV;\
    Double_t        centralityJLL;\
    Double_t        centralityJLLM;\
    Double_t        centralityJLLWithLoose;\
    Double_t        centralityJLLMWithLoose;\
    Double_t        sphericityJLL;\
    Double_t        sphericityJLLM;\
    Double_t        sphericityJLLWithLoose;\
    Double_t        sphericityJLLMWithLoose;\
    Double_t        aplanarityJLL;\
    Double_t        aplanarityJLLM;\
    Double_t        aplanarityJLLWithLoose;\
    Double_t        aplanarityJLLMWithLoose;\
    };" );


Vars = [['I', 'RunNum'],
        ['I', 'LumiNum'],
        ['I', 'EventNum'],
        ['D', 'weightA'],
        ['D', 'weightNoPUA'],
        ['D', 'weightB'],
        ['D', 'weightNoPUB'],
        ['D', 'weightC'],
        ['D', 'weightNoPUC'],
        ['D', 'weightBtagSF'],
        ['D', 'ptjet'],
        ['D', 'ptlep0'],
        ['D', 'ptlep1'],
        ['D', 'jetCSV'],
        ['D', 'ht'],
        ['D', 'htTot'],
        ['D', 'htNoMet'],
        ['D', 'msys'],
        ['D', 'mjll'],
        ['D', 'mjl0'],
        ['D', 'mjl1'],
        ['D', 'mjl0met'],
        ['D', 'mjl1met'],
        ['D', 'mjlmetmax'],
        ['D', 'mjlmetmin'],
        ['D', 'mjlmax'],
        ['D', 'mjlmin'],
        ['D', 'ptsys'],
        ['D', 'ptsysTot'],
        ['D', 'ptjll'],
        ['D', 'ptjl0'],
        ['D', 'ptjl1'],
        ['D', 'ptjl0met'],
        ['D', 'ptjl1met'],
        ['D', 'ptjlmetmax'],
        ['D', 'ptjlmetmin'],
        ['D', 'ptjlmax'],
        ['D', 'ptjlmin'],
        ['D', 'ptleps'],
        ['D', 'htleps'],
        ['D', 'ptsys_ht'],
        ['D', 'ptjet_ht'],
        ['D', 'ptlep0_ht'],
        ['D', 'ptlep1_ht'],
        ['D', 'ptleps_ht'],
        ['D', 'htleps_ht'],
        ['I', 'NlooseJet15Central'],
        ['I', 'NlooseJet15Forward'],
        ['I', 'NlooseJet20Central'],
        ['I', 'NlooseJet20Forward'],
        ['I', 'NlooseJet25Central'],
        ['I', 'NlooseJet25Forward'],
        ['I', 'NtightJetForward'],
        ['I', 'NlooseJet15'],
        ['I', 'NlooseJet20'],
        ['I', 'NlooseJet25'],
        ['I', 'NbtaggedlooseJet15'],
        ['I', 'NbtaggedlooseJet20'],
        ['I', 'NbtaggedlooseJet25'],
        ['D', 'unweightedEta_Avg'],
        ['D', 'unweightedEta_Vecjll'],
        ['D', 'unweightedEta_Vecsys'],
        ['D', 'unweightedPhi_Avg'],
        ['D', 'unweightedPhi_Vecjll'],
        ['D', 'unweightedPhi_Vecsys'],
        ['D', 'avgEta'],
        ['D', 'sysEta'],
        ['D', 'jllEta'],
        ['D', 'dRleps'],
        ['D', 'dRjlmin'],
        ['D', 'dRjlmax'],
        ['D', 'dEtaleps'],
        ['D', 'dEtajlmin'],
        ['D', 'dEtajlmax'],
        ['D', 'dPhileps'],
        ['D', 'dPhijlmin'],
        ['D', 'dPhijlmax'],
        ['D', 'dPhimetlmin'],
        ['D', 'dPhimetlmax'],
        ['D', 'dPhijmet'],
        ['D', 'met'],
        ['D', 'etajet'],
        ['D', 'etalep0'],
        ['D', 'etalep1'],
        ['D', 'phijet'],
        ['D', 'philep0'],
        ['D', 'philep1'],
        ['D', 'phimet'],
        ['D', 'sumeta2'],
        ['D', 'loosejetPt'],
        ['D', 'loosejetCSV'],
        ['D', 'centralityJLL'],
        ['D', 'centralityJLLM'],
        ['D', 'centralityJLLWithLoose'],
        ['D', 'centralityJLLMWithLoose'],
        ['D', 'sphericityJLL'],
        ['D', 'sphericityJLLM'],
        ['D', 'sphericityJLLWithLoose'],
        ['D', 'sphericityJLLMWithLoose'],
        ['D', 'aplanarityJLL'],
        ['D', 'aplanarityJLLM'],
        ['D', 'aplanarityJLLWithLoose'],
        ['D', 'aplanarityJLLMWithLoose']
        ]


#Trees for TMVA input (signal/control regions)

# treeList = {'tree1jNotagging':[TTree('1jNoTagging','1jNoTagging'),TTree('1jNoTagging','1jNoTagging'),TTree('1jNoTagging','1jNoTagging')],
#             'tree1j0t':[TTree('1j0t','1j0t'),TTree('1j0t','1j0t'),TTree('1j0t','1j0t')],
#             'tree1j1t':[TTree('1j1t','1j1t'),TTree('1j1t','1j1t'),TTree('1j1t','1j1t')],
#             'tree2jNotagging':[TTree('2jNoTagging','2jNoTagging'),TTree('2jNoTagging','2jNoTagging'),TTree('2jNoTagging','2jNoTagging')],
#             'tree2j0t':[TTree('2j0t','2j0t'),TTree('2j0t','2j0t'),TTree('2j0t','2j0t')],
#             'tree2j1t':[TTree('2j1t','2j1t'),TTree('2j1t','2j1t'),TTree('2j1t','2j1t')],
#             'tree2j2t':[TTree('2j2t','2j2t'),TTree('2j2t','2j2t'),TTree('2j2t','2j2t')],
#             'tree3plusjNotagging':[TTree('3plusjNoTagging','3plusjNoTagging'),TTree('3plusjNoTagging','3plusjNoTagging'),TTree('3plusjNoTagging','3plusjNoTagging')],
#             'tree1j1tZpeak':[TTree('1j1tZpeak','1j1tZpeak'),TTree('1j1tZpeak','1j1tZpeak'),TTree('1j1tZpeak','1j1tZpeak')],
#             'treeZpeakLepSel':[TTree('ZpeakLepSel','ZpeakLepSel'),TTree('ZpeakLepSel','ZpeakLepSel'),TTree('ZpeakLepSel','ZpeakLepSel')],
#             }

treeList = {#'tree1jNotagging':[TTree('1jNoTagging','1jNoTagging'),TTree('1jNoTagging','1jNoTagging'),TTree('1jNoTagging','1jNoTagging')],
            #'tree1j0t':[TTree('1j0t','1j0t'),TTree('1j0t','1j0t'),TTree('1j0t','1j0t')],
            'tree1j1t':[TTree('1j1t','1j1t'),TTree('1j1t','1j1t'),TTree('1j1t','1j1t')],
            #'tree2jNotagging':[TTree('2jNoTagging','2jNoTagging'),TTree('2jNoTagging','2jNoTagging'),TTree('2jNoTagging','2jNoTagging')],
            #'tree2j0t':[TTree('2j0t','2j0t'),TTree('2j0t','2j0t'),TTree('2j0t','2j0t')],
            'tree2j1t':[TTree('2j1t','2j1t'),TTree('2j1t','2j1t'),TTree('2j1t','2j1t')],
            'tree2j2t':[TTree('2j2t','2j2t'),TTree('2j2t','2j2t'),TTree('2j2t','2j2t')],
            #'tree3plusjNotagging':[TTree('3plusjNoTagging','3plusjNoTagging'),TTree('3plusjNoTagging','3plusjNoTagging'),TTree('3plusjNoTagging','3plusjNoTagging')],
            #'tree1j1tZpeak':[TTree('1j1tZpeak','1j1tZpeak'),TTree('1j1tZpeak','1j1tZpeak'),TTree('1j1tZpeak','1j1tZpeak')],
            'treeZpeakLepSel':[TTree('ZpeakLepSel','ZpeakLepSel'),TTree('ZpeakLepSel','ZpeakLepSel'),TTree('ZpeakLepSel','ZpeakLepSel')],
            }

#Branch variables for TMVA tree

eventInfo = eventInfo_t()

for i in treeList:
    trees = treeList[i]
    for tree in trees:
        for var in Vars:
            tree.Branch(var[1],AddressOf(eventInfo,var[1]),var[1]+'/'+var[0])

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

for event in fchain:

    evtCount += 1.
    if evtCount/nEvents > percent:
        i = int(percent*progSlots)
        progress = '0%[' + '-' * i + ' ' * (int(progSlots)-i) + ']100%\r'
        sys.stdout.write(progress)
        sys.stdout.flush()
        percent += 1./progSlots

#     if evtCount > 3000:
#         break

    runNum = event.runNum
    lumiNum = event.lumiNum
    eventNum = event.eventNum
    evtWeightA = event.weightA
    evtWeightB = event.weightB
    evtWeightCrereco = event.weightCrereco
    evtWeightCprompt = event.weightCprompt
    evtPUWeightA = event.PUWeightA
    evtPUWeightB = event.PUWeightB
    evtPUWeightCrereco = event.PUWeightCrereco
    evtPUWeightCprompt = event.PUWeightCprompt
    PDFweights = event.PDF_weights


    #Get Muon objects
    muonPt = event.muonPt
    muonEta = event.muonEta
    muonPhi = event.muonPhi
    muonE = event.muonE
    muonCharge = event.muonCharge
    muonRelIso = event.muonRelIso
    muonDeltaCorrectedRelIso = event.muonDeltaCorrectedRelIso

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


    goodMuonidx = list()
    goodEleidx = list()
    looseMuonidx = list()
    looseEleidx = list()

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
                        if electronMVATrigV0[i] >= 0.0 and electronMVATrigV0[i] <= 1.0:
                            if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
#                            if electronDeltaCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                                if electronTrackerExpectedInnerHits[i] <= 1:
                                    goodEleidx.append(i)
                                    isTightElectron = True
        if not isTightElectron:
            if electronPt[i] > 15:
                if abs(electronEta[i]) < 2.5:
                    if electronMVATrigV0[i] >= 0.0 and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                        if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
#                        if electronDeltaCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                            looseEleidx.append(i)
    nLooseLeptons = len(looseEleidx) + len(looseMuonidx)

    ModeIdx = -1

    lepton0 = TLorentzVector()
    lepton1 = TLorentzVector()

    if len(goodMuonidx) == 1 and len(goodEleidx) == 1:
        ModeIdx = 0
        i = goodMuonidx[0]
        j = goodEleidx[0]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = muonCharge[i]+electronCharge[j]
        chargeMult = muonCharge[i]*electronCharge[j]
    elif len(goodMuonidx) == 2 and len(goodEleidx) == 0:
        ModeIdx = 1
        i = goodMuonidx[0]
        j = goodMuonidx[1]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(muonPt[j],muonEta[j],muonPhi[j],muonE[j])
        totalCharge = muonCharge[i]+muonCharge[j]
        chargeMult = muonCharge[i]*muonCharge[j]
    elif len(goodMuonidx) == 0 and len(goodEleidx) == 2:
        ModeIdx = 2
        i = goodEleidx[0]
        j = goodEleidx[1]
        lepton0.SetPtEtaPhiE(electronPt[i],electronEta[i],electronPhi[i],electronE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        totalCharge = electronCharge[i]+electronCharge[j]
        chargeMult = electronCharge[i]*electronCharge[j]
    else: 
        continue  

    if chargeMult > 0:
        continue

    if totalCharge != 0:
        print "Charge Issue???"
        continue

    if nLooseLeptons != 0:
        continue


    mll = (lepton0 + lepton1).M()

    if mll < 20:
        continue

    inZpeak = False

#     if mll < 101 and mll > 81:
#         inZpeak = True

    if ModeIdx > 0:
        if mll < 101 and mll > 81:
            inZpeak = True

    MetPt = event.MetPt
    MetPhi = event.MetPhi

    passMET = False
#     if MetPt>50:
#         passMET = True
    if ModeIdx==0 or MetPt>50:
        passMET = True


    MET = TLorentzVector()
    MET.SetPtEtaPhiE(MetPt, 0, MetPhi, MetPt)

    jetPt = event.jetPt
    jetPhi = event.jetPhi
    jetEta = event.jetEta
    jetE = event.jetE
    jetCSV = event.jetCSV
    jetNumDaughters = event.jetNumDaughters
    jetCHEmEn = event.jetCHEmEn
    jetCHHadEn = event.jetCHHadEn
    jetCHMult = event.jetCHMult
    jetNeuEmEn = event.jetNeuEmEn
    jetNeuHadEn = event.jetNeuHadEn


    goodJetIdx = list()
    btaggedTightJetIdx = list()
    looseJetIdx = list()
    tightJetForwardIdx = list()
    looseJet25CentralIdx = list()
    looseJet25ForwardIdx = list()
    looseJet20CentralIdx = list()
    looseJet20ForwardIdx = list()
    looseJet15CentralIdx = list()
    looseJet15ForwardIdx = list()
    looseJet15Idx = list()
    looseJet20Idx = list()
    looseJet25Idx = list()
    btaggedLooseJet15Idx = list()
    btaggedLooseJet20Idx = list()
    btaggedLooseJet25Idx = list()

    for i in range(len(jetPt)):
        isTightJet = False
        jetID = False        
        btagSF_ = BtagSF(jetPt[i],SFsyst)
#        btagSF_ = 1.
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
        if jetPt[i] > 30:
            if abs(jetEta[i]) < 2.4:
                if jetID:
                    tJet = TLorentzVector()
                    tJet.SetPtEtaPhiE(jetPt[i],jetEta[i],jetPhi[i],jetE[i])
                    if min(lepton0.DeltaR(tJet),lepton1.DeltaR(tJet)) > 0.3 or ModeIdx == 1:
                        goodJetIdx.append(i)
                        isTightJet = True
                        if jetCSV[i] > 0.679:
                            if random.random() < btagSF_ or isData:
                                btaggedTightJetIdx.append(i)
#                         elif btagSF_>1 and random.random() < (btagSF_-1.) and not isData:
#                             btaggedTightJetIdx.append(i)

        if not isTightJet:
            if jetID:
                if jetPt[i] > 15:
                    looseJet15Idx.append(i)
                    if abs(jetEta[i]) < 2.4:
                        looseJet15CentralIdx.append(i)
                    else:
                        looseJet15ForwardIdx.append(i)
                    if jetCSV[i] > 0.679:
                        if random.random() < btagSF_ or isData:
                            btaggedLooseJet15Idx.append(i)
#                     elif btagSF_>1 and random.random() < (btagSF_-1.) and not isData:
#                         btaggedLooseJet15Idx.append(i)
                if jetPt[i] > 20:
                    looseJet20Idx.append(i)
                    if abs(jetEta[i]) < 2.4:
                        looseJet20CentralIdx.append(i)
                    else:
                        looseJet20ForwardIdx.append(i)
                    if jetCSV[i] > 0.679:
                        if random.random() < btagSF_ or isData:
                            btaggedLooseJet20Idx.append(i)
#                     elif btagSF_>1 and random.random() < (btagSF_-1.) and not isData:
#                         btaggedLooseJet20Idx.append(i)
                if jetPt[i] > 25:
                    looseJet25Idx.append(i)
                    if abs(jetEta[i]) < 2.4:
                        looseJet25CentralIdx.append(i)
                    else:
                        looseJet25ForwardIdx.append(i)
                    if jetCSV[i] > 0.679:
                        if random.random() < btagSF_ or isData:
                            btaggedLooseJet25Idx.append(i)
#                     elif btagSF_>1 and random.random() < (btagSF_-1.) and not isData:
#                         btaggedLooseJet25Idx.append(i)
                if jetPt[i] > 30:
                    if abs(jetEta[i]) > 2.4:
                        tightJetForwardIdx.append(i)


    if len(goodJetIdx) < 1:
        continue

    jetIdx = goodJetIdx[0]

    jet = TLorentzVector()
    jet.SetPtEtaPhiE(jetPt[jetIdx],jetEta[jetIdx], jetPhi[jetIdx], jetE[jetIdx])

    system = lepton0 + lepton1 + MET + jet 
    systemTot = lepton0 + lepton1 + MET + jet
    Ht = lepton0.Pt() + lepton1.Pt() + MET.Pt() + jet.Pt()
    HtTot = lepton0.Pt() + lepton1.Pt() + MET.Pt() + jet.Pt()
    HtNoMet = lepton0.Pt() + lepton1.Pt() + jet.Pt()
    
    jll = jet + lepton0 + lepton1
    jl0 = jet + lepton0
    jl1 = jet + lepton1
    jl0met = jet + lepton0 + MET
    jl1met = jet + lepton1 + MET
    leptons = lepton0 + lepton1

    H = jet.E() + lepton0.E() + lepton1.E() + MET.E()
    HNoMet = jet.E() + lepton0.E() + lepton1.E()

    for i in range(1,len(goodJetIdx)):
        tempidx = goodJetIdx[i]
        tempjet = TLorentzVector()
        tempjet.SetPtEtaPhiE(jetPt[tempidx],jetEta[tempidx], jetPhi[tempidx], jetE[tempidx])

        system = system + tempjet
        systemTot = systemTot + tempjet
        Ht = Ht + tempjet.Pt()
        HtTot = HtTot + tempjet.Pt()
        HtNoMet = HtNoMet + tempjet.Pt()

    listJLL = list()

    particles = list()
    particles.append(lepton0)
    particles.append(lepton1)
    particles.append(jet)
    particles.append(MET)

    listJLL.append(lepton0)
    listJLL.append(lepton1)
    listJLL.append(jet)

    listJLLM = list(listJLL)
    listJLLM.append(MET)

    listJLLWithLoose = list(listJLL)
    listJLLMWithLoose = list(listJLLM)

    for i in looseJet20Idx:
        temp = TLorentzVector()
        temp.SetPtEtaPhiE(jetPt[i],jetEta[i], jetPhi[i], jetE[i])
        listJLLWithLoose.append(temp)
        listJLLMWithLoose.append(temp)
        systemTot = systemTot + temp
        HtTot = HtTot + temp.Pt()



    centrality_jll = Centrality(listJLL)
    centrality_jllm = Centrality(listJLLM)
    centrality_jllWithLoose = Centrality(listJLLWithLoose)
    centrality_jllmWithLoose = Centrality(listJLLMWithLoose)

    sphericity_jll = Sphericity(listJLL)
    sphericity_jllm = Sphericity(listJLLM)
    sphericity_jllWithLoose = Sphericity(listJLLWithLoose)
    sphericity_jllmWithLoose = Sphericity(listJLLMWithLoose)

    aplanarity_jll = Aplanarity(listJLL)
    aplanarity_jllm = Aplanarity(listJLLM)
    aplanarity_jllWithLoose = Aplanarity(listJLLWithLoose)
    aplanarity_jllmWithLoose = Aplanarity(listJLLMWithLoose)

    AvgEta = (lepton0.Eta() + lepton1.Eta() + jet.Eta())/3.
    AvgPhi= (lepton0.Phi() + lepton1.Phi() + jet.Phi())/3.

    AvgVec = TLorentzVector()
    AvgVec.SetPtEtaPhiM(10,AvgEta, AvgPhi, 0)

    unweightedEta_Avg = pow(lepton0.Eta()-AvgEta,2) + pow(lepton1.Eta()-AvgEta,2) + pow(jet.Eta()-AvgEta,2)
    unweightedEta_Vecjll = pow(lepton0.Eta()-jll.Eta(),2) + pow(lepton1.Eta()-jll.Eta(),2) + pow(jet.Eta()-jll.Eta(),2)
    unweightedEta_Vecsys = pow(lepton0.Eta()-system.Eta(),2) + pow(lepton1.Eta()-system.Eta(),2) + pow(jet.Eta()-system.Eta(),2)

    unweightedPhi_Avg = pow(lepton0.DeltaPhi(AvgVec),2) + pow(lepton1.DeltaPhi(AvgVec),2) + pow(jet.DeltaPhi(AvgVec),2)
    unweightedPhi_Vecjll = pow(lepton0.DeltaPhi(jll),2) + pow(lepton1.DeltaPhi(jll),2) + pow(jet.DeltaPhi(jll),2)
    unweightedPhi_Vecsys = pow(lepton0.DeltaPhi(system),2) + pow(lepton1.DeltaPhi(system),2) + pow(jet.DeltaPhi(system),2)

    sumEta2 = pow(lepton0.Eta(),2) + pow(lepton1.Eta(),2) + pow(jet.Eta(),2)

    ptLooseJet = 0.
    csvLooseJet = -0.05
    if len(looseJet20Idx) > 0:
        ptLooseJet = jetPt[looseJet20Idx[0]]
        csvLooseJet = jetCSV[looseJet20Idx[0]]

    eventInfo.weightA = 0.
    eventInfo.weightNoPUA = 0.
    eventInfo.weightB = 0.
    eventInfo.weightNoPUB = 0.
    eventInfo.weightC = 0.
    eventInfo.weightNoPUC = 0.

    #Apply the lepton scale factors to the weights
    leptonSF = lepSF[ModeIdx]
    if isData:
        leptonSF = 1.
    
    if systName == 'LepSFUp':
        leptonSF = lepSF[ModeIdx] + lepSFUnc[ModeIdx]
    if systName == 'LepSFDown':
            leptonSF = lepSF[ModeIdx] - lepSFUnc[ModeIdx]

#     if useLeptonSF and not isData:
#         if systName == 'LepSFUp':
#             leptonSF = lepSF[ModeIdx] + lepSFUnc[ModeIdx]
#         elif systName == 'LepSFDown':
#             leptonSF = lepSF[ModeIdx] - lepSFUnc[ModeIdx]
            

    pdfWeightMult = 1.
    if systName == 'PDFUp':
        temp = 0.
        for i in PDFweights:
            if i > temp:
                temp = i
        pdfWeightMult = temp

    if systName == 'PDFDown':
        temp = 99.
        for i in PDFweights:
            if i < temp:
                temp = i
        pdfWeightMult = temp



    extraMultipliers = pdfWeightMult*leptonSF
            

    eventInfo.weightA      = extraMultipliers*evtWeightA*evtPUWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]
    eventInfo.weightNoPU   = extraMultipliers*evtWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]

    eventInfo.weightB      = extraMultipliers*evtWeightB*evtPUWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]
    eventInfo.weightNoPUB  = extraMultipliers*evtWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]

    eventInfo.weightC      = extraMultipliers*evtWeightCrereco*evtPUWeightCrereco*TrueLumis[ModeIdx][2]/UsedLumis[2]
    eventInfo.weightNoPUC  = extraMultipliers*evtWeightCrereco*TrueLumis[ModeIdx][2]/UsedLumis[2]

    eventInfo.weightC     += extraMultipliers*evtWeightCprompt*evtPUWeightCprompt*TrueLumis[ModeIdx][3]/UsedLumis[3]
    eventInfo.weightNoPUC += extraMultipliers*evtWeightCprompt*TrueLumis[ModeIdx][3]/UsedLumis[3]
            


    #Take the Btag SF weight as each btagged jet SF multiplied together

#     for i in btaggedTightJetIdx:        
#         btagSF_ = btagSF_ * BtagSF(jetPt[i],SFsyst)
                
#    eventInfo.weightBtagSF = btagSF_

    eventInfo.weightBtagSF = 1.


    eventInfo.RunNum = runNum
    eventInfo.LumiNum = lumiNum
    eventInfo.EventNum = eventNum
    eventInfo.ptjet = jet.Pt()
    eventInfo.ptlep0 = lepton0.Pt()
    eventInfo.ptlep1 = lepton1.Pt()
    eventInfo.jetCSV = jetCSV[jetIdx]
    eventInfo.ht = Ht
    eventInfo.htTot = HtTot
    eventInfo.htNoMet = HtNoMet
    eventInfo.msys = system.M()
    eventInfo.ptsys = system.Pt()
    eventInfo.ptsysTot = systemTot.Pt()
    eventInfo.mjll = jll.M()
    eventInfo.ptjll = jll.Pt()
    eventInfo.mjl0 = jl0.M()
    eventInfo.ptjl0 = jl0.Pt()
    eventInfo.mjl1 = jl1.M()
    eventInfo.ptjl1 = jl1.Pt() 
    eventInfo.mjl0met = jl0met.M()
    eventInfo.ptjl0met = jl0met.Pt()
    eventInfo.mjl1met = jl1met.M()
    eventInfo.ptjl1met = jl1met.Pt()
    eventInfo.mjlmax = max(jl0.M(),jl1.M())
    eventInfo.mjlmin = min(jl0.M(),jl1.M())
    eventInfo.ptjlmax = max(jl0.Pt(),jl1.Pt())
    eventInfo.ptjlmin = min(jl0.Pt(),jl1.Pt())
    eventInfo.mjlmetmax = max(jl0met.M(),jl1met.M())
    eventInfo.mjlmetmin = min(jl0met.M(),jl1met.M())
    eventInfo.ptjlmetmax = max(jl0met.Pt(),jl1met.Pt())
    eventInfo.ptjlmetmin = min(jl0met.Pt(),jl1met.Pt())    
    eventInfo.ptleps = leptons.Pt()
    eventInfo.htleps = lepton0.Pt() + lepton1.Pt()
    eventInfo.ptsys_ht = system.Pt()/Ht
    eventInfo.ptjet_ht = jet.Pt()/Ht
    eventInfo.ptlep0_ht = lepton0.Pt()/Ht
    eventInfo.ptlep1_ht = lepton1.Pt()/Ht
    eventInfo.ptleps_ht = leptons.Pt()/Ht
    eventInfo.htleps_ht = (lepton0.Pt()+lepton1.Pt())/Ht
    eventInfo.NlooseJet15Central = len(looseJet15CentralIdx)
    eventInfo.NlooseJet15Forward = len(looseJet15ForwardIdx)
    eventInfo.NlooseJet20Central = len(looseJet20CentralIdx)
    eventInfo.NlooseJet20Forward = len(looseJet20ForwardIdx)
    eventInfo.NlooseJet25Central = len(looseJet25CentralIdx)
    eventInfo.NlooseJet25Forward = len(looseJet25ForwardIdx)
    eventInfo.NtightJetForward = len(tightJetForwardIdx)
    eventInfo.NlooseJet15 = len(looseJet15Idx)
    eventInfo.NlooseJet20 = len(looseJet20Idx)
    eventInfo.NlooseJet25 = len(looseJet25Idx)
    eventInfo.NbtaggedlooseJet15 = len(btaggedLooseJet15Idx)
    eventInfo.NbtaggedlooseJet20 = len(btaggedLooseJet20Idx)
    eventInfo.NbtaggedlooseJet25 = len(btaggedLooseJet25Idx)
    eventInfo.unweightedEta_Avg = unweightedEta_Avg
    eventInfo.unweightedEta_Vecjll = unweightedEta_Vecjll
    eventInfo.unweightedEta_Vecsys = unweightedEta_Vecsys
    eventInfo.unweightedPhi_Avg = unweightedPhi_Avg
    eventInfo.unweightedPhi_Vecjll = unweightedPhi_Vecjll
    eventInfo.unweightedPhi_Vecsys = unweightedPhi_Vecsys
    eventInfo.avgEta = abs(AvgEta)
    eventInfo.sysEta = abs(system.Eta())
    eventInfo.jllEta = abs(jll.Eta())
    eventInfo.dRleps = abs(lepton0.DeltaR(lepton1))
    eventInfo.dRjlmin = min(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1)))
    eventInfo.dRjlmax = max(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1)))
    eventInfo.dEtaleps = abs(lepton0.Eta() - lepton1.Eta())
    eventInfo.dEtajlmin = min(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta()))
    eventInfo.dEtajlmax = max(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta()))
    eventInfo.dPhileps = abs(lepton0.DeltaPhi(lepton1))
    eventInfo.dPhijlmin = min(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1)))
    eventInfo.dPhijlmax = max(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1)))
    eventInfo.dPhimetlmin = min(abs(MET.DeltaPhi(lepton0)),abs(MET.DeltaPhi(lepton1)))
    eventInfo.dPhimetlmax = max(abs(MET.DeltaPhi(lepton0)),abs(MET.DeltaPhi(lepton1)))
    eventInfo.dPhijmet = abs(jet.DeltaPhi(MET))
    eventInfo.met = MET.Pt()
    eventInfo.etajet = abs(jet.Eta())
    eventInfo.etalep0 = abs(lepton0.Eta())
    eventInfo.etalep1 = abs(lepton1.Eta())
    eventInfo.phijet = jet.Phi()
    eventInfo.philep0 = lepton0.Phi()
    eventInfo.philep1 = lepton1.Phi()
    eventInfo.phimet = MET.Phi()
    eventInfo.sumeta2 = sumEta2
    eventInfo.loosejetPt = ptLooseJet
    eventInfo.loosejetCSV = csvLooseJet
    eventInfo.centralityJLL = centrality_jll
    eventInfo.centralityJLLM = centrality_jllm
    eventInfo.centralityJLLWithLoose = centrality_jllWithLoose
    eventInfo.centralityJLLMWithLoose = centrality_jllmWithLoose
    eventInfo.sphericityJLL = sphericity_jll
    eventInfo.sphericityJLLM = sphericity_jllm
    eventInfo.sphericityJLLWithLoose = sphericity_jllWithLoose
    eventInfo.sphericityJLLMWithLoose = sphericity_jllmWithLoose
    eventInfo.aplanarityJLL = aplanarity_jll
    eventInfo.aplanarityJLLM = aplanarity_jllm
    eventInfo.aplanarityJLLWithLoose = aplanarity_jllWithLoose
    eventInfo.aplanarityJLLMWithLoose = aplanarity_jllmWithLoose

    if not inZpeak and passMET:
        if len(goodJetIdx) == 1:
#            treeList['tree1jNotagging'][ModeIdx].Fill()
#            if len(btaggedTightJetIdx) == 0:
#                treeList['tree1j0t'][ModeIdx].Fill()
            if len(btaggedTightJetIdx) == 1:
                treeList['tree1j1t'][ModeIdx].Fill()
        if len(goodJetIdx) == 2:
#            treeList['tree2jNotagging'][ModeIdx].Fill()
#            if len(btaggedTightJetIdx) == 0:
#                treeList['tree2j0t'][ModeIdx].Fill()
            if len(btaggedTightJetIdx) == 1:
                treeList['tree2j1t'][ModeIdx].Fill()
            if len(btaggedTightJetIdx) == 2:
                treeList['tree2j2t'][ModeIdx].Fill()
#        if len(goodJetIdx) > 2:
#            treeList['tree3plusjNotagging'][ModeIdx].Fill()
    if inZpeak:
        treeList['treeZpeakLepSel'][ModeIdx].Fill()
#        #No MET cut is applied to 1j1t zpeak region
#        if len(goodJetIdx) == 1:
#            if len(btaggedTightJetIdx) == 1:
#                treeList['tree1j1tZpeak'][ModeIdx].Fill()


if not os.path.exists('tmvaFiles/'+fileVersion):
    command = 'mkdir tmvaFiles/'+fileVersion
    os.system(command)

outFileName = 'tmvaFiles/'+fileVersion+'/'+fileLists[ChanName][2]
if not 'noSyst' in systName:
    outFileName = outFileName.replace(".root",'_'+systName+'.root')

print
print outFileName
outputFile = TFile(outFileName,"RECREATE")

emuDir = outputFile.mkdir("emuChannel","emu channel");
mumuDir = outputFile.mkdir("mumuChannel","mumu channel");
eeDir = outputFile.mkdir("eeChannel","ee channel");
#combinedDir = outputFile.mkdir("combined","All Channels Combined");

for i in treeList:
    tree = treeList[i]
    emuDir.cd()
    tree[0].Write()
    mumuDir.cd()
    tree[1].Write()
    eeDir.cd()
    tree[2].Write()
#    combinedDir.cd()
#    tree[3].Write()

