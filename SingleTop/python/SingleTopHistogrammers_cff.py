import FWCore.ParameterSet.Config as cms

pre_cuts_top_histos = cms.EDAnalyzer('SingleTopAnalyzer', 
                                   electronProducer = cms.InputTag("selectedPatElectrons"),
                                   muonProducer     = cms.InputTag("selectedPatMuons"),
                                   jetProducer      = cms.InputTag("selectedPatJets"),
                                   metProducer      = cms.InputTag("preselectedMETs"),
                                   topProducer      = cms.InputTag("recoTops"),
                                   MCLeptonProducer   = cms.InputTag("MCTruthParticles","topLeptons"),
                                   MCJetProducer      = cms.InputTag("MCTruthParticles","bGenJets"),
                                   MCNeutrinoProducer = cms.InputTag("MCTruthParticles","topNeutrinos"),
                                   topNeutrinos   = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   bJetProducer = cms.InputTag("bJets"),
                                   nonBJetProducer = cms.InputTag("antiBJets"),

                                   forwardJetProducer =cms.InputTag("forwardJets"),
                                   MCBQuarkProducer = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   MCLightQuarkProducer = cms.InputTag("MCTruthParticles","singleTopRecoilQuark"),
                                     )



pre_cuts_clean_top_histos = cms.EDAnalyzer('SingleTopAnalyzer', 
                                   electronProducer = cms.InputTag("cleanPatElectrons"),
                                   muonProducer     = cms.InputTag("cleanPatMuons"),
                                   jetProducer      = cms.InputTag("cleanPatJets"),
                                   metProducer      = cms.InputTag("preselectedMETs"),
                                   topProducer      = cms.InputTag("recoTops"),
                                   MCLeptonProducer   = cms.InputTag("MCTruthParticles","topLeptons"),
                                   MCJetProducer      = cms.InputTag("MCTruthParticles","bGenJets"),
                                   MCNeutrinoProducer = cms.InputTag("MCTruthParticles","topNeutrinos"),
                                           
                                           bJetProducer = cms.InputTag("bJets"),
                                   nonBJetProducer = cms.InputTag("antiBJets"),

                                   forwardJetProducer =cms.InputTag("forwardJets"),
                                   MCBQuarkProducer = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   MCLightQuarkProducer = cms.InputTag("MCTruthParticles","singleTopRecoilQuark"),
                                     )


preselection_cuts_top_histos = cms.EDAnalyzer('SingleTopAnalyzer', 
                                   electronProducer = cms.InputTag("preselectedElectrons"),
                                   muonProducer     = cms.InputTag("preselectedMuons"),

                                   jetProducer      = cms.InputTag("preselectedJets"),
                                   metProducer      = cms.InputTag("preselectedMETs"),
                                   topProducer      = cms.InputTag("recoTops"),
                                   MCLeptonProducer   = cms.InputTag("MCTruthParticles","topLeptons"),
                                   MCJetProducer      = cms.InputTag("MCTruthParticles","bGenJets"),
                                   MCNeutrinoProducer = cms.InputTag("MCTruthParticles","topNeutrinos"),
                                   MCBquarkProducer   = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   bJetProducer = cms.InputTag("bJets"),
                                   nonBJetProducer = cms.InputTag("antiBJets"),
                                   forwardJetProducer =cms.InputTag("forwardJets"),
                                   MCBQuarkProducer = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   MCLightQuarkProducer = cms.InputTag("MCTruthParticles","singleTopRecoilQuark"),


                                   )


leptons_cuts_top_histos = cms.EDAnalyzer('SingleTopAnalyzer', 
                                   electronProducer = cms.InputTag("topElectrons"),
                                   muonProducer     = cms.InputTag("topMuons"),
                                   jetProducer      = cms.InputTag("topJets"),
                                   metProducer      = cms.InputTag("preselectedMETs"),
                                   topProducer      = cms.InputTag("recoTops"),
                                   MCLeptonProducer   = cms.InputTag("MCTruthParticles","topLeptons"),
                                   MCJetProducer      = cms.InputTag("MCTruthParticles","bGenJets"),
                                   MCNeutrinoProducer = cms.InputTag("MCTruthParticles","topNeutrinos"),
                                   MCBquarkProducer   = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   bJetProducer = cms.InputTag("bJets"),
                                   nonBJetProducer = cms.InputTag("antiBJets"),
                                   forwardJetProducer =cms.InputTag("forwardJets"),
                                   MCBQuarkProducer = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   MCLightQuarkProducer = cms.InputTag("MCTruthParticles","singleTopRecoilQuark"),

                                   )


jets_cuts_top_histos = cms.EDAnalyzer('SingleTopAnalyzer', 
                                   electronProducer = cms.InputTag("topElectrons"),
                                   muonProducer     = cms.InputTag("topMuons"),
                                   jetProducer      = cms.InputTag("preselectedJets"),
                                   metProducer      = cms.InputTag("preselectedMETs"),
                                   topProducer      = cms.InputTag("recoTops"),
                                   MCLeptonProducer   = cms.InputTag("MCTruthParticles","topLeptons"),
                                   MCJetProducer      = cms.InputTag("MCTruthParticles","bGenJets"),
                                   MCNeutrinoProducer = cms.InputTag("MCTruthParticles","topNeutrinos"),
                                   MCBquarkProducer   = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   bJetProducer = cms.InputTag("bJets"),
                                   nonBJetProducer = cms.InputTag("antiBJets"),
                                   forwardJetProducer =cms.InputTag("forwardJets"),
                                   MCBQuarkProducer = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   MCLightQuarkProducer = cms.InputTag("MCTruthParticles","singleTopRecoilQuark"),
                                   )

final_cuts_top_histos = cms.EDAnalyzer('SingleTopAnalyzer', 
                                   electronProducer = cms.InputTag("topElectrons"),
                                   muonProducer     = cms.InputTag("topMuons"),
                                   jetProducer      = cms.InputTag("preselectedJets"),
                                   metProducer      = cms.InputTag("preselectedMETs"),
                                   topProducer      = cms.InputTag("recoTops"),
                                   MCLeptonProducer   = cms.InputTag("MCTruthParticles","topLeptons"),
                                   MCJetProducer      = cms.InputTag("MCTruthParticles","bGenJets"),
                                   MCNeutrinoProducer = cms.InputTag("MCTruthParticles","topNeutrinos"),
                                   MCBquarkProducer   = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   bJetProducer = cms.InputTag("bJets"),
                                   nonBJetProducer = cms.InputTag("antiBJets"),
                                   forwardJetProducer =cms.InputTag("forwardJets"),
                                   MCBQuarkProducer = cms.InputTag("MCTruthParticles","bGenParticles"),
                                   MCLightQuarkProducer = cms.InputTag("MCTruthParticles","singleTopRecoilQuark"),

                                   )
