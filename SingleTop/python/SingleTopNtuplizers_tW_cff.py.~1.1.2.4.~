import FWCore.ParameterSet.Config as cms


nTupleTopJetsPF = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("topJetsPF"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("topJetsPF"),
    
    variables = cms.VPSet(
    cms.PSet(
    #B-Tagging
    tag = cms.untracked.string("TrackCountingHighPur"),
    quantity = cms.untracked.string("bDiscriminator('trackCountingHighPurBJetTags')"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PUFullDiscriminant"),
    quantity = cms.untracked.string("userFloat(\"PUFullDiscriminant\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PUChargedDiscriminant"),
    quantity = cms.untracked.string("userFloat(\"PUChargedDiscriminant\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PUFullWorkingPoint"),
    quantity = cms.untracked.string("userFloat(\"PUFullWorkingPoint\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PUChargedWorkingPoint"),
    quantity = cms.untracked.string("userFloat(\"PUChargedWorkingPoint\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("Beta"),
    quantity = cms.untracked.string("userFloat(\"beta\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("dZ"),
    quantity = cms.untracked.string("userFloat(\"dZ\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("BetaStar"),
    quantity = cms.untracked.string("userFloat(\"betaStar\")"),
    ),


    cms.PSet(
    tag = cms.untracked.string("NeutralMultiplicity"),
    quantity = cms.untracked.string("neutralMultiplicity"),
    ),
 
    cms.PSet(
    tag = cms.untracked.string("RMS"),
    quantity = cms.untracked.string("userFloat(\"RMS\")"),
    ),

    cms.PSet(
    tag = cms.untracked.string("NumberOfDaughters"),
    quantity = cms.untracked.string("numberOfDaughters"),
    ),

    cms.PSet(
    tag = cms.untracked.string("ChargedMultiplicity"),
    quantity = cms.untracked.string("chargedMultiplicity"),
    ),

    cms.PSet(
    tag = cms.untracked.string("NeuHadEnFrac"),
    quantity = cms.untracked.string("neutralHadronEnergyFraction"),
    ),

    cms.PSet(
    tag = cms.untracked.string("NeuEmEnFrac"),
    quantity = cms.untracked.string("neutralEmEnergyFraction"),
    ),

    cms.PSet(
    tag = cms.untracked.string("CHEmEnFrac"),
    quantity = cms.untracked.string("chargedEmEnergyFraction"),
    ),

    cms.PSet(
    tag = cms.untracked.string("CHHadEnFrac"),
    quantity = cms.untracked.string("chargedHadronEnergyFraction"),
    ),

    cms.PSet(
    tag = cms.untracked.string("CombinedSecondaryVertexBJetTags"),
    quantity = cms.untracked.string("bDiscriminator('combinedSecondaryVertexBJetTags')"),
    ),
    ##    4-momentum
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("E"),
    quantity = cms.untracked.string("energy")
    ),
    #Flavour
    cms.PSet(
    tag = cms.untracked.string("Flavour"),
    quantity = cms.untracked.string("partonFlavour")
    ),
    #JEC factor to uncorrected jet
    cms.PSet(
    tag = cms.untracked.string("JetCorrTotal"),
    quantity = cms.untracked.string("jecFactor('Uncorrected')")
    ),
    )
)

nTupleVertices = cms.EDProducer(
    "SingleTopVertexInfoDumper",
    src = cms.InputTag("goodOfflinePrimaryVertices"),
)

nTupleVertices2 = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("goodOfflinePrimaryVertices"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("offlinePV"),
    variables = cms.VPSet(

    cms.PSet(
    tag = cms.untracked.string("isFake"),
    quantity = cms.untracked.string("isFake")
    ),
    )
    )

nTuplePatMETsPF = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("patMETsPF"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("patMETsPF"),
    variables = cms.VPSet(

    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),

    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    
    )
    )


nTupleElectrons = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("tightElectrons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("tightElectrons"),
    variables = cms.VPSet(
    #4-momentum
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("E"),
    quantity = cms.untracked.string("energy")
    ),
    #Charge
    cms.PSet(
    tag = cms.untracked.string("Charge"),
    quantity = cms.untracked.string("charge")
    ),
    #Iso
    cms.PSet(
    tag = cms.untracked.string("PFDeltaCorrectedRelIso"),
#    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFRelIso"),
    quantity = cms.untracked.string('(chargedHadronIso+ neutralHadronIso + photonIso)/pt'),
#    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFRhoCorrectedRelIso"),
    quantity = cms.untracked.string("userFloat(\"RhoCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("ChargedHadronIso"),
    quantity = cms.untracked.string("chargedHadronIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("NeutralHadronIso"),
    quantity = cms.untracked.string("neutralHadronIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PhotonIso"),
    quantity = cms.untracked.string("photonIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PUChargedHadronIso"),
    quantity = cms.untracked.string("puChargedHadronIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDxy"),
    quantity = cms.untracked.string("userFloat(\"VertexDxy\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDz"),
    #    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"VertexDz\")"),
    ),
    #ID and other parameters
    cms.PSet(
    tag = cms.untracked.string("SimpleEleId70cIso"),
    quantity = cms.untracked.string("electronID('simpleEleId70cIso')")
    ),
    cms.PSet(
    tag = cms.untracked.string("SimpleEleId80cIso"),
    quantity = cms.untracked.string("electronID('simpleEleId80cIso')")
    ),
    cms.PSet(
    tag = cms.untracked.string("SimpleEleId90cIso"),
    quantity = cms.untracked.string("electronID('simpleEleId90cIso')")
    ),
#    cms.PSet(
#    tag = cms.untracked.string("SimpleEleId60cIso"),
#    quantity = cms.untracked.string("electronID('simpleEleId60cIso')")
#    ),
    cms.PSet(
    tag = cms.untracked.string("SimpleEleId95cIso"),
    quantity = cms.untracked.string("electronID('simpleEleId95cIso')")
    ),
    cms.PSet(
    tag = cms.untracked.string("MvaTrigV0"),
    quantity = cms.untracked.string("electronID('mvaTrigV0')")
    ),
    cms.PSet(
    tag = cms.untracked.string("MvaNonTrigV0"),
    quantity = cms.untracked.string("electronID('mvaNonTrigV0')")
    ),
    cms.PSet(
    tag = cms.untracked.string("SuperClusterEta"),
    quantity = cms.untracked.string("superCluster.eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("AbsoluteDB"),
    quantity = cms.untracked.string("dB"),
    ),
    cms.PSet(
    tag = cms.untracked.string("TrackerExpectedInnerHits"),
    quantity = cms.untracked.string("gsfTrack().trackerExpectedHitsInner.numberOfHits")
    ),
    cms.PSet(
    tag = cms.untracked.string("ecalDrivenMomentumPx"),
    quantity = cms.untracked.string("ecalDrivenMomentum.Px")    
    ),
    cms.PSet(
    tag = cms.untracked.string("ecalDrivenMomentumPy"),
    quantity = cms.untracked.string("ecalDrivenMomentum.Py")    
    ),
    cms.PSet(
    tag = cms.untracked.string("ecalDrivenMomentumPz"),
    quantity = cms.untracked.string("ecalDrivenMomentum.Pz")    
    ),
    cms.PSet(
    tag = cms.untracked.string("ecalDrivenMomentumE"),
    quantity = cms.untracked.string("ecalDrivenMomentum.E")    
    ),
    cms.PSet(
    tag = cms.untracked.string("ecalDrivenMomentumEt"),
    quantity = cms.untracked.string("ecalDrivenMomentum.Et")    
    ),
    cms.PSet(
    tag = cms.untracked.string("ecalDrivenMomentumPt"),
    quantity = cms.untracked.string("ecalDrivenMomentum.Pt")    
    ),
    cms.PSet(
    tag = cms.untracked.string("PassConversionVeto"),
    quantity = cms.untracked.string("passConversionVeto")    
    ),

#     cms.PSet(
#     tag = cms.untracked.string("IsoTest"),
#     quantity = cms.untracked.string("isoDeposit().depositWithin(0.3)")    
#     ),

    )
    )

nTupleMuons = nTupleElectrons.clone(
    src = cms.InputTag("tightMuons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("tightMuons"),
    variables = cms.VPSet(
    #4-momentum
    #4-momentum
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("E"),
    quantity = cms.untracked.string("energy")
    ),
    #Charge
    cms.PSet(
    tag = cms.untracked.string("Charge"),
    quantity = cms.untracked.string("charge")
    ),
    #Iso
    cms.PSet(
    tag = cms.untracked.string("PFRelIso"),
    quantity = cms.untracked.string('(chargedHadronIso+ neutralHadronIso + photonIso)/pt'),
#    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFDeltaCorrectedRelIso"),
#    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFRhoCorrectedRelIso"),
    quantity = cms.untracked.string("userFloat(\"RhoCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("ChargedHadronIso"),
    quantity = cms.untracked.string("chargedHadronIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("NeutralHadronIso"),
    quantity = cms.untracked.string("neutralHadronIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PhotonIso"),
    quantity = cms.untracked.string("photonIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PUChargedHadronIso"),
    quantity = cms.untracked.string("puChargedHadronIso"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDz"),
    #    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"VertexDz\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDxy"),
    quantity = cms.untracked.string("userFloat(\"VertexDxy\")"),
    ),
    #ID and other parameters
    cms.PSet(
    tag = cms.untracked.string("IsGlobalMuonPromptTight"),
    quantity = cms.untracked.string("muonID('GlobalMuonPromptTight')")
    ),
    cms.PSet(
    tag = cms.untracked.string("IsGlobalMuon"),
    quantity = cms.untracked.string("isGlobalMuon")
    ),
    cms.PSet(
    tag = cms.untracked.string("IsTrackerMuon"),
    quantity = cms.untracked.string("isTrackerMuon")
    ),
    cms.PSet(
    tag = cms.untracked.string("AbsoluteDB"),
    quantity = cms.untracked.string("dB"),
    ),
    cms .PSet(
    tag = cms.untracked.string("TrackerValidInnerHits"),
    quantity = cms.untracked.string("innerTrack.numberOfValidHits")
    ),

    cms.PSet(
    tag = cms.untracked.string("SumChargedHadronPtR03"),
    quantity = cms.untracked.string("pfIsolationR03.sumChargedHadronPt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumChargedParticlePtR03"),
    quantity = cms.untracked.string("pfIsolationR03.sumChargedParticlePt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumNeutralHadronEtR03"),
    quantity = cms.untracked.string("pfIsolationR03.sumNeutralHadronEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumPhotonEtR03"),
    quantity = cms.untracked.string("pfIsolationR03.sumPhotonEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumNeutralHadronEtHighThresholdR03"),
    quantity = cms.untracked.string("pfIsolationR03.sumNeutralHadronEtHighThreshold")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumPhotonEtHighThresholdR03"),
    quantity = cms.untracked.string("pfIsolationR03.sumPhotonEtHighThreshold")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumPUPtR03"),
    quantity = cms.untracked.string("pfIsolationR03.sumPUPt")
    ),

    cms.PSet(
    tag = cms.untracked.string("SumChargedHadronPtR04"),
    quantity = cms.untracked.string("pfIsolationR04.sumChargedHadronPt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumChargedParticlePtR04"),
    quantity = cms.untracked.string("pfIsolationR04.sumChargedParticlePt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumNeutralHadronEtR04"),
    quantity = cms.untracked.string("pfIsolationR04.sumNeutralHadronEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumPhotonEtR04"),
    quantity = cms.untracked.string("pfIsolationR04.sumPhotonEt")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumNeutralHadronEtHighThresholdR04"),
    quantity = cms.untracked.string("pfIsolationR04.sumNeutralHadronEtHighThreshold")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumPhotonEtHighThresholdR04"),
    quantity = cms.untracked.string("pfIsolationR04.sumPhotonEtHighThreshold")
    ),
    cms.PSet(
    tag = cms.untracked.string("SumPUPtR04"),
    quantity = cms.untracked.string("pfIsolationR04.sumPUPt")
    ),
    

    )
    )

nTupleLooseMuons = nTupleMuons.clone(
    src = cms.InputTag("looseMuons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("looseMuons"),
    variables = cms.VPSet(
    #4-momentum
    #4-momentum
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("E"),
    quantity = cms.untracked.string("energy")
    ),
    #Charge
    cms.PSet(
    tag = cms.untracked.string("Charge"),
    quantity = cms.untracked.string("charge")
    ),
    #Iso
    cms.PSet(
    tag = cms.untracked.string("PFRelIso"),
    quantity = cms.untracked.string('(chargedHadronIso+ neutralHadronIso + photonIso)/pt'),
#    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFDeltaCorrectedRelIso"),
#    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFRhoCorrectedRelIso"),
    quantity = cms.untracked.string("userFloat(\"RhoCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDz"),
    #    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"VertexDz\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDxy"),
    quantity = cms.untracked.string("userFloat(\"VertexDxy\")"),
    ),
    #ID and other parameters
#    cms.PSet(
#    tag = cms.untracked.string("IsGlobalMuonPromptTight"),
#    quantity = cms.untracked.string("muonID('GlobalMuonPromptTight')")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("IsGlobalMuon"),
#    quantity = cms.untracked.string("isGlobalMuon")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("IsTrackerMuon"),
#    quantity = cms.untracked.string("isTrackerMuon")
#    ),
    cms.PSet(
    tag = cms.untracked.string("AbsoluteDB"),
    quantity = cms.untracked.string("dB"),
    ),
    #    cms .PSet(
    #    tag = cms.untracked.string("TrackerValidInnerHits"),
    #    quantity = cms.untracked.string("innerTrack.numberOfValidHits")
    #    ),
    
    )
    )

nTupleAllMuons = nTupleLooseMuons.clone(
    src = cms.InputTag("selectedPatMuons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("allMuons"),
    )

nTupleLooseElectrons = nTupleElectrons.clone(
    src = cms.InputTag("looseElectrons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("looseElectrons"),
    variables = cms.VPSet(
    #4-momentum
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("E"),
    quantity = cms.untracked.string("energy")
    ),
    #Charge
    cms.PSet(
    tag = cms.untracked.string("Charge"),
    quantity = cms.untracked.string("charge")
    ),
    #Iso
    cms.PSet(
    tag = cms.untracked.string("PFRelIso"),
    quantity = cms.untracked.string('(chargedHadronIso+ neutralHadronIso + photonIso)/pt'),
#    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFDeltaCorrectedRelIso"),
#    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"DeltaCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PFRhoCorrectedRelIso"),
    quantity = cms.untracked.string("userFloat(\"RhoCorrectedIso\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDxy"),
    quantity = cms.untracked.string("userFloat(\"VertexDxy\")"),
    ),
    cms.PSet(
    tag = cms.untracked.string("PVDz"),
    #    quantity = cms.untracked.string('(chargedHadronIso+ max(0., neutralHadronIso + photonIso -0.5*puChargedHadronIso()))/pt'),
    quantity = cms.untracked.string("userFloat(\"VertexDz\")"),
    ),

    #ID and other parameters
#    cms.PSet(
#    tag = cms.untracked.string("SimpleEleId70cIso"),
#    quantity = cms.untracked.string("electronID('simpleEleId70cIso')")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("SimpleEleId80cIso"),
#    quantity = cms.untracked.string("electronID('simpleEleId80cIso')")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("SimpleEleId90cIso"),
#    quantity = cms.untracked.string("electronID('simpleEleId90cIso')")
#    ),
##    cms.PSet(
##    tag = cms.untracked.string("SimpleEleId60cIso"),
##    quantity = cms.untracked.string("electronID('simpleEleId60cIso')")
##    ),
    cms.PSet(
    tag = cms.untracked.string("SimpleEleId95cIso"),
    quantity = cms.untracked.string("electronID('simpleEleId95cIso')")
    ),
    cms.PSet(
    tag = cms.untracked.string("MvaTrigV0"),
    quantity = cms.untracked.string("electronID('mvaTrigV0')")
    ),
#    cms.PSet(
#    tag = cms.untracked.string("MvaNonTrigV0"),
#    quantity = cms.untracked.string("electronID('mvaNonTrigV0')")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("SuperClusterEta"),
#    quantity = cms.untracked.string("superCluster.eta")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("AbsoluteDB"),
#    quantity = cms.untracked.string("dB"),
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("TrackerExpectedInnerHits"),
#    quantity = cms.untracked.string("gsfTrack().trackerExpectedHitsInner.numberOfHits")
#    ),
    )
    )

nTupleAllElectrons = nTupleLooseElectrons.clone(
    src = cms.InputTag("selectedPatElectrons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("allElectrons"),
    )

nTupleLooseElectronsEle = nTupleLooseElectrons.clone(
    src = cms.InputTag("looseElectronsEle"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("looseElectronsEle"),
    )

nTupleZVetoElectrons = nTupleLooseElectrons.clone(
    src = cms.InputTag("zVetoElectrons"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("zVetoElectrons"),
    )

nTupleAllJets = nTupleTopJetsPF.clone(
    src = cms.InputTag("selectedPatJets"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("allJets"),
    variables = cms.VPSet(
    cms.PSet(
    #B-Tagging
    tag = cms.untracked.string("TrackCountingHighPur"),
    quantity = cms.untracked.string("bDiscriminator('trackCountingHighPurBJetTags')")
    ),
#    cms.PSet(
#    tag = cms.untracked.string("TrackCountingHighEff"),
#    quantity = cms.untracked.string("bDiscriminator('trackCountingHighEffBJetTags')")
#    ),
    cms.PSet(
    tag = cms.untracked.string("CombinedSecondaryVertexBJetTags"),
    quantity = cms.untracked.string("bDiscriminator('combinedSecondaryVertexBJetTags')"),
    ),
#    cms.PSet(
#    tag = cms.untracked.string("SecondaryVertexHighPurBJetTags"),
#    quantity = cms.untracked.string("bDiscriminator('simpleSecondaryVertexHighPurBJetTags')"),
#    ),
    #4-momentum
    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),
    cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),
    cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),
    cms.PSet(
    tag = cms.untracked.string("E"),
    quantity = cms.untracked.string("energy")
    ),
    #Flavour
    cms.PSet(
    tag = cms.untracked.string("Flavour"),
    quantity = cms.untracked.string("partonFlavour")
    ),
    #ID 
#    cms.PSet(
#    tag = cms.untracked.string("NumberOfDaughters"),
#    quantity = cms.untracked.string("numberOfDaughters")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("ChargedMultiplicity"),
#    quantity = cms.untracked.string("chargedMultiplicity")
#    ),
#    cms.PSet(
#    tag = cms.untracked.string("ChargedHadronEnergyFraction"),
 #   quantity = cms.untracked.string("chargedHadronEnergyFraction")
 #   ),
 #   cms.PSet(
 #   tag = cms.untracked.string("ChargedEmEnergyFraction"),
 #   quantity = cms.untracked.string("chargedEmEnergyFraction")
 #   ),:
 #   cms.PSet(
 #   tag = cms.untracked.string("NeutralHadronEnergyFraction"),
 #   quantity = cms.untracked.string("neutralHadronEnergyFraction")
 #   ),
 #   cms.PSet(
 #   tag = cms.untracked.string("NeutralEmEnergyFraction"),
 #   quantity = cms.untracked.string("neutralEmEnergyFraction")
 #   ),
 #   #JEC factor to uncorrected jet
    cms.PSet(
    tag = cms.untracked.string("JetCorrTotal"),
    quantity = cms.untracked.string("jecFactor('Uncorrected')")
    ),
    )
    )

singleTopMCNeutrinos = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("MCTruthParticles","topNeutrinos"),
    prefix = cms.untracked.string("mcNeutrinos"),

    variables = cms.VPSet(

    cms.PSet(
    tag = cms.untracked.string("PdgId"),
    quantity = cms.untracked.string("pdgId")
    ),


    cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),

        cms.PSet(
    tag = cms.untracked.string("Eta"),
    quantity = cms.untracked.string("eta")
    ),

        cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),

        cms.PSet(
    tag = cms.untracked.string("Pt"),
    quantity = cms.untracked.string("pt")
    ),

        cms.PSet(
    tag = cms.untracked.string("Phi"),
    quantity = cms.untracked.string("phi")
    ),

        cms.PSet(
    tag = cms.untracked.string("P"),
    quantity = cms.untracked.string("p")
    ),

        cms.PSet(
    tag = cms.untracked.string("Theta"),
    quantity = cms.untracked.string("theta")
    ),

    ),

)

nTuplePFJetsForIsolation = cms.EDProducer(
          "CandViewNtpProducer",
          src = cms.InputTag("kt6PFJetsForIsolation"),
          lazyParser = cms.untracked.bool(True),
          prefix = cms.untracked.string("kt6pfJetsForIso"),
          variables = cms.VPSet(
    
          cms.PSet(
          tag = cms.untracked.string("Rho"),
          quantity = cms.untracked.string("rho")
          ),

          )
          )

nTuplePatType1METsPF = cms.EDProducer(
          "CandViewNtpProducer",
          src = cms.InputTag("patType1CorrectedPFMet"),
          lazyParser = cms.untracked.bool(True),
          prefix = cms.untracked.string("patType1METsPF"),
          variables = cms.VPSet(
    
          cms.PSet(
          tag = cms.untracked.string("Pt"),
          quantity = cms.untracked.string("pt")
          ),
    
          cms.PSet(
          tag = cms.untracked.string("Phi"),
          quantity = cms.untracked.string("phi")
          ),
    
         )
         )
  

nTupleQCDMuons = nTupleMuons.clone(
     src = cms.InputTag("tightMuonsZeroIso"),
     lazyParser = cms.untracked.bool(True),
     prefix = cms.untracked.string("QCDMuons"),
 )

nTupleQCDElectrons = nTupleElectrons.clone(
    src = cms.InputTag("tightElectronsZeroIso"),
    lazyParser = cms.untracked.bool(True),
    prefix = cms.untracked.string("QCDElectrons"),
)
 

singleTopMCNeutrinos = cms.EDProducer(
    "CandViewNtpProducer",
    src = cms.InputTag("MCTruthParticles","topNeutrinos"),
    prefix = cms.untracked.string("mcNeutrinos"),

    variables = cms.VPSet(

    cms.PSet(
    tag = cms.untracked.string("PdgId"),
    quantity = cms.untracked.string("pdgId")
    ),
    ),
)

singleTopMCLeptons = singleTopMCNeutrinos.clone( src = cms.InputTag("MCTruthParticles","topLeptons"), prefix = cms.untracked.string("mcLeptons"))

singleTopMCRecoilQuark = singleTopMCNeutrinos.clone( src = cms.InputTag("MCTruthParticles","singleTopRecoilQuark"), prefix = cms.untracked.string("mcRecoilQuark"))
singleTopMCBQuark = singleTopMCNeutrinos.clone( src = cms.InputTag("MCTruthParticles","bGenParticles"), prefix = cms.untracked.string("mcBQuark"))
 


nTuplesSkim = cms.Sequence(
    nTupleTopJetsPF +
    nTupleAllJets +
    nTuplePatMETsPF +
#    nTuplePatType1METsPF +
    nTupleAllElectrons +
    nTupleAllMuons +
    nTupleLooseElectrons +
    nTupleLooseElectronsEle +
    nTupleLooseMuons +
    nTupleElectrons +
    nTupleMuons +
#     nTupleQCDElectrons +
#     nTupleQCDMuons +
    nTupleVertices
    )

saveNTuplesSkim = cms.untracked.vstring(
    'drop *',
#    'keep *_nTupleGenerator_*_*',
    'keep *_PDFInfo_*_*',
    
    'keep *_cFlavorHistoryProducer_*_*',
    'keep *_bFlavorHistoryProducer_*_*',

    'keep floats_nTupleAllJets_*_*',
    'keep floats_nTuplePatMETsPF_*_*',
    'keep floats_nTupleTopJetsPF_*_*',
    'keep *_UnclusteredMETPF_*_*',
    'keep *_NVertices_*_*',
    'keep floats_nTuplePatType1METsPF_*_*',
    'keep *_UnclusteredType1METPF_*_*',
    'keep *_genJetsPF_*_*',
    'keep *_nTupleVertices_*_*',
    'keep *_kt6PFJetsForIsolation_rho_*',
         )



saveNTuplesSkimMu = cms.untracked.vstring(saveNTuplesSkim)
saveNTuplesSkimEle = cms.untracked.vstring(saveNTuplesSkim)

saveNTuplesSkimLoose = cms.untracked.vstring(saveNTuplesSkim)

saveNTuplesSkimMu.append('keep floats_nTupleMuons_*_*')
saveNTuplesSkimEle.append('keep floats_nTupleElectrons_*_*')


##Skimmed Ntuple
saveNTuplesSkimLoose.append('keep floats_nTupleMuons_*_*')
saveNTuplesSkimLoose.append('keep floats_nTupleElectrons_*_*')

# saveNTuplesSkimLoose.append('keep floats_nTupleAllMuons_*_*')
# saveNTuplesSkimLoose.append('keep floats_nTupleAllElectrons_*_*')

# saveNTuplesSkimLoose.append('keep floats_nTupleLooseMuons_*_*')
# saveNTuplesSkimLoose.append('keep floats_nTupleLooseElectrons_*_*')
# saveNTuplesSkimLoose.append('keep floats_nTupleLooseElectronsEle_*_*')
#saveNTuplesSkimLoose.append('keep floats_nTupleZVetoElectrons_*_*')

# saveNTuplesSkimLoose.append('keep floats_nTupleQCDMuons_*_*')
# saveNTuplesSkimLoose.append('keep floats_nTupleQCDElectrons_*_*')
  

saveNTuplesSkimLoose.append('keep *_TriggerResults_*_*')


