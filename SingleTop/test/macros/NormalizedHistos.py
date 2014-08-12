#!/usr/bin/env python                                                                                                                  

from ROOT import *
import sys
from EventShapeVariables import *        

fileNamesList = ['../output/ntuple_SysTrees_TWDilepton.root', '../output/ntuple_SysTrees_TTBarDilepton.root']
#fileNamesList =  ['../output/ntuple_SysTrees_TWChannel.root']

Channel = ['emu', 'mumu', 'ee']

LepSelection = [0,0,0]
LepVeto = [0,0,0]
mllCut = [0,0,0]
MetCut = [0,0,0]
OneJet = [0,0,0]
JetBtagL = [0,0,0]
JetBtagM = [0,0,0]
JetBtagT = [0,0,0]

plotInfo = [['ptjet',60,0,300],
            ['ptlep0',60,0,300],
            ['ptlep1',60,0,300],
            ['jetCSV',100,0,1],
            ['ht',100,0,500],
            ['htNoMet',100,0,500],
            ['msys',60,0,600],
            ['mjll',60,0,600],
            ['mjl0',60,0,600],
            ['mjl1',60,0,600],
            ['ptsys',60,0,300],
            ['ptjll',60,0,300],
            ['ptjl0',60,0,300],
            ['ptjl1',60,0,300],
            ['ptleps',60,0,300],
            ['htleps',60,0,300],
            ['ptsys_ht',100,0,1],
            ['ptjet_ht',100,0,1],
            ['ptlep0_ht',100,0,1],
            ['ptlep1_ht',100,0,1],
            ['ptleps_ht',100,0,1],
            ['htleps_ht',100,0,1],
            ['NlooseJet15Central',10,0,10],
            ['NlooseJet15Forward',10,0,10],
            ['NlooseJet20Central',10,0,10],
            ['NlooseJet20Forward',10,0,10],
            ['NlooseJet25Central',10,0,10],
            ['NlooseJet25Forward',10,0,10],
            ['NtightJetForward',10,0,10],            
            ['NlooseJet15',10,0,10],
            ['NlooseJet20',10,0,10],
            ['NlooseJet25',10,0,10],
            ['NbtaggedlooseJet15',4,0,4],
            ['NbtaggedlooseJet20',4,0,4],
            ['NbtaggedlooseJet25',4,0,4],
            ['unweightedEta_Avg', 300,0,30],
            ['unweightedEta_Vecjll', 300,0,30],
            ['unweightedEta_Vecsys', 300,0,30],
            ['unweightedPhi_Avg', 300,0,30],
            ['unweightedPhi_Vecjll', 300,0,30],
            ['unweightedPhi_Vecsys', 300,0,30],
            ['avgEta', 100, 0,5],
            ['sysEta', 100, 0,5],
            ['jllEta', 100, 0,5],
            ['dRleps', 100, 0,10],
            ['dRjlmin', 100, 0,10],
            ['dRjlmax', 100, 0,10],
            ['dEtaleps', 100, 0,10],
            ['dEtajlmin', 100, 0,10],
            ['dEtajlmax', 100, 0,10],
            ['dPhileps', 100, 0,3.15],
            ['dPhijlmin', 100, 0,3.15],
            ['dPhijlmax', 100, 0,3.15],
#             ['cosThetaleps', 100, 0,10],
#             ['cosThetajlmin', 100, 0,10],
#             ['cosThetajlmax', 100, 0,10]
            ['met', 60, 0, 300],
            ['flavourJet', 100, -25, 25],
            ['etajet', 100, 0, 5],
            ['etalep0', 100, 0, 5],
            ['etalep1', 100, 0, 5],
            ['phijet', 100, -3.15, 3.15],
            ['philep0', 100, -3.15, 3.15],
            ['philep1', 100, -3.15, 3.15],
            ['phimet', 100, -3.15, 3.15],
            ['sumeta2', 100, 0, 15],
            ['loosejetPt', 60, 0, 300],
            ['loosejetCSV', 175, -0.75, 1.0],
            ['loosejetFlavour', 100, -25, 25],            
            ['centralityJLL',100,0,1],
            ['centralityJLLM',100,0,1],
            ['centralityJLLWithLoose',100,0,1],
            ['centralityJLLMWithLoose',100,0,1],
            ['sphericityJLL',100,0,1],
            ['sphericityJLLM',100,0,1],
            ['sphericityJLLWithLoose',100,0,1],
            ['sphericityJLLMWithLoose',100,0,1],
            ['aplanarityJLL',100,0,.5],
            ['aplanarityJLLM',100,0,.5],
            ['aplanarityJLLWithLoose',100,0,.5],
            ['aplanarityJLLMWithLoose',100,0,.5],

            ]

outputHistos = TFile('histos.root','RECREATE')

