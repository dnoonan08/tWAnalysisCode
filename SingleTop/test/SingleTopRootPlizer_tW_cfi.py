import FWCore.ParameterSet.Config as cms

TreesDileptontW = cms.EDAnalyzer('SingleTopSystematicsTreesDumper_tW',
#General Info
#systematics = cms.untracked.vstring("BTagUp","BTagDown","MisTagUp","MisTagDown","JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown","PUUp","PUDown"),
#######THISWASORIGINAL######systematics = cms.untracked.vstring("JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown","JERUp","JERDown","LESUp","LESDown","PUUp","PUDown"),

systematics = cms.untracked.vstring("JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown","JERUp","JERDown","LESUp","LESDown","PUUp","PUDown","JESUpCorrelationGroupInSitu", "JESDownCorrelationGroupInSitu", "JESUpCorrelationGroupFlavor", "JESDownCorrelationGroupFlavor", "JESUpCorrelationGroupIntercalibration", "JESDownCorrelationGroupIntercalibration", "JESUpCorrelationGroupUncorrelated", "JESDownCorrelationGroupUncorrelated"),

#systematics = cms.untracked.vstring("JESUp","JESDown","UnclusteredMETUp","UnclusteredMETDown"),
#systematics = cms.untracked.vstring(""),
#rateSystematics = cms.untracked.vstring("WLightRateUp",                                        "WLightRateDown",                                        "TTBarRateUp",                                        "Ttbarratedown ",                                        "WHFRateUp",                                        "WHFRateDown"),

# systematics = cms.untracked.vstring("JESUp",                                 "JESDown",
#                                     "JESUpCorrelationGroupInSitu",           "JESDownCorrelationGroupInSitu",          
#                                     "JESUpCorrelationGroupFlavor",           "JESDownCorrelationGroupFlavor",          
#                                     "JESUpCorrelationGroupIntercalibration", "JESDownCorrelationGroupIntercalibration",
#                                     "JESUpCorrelationGroupUncorrelated",     "JESDownCorrelationGroupUncorrelated"
#                                     ),

rateSystematics = cms.untracked.vstring(),
doPU = cms.untracked.bool(True),
#doResol  = cms.untracked.bool(False),

doGen = cms.untracked.bool(True),

#algo  = cms.untracked.string("TCHPT"),
algo  = cms.untracked.string("CSVM"),#doLooseBJetVeto= cms.untracked.bool(True),

doResol  = cms.untracked.bool(True),
takeBTagSFFromDB = cms.untracked.bool(False),
#dataPUFile = cms.untracked.string("pileUpDistr.root"),
#mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
#puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
#mode = cms.untracked.string("pt"),
#maxPtCut = cms.untracked.double("45"),

#x1/x2
x1 = cms.InputTag("PDFInfo","x1"),
x2 = cms.InputTag("PDFInfo","x2"),
id1 = cms.InputTag("PDFInfo","id1"),
id2 = cms.InputTag("PDFInfo","id2"),
scalePDF = cms.InputTag("PDFInfo","scalePDF"),
doPDF =cms.untracked.bool(True),

channelInfo = cms.PSet(
    crossSection = cms.untracked.double(20.93),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(480000),
    finalLumiA = cms.untracked.double(14.5),
    finalLumiB = cms.untracked.double(14.5),
    finalLumiC = cms.untracked.double(14.5),
    finalLumiD = cms.untracked.double(14.5),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    loosePtCut = cms.untracked.double(30.0),#Default 30.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),

    ),

#Electrons
electronsPt = cms.InputTag("nTupleElectrons","tightElectronsPt"),  
electronsEta = cms.InputTag("nTupleElectrons","tightElectronsEta"),  
electronsPhi = cms.InputTag("nTupleElectrons","tightElectronsPhi"),  
electronsEnergy = cms.InputTag("nTupleElectrons","tightElectronsE"),  
electronsCharge = cms.InputTag("nTupleElectrons","tightElectronsCharge"),  
electronsDB = cms.InputTag("nTupleElectrons","tightElectronsAbsoluteDB"),  
electronsDXY = cms.InputTag("nTupleElectrons","tightElectronsPVDxy"),  
electronsDZ = cms.InputTag("nTupleElectrons","tightElectronsPVDz"),  
electronsRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFRelIso"),  
electronsDeltaCorrectedRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFDeltaCorrectedRelIso"),  
electronsRhoCorrectedRelIso = cms.InputTag("nTupleElectrons","tightElectronsPFRhoCorrectedRelIso"),  
electronsEleId70cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId70cIso"),  
electronsEleId80cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId80cIso"),  
electronsEleId90cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId90cIso"),  
electronsEleId95cIso = cms.InputTag("nTupleElectrons","tightElectronsSimpleEleId95cIso"),  
electronsMVAID = cms.InputTag("nTupleElectrons","tightElectronsMvaTrigV0"),  
electronsMVAIDNonTrig = cms.InputTag("nTupleElectrons","tightElectronsMvaNonTrigV0"),  
electronsTrackerExpectedInnerHits = cms.InputTag("nTupleElectrons","tightElectronsTrackerExpectedInnerHits"),  
electronsSuperClusterEta = cms.InputTag("nTupleElectrons","tightElectronsSuperClusterEta"),  
electronsECALPt = cms.InputTag("nTupleElectrons","tightElectronsecalDrivenMomentumPt"),
electronsChargedHadronIso = cms.InputTag("nTupleElectrons","tightElectronsChargedHadronIso"),
electronsPUChargedHadronIso = cms.InputTag("nTupleElectrons","tightElectronsPUChargedHadronIso"),
electronsNeutralHadronIso = cms.InputTag("nTupleElectrons","tightElectronsNeutralHadronIso"),
electronsPhotonIso = cms.InputTag("nTupleElectrons","tightElectronsPhotonIso"),
electronsPassConversionVeto = cms.InputTag("nTupleElectrons","tightElectronsPassConversionVeto"),

electronsGenPDGId = cms.InputTag("nTupleElectrons","tightElectronsgenPDGId"),  
electronsHasBParent = cms.InputTag("nTupleElectrons","tightElectronshasBparent"),  
electronsHasTParent = cms.InputTag("nTupleElectrons","tightElectronshasTparent"),  
electronsHasZParent = cms.InputTag("nTupleElectrons","tightElectronshasZparent"),  
electronsHasWParent = cms.InputTag("nTupleElectrons","tightElectronshasWparent"),  
electronsHasHParent = cms.InputTag("nTupleElectrons","tightElectronshasHparent"),  

#Muons
muonsPt = cms.InputTag("nTupleMuons","tightMuonsPt"),  
muonsEta = cms.InputTag("nTupleMuons","tightMuonsEta"),  
muonsPhi = cms.InputTag("nTupleMuons","tightMuonsPhi"),  
muonsEnergy = cms.InputTag("nTupleMuons","tightMuonsE"),  
muonsCharge = cms.InputTag("nTupleMuons","tightMuonsCharge"),  
muonsDB = cms.InputTag("nTupleMuons","tightMuonsAbsoluteDB"),  
muonsDXY = cms.InputTag("nTupleMuons","tightMuonsPVDxy"),  
muonsDZ = cms.InputTag("nTupleMuons","tightMuonsPVDz"),  
muonsRelIso = cms.InputTag("nTupleMuons","tightMuonsPFRelIso"),  
muonsDeltaCorrectedRelIso = cms.InputTag("nTupleMuons","tightMuonsPFDeltaCorrectedRelIso"),  
muonsRhoCorrectedRelIso = cms.InputTag("nTupleMuons","tightMuonsPFRhoCorrectedRelIso"),  
muonsChargedHadronIso = cms.InputTag("nTupleMuons","tightMuonsChargedHadronIso"),
muonsPUChargedHadronIso = cms.InputTag("nTupleMuons","tightMuonsPUChargedHadronIso"),
muonsNeutralHadronIso = cms.InputTag("nTupleMuons","tightMuonsNeutralHadronIso"),
muonsPhotonIso = cms.InputTag("nTupleMuons","tightMuonsPhotonIso"),
muonsSumChargedHadronPtR03 = cms.InputTag("nTupleMuons","tightMuonsSumChargedHadronPtR03"),
muonsSumChargedParticlePtR03 = cms.InputTag("nTupleMuons","tightMuonsSumChargedParticlePtR03"),
muonsSumNeutralHadronEtR03 = cms.InputTag("nTupleMuons","tightMuonsSumNeutralHadronEtR03"),
muonsSumPhotonEtR03 = cms.InputTag("nTupleMuons","tightMuonsSumPhotonEtR03"),
muonsSumNeutralHadronEtHighThresholdR03 = cms.InputTag("nTupleMuons","tightMuonsSumNeutralHadronEtHighThresholdR03"),
muonsSumPhotonEtHighThresholdR03 = cms.InputTag("nTupleMuons","tightMuonsSumPhotonEtHighThresholdR03"),
muonsSumPUPtR03 = cms.InputTag("nTupleMuons","tightMuonsSumPUPtR03"),
muonsSumChargedHadronPtR04 = cms.InputTag("nTupleMuons","tightMuonsSumChargedHadronPtR04"),
muonsSumChargedParticlePtR04 = cms.InputTag("nTupleMuons","tightMuonsSumChargedParticlePtR04"),
muonsSumNeutralHadronEtR04 = cms.InputTag("nTupleMuons","tightMuonsSumNeutralHadronEtR04"),
muonsSumPhotonEtR04 = cms.InputTag("nTupleMuons","tightMuonsSumPhotonEtR04"),
muonsSumNeutralHadronEtHighThresholdR04 = cms.InputTag("nTupleMuons","tightMuonsSumNeutralHadronEtHighThresholdR04"),
muonsSumPhotonEtHighThresholdR04 = cms.InputTag("nTupleMuons","tightMuonsSumPhotonEtHighThresholdR04"),
muonsSumPUPtR04 = cms.InputTag("nTupleMuons","tightMuonsSumPUPtR04"),

muonsGenPDGId = cms.InputTag("nTupleMuons","tightMuonsgenPDGId"),  
muonsHasBParent = cms.InputTag("nTupleMuons","tightMuonshasBparent"),  
muonsHasTParent = cms.InputTag("nTupleMuons","tightMuonshasTparent"),  
muonsHasZParent = cms.InputTag("nTupleMuons","tightMuonshasZparent"),  
muonsHasWParent = cms.InputTag("nTupleMuons","tightMuonshasWparent"),  
muonsHasHParent = cms.InputTag("nTupleMuons","tightMuonshasHparent"),  

ktJetsForIsoRho = cms.InputTag("kt6PFJetsForIsolation","rho"),

#Vertex
#Vertices
vertexX = cms.InputTag("nTupleVertices","x"),  
vertexY = cms.InputTag("nTupleVertices","y"),  
vertexZ = cms.InputTag("nTupleVertices","z"),  
vertexchi = cms.InputTag("nTupleVertices","chi"),  
vertexrho = cms.InputTag("nTupleVertices","rho"),  
vertexNDOF = cms.InputTag("nTupleVertices","ndof"),  
vertexIsFake = cms.InputTag("nTupleVertices","isFake"),  

nVerticesPlus = cms.InputTag("NVertices","PileUpP1"),
nVerticesMinus = cms.InputTag("NVertices","PileUpM1"),
nVertices = cms.InputTag("NVertices","PileUpTrue"),

#generated Particles
genPartPt = cms.InputTag("nTupleGenParticles","genParticlespt"),
genPartPdgId = cms.InputTag("nTupleGenParticles","genParticlespdgId"),



#Jets

genjetsPt =cms.InputTag("genJetsPF","genJetsPt"),  
genjetsEta =cms.InputTag("genJetsPF","genJetsEta"),  
#genjetsPhi =cms.InputTag("genJetsPF","genJetsPhi"),  
#genJetsPt =cms.InputTag("nTupleTopJetsPF","topJetsPFPt"),  
#genJetsEta =cms.InputTag("nTupleTopJetsPF","topJetsPFEta"),  

jetsPt = cms.InputTag("nTupleTopJetsPF","topJetsPFPt"),  
jetsPhi = cms.InputTag("nTupleTopJetsPF","topJetsPFPhi"),  
jetsEta = cms.InputTag("nTupleTopJetsPF","topJetsPFEta"),  
jetsEnergy = cms.InputTag("nTupleTopJetsPF","topJetsPFE"),  

jetsTCHP = cms.InputTag("nTupleTopJetsPF","topJetsPFTrackCountingHighPur"),  
jetsCSV =  cms.InputTag("nTupleTopJetsPF","topJetsPFCombinedSecondaryVertexBJetTags"),  
jetsRMS = cms.InputTag("nTupleTopJetsPF","topJetsPFRMS"),  
jetsNumDaughters = cms.InputTag("nTupleTopJetsPF","topJetsPFNumberOfDaughters"),  
jetsCHEmEn = cms.InputTag("nTupleTopJetsPF","topJetsPFCHEmEnFrac"),  
jetsCHHadEn = cms.InputTag("nTupleTopJetsPF","topJetsPFCHHadEnFrac"),  
jetsCHMult = cms.InputTag("nTupleTopJetsPF","topJetsPFChargedMultiplicity"),  
jetsNeuEmEn = cms.InputTag("nTupleTopJetsPF","topJetsPFNeuEmEnFrac"),  
jetsNeuHadEn = cms.InputTag("nTupleTopJetsPF","topJetsPFNeuHadEnFrac"),  
jetsNeuMult = cms.InputTag("nTupleTopJetsPF","topJetsPFNeutralMultiplicity"),  
jetsBeta = cms.InputTag("nTupleTopJetsPF","topJetsPFBeta"),  
jetsBetaStar = cms.InputTag("nTupleTopJetsPF","topJetsPFBetaStar"),  
jetsFlavour = cms.InputTag("nTupleTopJetsPF","topJetsPFFlavour"),   
jetsDZ = cms.InputTag("nTupleTopJetsPF","topJetsPFdZ"),  

jetsPUChargedDiscr = cms.InputTag("nTupleTopJetsPF","topJetsPFPUChargedDiscriminant"),  
jetsPUChargedWP = cms.InputTag("nTupleTopJetsPF","topJetsPFPUChargedWorkingPoint"),  
jetsPUFullDiscr = cms.InputTag("nTupleTopJetsPF","topJetsPFPUFullDiscriminant"),  
jetsPUFullWP = cms.InputTag("nTupleTopJetsPF","topJetsPFPUFullWorkingPoint"),  

jetsGenPDGId = cms.InputTag("nTupleTopJetsPF","topJetsPFgenPDGId"),  
jetsHasBParent = cms.InputTag("nTupleTopJetsPF","topJetsPFhasBparent"),  
jetsHasTParent = cms.InputTag("nTupleTopJetsPF","topJetsPFhasTparent"),  
jetsHasZParent = cms.InputTag("nTupleTopJetsPF","topJetsPFhasZparent"),  
jetsHasWParent = cms.InputTag("nTupleTopJetsPF","topJetsPFhasWparent"),  
jetsHasHParent = cms.InputTag("nTupleTopJetsPF","topJetsPFhasHparent"),  


#REMOVED###jetsCorrTotal = cms.InputTag("nTupleTopJetsPF","topJetsPFJetCorrTotal"),   

#MET 

METPhi = cms.InputTag("nTuplePatMETsPF","patMETsPFPhi"),
METPt = cms.InputTag("nTuplePatMETsPF","patMETsPFPt"),

UnclusteredMETPx = cms.InputTag("UnclusteredMETPF","UnclusteredMETPx"),
UnclusteredMETPy = cms.InputTag("UnclusteredMETPF","UnclusteredMETPy"),


)

