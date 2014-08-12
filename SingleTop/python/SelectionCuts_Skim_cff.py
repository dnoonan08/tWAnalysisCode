import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.SingleTop.SingleTopProducers_cff import *
from TopQuarkAnalysis.SingleTop.SingleTopSelectors_cff import *

#### Set the cuts values ####

#N.B.:
#We set loose values for the cuts in order to allow for control samples studies.
#We commented the lines necessary to set a tighter, more standard object selection.

#Loose lepton selection criteria

#No isolation requirement
#muLooseCut = cms.string("isGlobalMuon & pt > 10 & abs(eta) < 2.5")#RelIso < 0.2
#eleLooseCut = cms.string("et > 15 & abs(eta) < 2.5")#RelIso < 0.2

#With isolation requirements
muLooseCut = cms.string("isGlobalMuon & pt > 10 & abs(eta) < 2.5 & (isolationR03.sumPt + isolationR03.emEt + isolationR03.hadEt)/pt < 0.2") 
eleLooseCut = cms.string("et > 15 & abs(eta) < 2.5 & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et < 0.2 ")

eleZVetoCut = cms.string("et > 20 &  (abs(superCluster.eta)> 1.5660 || abs(superCluster.eta)<1.4442) & eta < 2.5 & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et < 0.1 & (electronID('simpleEleId95cIso')==1 || electronID('simpleEleId70cIso')==3 ||  electronID('simpleEleId70cIso')==5 ||  electronID('simpleEleId70cIso')==7)")
# Require ID + or of all possible combinations

#Tight leptons selection criteria
#No isolation or electronID requirement
eleTightCut = cms.string("et>30  && abs(eta)<2.5  & (gsfTrack().trackerExpectedHitsInner.numberOfHits == 0) & dB < 0.02 & ( abs(superCluster.eta)> 1.5660 || abs(superCluster.eta)<1.4442)")

muTightCut = cms.string("pt > 20 & isGlobalMuon && isTrackerMuon & abs(eta) < 2.1 && numberOfMatches() > 1  && muonID('GlobalMuonPromptTight') > 0 & dB < 0.02 & innerTrack.numberOfValidHits > 10 && innerTrack.hitPattern.pixelLayersWithMeasurement() >= 1 ")

#Jet definition
jetLooseCut = cms.string("numberOfDaughters()>1 & pt()> 20 && abs(eta())<5 & ((abs(eta())>2.4) || ( chargedHadronEnergyFraction() > 0 & chargedMultiplicity()>0 & neutralEmEnergyFraction() < 0.99 & neutralHadronEnergyFraction() < 0.99 & chargedEmEnergyFraction()<0.99))")

#Requirement on the number of leptons in the event
#Loose: at least 1 tight lepton
minTightLeptons = cms.int32(1)
maxTightLeptons = cms.int32(99)

#Number of leptons that survive loose cuts and do not overlap with tight leptons
#Cannot apply as long as there is the extra z-vetoed electron
#Loose: up to 1 extra loose lepton
minLooseLeptons = cms.int32(0)
maxLooseLeptons = cms.int32(99)


#Tighter cuts:

#With isolation and electronID requirements
#eleTightCut = cms.string("et>30  && abs(eta)<2.5  & (gsfTrack().trackerExpectedHitsInner.numberOfHits == 0) & (dr03TkSumPt + dr03EcalRecHitSumEt + dr03HcalTowerSumEt)/et < 0.1  & dB < 0.02 & ( abs(superCluster.eta)> 1.5660 || abs(superCluster.eta)<1.4442) & (electronID('simpleEleId70cIso')==5 || electronID('simpleEleId70cIso')==7)")#RelIso < 0.1
#Legenda for eleId : 0 fail, 1 ID only, 2 iso Only, 3 ID iso only, 4 conv rej, 5 conv rej and ID, 6 conv rej and iso, 7 all 

#muTightCut = cms.string("pt > 20 & isGlobalMuon && isTrackerMuon & abs(eta) < 2.1 && numberOfMatches() > 1  && muonID('GlobalMuonPromptTight') > 0 & (isolationR03.sumPt + isolationR03.emEt + isolationR03.hadEt)/pt < 0.05 & dB < 0.02 & innerTrack.numberOfValidHits > 10 && innerTrack()->hitPattern().pixelLayersWithMeasurement() >= 1 ")#RelIso < 0.05 

#Tight: exactly 1 tight lepton 
#maxTightLeptons = cms.int32(1)

#Tight: no extra loose leptons
#minLooseLeptons = cms.int32(0)
#maxLooseLeptons = cms.int32(0)




#Detailed request for number of leptons ( not used in standard analysis )
#minMuons = cms.uint32(1)
#maxMuons = cms.uint32(1)

#minElectrons = cms.uint32(1)
#maxElectrons = cms.uint32(1)

### MC details that do not influence the selection  ###

#Check to see if it is signal channel ( MC only )
isMCSingleTopTChannel = cms.untracked.bool(False)

#definition: Leptons Loose
looseElectrons.cut =  eleLooseCut
looseMuons.cut = muLooseCut

#definition: z-Veto electrons
zVetoElectrons.cut = eleZVetoCut 

#definition: Leptons Tight
tightElectrons.cut =  eleTightCut
tightMuons.cut = muTightCut

#definition: Jets Loose
topJetsPF.cut = jetLooseCut

countLeptons.minNumberLoose = minLooseLeptons
countLeptons.maxNumberLoose = maxLooseLeptons

countLeptons.minNumberTight = minTightLeptons
countLeptons.maxNumberTight = maxTightLeptons
