import FWCore.ParameterSet.Config as cms

#lumiMu = cms.untracked.double(869.129366562)
lumiMu = cms.untracked.double(1078.75640263)
#lumiEle = cms.untracked.double(191.091)
lumiEle = cms.untracked.double(887.239)

TChannelMu = cms.PSet(
    crossSection = cms.untracked.double(20.93),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(480000),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    )


TChannelEle = cms.PSet(
    crossSection = cms.untracked.double(20.93),
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(480000),
    finalLumi = lumiEle,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    mcPUFile = cms.untracked.string("pileupdistr_TChannel.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTChannel"),
    )

TWChannelMu = cms.PSet(
        crossSection = cms.untracked.double(10.6),
            channel = cms.untracked.string("TWChannel"),
#            originalEvents = cms.untracked.double(494961),
            originalEvents = cms.untracked.double(409417),
            finalLumi = lumiMu,
            MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
            RelIsoCut = cms.untracked.double(0.1),
        mcPUFile = cms.untracked.string("pileupdistr_TWChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpTWChannel"),
            )

TWChannelEle = cms.PSet(
        crossSection = cms.untracked.double(10.6),
            channel = cms.untracked.string("TWChannel"),
            finalLumi = lumiEle,
            originalEvents = cms.untracked.double(409417),
#            originalEvents = cms.untracked.double(494961),
        mcPUFile = cms.untracked.string("pileupdistr_TWChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpTWChannel"),

            )

SChannelMu = cms.PSet(
            crossSection = cms.untracked.double(1.533),
                        channel = cms.untracked.string("SChannel"),
                        originalEvents = cms.untracked.double(494967),
                        finalLumi = lumiMu,
                        MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
                        RelIsoCut = cms.untracked.double(0.1),
            mcPUFile = cms.untracked.string("pileupdistr_SChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpSChannel"),
                        )

SChannelEle = cms.PSet(
            crossSection = cms.untracked.double(1.533),
                        channel = cms.untracked.string("SChannel"),
                        finalLumi = lumiEle,
                        originalEvents = cms.untracked.double(494967),
            mcPUFile = cms.untracked.string("pileupdistr_SChannel.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpSChannel"),

                        )
  

ZJetsMu = cms.PSet(
    crossSection = cms.untracked.double(3048),
    channel = cms.untracked.string("ZJets"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2595097),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
)


ZJetsEle = cms.PSet(
    crossSection = cms.untracked.double(3048),
    channel = cms.untracked.string("ZJets"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2595097),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )

WJetsMu = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
)


WJetsEle = cms.PSet(
    crossSection = cms.untracked.double(31314),
    channel = cms.untracked.string("WJets"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )
  


WJets_wlightMu = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wlight"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )


WJets_wlightEle = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wlight"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )
  


WJets_wccMu = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wcc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )


WJets_wccEle = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wcc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )

WJets_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wbb"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(14800000),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )
WJets_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(24170),
    channel = cms.untracked.string("WJets_wbb"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(14800000),
    mcPUFile = cms.untracked.string("pileupdistr_WJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWJets"),
    )
  


#Z


ZJets_wlightMu = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wlight"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2543706),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )


ZJets_wlightEle = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wlight"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2543706),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )
  


ZJets_wccMu = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wcc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2543706),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )


ZJets_wccEle = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wcc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2543706),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )

ZJets_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wbb"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2543706),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )
ZJets_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(2321),
    channel = cms.untracked.string("ZJets_wbb"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2543706),
    mcPUFile = cms.untracked.string("pileupdistr_ZJets.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpZJets"),
    )
  





Vqq_wbbMu = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wbb"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )


Vqq_wbbEle = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wbb"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )
  

Vqq_wccMu = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wcc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )


Vqq_wccEle = cms.PSet(
    crossSection = cms.untracked.double(36),
    channel = cms.untracked.string("Vqq_wcc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(740488),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_Vqq.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVqq"),
    )
  