for fileName in fileNamesList:
    
    #    file = TFile('../output/ntuple_SysTrees_TWChannel.root')
    print fileName

    channelName = fileName.split('_')[-1][:-5]
    
    file = TFile(fileName)
    
    file.cd('TreesDileptontW')

    treeName = channelName + '_noSyst'
    if channelName == 'TWDilepton':
        treeName = 'TWChannelDilepton_noSyst'
        
    print treeName
    
    tWtree = gROOT.FindObject(treeName)

    Histos = dict()
    HistosBtaggedL = dict()
    HistosBtaggedM = dict()
    HistosBtaggedT = dict()

    for plot in plotInfo:
        Histos[plot[0]] = TH1F(plot[0],plot[0],plot[1],plot[2],plot[3])
        HistosBtaggedL[plot[0]] = TH1F(plot[0]+'btagL',plot[0],plot[1],plot[2],plot[3])
        HistosBtaggedM[plot[0]] = TH1F(plot[0]+'btagM',plot[0],plot[1],plot[2],plot[3])
        HistosBtaggedT[plot[0]] = TH1F(plot[0]+'btagT',plot[0],plot[1],plot[2],plot[3])

    nEvents = tWtree.GetEntries()*1.
    print nEvents

    emuStart = 0
    mumuStart = 0
    eeStart = 0
    
    evtCount = 0.
    reportEvery = 1000
    percent = 0.0

    for event in tWtree:
        evtCount += 1.
        if evtCount/nEvents > percent:
            i = int(percent*25.)
            progress = '0%[' + '-' * i + ' ' * (25-i) + ']100%\r'
            sys.stdout.write(progress)
            sys.stdout.flush()
            percent += 0.04
            
