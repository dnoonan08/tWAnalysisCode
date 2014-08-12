import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.SingleTop.SingleTopProducers_cff import *
from TopQuarkAnalysis.SingleTop.SingleTopSelectors_cff import *

#### Set the cuts values ####

#N.B.:
#We set loose values for the cuts in order to allow for control samples studies.
#We commented the lines necessary to set a tighter, more standard object selection.

#Loose lepton selection criteria

#No isolation requirement
muLooseCut = cms.string("isGlobalMuon & pt > 10 & abs(eta) < 2.5")
eleLooseCut = cms.string("et > 10 & abs(eta) < 2.5")

#Tight leptons selection criteria
#No isolation or electronID requirement
eleTightCut = cms.string("pt>10  && abs(eta)<2.5") # && passConversionVeto")

muTightCut = cms.string("pt > 10 & (isGlobalMuon || isTrackerMuon) && isPFMuon & abs(eta) < 2.5")


#Isolation cones definitions
#coneOpening = cms.double(0.4)
#defaultIsolationCut = cms.double(0.2)

#eJet definition
jetLooseCut = cms.string("pt()> 5 & abs(eta())<5.")
# & numberOfDaughters()>1 & ((abs(eta())>=2.4) || ( chargedHadronEnergyFraction() > 0 & chargedMultiplicity()>0 & chargedEmEnergyFraction()<0.99)) & neutralEmEnergyFraction() < 0.99 & neutralHadronEnergyFraction() < 0.99 "  )



#Requirement on the number of leptons in the event
#Loose: at least 1 tight lepton
minTightLeptons = cms.untracked.int32(2)
maxTightLeptons = cms.untracked.int32(99)

#Number of leptons that survive loose cuts and do not overlap with tight leptons
#Cannot apply as long as there is the extra z-vetoed electron
#Loose: up to 1 extra loose lepton
minLooseLeptons = cms.untracked.int32(0)
maxLooseLeptons = cms.untracked.int32(99)

### MC details that do not influence the selection  ###

#Check to see if it is signal channel ( MC only )
isMCSingleTopTChannel = cms.untracked.bool(False)

#definition: Leptons Loose
looseElectrons.cut =  eleLooseCut
looseMuons.cut = muLooseCut

#definition: z-Veto electrons
#zVetoElectrons.cut = eleZVetoCut 

#definition: Leptons Tight
tightElectrons.cut =  eleTightCut
tightMuons.cut = muTightCut

tightElectronsZeroIso.cut =  eleTightCut
tightMuonsZeroIso.cut = muTightCut

#definition: Jets Loose
topJetsPF.cut = jetLooseCut

countLeptons.minNumberLoose = minLooseLeptons
countLeptons.maxNumberLoose = maxLooseLeptons

countLeptons.minNumberTight = minTightLeptons
countLeptons.maxNumberTight = maxTightLeptons

countLeptons.doQCD = False


countLeptons.qcdMuons = cms.InputTag("tightMuons")
countLeptons.qcdElectrons = cms.InputTag("tightElectrons")


#countLeptonsQCD.minNumber = minTightLeptons
#countLeptonsQCD.maxNumber = maxTightLeptons

