import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.jetTools import *


def run35xOn31xMC(process,
                  jetSrc = cms.InputTag("antikt5CaloJets"),
                  jetIdTag = "antikt5"):
    addJetID(process,jetSrc,jetIdTag) #Comment this line to run on 3_5_1
    #addJetID(process,"antikt5CaloJets",jetIdTag) #Un-comment this line to run on 3_5_1 
    switchJetCollection(process,
                        cms.InputTag('antikt5CaloJets'),
                        doJTA                 = True,
                        doBTagging            = True,
                        jetCorrLabel          = ('AK5','Calo'),
                        doType1MET            = True,
                        genJetCollection      = cms.InputTag("antikt5GenJets"),
                        doJetID               = True,
                        jetIdLabel            = "antikt5",
                        )
