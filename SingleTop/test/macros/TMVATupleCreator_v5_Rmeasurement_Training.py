#!/usr/bin/env python

#Uses random numbers for btagging scale factors

#Added in the variables for the tW vs tbarW R measurement
#
#

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
RunD = True

#fileVersion = 'v11_MET50'
fileVersion = 'RmeasurementTrain'
#fileVersion = 'TestDir'

useLeptonSF = True

#Input actual luminosities for runA, B, C, and D for each channel from data

isData = False

SFsyst = ''
if systName == 'BtagSFUp':
    SFsyst = 'Up'
if systName == 'BtagSFDown':
    SFsyst = 'Down'
if 'Data' in ChanName:
    SFsyst = 'Data'
    isData = True


##Numbers from pixellumicalc overview
TrueLumis = [[876.,4412.,7055.,7360.],
             [876.,4412.,7017.,7369.],
             [876.,4412.,7055.,7369.]]


#The values used from SingleTopPSetsSummer_tW for the luminosities of run A, B, C, and D
UsedLumis = [15000.,15000.,15000.,15000.]

#Lepton Scale Factors
#lepSF = [0.936,0.962,0.950]
lepSFUnc = [0.011,0.012,0.014]

lepSF = [0.916,0.963,0.903]
        
### a C/C++ structure is required, to allow memory based access
gROOT.ProcessLine(
    "struct eventInfo_t {\
    Int_t      RunNum;\
    Int_t      LumiNum;\
    Int_t      EventNum;\
    Double_t   weightA;\
    Double_t   weightNoPUA;\
    Double_t   weightB;\
    Double_t   weightNoPUB;\
    Double_t   weightC;\
    Double_t   weightNoPUC;\
    Double_t   weightD;\
    Double_t   weightNoPUD;\
    Double_t   weightBtagSF;\
    Double_t   lepJetPt;\
    Double_t   lepPt;\
    Double_t   lepJetDR;\
    Double_t   lepJetDPhi;\
    Double_t   lepJetDEta;\
    Double_t   lepJetM;\
    Double_t   lepPtRelJet;\
    Double_t   jetPtRelLep;\
    Double_t   lepPtRelJetSameLep;\
    Double_t   lepPtRelJetOtherLep;\
    Double_t   lepJetMt;\
    Double_t   lepCosTheta_boosted;\
    Double_t   lepJetCosTheta_boosted;\
    Double_t   lepCosTheta;\
    Double_t   lepJetCosTheta;\
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
        ['D', 'weightD'],
        ['D', 'weightNoPUD'],
        ['D', 'weightBtagSF'],
        ['D', 'lepJetPt'],
        ['D', 'lepPt'],
        ['D', 'lepJetDR'],
        ['D', 'lepJetDPhi'],
        ['D', 'lepJetDEta'],
        ['D', 'lepJetM'],
        ['D', 'lepPtRelJet'],
        ['D', 'jetPtRelLep'],
        ['D', 'lepPtRelJetSameLep'],
        ['D', 'lepPtRelJetOtherLep'],
        ['D', 'lepJetMt'],
        ['D', 'lepCosTheta_boosted'],
        ['D', 'lepJetCosTheta_boosted'],
        ['D', 'lepCosTheta'],
        ['D', 'lepJetCosTheta'],
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

treeListRight = {'tree1j1t':[TTree('1j1tRight','1j1t'),TTree('1j1tRight','1j1t'),TTree('1j1tRight','1j1t')],
            }

treeListWrong = {'tree1j1t':[TTree('1j1tWrong','1j1t'),TTree('1j1tWrong','1j1t'),TTree('1j1tWrong','1j1t')],
            }

#Branch variables for TMVA tree

eventInfoRight = eventInfo_t()

eventInfoWrong = eventInfo_t()

for i in treeListRight:
    trees = treeListRight[i]
    for tree in trees:
        for var in Vars:
            tree.Branch(var[1],AddressOf(eventInfoRight,var[1]),var[1]+'/'+var[0])

for i in treeListWrong:
    trees = treeListWrong[i]
    for tree in trees:
        for var in Vars:
            tree.Branch(var[1],AddressOf(eventInfoWrong,var[1]),var[1]+'/'+var[0])

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

previousCount = 0.
for file in fileLists[ChanName][1]:
    fchain.Add(file)
    print file, fchain.GetEntries()*1., fchain.GetEntries()*1.-previousCount
    previousCount = fchain.GetEntries()*1.

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
    evtWeightC = event.weightC
    evtWeightD = event.weightD
    evtPUWeightA = event.PUWeightA
    evtPUWeightB = event.PUWeightB
    evtPUWeightC = event.PUWeightC
    evtPUWeightD = event.PUWeightD
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
#                        if electronMVATrigV0[i] >= 0.0 and electronMVATrigV0[i] <= 1.0:
                        if electronMVATrigV0[i] >= 0.5 and electronMVATrigV0[i] <= 1.0:
                            if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
#                            if electronDeltaCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                                if electronTrackerExpectedInnerHits[i] <= 1:
                                    goodEleidx.append(i)
                                    isTightElectron = True
        if not isTightElectron:
            if electronPt[i] > 15:
                if abs(electronEta[i]) < 2.5:
#                    if electronMVATrigV0[i] >= 0.0 and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                    if electronMVATrigV0[i] >= 0.5 and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                        if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
#                        if electronDeltaCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                            looseEleidx.append(i)
    nLooseLeptons = len(looseEleidx) + len(looseMuonidx)

    ModeIdx = -1

    lepton0 = TLorentzVector()
    lepton1 = TLorentzVector()
    lep0Charge = 0
    lep1Charge = 0

    if len(goodMuonidx) == 1 and len(goodEleidx) == 1:
        ModeIdx = 0
        i = goodMuonidx[0]
        j = goodEleidx[0]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        lep0Charge = muonCharge[i]
        lep1Charge = electronCharge[j]
        totalCharge = muonCharge[i]+electronCharge[j]
        chargeMult = muonCharge[i]*electronCharge[j]
    elif len(goodMuonidx) == 2 and len(goodEleidx) == 0:
        ModeIdx = 1
        i = goodMuonidx[0]
        j = goodMuonidx[1]
        lepton0.SetPtEtaPhiE(muonPt[i],muonEta[i],muonPhi[i],muonE[i])
        lepton1.SetPtEtaPhiE(muonPt[j],muonEta[j],muonPhi[j],muonE[j])
        lep0Charge = muonCharge[i]
        lep1Charge = muonCharge[j]
        totalCharge = muonCharge[i]+muonCharge[j]
        chargeMult = muonCharge[i]*muonCharge[j]
    elif len(goodMuonidx) == 0 and len(goodEleidx) == 2:
        ModeIdx = 2
        i = goodEleidx[0]
        j = goodEleidx[1]
        lepton0.SetPtEtaPhiE(electronPt[i],electronEta[i],electronPhi[i],electronE[i])
        lepton1.SetPtEtaPhiE(electronPt[j],electronEta[j],electronPhi[j],electronE[j])
        lep0Charge = electronCharge[i]
        lep1Charge = electronCharge[j]
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
    
#     jll = jet + lepton0 + lepton1
#     jl0 = jet + lepton0
#     jl1 = jet + lepton1
#     jl0met = jet + lepton0 + MET
#     jl1met = jet + lepton1 + MET
#     leptons = lepton0 + lepton1

#     H = jet.E() + lepton0.E() + lepton1.E() + MET.E()
#     HNoMet = jet.E() + lepton0.E() + lepton1.E()

#     for i in range(1,len(goodJetIdx)):
#         tempidx = goodJetIdx[i]
#         tempjet = TLorentzVector()
#         tempjet.SetPtEtaPhiE(jetPt[tempidx],jetEta[tempidx], jetPhi[tempidx], jetE[tempidx])

#         system = system + tempjet
#         systemTot = systemTot + tempjet
#         Ht = Ht + tempjet.Pt()
#         HtTot = HtTot + tempjet.Pt()
#         HtNoMet = HtNoMet + tempjet.Pt()

#     listJLL = list()

#     particles = list()
#     particles.append(lepton0)
#     particles.append(lepton1)
#     particles.append(jet)
#     particles.append(MET)

#     listJLL.append(lepton0)
#     listJLL.append(lepton1)
#     listJLL.append(jet)

#     listJLLM = list(listJLL)
#     listJLLM.append(MET)

#     listJLLWithLoose = list(listJLL)
#     listJLLMWithLoose = list(listJLLM)

#     for i in looseJet20Idx:
#         temp = TLorentzVector()
#         temp.SetPtEtaPhiE(jetPt[i],jetEta[i], jetPhi[i], jetE[i])
#         listJLLWithLoose.append(temp)
#         listJLLMWithLoose.append(temp)
#         systemTot = systemTot + temp
#         HtTot = HtTot + temp.Pt()



#     centrality_jll = Centrality(listJLL)
#     centrality_jllm = Centrality(listJLLM)
#     centrality_jllWithLoose = Centrality(listJLLWithLoose)
#     centrality_jllmWithLoose = Centrality(listJLLMWithLoose)

#     sphericity_jll = Sphericity(listJLL)
#     sphericity_jllm = Sphericity(listJLLM)
#     sphericity_jllWithLoose = Sphericity(listJLLWithLoose)
#     sphericity_jllmWithLoose = Sphericity(listJLLMWithLoose)

#     aplanarity_jll = Aplanarity(listJLL)
#     aplanarity_jllm = Aplanarity(listJLLM)
#     aplanarity_jllWithLoose = Aplanarity(listJLLWithLoose)
#     aplanarity_jllmWithLoose = Aplanarity(listJLLMWithLoose)

#     AvgEta = (lepton0.Eta() + lepton1.Eta() + jet.Eta())/3.
#     AvgPhi= (lepton0.Phi() + lepton1.Phi() + jet.Phi())/3.

#     AvgVec = TLorentzVector()
#     AvgVec.SetPtEtaPhiM(10,AvgEta, AvgPhi, 0)

#     unweightedEta_Avg = pow(lepton0.Eta()-AvgEta,2) + pow(lepton1.Eta()-AvgEta,2) + pow(jet.Eta()-AvgEta,2)
#     unweightedEta_Vecjll = pow(lepton0.Eta()-jll.Eta(),2) + pow(lepton1.Eta()-jll.Eta(),2) + pow(jet.Eta()-jll.Eta(),2)
#     unweightedEta_Vecsys = pow(lepton0.Eta()-system.Eta(),2) + pow(lepton1.Eta()-system.Eta(),2) + pow(jet.Eta()-system.Eta(),2)

#     unweightedPhi_Avg = pow(lepton0.DeltaPhi(AvgVec),2) + pow(lepton1.DeltaPhi(AvgVec),2) + pow(jet.DeltaPhi(AvgVec),2)
#     unweightedPhi_Vecjll = pow(lepton0.DeltaPhi(jll),2) + pow(lepton1.DeltaPhi(jll),2) + pow(jet.DeltaPhi(jll),2)
#     unweightedPhi_Vecsys = pow(lepton0.DeltaPhi(system),2) + pow(lepton1.DeltaPhi(system),2) + pow(jet.DeltaPhi(system),2)

#     sumEta2 = pow(lepton0.Eta(),2) + pow(lepton1.Eta(),2) + pow(jet.Eta(),2)

#     ptLooseJet = 0.
#     csvLooseJet = -0.05
#     if len(looseJet20Idx) > 0:
#         ptLooseJet = jetPt[looseJet20Idx[0]]
#         csvLooseJet = jetCSV[looseJet20Idx[0]]

    eventInfoRight.weightA = 0.
    eventInfoRight.weightNoPUA = 0.
    eventInfoRight.weightB = 0.
    eventInfoRight.weightNoPUB = 0.
    eventInfoRight.weightC = 0.
    eventInfoRight.weightNoPUC = 0.
    eventInfoRight.weightD = 0.
    eventInfoRight.weightNoPUD = 0.

    eventInfoWrong.weightA = 0.
    eventInfoWrong.weightNoPUA = 0.
    eventInfoWrong.weightB = 0.
    eventInfoWrong.weightNoPUB = 0.
    eventInfoWrong.weightC = 0.
    eventInfoWrong.weightNoPUC = 0.
    eventInfoWrong.weightD = 0.
    eventInfoWrong.weightNoPUD = 0.

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
            

    eventInfoRight.weightA      = extraMultipliers*evtWeightA*evtPUWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]
    eventInfoRight.weightNoPU   = extraMultipliers*evtWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]
    eventInfoRight.weightB      = extraMultipliers*evtWeightB*evtPUWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]
    eventInfoRight.weightNoPUB  = extraMultipliers*evtWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]
    eventInfoRight.weightC      = extraMultipliers*evtWeightC*evtPUWeightC*TrueLumis[ModeIdx][2]/UsedLumis[2]
    eventInfoRight.weightNoPUC  = extraMultipliers*evtWeightC*TrueLumis[ModeIdx][2]/UsedLumis[2]
    eventInfoRight.weightD      = extraMultipliers*evtWeightD*evtPUWeightD*TrueLumis[ModeIdx][3]/UsedLumis[3]
    eventInfoRight.weightNoPUD  = extraMultipliers*evtWeightD*TrueLumis[ModeIdx][3]/UsedLumis[3]



    eventInfoWrong.weightA      = extraMultipliers*evtWeightA*evtPUWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]
    eventInfoWrong.weightNoPU   = extraMultipliers*evtWeightA*TrueLumis[ModeIdx][0]/UsedLumis[0]
    eventInfoWrong.weightB      = extraMultipliers*evtWeightB*evtPUWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]
    eventInfoWrong.weightNoPUB  = extraMultipliers*evtWeightB*TrueLumis[ModeIdx][1]/UsedLumis[1]
    eventInfoWrong.weightC      = extraMultipliers*evtWeightC*evtPUWeightC*TrueLumis[ModeIdx][2]/UsedLumis[2]
    eventInfoWrong.weightNoPUC  = extraMultipliers*evtWeightC*TrueLumis[ModeIdx][2]/UsedLumis[2]
    eventInfoWrong.weightD      = extraMultipliers*evtWeightD*evtPUWeightD*TrueLumis[ModeIdx][3]/UsedLumis[3]
    eventInfoWrong.weightNoPUD  = extraMultipliers*evtWeightD*TrueLumis[ModeIdx][3]/UsedLumis[3]




    #Take the Btag SF weight as each btagged jet SF multiplied together

