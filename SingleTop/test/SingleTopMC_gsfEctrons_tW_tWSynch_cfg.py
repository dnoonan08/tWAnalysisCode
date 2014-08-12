import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 100

#from PhysicsTools.PatAlgos.tools.cmsswVersionTools import run36xOn35xInput


# conditions ------------------------------------------------------------------

print "test "

#process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data

ChannelName = "tWSynch"

process.GlobalTag.globaltag = cms.string('START53_V7::All')

#from Configuration.PyReleaseValidation.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['startup']
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_tW_cff") 
##############process.load("SelectionCuts_tW_Skim_cff")################<----------



process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('dummy.root'),
                               outputCommands = cms.untracked.vstring(""),
                               )


# Get a list of good primary vertices, in 42x, these are DAF vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = pvSelector.clone( minNdof = cms.double(4.0), maxZ = cms.double(24.0), maxRho = cms.double(2.)  ),
    src=cms.InputTag('offlinePrimaryVertices')
    )



from RecoJets.JetProducers.kt4PFJets_cfi import *

process.kt6PFJetsForIsolation = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation.Rho_EtaMax = cms.double(2.5)


# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)

#postfix = "SingleTop"
postfix = ""

# Configure PAT to use PF2PAT instead of AOD sources
from PhysicsTools.PatAlgos.tools.pfTools import *
#Postfix = "SingleTop"
Postfix = ""

runOnMC = True
jetAlgoName = "AK5"
print "test2.2"
usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('goodOfflinePrimaryVertices'),  typeIMetCorrections=True)
#usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('offlinePrimaryVertices'),  typeIMetCorrections=True)
#          jetCorrections=('AK5PFchs', jetCorrections)

process.pfPileUp.Enable = True
process.load("CMGTools.External.pujetidsequence_cff")


#Use gsfElectrons:
process.patElectrons.useParticleFlow = False
process.eleIsoSequence = setupPFElectronIso(process, 'gsfElectrons', "PFIso"+postfix)
adaptPFIsoElectrons( process, process.patElectrons, "PFIso"+postfix)
getattr(process,'patDefaultSequence'+postfix).replace( getattr(process,"patElectrons"+postfix),
                                                       process.pfParticleSelectionSequence +
                                                       process.eleIsoSequence +
                                                       getattr(process,"patElectrons"+postfix)
                                                       )
#getattr(process,"pfNoTau"+postfix).enable = False


# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)

#Muons

#Electrons
process.pfIsolatedElectrons.isolationValueMapsCharged = cms.VInputTag( cms.InputTag("elPFIsoValueCharged03PFId"),    )
process.pfIsolatedElectrons.isolationValueMapsNeutral = cms.VInputTag( cms.InputTag("elPFIsoValueNeutral03PFId"),  cms.InputTag("elPFIsoValueGamma03PFId")  )
process.pfIsolatedElectrons.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFId")

# NOT for gsfElectrons
#process.patElectrons.isolationValues = cms.PSet(
#    pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFId"),
#    pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFId"),
#    pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFId"),
#    pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFId"),
#    pfPhotons = cms.InputTag("elPFIsoValueGamma03PFId")
#    )

print " test 0 " 
process.pfIsolatedMuons.combinedIsolationCut = cms.double(0.2)
process.pfIsolatedElectrons.combinedIsolationCut = cms.double(0.2)

process.pfIsolatedMuons.isolationCut = cms.double(0.2)
process.pfIsolatedElectrons.isolationCut = cms.double(0.2)
#applyPostfix(process,"pfIsolatedElectrons",postfix).combinedIsolationCut = cms.double(0.2)#

#applyPostfix(process,"pfIsolatedMuons",postfix).isolationCut = cms.double(0.2)
#applyPostfix(process,"pfIsolatedElectrons",postfix).isolationCut = cms.double(0.2)

#
process.patseq = cms.Sequence(
#    process.patElectronIDs +
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    process.kt6PFJetsForIsolation *
    getattr(process,"patPF2PATSequence"+postfix) #*
#    process.producePatPFMETCorrections
#    getattr(process,"patPF2PATSequence"+postfixQCD) 
    )


print " test 1 " 
process.pfIsolatedMuonsZeroIso = process.pfIsolatedMuons.clone(combinedIsolationCut =  cms.double(float("inf")),
                                                               isolationCut =  cms.double(float("inf")),
                                                               )

