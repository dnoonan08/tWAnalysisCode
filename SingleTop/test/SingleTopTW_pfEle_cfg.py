import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTop")

process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
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

runOnMC = True
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





#Use gsfElectrons:
#useGsfElectrons(process,Postfix,"03") 

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

process.patElectrons.isolationValues = cms.PSet(
            pfChargedHadrons = cms.InputTag("elPFIsoValueCharged03PFId"),
            pfChargedAll = cms.InputTag("elPFIsoValueChargedAll03PFId"),
            pfPUChargedHadrons = cms.InputTag("elPFIsoValuePU03PFId"),
            pfNeutralHadrons = cms.InputTag("elPFIsoValueNeutral03PFId"),
            pfPhotons = cms.InputTag("elPFIsoValueGamma03PFId")
            )


# set the dB to the beamspot
process.patMuons.usePV = cms.bool(False)
process.patElectrons.usePV = cms.bool(False)


process.tightElectrons.category = cms.untracked.string("")

#process.countLeptons.minNumberTight = cms.untracked.int32(2)


#
process.patseq = cms.Sequence(
#    process.patElectronIDs +
    process.goodOfflinePrimaryVertices *
    process.patElectronIDs *
    process.kt6PFJetsForIsolation *
    getattr(process,"patPF2PATSequence"+postfix) #*
    )

print " test 2 " 

process.pathPreselection = cms.Path(
        process.patseq
        + process.puJetIdSqeuence + process.puJetIdSqeuenceChs
        #+  process.producePatPFMETCorrections
        )


print " test 3 " 


#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0024E066-2BEA-E111-B72F-001BFCDBD11E.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/004AB6FA-2CEA-E111-A804-0018F3D095FC.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/02A8F22B-2DEA-E111-94A3-003048FF9AC6.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0477BBF6-2CEA-E111-AD91-0018F3D096C0.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/0E57221B-2BEA-E111-9E01-003048FFD740.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/12787775-33EA-E111-A590-002618943924.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/1C1B4974-47EA-E111-B258-003048678DD6.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/2A558500-4BEA-E111-AC62-002354EF3BDB.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/308E878D-1DEA-E111-B295-00261894388F.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/34818BF6-2CEA-E111-BB3B-00261894389E.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/363AF39E-48EA-E111-A35B-001A928116F4.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/381E985F-34EA-E111-8622-003048FFCC18.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/38B37127-2BEA-E111-91CC-0018F3D095F2.root",
                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/3C4FD424-30EA-E111-93FD-003048FFD752.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/4657C86E-4EEA-E111-B982-001BFCDBD166.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/5A69EE6D-2BEA-E111-9F8B-00261894386E.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/5E068A1E-5CEA-E111-B96B-0018F3D096D2.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/5E4EE11D-31EA-E111-9E76-0018F3D09676.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/5EAE95F4-2CEA-E111-A905-001A92971B30.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/606751D2-2DEA-E111-993B-001A92971B30.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/64B83F4A-2CEA-E111-8F2F-00261894380A.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/68B9FC2A-2AEA-E111-97F3-00248C55CC97.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/6E397F21-2BEA-E111-88AB-002618943974.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/707FD76C-2BEA-E111-ADA3-001A928116B0.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/76427DAA-3DEA-E111-B442-001A92971B96.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/88C5082B-60EA-E111-B929-001A92971AD8.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/8AE2565B-40EA-E111-9248-001A92810AE6.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/8C89E604-2CEA-E111-8D8D-00261894394F.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/8E7A543F-3BEA-E111-A78C-003048FFD754.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/96B26E58-2CEA-E111-A9B1-001A92971B30.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/A6FE6D4F-20EA-E111-BEEB-001A9281172A.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/AADF70D6-29EA-E111-BB51-003048678C06.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/B0DF0D19-2BEA-E111-84E7-002618943933.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/B0EE2BF5-2BEA-E111-9A4E-002618943962.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/B22FBEFB-2CEA-E111-96CC-0018F3D096A2.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/B27685BA-46EA-E111-88C6-003048FFCC18.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/B2B5A53F-44EA-E111-A0C3-001A92811726.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/B403432C-42EA-E111-80FF-001A928116DC.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/B694B034-2AEA-E111-9ADE-0018F3D09650.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/BA4B0493-5DEA-E111-AD89-001A92811724.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/BC23B55F-2EEA-E111-A6FA-003048FF9AC6.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/BEE2FBD7-49EA-E111-94CA-001A92971B48.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/C662C644-35EA-E111-96F7-001A92971B8C.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/C82AE3C9-2DEA-E111-8415-003048FFCBA8.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/C87DDC13-2EEA-E111-8767-003048FFD71E.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/CA6BD593-56EA-E111-B1FF-003048FFD71E.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/CE9E7E9E-3EEA-E111-B81A-001A92811706.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/D0AA024C-2CEA-E111-860B-002618FDA250.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/D8B8971D-37EA-E111-924A-0018F3D09676.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/DC1958F9-2BEA-E111-8E57-003048679244.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/DEE167EC-59EA-E111-998B-001BFCDBD1BC.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/E0015B79-3FEA-E111-AB0E-001A92971BBA.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/E681AFD1-52EA-E111-8570-001BFCDBD1BC.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/E87393FE-57EA-E111-BE1D-003048FF9AA6.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F0E73861-3DEA-E111-9B78-003048D15E2C.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/F4FEBE8F-3BEA-E111-8373-003048FF9AA6.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FA66A1F2-28EA-E111-94DF-003048679188.root",
#                                 "/store/mc/Summer12_DR53X/T_tW-channel-DR_TuneZ2star_8TeV-powheg-tauola/AODSIM/PU_S10_START53_V7A-v1/0000/FA8766A2-38EA-E111-9624-001A92811738.root",

),
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
#     'drop *',

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
   process.singleTopNTuple #+
#   process.singleTopPatTuple 
   )

print " test 7"