#         if evtCount%reportEvery == 0:
#             print str(evtCount) + "th event"

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
        
        if len(electronPt) > 0 and len(muonPt) > 0:
            emuStart += 1
        if len(electronPt) > 1:
            eeStart += 1
        if len(muonPt) > 1:
            mumuStart += 1

        goodMuonidx = list()
        goodEleidx = list()
        looseMuonidx = list()
        looseEleidx = list()

        # print 'Total Leptons ', (len(muonPt)+len(electronPt))
        # print 'Muons ', len(muonPt)
        # print 'Electrons ', len(electronPt)

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
                            if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0:
                                #                            if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                                if electronDeltaCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                                    if electronTrackerExpectedInnerHits[i] <= 1:
                                        goodEleidx.append(i)
                                        isTightElectron = True
            if not isTightElectron:
                if electronPt[i] > 15:
                    if abs(electronEta[i]) < 2.5:
                        if electronMVATrigV0[i] >= 0. and electronMVATrigV0[i] <= 1.0: #####ADJUSTMENT
                            #                        if electronRhoCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
                            if electronDeltaCorrectedRelIso[i] < 0.15: #####ADJUSTMENT
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
    
        LepSelection[ModeIdx] += 1

        if nLooseLeptons != 0:
            continue

        LepVeto[ModeIdx] += 1

        mll = (lepton0 + lepton1).M()

        if mll < 20:
            continue

        if ModeIdx > 0:
            if mll < 101 and mll > 81:
                continue

    
        mllCut[ModeIdx] += 1



        MetPt = event.MetPt
        MetPhi = event.MetPhi

        if MetPt < 30 and not ModeIdx == 0:
            continue

        MetCut[ModeIdx] += 1
        

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
        jetFlavour = event.jetFlavour

        goodJetIdx = list()
        looseJetIdx = list()
        btaggedLooseJetIdx = list()
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
                        if min(lepton0.DeltaR(tJet),lepton1.DeltaR(tJet)) > 0.3:
                            goodJetIdx.append(i)
                            isTightJet = True
            if not isTightJet:
                if jetID:
                    if jetPt[i] > 15:
                        looseJet15Idx.append(i)
                        if abs(jetEta[i]) < 2.5:
                            looseJet15CentralIdx.append(i)
                        else:
                            looseJet15ForwardIdx.append(i)
                        if jetCSV[i] > 0.679:
                                btaggedLooseJet15Idx.append(i)
                    if jetPt[i] > 20:
                        looseJet20Idx.append(i)
                        if abs(jetEta[i]) < 2.5:
                            looseJet20CentralIdx.append(i)
                        else:
                            looseJet20ForwardIdx.append(i)
                        if jetCSV[i] > 0.679:
                            btaggedLooseJet20Idx.append(i)
                    if jetPt[i] > 25:
                        looseJet25Idx.append(i)
                        if abs(jetEta[i]) < 2.5:
                            looseJet25CentralIdx.append(i)
                        else:
                            looseJet25ForwardIdx.append(i)
                        if jetCSV[i] > 0.679:
                            btaggedLooseJet25Idx.append(i)
                    if jetPt[i] > 30:
                        if abs(jetEta[i]) > 2.5:
                            tightJetForwardIdx.append(i)
                    

        if len(goodJetIdx) != 1:
            continue


        OneJet[ModeIdx] += 1

        jetIdx = goodJetIdx[0]

        jet = TLorentzVector()
        jet.SetPtEtaPhiE(jetPt[jetIdx],jetEta[jetIdx], jetPhi[jetIdx], jetE[jetIdx])



        system = lepton0 + lepton1 + MET + jet
        Ht = lepton0.Pt() + lepton1.Pt() + MET.Pt() + jet.Pt()
        HtNoMet = lepton0.Pt() + lepton1.Pt() + jet.Pt()
        jll = jet + lepton0 + lepton1
        jl0 = jet + lepton0
        jl1 = jet + lepton1
        leptons = lepton0 + lepton1

        H = jet.E() + lepton0.E() + lepton1.E() + MET.E()
        HNoMet = jet.E() + lepton0.E() + lepton1.E()

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

        for i in looseJet15Idx:
            temp = TLorentzVector()
            temp.SetPtEtaPhiE(jetPt[i],jetEta[i], jetPhi[i], jetE[i])
            listJLLWithLoose.append(temp)
            listJLLMWithLoose.append(temp)



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
        csvLooseJet = -0.5
        flavourLooseJet = -24.
        if len(looseJet15Idx) > 0:
            ptLooseJet = jetPt[looseJet15Idx[0]]
            csvLooseJet = jetCSV[looseJet15Idx[0]]
            flavourLooseJet = jetFlavour[looseJet15Idx[0]]
            
        Histos['ptjet'].Fill(jet.Pt())
        Histos['ptlep0'].Fill(lepton0.Pt())
        Histos['ptlep1'].Fill(lepton1.Pt())
        Histos['jetCSV'].Fill(jetCSV[jetIdx])
        Histos['ht'].Fill(Ht)
        Histos['htNoMet'].Fill(HtNoMet)
        Histos['msys'].Fill(system.M())
        Histos['ptsys'].Fill(system.Pt())
        Histos['mjll'].Fill(jll.M())
        Histos['ptjll'].Fill(jll.Pt())
        Histos['mjl0'].Fill(jl0.M())
        Histos['ptjl0'].Fill(jl0.Pt())
        Histos['mjl1'].Fill(jl1.M())
        Histos['ptjl1'].Fill(jl1.Pt())
        Histos['ptleps'].Fill(leptons.Pt())
        Histos['htleps'].Fill(lepton0.Pt() + lepton1.Pt())
        Histos['ptsys_ht'].Fill(system.Pt()/Ht)
        Histos['ptjet_ht'].Fill(jet.Pt()/Ht)
        Histos['ptlep0_ht'].Fill(lepton0.Pt()/Ht)
        Histos['ptlep1_ht'].Fill(lepton1.Pt()/Ht)
        Histos['ptleps_ht'].Fill(leptons.Pt()/Ht)
        Histos['htleps_ht'].Fill((lepton0.Pt()+lepton1.Pt())/Ht)
        Histos['NlooseJet15Central'].Fill(len(looseJet15CentralIdx))
        Histos['NlooseJet15Forward'].Fill(len(looseJet15ForwardIdx))
        Histos['NlooseJet20Central'].Fill(len(looseJet20CentralIdx))
        Histos['NlooseJet20Forward'].Fill(len(looseJet20ForwardIdx))
        Histos['NlooseJet25Central'].Fill(len(looseJet25CentralIdx))
        Histos['NlooseJet25Forward'].Fill(len(looseJet25ForwardIdx))
        Histos['NtightJetForward'].Fill(len(tightJetForwardIdx))
        Histos['NlooseJet15'].Fill(len(looseJet15Idx))
        Histos['NlooseJet20'].Fill(len(looseJet20Idx))
        Histos['NlooseJet25'].Fill(len(looseJet25Idx))
        Histos['NbtaggedlooseJet15'].Fill(len(btaggedLooseJet15Idx))
        Histos['NbtaggedlooseJet20'].Fill(len(btaggedLooseJet20Idx))
        Histos['NbtaggedlooseJet25'].Fill(len(btaggedLooseJet25Idx))
        Histos['unweightedEta_Avg'].Fill(unweightedEta_Avg)
        Histos['unweightedEta_Vecjll'].Fill(unweightedEta_Vecjll)
        Histos['unweightedEta_Vecsys'].Fill(unweightedEta_Vecsys)
        Histos['unweightedPhi_Avg'].Fill(unweightedPhi_Avg)
        Histos['unweightedPhi_Vecjll'].Fill(unweightedPhi_Vecjll)
        Histos['unweightedPhi_Vecsys'].Fill(unweightedPhi_Vecsys)
        Histos['avgEta'].Fill(abs(AvgEta))
        Histos['sysEta'].Fill(abs(system.Eta()))
        Histos['jllEta'].Fill(abs(jll.Eta()))
        Histos['dRleps'].Fill(abs(lepton0.DeltaR(lepton1)))
        Histos['dRjlmin'].Fill(min(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        Histos['dRjlmax'].Fill(max(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        Histos['dEtaleps'].Fill(abs(lepton0.Eta() - lepton1.Eta()))
        Histos['dEtajlmin'].Fill(min(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        Histos['dEtajlmax'].Fill(max(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        Histos['dPhileps'].Fill(abs(lepton0.DeltaPhi(lepton1)))
        Histos['dPhijlmin'].Fill(min(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        Histos['dPhijlmax'].Fill(max(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        Histos['met'].Fill(MET.Pt())
        Histos['flavourJet'].Fill(jetFlavour[jetIdx])
        Histos['etajet'].Fill(abs(jet.Eta()))
        Histos['etalep0'].Fill(abs(lepton0.Eta()))
        Histos['etalep1'].Fill(abs(lepton1.Eta()))
        Histos['phijet'].Fill(jet.Phi())
        Histos['philep0'].Fill(lepton0.Phi())
        Histos['philep1'].Fill(lepton1.Phi())
        Histos['phimet'].Fill(MET.Phi())
        Histos['sumeta2'].Fill(sumEta2)
        Histos['loosejetPt'].Fill(ptLooseJet)
        Histos['loosejetCSV'].Fill(csvLooseJet)
        Histos['loosejetFlavour'].Fill(flavourLooseJet)
        Histos['centralityJLL'].Fill(centrality_jll)
        Histos['centralityJLLM'].Fill(centrality_jllm)
        Histos['centralityJLLWithLoose'].Fill(centrality_jllWithLoose)
        Histos['centralityJLLMWithLoose'].Fill(centrality_jllmWithLoose)
        Histos['sphericityJLL'].Fill(sphericity_jll)
        Histos['sphericityJLLM'].Fill(sphericity_jllm)
        Histos['sphericityJLLWithLoose'].Fill(sphericity_jllWithLoose)
        Histos['sphericityJLLMWithLoose'].Fill(sphericity_jllmWithLoose)
        Histos['aplanarityJLL'].Fill(aplanarity_jll)
        Histos['aplanarityJLLM'].Fill(aplanarity_jllm)
        Histos['aplanarityJLLWithLoose'].Fill(aplanarity_jllWithLoose)
        Histos['aplanarityJLLMWithLoose'].Fill(aplanarity_jllmWithLoose)
        
        
        if jetCSV[jetIdx] < 0.244:
            continue

        JetBtagL[ModeIdx] += 1

        HistosBtaggedL['ptjet'].Fill(jet.Pt())
        HistosBtaggedL['ptlep0'].Fill(lepton0.Pt())
        HistosBtaggedL['ptlep1'].Fill(lepton1.Pt())
        HistosBtaggedL['jetCSV'].Fill(jetCSV[jetIdx])
        HistosBtaggedL['ht'].Fill(Ht)
        HistosBtaggedL['htNoMet'].Fill(HtNoMet)
        HistosBtaggedL['msys'].Fill(system.M())
        HistosBtaggedL['ptsys'].Fill(system.Pt())
        HistosBtaggedL['mjll'].Fill(jll.M())
        HistosBtaggedL['ptjll'].Fill(jll.Pt())
        HistosBtaggedL['mjl0'].Fill(jl0.M())
        HistosBtaggedL['ptjl0'].Fill(jl0.Pt())
        HistosBtaggedL['mjl1'].Fill(jl1.M())
        HistosBtaggedL['ptjl1'].Fill(jl1.Pt())
        HistosBtaggedL['ptleps'].Fill(leptons.Pt())
        HistosBtaggedL['htleps'].Fill(lepton0.Pt() + lepton1.Pt())
        HistosBtaggedL['ptsys_ht'].Fill(system.Pt()/Ht)
        HistosBtaggedL['ptjet_ht'].Fill(jet.Pt()/Ht)
        HistosBtaggedL['ptlep0_ht'].Fill(lepton0.Pt()/Ht)
        HistosBtaggedL['ptlep1_ht'].Fill(lepton1.Pt()/Ht)
        HistosBtaggedL['ptleps_ht'].Fill(leptons.Pt()/Ht)
        HistosBtaggedL['htleps_ht'].Fill((lepton0.Pt()+lepton1.Pt())/Ht)
        HistosBtaggedL['NlooseJet15Central'].Fill(len(looseJet15CentralIdx))
        HistosBtaggedL['NlooseJet15Forward'].Fill(len(looseJet15ForwardIdx))
        HistosBtaggedL['NlooseJet20Central'].Fill(len(looseJet20CentralIdx))
        HistosBtaggedL['NlooseJet20Forward'].Fill(len(looseJet20ForwardIdx))
        HistosBtaggedL['NlooseJet25Central'].Fill(len(looseJet25CentralIdx))
        HistosBtaggedL['NlooseJet25Forward'].Fill(len(looseJet25ForwardIdx))
        HistosBtaggedL['NtightJetForward'].Fill(len(tightJetForwardIdx))
        HistosBtaggedL['NlooseJet15'].Fill(len(looseJet15Idx))
        HistosBtaggedL['NlooseJet20'].Fill(len(looseJet20Idx))
        HistosBtaggedL['NlooseJet25'].Fill(len(looseJet25Idx))
        HistosBtaggedL['NbtaggedlooseJet15'].Fill(len(btaggedLooseJet15Idx))
        HistosBtaggedL['NbtaggedlooseJet20'].Fill(len(btaggedLooseJet20Idx))
        HistosBtaggedL['NbtaggedlooseJet25'].Fill(len(btaggedLooseJet25Idx))
        HistosBtaggedL['unweightedEta_Avg'].Fill(unweightedEta_Avg)
        HistosBtaggedL['unweightedEta_Vecjll'].Fill(unweightedEta_Vecjll)
        HistosBtaggedL['unweightedEta_Vecsys'].Fill(unweightedEta_Vecsys)
        HistosBtaggedL['unweightedPhi_Avg'].Fill(unweightedPhi_Avg)
        HistosBtaggedL['unweightedPhi_Vecjll'].Fill(unweightedPhi_Vecjll)
        HistosBtaggedL['unweightedPhi_Vecsys'].Fill(unweightedPhi_Vecsys)
        HistosBtaggedL['avgEta'].Fill(abs(AvgEta))
        HistosBtaggedL['sysEta'].Fill(abs(system.Eta()))
        HistosBtaggedL['jllEta'].Fill(abs(jll.Eta()))
        HistosBtaggedL['dRleps'].Fill(abs(lepton0.DeltaR(lepton1)))
        HistosBtaggedL['dRjlmin'].Fill(min(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        HistosBtaggedL['dRjlmax'].Fill(max(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        HistosBtaggedL['dEtaleps'].Fill(abs(lepton0.Eta() - lepton1.Eta()))
        HistosBtaggedL['dEtajlmin'].Fill(min(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        HistosBtaggedL['dEtajlmax'].Fill(max(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        HistosBtaggedL['dPhileps'].Fill(abs(lepton0.DeltaPhi(lepton1)))
        HistosBtaggedL['dPhijlmin'].Fill(min(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        HistosBtaggedL['dPhijlmax'].Fill(max(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        HistosBtaggedL['met'].Fill(MET.Pt())
        HistosBtaggedL['flavourJet'].Fill(jetFlavour[jetIdx])
        HistosBtaggedL['etajet'].Fill(abs(jet.Eta()))
        HistosBtaggedL['etalep0'].Fill(abs(lepton0.Eta()))
        HistosBtaggedL['etalep1'].Fill(abs(lepton1.Eta()))
        HistosBtaggedL['phijet'].Fill(jet.Phi())
        HistosBtaggedL['philep0'].Fill(lepton0.Phi())
        HistosBtaggedL['philep1'].Fill(lepton1.Phi())
        HistosBtaggedL['phimet'].Fill(MET.Phi())
        HistosBtaggedL['sumeta2'].Fill(sumEta2)
        HistosBtaggedL['loosejetPt'].Fill(ptLooseJet)
        HistosBtaggedL['loosejetCSV'].Fill(csvLooseJet)
        HistosBtaggedL['loosejetFlavour'].Fill(flavourLooseJet)
        HistosBtaggedL['centralityJLL'].Fill(centrality_jll)
        HistosBtaggedL['centralityJLLM'].Fill(centrality_jllm)
        HistosBtaggedL['centralityJLLWithLoose'].Fill(centrality_jllWithLoose)
        HistosBtaggedL['centralityJLLMWithLoose'].Fill(centrality_jllmWithLoose)
        HistosBtaggedL['sphericityJLL'].Fill(sphericity_jll)
        HistosBtaggedL['sphericityJLLM'].Fill(sphericity_jllm)
        HistosBtaggedL['sphericityJLLWithLoose'].Fill(sphericity_jllWithLoose)
        HistosBtaggedL['sphericityJLLMWithLoose'].Fill(sphericity_jllmWithLoose)
        HistosBtaggedL['aplanarityJLL'].Fill(aplanarity_jll)
        HistosBtaggedL['aplanarityJLLM'].Fill(aplanarity_jllm)
        HistosBtaggedL['aplanarityJLLWithLoose'].Fill(aplanarity_jllWithLoose)
        HistosBtaggedL['aplanarityJLLMWithLoose'].Fill(aplanarity_jllmWithLoose)




        if jetCSV[jetIdx] < 0.679:
            continue

        JetBtagM[ModeIdx] += 1

        HistosBtaggedM['ptjet'].Fill(jet.Pt())
        HistosBtaggedM['ptlep0'].Fill(lepton0.Pt())
        HistosBtaggedM['ptlep1'].Fill(lepton1.Pt())
        HistosBtaggedM['jetCSV'].Fill(jetCSV[jetIdx])
        HistosBtaggedM['ht'].Fill(Ht)
        HistosBtaggedM['htNoMet'].Fill(HtNoMet)
        HistosBtaggedM['msys'].Fill(system.M())
        HistosBtaggedM['ptsys'].Fill(system.Pt())
        HistosBtaggedM['mjll'].Fill(jll.M())
        HistosBtaggedM['ptjll'].Fill(jll.Pt())
        HistosBtaggedM['mjl0'].Fill(jl0.M())
        HistosBtaggedM['ptjl0'].Fill(jl0.Pt())
        HistosBtaggedM['mjl1'].Fill(jl1.M())
        HistosBtaggedM['ptjl1'].Fill(jl1.Pt())
        HistosBtaggedM['ptleps'].Fill(leptons.Pt())
        HistosBtaggedM['htleps'].Fill(lepton0.Pt() + lepton1.Pt())
        HistosBtaggedM['ptsys_ht'].Fill(system.Pt()/Ht)
        HistosBtaggedM['ptjet_ht'].Fill(jet.Pt()/Ht)
        HistosBtaggedM['ptlep0_ht'].Fill(lepton0.Pt()/Ht)
        HistosBtaggedM['ptlep1_ht'].Fill(lepton1.Pt()/Ht)
        HistosBtaggedM['ptleps_ht'].Fill(leptons.Pt()/Ht)
        HistosBtaggedM['htleps_ht'].Fill((lepton0.Pt()+lepton1.Pt())/Ht)
        HistosBtaggedM['NlooseJet15Central'].Fill(len(looseJet15CentralIdx))
        HistosBtaggedM['NlooseJet15Forward'].Fill(len(looseJet15ForwardIdx))
        HistosBtaggedM['NlooseJet20Central'].Fill(len(looseJet20CentralIdx))
        HistosBtaggedM['NlooseJet20Forward'].Fill(len(looseJet20ForwardIdx))
        HistosBtaggedM['NlooseJet25Central'].Fill(len(looseJet25CentralIdx))
        HistosBtaggedM['NlooseJet25Forward'].Fill(len(looseJet25ForwardIdx))
        HistosBtaggedM['NtightJetForward'].Fill(len(tightJetForwardIdx))
        HistosBtaggedM['NlooseJet15'].Fill(len(looseJet15Idx))
        HistosBtaggedM['NlooseJet20'].Fill(len(looseJet20Idx))
        HistosBtaggedM['NlooseJet25'].Fill(len(looseJet25Idx))
        HistosBtaggedM['NbtaggedlooseJet15'].Fill(len(btaggedLooseJet15Idx))
        HistosBtaggedM['NbtaggedlooseJet20'].Fill(len(btaggedLooseJet20Idx))
        HistosBtaggedM['NbtaggedlooseJet25'].Fill(len(btaggedLooseJet25Idx))
        HistosBtaggedM['unweightedEta_Avg'].Fill(unweightedEta_Avg)
        HistosBtaggedM['unweightedEta_Vecjll'].Fill(unweightedEta_Vecjll)
        HistosBtaggedM['unweightedEta_Vecsys'].Fill(unweightedEta_Vecsys)
        HistosBtaggedM['unweightedPhi_Avg'].Fill(unweightedPhi_Avg)
        HistosBtaggedM['unweightedPhi_Vecjll'].Fill(unweightedPhi_Vecjll)
        HistosBtaggedM['unweightedPhi_Vecsys'].Fill(unweightedPhi_Vecsys)
        HistosBtaggedM['avgEta'].Fill(abs(AvgEta))
        HistosBtaggedM['sysEta'].Fill(abs(system.Eta()))
        HistosBtaggedM['jllEta'].Fill(abs(jll.Eta()))
        HistosBtaggedM['dRleps'].Fill(abs(lepton0.DeltaR(lepton1)))
        HistosBtaggedM['dRjlmin'].Fill(min(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        HistosBtaggedM['dRjlmax'].Fill(max(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        HistosBtaggedM['dEtaleps'].Fill(abs(lepton0.Eta() - lepton1.Eta()))
        HistosBtaggedM['dEtajlmin'].Fill(min(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        HistosBtaggedM['dEtajlmax'].Fill(max(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        HistosBtaggedM['dPhileps'].Fill(abs(lepton0.DeltaPhi(lepton1)))
        HistosBtaggedM['dPhijlmin'].Fill(min(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        HistosBtaggedM['dPhijlmax'].Fill(max(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        HistosBtaggedM['met'].Fill(MET.Pt())
        HistosBtaggedM['flavourJet'].Fill(jetFlavour[jetIdx])
        HistosBtaggedM['etajet'].Fill(abs(jet.Eta()))
        HistosBtaggedM['etalep0'].Fill(abs(lepton0.Eta()))
        HistosBtaggedM['etalep1'].Fill(abs(lepton1.Eta()))
        HistosBtaggedM['phijet'].Fill(jet.Phi())
        HistosBtaggedM['philep0'].Fill(lepton0.Phi())
        HistosBtaggedM['philep1'].Fill(lepton1.Phi())
        HistosBtaggedM['phimet'].Fill(MET.Phi())
        HistosBtaggedM['sumeta2'].Fill(sumEta2)
        HistosBtaggedM['loosejetPt'].Fill(ptLooseJet)
        HistosBtaggedM['loosejetCSV'].Fill(csvLooseJet)
        HistosBtaggedM['loosejetFlavour'].Fill(flavourLooseJet)
        HistosBtaggedM['centralityJLL'].Fill(centrality_jll)
        HistosBtaggedM['centralityJLLM'].Fill(centrality_jllm)
        HistosBtaggedM['centralityJLLWithLoose'].Fill(centrality_jllWithLoose)
        HistosBtaggedM['centralityJLLMWithLoose'].Fill(centrality_jllmWithLoose)
        HistosBtaggedM['sphericityJLL'].Fill(sphericity_jll)
        HistosBtaggedM['sphericityJLLM'].Fill(sphericity_jllm)
        HistosBtaggedM['sphericityJLLWithLoose'].Fill(sphericity_jllWithLoose)
        HistosBtaggedM['sphericityJLLMWithLoose'].Fill(sphericity_jllmWithLoose)
        HistosBtaggedM['aplanarityJLL'].Fill(aplanarity_jll)
        HistosBtaggedM['aplanarityJLLM'].Fill(aplanarity_jllm)
        HistosBtaggedM['aplanarityJLLWithLoose'].Fill(aplanarity_jllWithLoose)
        HistosBtaggedM['aplanarityJLLMWithLoose'].Fill(aplanarity_jllmWithLoose)



        if jetCSV[jetIdx] < 0.898:
            continue

        JetBtagT[ModeIdx] += 1

        HistosBtaggedT['ptjet'].Fill(jet.Pt())
        HistosBtaggedT['ptlep0'].Fill(lepton0.Pt())
        HistosBtaggedT['ptlep1'].Fill(lepton1.Pt())
        HistosBtaggedT['jetCSV'].Fill(jetCSV[jetIdx])
        HistosBtaggedT['ht'].Fill(Ht)
        HistosBtaggedT['htNoMet'].Fill(HtNoMet)
        HistosBtaggedT['msys'].Fill(system.M())
        HistosBtaggedT['ptsys'].Fill(system.Pt())
        HistosBtaggedT['mjll'].Fill(jll.M())
        HistosBtaggedT['ptjll'].Fill(jll.Pt())
        HistosBtaggedT['mjl0'].Fill(jl0.M())
        HistosBtaggedT['ptjl0'].Fill(jl0.Pt())
        HistosBtaggedT['mjl1'].Fill(jl1.M())
        HistosBtaggedT['ptjl1'].Fill(jl1.Pt())
        HistosBtaggedT['ptleps'].Fill(leptons.Pt())
        HistosBtaggedT['htleps'].Fill(lepton0.Pt() + lepton1.Pt())
        HistosBtaggedT['ptsys_ht'].Fill(system.Pt()/Ht)
        HistosBtaggedT['ptjet_ht'].Fill(jet.Pt()/Ht)
        HistosBtaggedT['ptlep0_ht'].Fill(lepton0.Pt()/Ht)
        HistosBtaggedT['ptlep1_ht'].Fill(lepton1.Pt()/Ht)
        HistosBtaggedT['ptleps_ht'].Fill(leptons.Pt()/Ht)
        HistosBtaggedT['htleps_ht'].Fill((lepton0.Pt()+lepton1.Pt())/Ht)
        HistosBtaggedT['NlooseJet15Central'].Fill(len(looseJet15CentralIdx))
        HistosBtaggedT['NlooseJet15Forward'].Fill(len(looseJet15ForwardIdx))
        HistosBtaggedT['NlooseJet20Central'].Fill(len(looseJet20CentralIdx))
        HistosBtaggedT['NlooseJet20Forward'].Fill(len(looseJet20ForwardIdx))
        HistosBtaggedT['NlooseJet25Central'].Fill(len(looseJet25CentralIdx))
        HistosBtaggedT['NlooseJet25Forward'].Fill(len(looseJet25ForwardIdx))
        HistosBtaggedT['NtightJetForward'].Fill(len(tightJetForwardIdx))
        HistosBtaggedT['NlooseJet15'].Fill(len(looseJet15Idx))
        HistosBtaggedT['NlooseJet20'].Fill(len(looseJet20Idx))
        HistosBtaggedT['NlooseJet25'].Fill(len(looseJet25Idx))
        HistosBtaggedT['NbtaggedlooseJet15'].Fill(len(btaggedLooseJet15Idx))
        HistosBtaggedT['NbtaggedlooseJet20'].Fill(len(btaggedLooseJet20Idx))
        HistosBtaggedT['NbtaggedlooseJet25'].Fill(len(btaggedLooseJet25Idx))
        HistosBtaggedT['unweightedEta_Avg'].Fill(unweightedEta_Avg)
        HistosBtaggedT['unweightedEta_Vecjll'].Fill(unweightedEta_Vecjll)
        HistosBtaggedT['unweightedEta_Vecsys'].Fill(unweightedEta_Vecsys)
        HistosBtaggedT['unweightedPhi_Avg'].Fill(unweightedPhi_Avg)
        HistosBtaggedT['unweightedPhi_Vecjll'].Fill(unweightedPhi_Vecjll)
        HistosBtaggedT['unweightedPhi_Vecsys'].Fill(unweightedPhi_Vecsys)
        HistosBtaggedT['avgEta'].Fill(abs(AvgEta))
        HistosBtaggedT['sysEta'].Fill(abs(system.Eta()))
        HistosBtaggedT['jllEta'].Fill(abs(jll.Eta()))
        HistosBtaggedT['dRleps'].Fill(abs(lepton0.DeltaR(lepton1)))
        HistosBtaggedT['dRjlmin'].Fill(min(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        HistosBtaggedT['dRjlmax'].Fill(max(abs(jet.DeltaR(lepton0)),abs(jet.DeltaR(lepton1))))
        HistosBtaggedT['dEtaleps'].Fill(abs(lepton0.Eta() - lepton1.Eta()))
        HistosBtaggedT['dEtajlmin'].Fill(min(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        HistosBtaggedT['dEtajlmax'].Fill(max(abs(jet.Eta()-lepton0.Eta()),abs(jet.Eta()-lepton1.Eta())))
        HistosBtaggedT['dPhileps'].Fill(abs(lepton0.DeltaPhi(lepton1)))
        HistosBtaggedT['dPhijlmin'].Fill(min(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        HistosBtaggedT['dPhijlmax'].Fill(max(abs(jet.DeltaPhi(lepton0)),abs(jet.DeltaPhi(lepton1))))
        HistosBtaggedT['met'].Fill(MET.Pt())
        HistosBtaggedT['flavourJet'].Fill(jetFlavour[jetIdx])
        HistosBtaggedT['etajet'].Fill(abs(jet.Eta()))
        HistosBtaggedT['etalep0'].Fill(abs(lepton0.Eta()))
        HistosBtaggedT['etalep1'].Fill(abs(lepton1.Eta()))
        HistosBtaggedT['phijet'].Fill(jet.Phi())
        HistosBtaggedT['philep0'].Fill(lepton0.Phi())
        HistosBtaggedT['philep1'].Fill(lepton1.Phi())
        HistosBtaggedT['phimet'].Fill(MET.Phi())
        HistosBtaggedT['sumeta2'].Fill(sumEta2)
        HistosBtaggedT['loosejetPt'].Fill(ptLooseJet)
        HistosBtaggedT['loosejetCSV'].Fill(csvLooseJet)
        HistosBtaggedT['loosejetFlavour'].Fill(flavourLooseJet)
        HistosBtaggedT['centralityJLL'].Fill(centrality_jll)
        HistosBtaggedT['centralityJLLM'].Fill(centrality_jllm)
        HistosBtaggedT['centralityJLLWithLoose'].Fill(centrality_jllWithLoose)
        HistosBtaggedT['centralityJLLMWithLoose'].Fill(centrality_jllmWithLoose)
        HistosBtaggedT['sphericityJLL'].Fill(sphericity_jll)
        HistosBtaggedT['sphericityJLLM'].Fill(sphericity_jllm)
        HistosBtaggedT['sphericityJLLWithLoose'].Fill(sphericity_jllWithLoose)
        HistosBtaggedT['sphericityJLLMWithLoose'].Fill(sphericity_jllmWithLoose)
        HistosBtaggedT['aplanarityJLL'].Fill(aplanarity_jll)
        HistosBtaggedT['aplanarityJLLM'].Fill(aplanarity_jllm)
        HistosBtaggedT['aplanarityJLLWithLoose'].Fill(aplanarity_jllWithLoose)
        HistosBtaggedT['aplanarityJLLMWithLoose'].Fill(aplanarity_jllmWithLoose)




    for i in range(3):
        print
        print '----------------------------'
        print Channel[i] + ' Channel'
        print 'Lepton Selection '+ str(LepSelection[i])
        print 'Lepton Veto      '+ str(LepVeto[i])
        print 'Mll Cut          '+ str(mllCut[i])
        print 'Met Cut          '+ str(MetCut[i])
        print 'One Jet          '+ str(OneJet[i])
        print 'Btagged Loose    '+ str(JetBtagL[i])
        print 'Btagged Medium   '+ str(JetBtagM[i])
        print 'Btagged Tight    '+ str(JetBtagT[i])


    print '----------------------------'

    print emuStart
    print mumuStart
    print eeStart

    outputHistos.cd()
    for plot in plotInfo:
        name = fileName.split('_')[-1][:-5] + "_" + plot[0]
        Histos[plot[0]].Write(name)
        name = fileName.split('_')[-1][:-5] + "_BtaggedL_" + plot[0]
        HistosBtaggedL[plot[0]].Write(name)
        name = fileName.split('_')[-1][:-5] + "_BtaggedM_" + plot[0]
        HistosBtaggedM[plot[0]].Write(name)
        name = fileName.split('_')[-1][:-5] + "_BtaggedT_" + plot[0]
        HistosBtaggedT[plot[0]].Write(name)
    