process.patMuonsZeroIso = process.patMuons.clone(pfMuonSource = cms.InputTag("pfIsolatedMuonsZeroIso"))#, genParticleMatch = cms.InputTag("muonMatchZeroIso"))
# use pf isolation, but do not change matching
tmp = process.muonMatch.src
adaptPFIsoMuons(process, process.patMuonsZeroIso, "")
process.patMuonsZeroIso.pfMuonSource = cms.InputTag("pfIsolatedMuons")
process.muonMatch.src = tmp
process.muonMatchZeroIso = process.muonMatch.clone(src = cms.InputTag("pfIsolatedMuonsZeroIso"))

process.pfIsolatedElectronsZeroIso = process.pfIsolatedElectrons.clone(combinedIsolationCut = cms.double(float("inf")),
                                                                       isolationCut =  cms.double(float("inf")),
                                                                       )
process.patElectronsZeroIso = process.patElectrons.clone(pfElectronSource = cms.InputTag("pfIsolatedElectronsZeroIso"))
#adaptPFElectrons(process, process.patElectronsZeroIso, "")


print " test 2 " 

process.pathPreselection = cms.Path(
        process.patseq + process.puJetIdSqeuence + process.puJetIdSqeuenceChs
        #+  process.producePatPFMETCorrections
        )


process.ZeroIsoLeptonSequence = cms.Path(
         process.pfIsolatedMuonsZeroIso +
#         process.muonMatchZeroIso +
         process.patMuonsZeroIso +
         process.pfIsolatedElectronsZeroIso +
         process.patElectronsZeroIso
         )

print " test 3 " 


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
                                "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F4FEBE8F-3BEA-E111-8373-003048FF9AA6.root", #53X version
#                                "/store/mc/Summer12/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S7_START52_V9-v1/0000/FAD2E60D-868E-E111-AEFE-001BFCDBD11E.root", # 52X version
),
#eventsToProcess = cms.untracked.VEventRange('1:65161675-1:65161677'),#1:95606867-1:95606869')
duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

#process.basePath += process.tightMuonsTest

process.baseLeptonSequence = cms.Path(
    process.basePath
    )
#
process.topJetsPF.removeOverlap = cms.untracked.bool(False)

process.selection = cms.Path (
    process.preselection + 
    process.nTuplesSkim
    )

print " test 4 " 


from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import saveNTuplesSkimLoose
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import saveNTuplesSkimMu
    
savePatTupleSkimLoose = cms.untracked.vstring(
    'drop *',

    'keep patMuons_selectedPatMuons_*_*',
    'keep patElectrons_selectedPatElectrons_*_*',
    'keep patJets_selectedPatJets_*_*',
    'keep patMETs_patMETs_*_*',
    'keep *_patPFMet_*_*',
    'keep *_patType1CorrectedPFMet_*_*',
    'keep *_PVFilterProducer_*_*',

    'keep *_kt6PFJetsForIsolation_rho_*',

    'keep patJets_topJetsPF_*_*',
    'keep patMuons_looseMuons_*_*',
    'keep *_looseElectrons_*_*',
    'keep patMuons_tightMuons_*_*',
    'keep patMuons_tightMuonsTest_*_*',
    'keep *_tightElectrons_*_*',

    'keep *_PDFInfo_*_*',

    'keep *_patElectronsZeroIso_*_*',
    'keep *_patMuonsZeroIso_*_*',
    'keep *_kt6PFJetsCentral_*_*',
    'keep *_PVFilterProducer_*_*',
    
    'keep *_cFlavorHistoryProducer_*_*',
    'keep *_bFlavorHistoryProducer_*_*',
    "keep *_puJetId_*_*", # input variables
    "keep *_puJetMva_*_*", # final MVAs and working point flags
    "keep *_puJetIdChs_*_*", # input variables
    "keep *_puJetMvaChs_*_*" # final MVAs and working point flags

    )

print " test 5 " 

#process.out.extend(["keep *_puJetId_*_*", # input variables
#                    "keep *_puJetMva_*_*" # final MVAs and working point flags
#                    ])

#process.saveNTuplesSkimLoose.append()

## Output module configuration
process.singleTopNTuple = cms.OutputModule("PoolOutputModule",
                   fileName = cms.untracked.string('edmntuple_'+ChannelName+'.root'),
                                             
                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = saveNTuplesSkimLoose,
)

process.singleTopPatTuple = cms.OutputModule("PoolOutputModule",
                   fileName = cms.untracked.string('pattuple_'+ChannelName+'.root'),


                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = savePatTupleSkimLoose
)
process.singleTopNTuple.dropMetaData = cms.untracked.string("ALL")

print " test 6"

process.outpath = cms.EndPath(
   process.singleTopNTuple +
   process.singleTopPatTuple 
   )

print " test 7"