#     for i in btaggedTightJetIdx:        
#         btagSF_ = btagSF_ * BtagSF(jetPt[i],SFsyst)
                
#    eventInfo.weightBtagSF = btagSF_

    eventInfoRight.weightBtagSF = 1.
    eventInfoWrong.weightBtagSF = 1.


    eventInfoRight.RunNum = runNum
    eventInfoRight.LumiNum = lumiNum
    eventInfoRight.EventNum = eventNum

    eventInfoWrong.RunNum = runNum
    eventInfoWrong.LumiNum = lumiNum
    eventInfoWrong.EventNum = eventNum


    if lep0Charge > lep1Charge:
        leps = [lepton0, lepton1]
    else:
        leps = [lepton1, lepton0]


    if not 'bar' in ChanName:
        if lep0Charge > lep1Charge:
            leps = [lepton0, lepton1]
        else:
            leps = [lepton1, lepton0]
    elif 'bar' in ChanName:
        if lep0Charge > lep1Charge:
            leps = [lepton1, lepton0]
        else:
            leps = [lepton0, lepton1]
        


    b_ = TVector3((system).BoostVector())
            
    
    boostedJet_ = TLorentzVector(jet)
    boostedJet_.Boost(-b_)
    p3Jet_ = boostedJet_.Vect()

    
            
    eventInfoRight.lepJetPt            = (leps[0] + jet).Pt()
    eventInfoRight.lepPt               = leps[0].Pt()
    eventInfoRight.lepJetDR            = abs(leps[0].DeltaR(jet))
    eventInfoRight.lepJetDPhi          = abs(leps[0].DeltaPhi(jet))
    eventInfoRight.lepJetDEta          = abs(leps[0].Eta() - jet.Eta())
    eventInfoRight.lepJetM             = (leps[0] + jet).M()
    eventInfoRight.lepPtRelJet         = leps[0].Perp(jet.Vect())
    eventInfoRight.jetPtRelLep         = jet.Perp(leps[0].Vect())
    eventInfoRight.lepPtRelJetSameLep  = leps[0].Perp((leps[0]+jet).Vect())
    eventInfoRight.lepPtRelJetOtherLep = leps[0].Perp((leps[1]+jet).Vect())
    eventInfoRight.lepJetMt            = (leps[0] + jet).Mt()    
    boostedLep_ = TLorentzVector(leps[0])
    boostedLep_.Boost(-b_)
    p3Lepton_ = boostedLep_.Vect()
    eventInfoRight.lepCosTheta_boosted    = p3Lepton_.CosTheta()
    eventInfoRight.lepJetCosTheta_boosted = p3Lepton_.Dot(p3Jet_)/(p3Lepton_.Mag()*p3Jet_.Mag())
    eventInfoRight.lepCosTheta         = leps[0].Vect().CosTheta()
    eventInfoRight.lepJetCosTheta      = leps[0].Vect().Dot(jet.Vect())/(leps[0].Vect().Mag()*jet.Vect().Mag())

    

    eventInfoWrong.lepJetPt            = (leps[1] + jet).Pt()
    eventInfoWrong.lepPt               = leps[1].Pt()
    eventInfoWrong.lepJetDR            = abs(leps[1].DeltaR(jet))
    eventInfoWrong.lepJetDPhi          = abs(leps[1].DeltaPhi(jet))
    eventInfoWrong.lepJetDEta          = abs(leps[1].Eta() - jet.Eta())
    eventInfoWrong.lepJetM             = (leps[1] + jet).M()
    eventInfoWrong.lepPtRelJet         = leps[1].Perp(jet.Vect())
    eventInfoWrong.jetPtRelLep         = jet.Perp(leps[1].Vect())
    eventInfoWrong.lepPtRelJetSameLep  = leps[1].Perp((leps[1]+jet).Vect())
    eventInfoWrong.lepPtRelJetOtherLep = leps[1].Perp((leps[0]+jet).Vect())
    eventInfoWrong.lepJetMt            = (leps[1] + jet).Mt()    
    boostedLep_ = TLorentzVector(leps[1])
    boostedLep_.Boost(-b_)
    p3Lepton_ = boostedLep_.Vect()
    eventInfoWrong.lepCosTheta_boosted    = p3Lepton_.CosTheta()
    eventInfoWrong.lepJetCosTheta_boosted = p3Lepton_.Dot(p3Jet_)/(p3Lepton_.Mag()*p3Jet_.Mag())
    eventInfoWrong.lepCosTheta         = leps[1].Vect().CosTheta()
    eventInfoWrong.lepJetCosTheta      = leps[1].Vect().Dot(jet.Vect())/(leps[1].Vect().Mag()*jet.Vect().Mag())
    


    if not inZpeak and passMET:
        if len(goodJetIdx) == 1:
            if len(btaggedTightJetIdx) == 1:
                treeListRight['tree1j1t'][ModeIdx].Fill()
                treeListWrong['tree1j1t'][ModeIdx].Fill()


if not os.path.exists('tmvaFiles/'+fileVersion):
    command = 'mkdir tmvaFiles/'+fileVersion
    os.system(command)

outFileName = 'tmvaFiles/'+fileVersion+'/'+fileLists[ChanName][2]
if not 'noSyst' in systName:
    outFileName = outFileName.replace(".root",'_'+systName+'.root')
outFileName = outFileName.replace(".root",'_TRAINTEST.root')

print
print outFileName
outputFile = TFile(outFileName,"RECREATE")

emuDir = outputFile.mkdir("emuChannel","emu channel");
mumuDir = outputFile.mkdir("mumuChannel","mumu channel");
eeDir = outputFile.mkdir("eeChannel","ee channel");
#combinedDir = outputFile.mkdir("combined","All Channels Combined");

for i in treeListRight:
    treeRight = treeListRight[i]
    treeWrong = treeListWrong[i]
    emuDir.cd()
    treeRight[0].Write()
    treeWrong[0].Write()
    mumuDir.cd()
    treeRight[1].Write()
    treeWrong[1].Write()
    eeDir.cd()
    treeRight[2].Write()
    treeWrong[2].Write()


#    combinedDir.cd()
#    tree[3].Write()