Wc_wcMu = cms.PSet(
    crossSection = cms.untracked.double(606),
    channel = cms.untracked.string("Wc_wc"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(2792637),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_Wc.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWc"),
    )

Wc_wcEle = cms.PSet(
    crossSection = cms.untracked.double(606),
    channel = cms.untracked.string("Wc_wc"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2792637),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_Wc.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpWc"),
    )
  

VVMu = cms.PSet(
    crossSection = cms.untracked.double(4.8),
    channel = cms.untracked.string("VV"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(963356),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_VV.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVV"),
    )

VVEle = cms.PSet(
    crossSection = cms.untracked.double(4.8),
    channel = cms.untracked.string("VV"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(963356),
    MTWCut = cms.untracked.double(50.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_VV.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVV"),
    )
  

TTBarMu = cms.PSet(
    crossSection = cms.untracked.double(150.),
    channel = cms.untracked.string("TTBar"),
#    originalEvents = cms.untracked.double(1100000),
#    originalEvents = cms.untracked.double(1014208),
    originalEvents = cms.untracked.double(924208),
    finalLumi = lumiMu,
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_TTBar.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar"),
    )

TTBarEle = cms.PSet(
    crossSection = cms.untracked.double(150.),
    channel = cms.untracked.string("TTBar"),
    finalLumi = lumiEle,
#    originalEvents = cms.untracked.double(1014208),
    originalEvents = cms.untracked.double(924208),
#    originalEvents = cms.untracked.double(1100000),
    mcPUFile = cms.untracked.string("pileupdistr_TTBar.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpTTBar"),
    )
    

DataMu = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(-1),
    MTWCut = cms.untracked.double(40.0),#Default 50.0 GeV
    RelIsoCut = cms.untracked.double(0.1),
    mcPUFile = cms.untracked.string("pileupdistr_VV.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVV"),
    )

DataEle = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(-1),
    mcPUFile = cms.untracked.string("pileupdistr_VV.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpVV"),
    )


#QCDQCD_Pt_20to30_EMEnriched = cms.PSet(
#    crossSection = cms.untracked.double(2454400.),
#    channel = cms.untracked.string("QCD"),
#    finalLumi = lumiEle,
#    originalEvents = cms.untracked.double(1100000),
#    )

QCD_Pt_30to80_EMEnrichedEle = cms.PSet(
    crossSection = cms.untracked.double(3866200.),
    channel = cms.untracked.string("QCD_Pt_30to80_EMEnriched"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(70708892),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-30to80_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-30to80_EMEnriched"),
    )

QCD_Pt_30to80_EMEnrichedMu = cms.PSet(
        crossSection = cms.untracked.double(3866200.),
            channel = cms.untracked.string("QCD_Pt_30to80_EMEnriched"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(70708892),
        mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-30to80_EMEnriched.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-30to80_EMEnriched"),
            )


QCD_Pt_80to170_EMEnrichedEle = cms.PSet(
    crossSection = cms.untracked.double(139500.),
    channel = cms.untracked.string("QCD_Pt_80to170_EMEnriched"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(8069591),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-80to170_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-80to170_EMEnriched"),
    )

QCD_Pt_80to170_EMEnrichedMu = cms.PSet(
        crossSection = cms.untracked.double(139500.),
            channel = cms.untracked.string("QCD_Pt_80to170_EMEnriched"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(8069591),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-80to170_EMEnriched.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-80to170_EMEnriched"),
            )



QCD_Pt_20to30_BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(132160.),
    channel = cms.untracked.string("QCD_Pt_20to30_BCtoE"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1993439),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-20to30_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-20to30_BCtoE"),
    )

QCD_Pt_20to30_BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(132160.),
            channel = cms.untracked.string("QCD_Pt_20to30_BCtoE"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1993439),
        mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-20to30_BCtoE.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-20to30_BCtoE"),
            )


QCD_Pt_30to80_BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(136804.),
    channel = cms.untracked.string("QCD_Pt_30to80_BCtoE"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1795502),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-30to80_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-30to80_BCtoE"),
    )

QCD_Pt_30to80_BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(136804.),
            channel = cms.untracked.string("QCD_Pt_30to80_BCtoE"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1795502),
        mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-30to80_BCtoE.root"),
        puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-30to80_BCtoE"),
            )


QCD_Pt_80to170_BCtoEEle = cms.PSet(
    crossSection = cms.untracked.double(9360.),
    channel = cms.untracked.string("QCD_Pt_80to170_BCtoE"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1043390),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-80to170_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-80to170_BCtoE"),
    )

QCD_Pt_80to170_BCtoEMu = cms.PSet(
        crossSection = cms.untracked.double(9360.),
            channel = cms.untracked.string("QCD_Pt_80to170_BCtoE"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1043390),
    mcPUFile = cms.untracked.string("pileupdistr_QCD_Pt-80to170_BCtoE.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCD_Pt-80to170_BCtoE"),
            )


HT_40To100Ele = cms.PSet(
    crossSection = cms.untracked.double(23620.),
    channel = cms.untracked.string("HT_40To100"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(2217101),
    mcPUFile = cms.untracked.string("pileupdistr_HT_40To100.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpHT_40To100"),
    )

HT_40To100Mu = cms.PSet(
        crossSection = cms.untracked.double(23620.),
        channel = cms.untracked.string("HT_40To100"),
        finalLumi = lumiMu,
        originalEvents = cms.untracked.double(2217101),
    mcPUFile = cms.untracked.string("pileupdistr_HT_40To100.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpHT_40To100"),
        )



HT_100to200Ele = cms.PSet(
    crossSection = cms.untracked.double(3476.),
    channel = cms.untracked.string("HT_100to200"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(1065691),
    mcPUFile = cms.untracked.string("pileupdistr_HT_100To200.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpHT_100To200"),
    )

HT_100to200Mu = cms.PSet(
        crossSection = cms.untracked.double(3476.),
            channel = cms.untracked.string("HT_100to200"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(1065691),
    mcPUFile = cms.untracked.string("pileupdistr_HT_100To200.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpHT_100To200"),
            )


HT_200Ele = cms.PSet(
    crossSection = cms.untracked.double(485.),
    channel = cms.untracked.string("HT_200"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(942171), 
    mcPUFile = cms.untracked.string("pileupdistr_HT_200.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpHT_200"),
   )

HT_200Mu = cms.PSet(
        crossSection = cms.untracked.double(485.),
            channel = cms.untracked.string("HT_200"),
            finalLumi = lumiMu,
            originalEvents = cms.untracked.double(942171),
    mcPUFile = cms.untracked.string("pileupdistr_HT_200.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpHT_200"),
            )


QCDMuMu = cms.PSet(
    crossSection = cms.untracked.double(84679.),
    channel = cms.untracked.string("QCDMu"),
    finalLumi = lumiMu,
    originalEvents = cms.untracked.double(29434562),
    mcPUFile = cms.untracked.string("pileupdistr_QCDMu.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCDMu"),
    )


QCDMuEle = cms.PSet(
    crossSection = cms.untracked.double(84679.),
    channel = cms.untracked.string("QCDMu"),
    finalLumi = lumiEle,
    originalEvents = cms.untracked.double(29434562),
    mcPUFile = cms.untracked.string("pileupdistr_QCDMu.root"),
    puHistoName = cms.untracked.string("pileUpDumper/PileUpQCDMu"),
    )

