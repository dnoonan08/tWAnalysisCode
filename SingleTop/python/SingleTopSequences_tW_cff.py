import FWCore.ParameterSet.Config as cms

from TopQuarkAnalysis.SingleTop.SelectionCuts_tW_Skim_cff import *

from PhysicsTools.HepMCCandAlgos.flavorHistoryPaths_cfi import *

from PhysicsTools.PatAlgos.patSequences_cff import *

from TopQuarkAnalysis.SingleTop.simpleEleIdSequence_cff import *


#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleTopJetsPF
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTuplePatMETsPF
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleElectrons
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleMuons
#from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTuplesSkim

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleTopJetsPF
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTuplePatMETsPF
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTuplePatType1METsPF
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleElectrons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleMuons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleGenParticles
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTuplesSkim
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTuplesSkimData

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleAllElectrons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleAllMuons


# from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleQCDElectrons
# from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleQCDMuons

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleAllJets

from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleLooseElectrons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleLooseElectronsEle
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleLooseMuons
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleVertices
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleVertices2
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import nTupleZVetoElectrons


#if isdata: process.looseLeptonSequence.remove(process.muonMatchLoose)


# require scraping filter
scrapingVeto = cms.EDFilter("FilterOutScraping",
                            applyfilter=cms.untracked.bool(True),
                            debugOn=cms.untracked.bool(False),
                            numtrack=cms.untracked.uint32(10),
                            thresh=cms.untracked.double(0.2)
                            )

scrapingFilter=cms.EDFilter("FilterOutScraping" ,
                            applyfilter = cms.untracked.bool( True ),
                            debugOn = cms.untracked.bool( False ) ,
                            numtrack = cms.untracked.uint32( 10 ) ,
                            thresh = cms.untracked.double( 0.25 )
                            )


# HB + HE noise filtering
from CommonTools.RecoAlgos.HBHENoiseFilter_cfi import HBHENoiseFilter

HBHENoiseFilter.minIsolatedNoiseSumE = cms.double(999999.)
HBHENoiseFilter.minNumIsolatedNoiseChannels = cms.int32(999999)
HBHENoiseFilter.minIsolatedNoiseSumEt = cms.double(999999.)

from CommonTools.RecoAlgos.HBHENoiseFilterResultProducer_cfi import HBHENoiseFilterResultProducer
HBHENoiseFilterResultProducer.minRatio = cms.double(-999)
HBHENoiseFilterResultProducer.maxRatio = cms.double(999)
HBHENoiseFilterResultProducer.minHPDHits = cms.int32(17)
HBHENoiseFilterResultProducer.minRBXHits = cms.int32(999)
HBHENoiseFilterResultProducer.minHPDNoOtherHits = cms.int32(10)
HBHENoiseFilterResultProducer.minZeros = cms.int32(10)
HBHENoiseFilterResultProducer.minHighEHitTime = cms.double(-9999.0)
HBHENoiseFilterResultProducer.maxHighEHitTime = cms.double(9999.0)
HBHENoiseFilterResultProducer.maxRBXEMF = cms.double(-999.0)
HBHENoiseFilterResultProducer.minNumIsolatedNoiseChannels = cms.int32(999999)
HBHENoiseFilterResultProducer.minIsolatedNoiseSumE = cms.double(999999.)
HBHENoiseFilterResultProducer.minIsolatedNoiseSumEt = cms.double(999999.)
HBHENoiseFilterResultProducer.useTS4TS5 = cms.bool(True)



nTuplePatMETsPF.src = cms.InputTag('patMETs')

from RecoEgamma.ElectronIdentification.electronIdSequence_cff import *
from EgammaAnalysis.ElectronTools.electronIdMVAProducer_cfi import *
#from EGamma.EGammaAnalysisTools.electronIdMVAProducer_cfi import *

mvaID = cms.Sequence(  mvaTrigV0 + mvaNonTrigV0 )

patElectronIDs = cms.Sequence(simpleEleIdSequence +
                              eIdSequence +
                              mvaID
                              )


electronIDSources = cms.PSet(
    mvaTrigV0    = cms.InputTag("mvaTrigV0"),
    mvaNonTrigV0    = cms.InputTag("mvaNonTrigV0"),
#    simpleEleId60cIso = cms.InputTag("simpleEleId60cIso"),
    simpleEleId70cIso = cms.InputTag("simpleEleId70cIso"),
    simpleEleId80cIso = cms.InputTag("simpleEleId80cIso"),
    simpleEleId90cIso = cms.InputTag("simpleEleId90cIso"),
    simpleEleId95cIso = cms.InputTag("simpleEleId95cIso"),
#    eidRobustLoose= cms.InputTag("eidRobustLoose"),
#    eidRobustTight= cms.InputTag("eidRobustTight"),
#    eidRobustHighEnergy= cms.InputTag("eidRobustHighEnergy")
    )

#cFlavorHistory

patElectrons.addElectronID = cms.bool(True)
patElectrons.electronIDSources = electronIDSources


#makeNewPatElectrons = cms.Sequence(patElectronIDs * patElectronIsolation * patElectrons)

patElectrons.usePV = cms.bool(False)
patMuons.usePV = cms.bool(False)


#In those paths the customized collections are produced

basePath = cms.Sequence(
       preselectedMETs +
          looseMuons +
          PVFilterProducer +
          looseElectrons +
          looseElectronsEle +
       #   zVetoElectrons +
          topJetsPF +
          UnclusteredMETPF +
       #   UnclusteredType1METPF +
          genJetsPF +
          NVertices +
#          tightMuonsZeroIso +
#          tightElectronsZeroIso +
          tightMuons +
          tightElectrons +
      #    tightZeroIsoRhoCorrectedRelIso+
       #  SingleTopMCProducer +
          PDFInfo
          )

basePathData = cms.Sequence(
       preselectedMETs +
       looseMuons +
       PVFilterProducer +
       looseElectrons +
       looseElectronsEle +
       #   zVetoElectrons +
       topJetsPF +
       UnclusteredMETPF +
       #   UnclusteredType1METPF +
       #          NVertices +
       #          tightMuonsZeroIso +
       #          tightElectronsZeroIso +
       tightMuons +
       tightElectrons 
       #  SingleTopMCProducer +
       )

#Flavor history tools sequence
flavorHistorySequence = cms.Sequence(
        cFlavorHistoryProducer *
            bFlavorHistoryProducer
            )

#Selection step: require 1 high pt muon/electron
preselection = cms.Sequence(
    PVFilter +
    countLeptons
    )

#Selection step: require 1 high pt muon/electron
preselectionData = cms.Sequence(
    #    hltFilter +
    PVFilter +
    HBHENoiseFilter +
#    scrapingVeto +
    scrapingFilter +
    countLeptons
    )

#Selection step: require 1 high pt muon/electron
#process.preselection(
#    hltFilter +
#    PVFilter +
#    countLeptons
#    )

#Ntuple production sequences:

#!!!Work in progress!!!#
