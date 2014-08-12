import FWCore.ParameterSet.Config as cms

##### WMuNu group standard selector ####

#from ElectroWeakAnalysis.WMuNu.WMuNuSelection_cff import *


### HLT filter ###
import HLTrigger.HLTfilters.hltHighLevel_cfi
hltFilter = HLTrigger.HLTfilters.hltHighLevel_cfi.hltHighLevel.clone()
hltFilter.TriggerResultsTag = cms.InputTag("TriggerResults","","REDIGI")
hltFilter.HLTPaths = ['HLT_Mu9']#,'HLT_Ele15_LW_L1R']


hltFilterEle = cms.EDFilter("HLTSummaryFilter",
                            summary = cms.InputTag("hltTriggerSummaryAOD","","HLT"),
                            member = cms.InputTag("hltL1NonIsoHLTNonIsoSinglePhotonEt10HcalIsolFilter","","HLT"),
                            cut = cms.string("pt> 20"),
                            minN = cms.int32(1),
                                 )

#####Primary vertex filter
PVFilter = cms.EDFilter(
    'SingleTopVertexFilter',
    src = cms.InputTag("goodOfflinePrimaryVertices"),
    cut = cms.string('!isFake & position().Rho() < 2.0 & abs(z) < 24 & ndof >= 4. '),
    filter = cms.bool(False)
    )

PVFilterProducer = cms.EDFilter(
    'VertexSelector',
    src = cms.InputTag("offlinePrimaryVertices"),
    cut = cms.string('!isFake & position().Rho() < 2.0 & abs(z) < 24 & ndof >= 4.'),
    filter = cms.bool(False)
    )

######### Part of selection: Particle counting ##########
countElectrons = cms.EDFilter("PATCandViewCountFilter",
                              src = cms.InputTag("tightElectrons"),
                              minNumber = cms.uint32(1),
                              maxNumber = cms.uint32(9999),
                              filter = cms.bool(True)
                              )

countMuons = cms.EDFilter("PATCandViewCountFilter",
                          src = cms.InputTag("tightMuons"),
                          minNumber = cms.uint32(1),
                          maxNumber = cms.uint32(9999),
                          filter = cms.bool(True)
                          )

countLeptonsNoOverlap = cms.EDFilter("CandOrCounterNoOverlap",
                            
                            src1 = cms.InputTag("tightMuons"),
                            src2 = cms.InputTag("tightElectrons"),

                            srcOverlap1 = cms.InputTag("looseMuons"),
                            srcOverlap2 = cms.InputTag("looseElectrons"),
                            
                            minNumberTight = cms.untracked.int32(1),
                            maxNumberTight = cms.untracked.int32(9999),

                            minNumberLoose = cms.untracked.int32(1),
                            maxNumberLoose = cms.untracked.int32(9999),
                            )


countLeptons = cms.EDFilter("SingleTopLeptonCounter",
                            
                            looseMuons = cms.InputTag("looseMuons"),
                            looseElectrons = cms.InputTag("looseElectrons"),

                            tightMuons = cms.InputTag("tightMuons"),
                            tightElectrons = cms.InputTag("tightElectrons"),

                            qcdMuons = cms.InputTag("tightMuonsZeroIso"),
                            qcdElectrons = cms.InputTag("tightElectronsZeroIso"),
                            
                            minNumberTight = cms.untracked.int32(1),
                            maxNumberTight = cms.untracked.int32(1),

                            minNumberLoose = cms.untracked.int32(0),
                            maxNumberLoose = cms.untracked.int32(0),
                            
                            minNumberQCD = cms.untracked.int32(1),
                            maxNumberQCD = cms.untracked.int32(1),

                            rejectOverlap = cms.untracked.bool(True),
                            doQCD = cms.untracked.bool(True),

                            )
