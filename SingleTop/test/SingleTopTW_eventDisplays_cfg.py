import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(False),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 100




# conditions ------------------------------------------------------------------

print "test "

#process.load("Configuration.StandardSequences.MixingNoPileUp_cff")
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data

ChannelName = "tW_New_Test"

process.GlobalTag.globaltag = cms.string('START53_V10::All')

#from Configuration.PyReleaseValidation.autoCond import autoCond
#process.GlobalTag.globaltag = autoCond['startup']
process.load("TopQuarkAnalysis.SingleTop.SingleTopSequences_tW_cff") 
######process.load("SelectionCuts_tW_Skim_cff")################<----------



process.out = cms.OutputModule("PoolOutputModule",
                               fileName = cms.untracked.string('dummy.root'),
                               outputCommands = cms.untracked.vstring(""),
                               )


# Get a list of good primary vertices, in 42x, these are DAF vertices
from PhysicsTools.SelectorUtils.pvSelector_cfi import pvSelector

process.goodOfflinePrimaryVertices = cms.EDFilter(
    "PrimaryVertexObjectFilter",
    filterParams = cms.PSet( minNdof = cms.double( 4. ) , maxZ = cms.double( 24. ) , maxRho = cms.double( 2. ) ) ,
    filter = cms.bool( True) ,
    src=cms.InputTag('offlinePrimaryVertices')
    )





from RecoJets.JetProducers.kt4PFJets_cfi import *

process.kt6PFJetsForIsolation = kt4PFJets.clone( rParam = 0.6, doRhoFastjet = True )
process.kt6PFJetsForIsolation.Rho_EtaMax = cms.double(2.5)


# set the dB to the beamspot
# process.patMuons.usePV = cms.bool(False)
# process.patElectrons.usePV = cms.bool(False)

#postfix = "SingleTop"
postfix = ""

# Configure PAT to use PF2PAT instead of AOD sources
from PhysicsTools.PatAlgos.tools.pfTools import *
#Postfix = "SingleTop"
Postfix = ""

runOnMC = False
jetAlgoName = "AK5"

print "test2.2"

#usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('goodOfflinePrimaryVertices'),  typeIMetCorrections=True)
usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('goodOfflinePrimaryVertices'),  typeIMetCorrections=True)
#usePF2PAT(process, runPF2PAT=True, jetAlgo=jetAlgoName, runOnMC=runOnMC, postfix=Postfix, jetCorrections=('AK5PFchs',['L1FastJet','L2Relative','L3Absolute']), pvCollection=cms.InputTag('goodofflinePrimaryVertices'),  typeIMetCorrections=True)
#          jetCorrections=('AK5PFchs', jetCorrections)

print "test2.3"

process.pfPileUp.checkClosestZVertex = False


#process.pfPileUp.Enable = True
getattr(process,"pfNoPileUp"+postfix).enable = True
getattr(process,"pfNoMuon"+postfix).enable = True
getattr(process,"pfNoElectron"+postfix).enable = True
getattr(process,"pfNoTau"+postfix).enable = False
getattr(process,"pfNoJet"+postfix).enable = False

process.load("CMGTools.External.pujetidsequence_cff")






#Use PFelectrons
process.pfIsolatedMuons.isolationCut = cms.double(0.2)
process.pfIsolatedMuons.doDeltaBetaCorrection = True
process.pfSelectedMuons.cut = cms.string('pt > 10. && abs(eta) < 2.5')
process.pfIsolatedMuons.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("muPFIsoValueCharged04"))
process.pfIsolatedMuons.deltaBetaIsolationValueMap = cms.InputTag("muPFIsoValuePU04")
process.pfIsolatedMuons.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("muPFIsoValueNeutral04"), cms.InputTag("muPFIsoValueGamma04"))

process.pfIsolatedElectrons.isolationCut = cms.double(0.2)
process.pfIsolatedElectrons.doDeltaBetaCorrection = True
process.pfSelectedElectrons.cut = cms.string('pt > 15. && abs(eta) < 2.5')
process.pfIsolatedElectrons.isolationValueMapsCharged = cms.VInputTag(cms.InputTag("elPFIsoValueCharged03PFId"))
process.pfIsolatedElectrons.deltaBetaIsolationValueMap = cms.InputTag("elPFIsoValuePU03PFId")
process.pfIsolatedElectrons.isolationValueMapsNeutral = cms.VInputTag(cms.InputTag("elPFIsoValueNeutral03PFId"), cms.InputTag("elPFIsoValueGamma03PFId"))

#Use gsfElectrons:
useGsfElectrons(process,Postfix,"03") 

# process.patElectrons.isolationValues = cms.PSet(
#             pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFId"),
#             pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFId"),
#             pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFId"),
#             pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFId"),
#             pfPhotons = cms.InputTag("elPFIsoValueGamma03PFId")
#             )


# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)


process.tightElectrons.category = cms.untracked.string("")

#process.countLeptons.minNumberTight = cms.untracked.int32(0)


#
process.patseq = cms.Sequence(
#    process.patElectronIDs +
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    process.kt6PFJetsForIsolation *
    getattr(process,"patPF2PATSequence"+postfix) #*
    )

print " test 2 " 

#process.load("TopQuarkAnalysis.TopEventProducers.sequences.ttGenEvent_cff")   

process.pathPreselection = cms.Path(
        process.patseq
        + process.puJetIdSqeuence + process.puJetIdSqeuenceChs #+ process.makeGenEvt
        #+  process.producePatPFMETCorrections
        )

print " test 3 " 


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(200) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
                                 "file:../../../../work/MuMuEvents.root",
#                                "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/1C1B4974-47EA-E111-B258-003048678DD6.root",
#                                "/store/mc/Summer12_DR53X/TTJets_MassiveBinDECAY_TuneZ2star_8TeV-madgraph-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/001C868B-B2E1-E111-9BE3-003048D4DCD8.root"
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0024E066-2BEA-E111-B72F-001BFCDBD11E.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/004AB6FA-2CEA-E111-A804-0018F3D095FC.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02A8F22B-2DEA-E111-94A3-003048FF9AC6.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0477BBF6-2CEA-E111-AD91-0018F3D096C0.root",

),

#eventsToProcess = cms.untracked.VEventRange('1:16531','1:16731'),

#eventsToProcess = cms.untracked.VEventRange('1:278867'),
#eventsToProcess = cms.untracked.VEventRange('1:361971'),
#eventsToProcess = cms.untracked.VEventRange('1:231811'),
#eventsToProcess = cms.untracked.VEventRange('1:233540'),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#skipEvents = cms.untracked.uint32(133),
)

process.baseLeptonSequence = cms.Path(
#    process.PVFilter +
    process.basePath
    )

process.topJetsPF.removeOverlap = cms.untracked.bool(False)

process.preselection.remove(process.PVFilter)

process.selection = cms.Path (
    process.preselection + 
    process.nTuplesSkim
    )

print " test 4 " 


from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import saveNTuplesSkimLoose
from TopQuarkAnalysis.SingleTop.SingleTopNtuplizers_tW_cff import saveNTuplesSkimMu
    
savePatTupleSkimLoose = cms.untracked.vstring(
     'keep *'
#    'drop *',

#     'keep patMuons_selectedPatMuons_*_*',
#     'keep patElectrons_selectedPatElectrons_*_*',
#     'keep patJets_selectedPatJets_*_*',
#     'keep patMETs_patMETs_*_*',
#     'keep *_patPFMet_*_*',
#     'keep *_patType1CorrectedPFMet_*_*',
#     'keep *_PVFilterProducer_*_*',

#     'keep *_kt6PFJetsForIsolation_rho_*',

#     'keep patJets_topJetsPF_*_*',
#     'keep patMuons_looseMuons_*_*',
#     'keep *_looseElectrons_*_*',
#     'keep patMuons_tightMuons_*_*',
#     'keep patMuons_tightMuonsTest_*_*',
#     'keep *_tightElectrons_*_*',

#     'keep *_PDFInfo_*_*',

#     'keep *_patElectronsZeroIso_*_*',
#     'keep *_patMuonsZeroIso_*_*',
#     'keep *_kt6PFJetsCentral_*_*',
#     'keep *_PVFilterProducer_*_*',
    
#     'keep *_cFlavorHistoryProducer_*_*',
#     'keep *_bFlavorHistoryProducer_*_*',
#     "keep *_puJetId_*_*", # input variables
#     "keep *_puJetMva_*_*", # final MVAs and working point flags
#     "keep *_puJetIdChs_*_*", # input variables
#     "keep *_puJetMvaCmvahs_*_*" # final MVAs and working point flags

    )

print " test 5 " 

#process.out.extend(["keep *_puJetId_*_*", # input variables
#                    "keep *_puJetMva_*_*" # final MVAs and working point flags
#                    ])

#process.saveNTuplesSkimLoose.append()

## Output module configuration
process.singleTopNTuple = cms.OutputModule("PoolOutputModule",
                   fileName = cms.untracked.string('edmntuple.root'),
                                             
                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = saveNTuplesSkimLoose,
)

process.singleTopPatTuple = cms.OutputModule("PoolOutputModule",
                   fileName = cms.untracked.string('pattuple.root'),


                   SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('selection')),
                   outputCommands = savePatTupleSkimLoose
)
process.singleTopNTuple.dropMetaData = cms.untracked.string("ALL")

print " test 6"

process.outpath = cms.EndPath(
   process.singleTopNTuple 
   + process.singleTopPatTuple 
   )

print " test 7"

