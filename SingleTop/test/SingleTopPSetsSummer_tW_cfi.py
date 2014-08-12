import FWCore.ParameterSet.Config as cms


lumiA = cms.untracked.double(15000.)
lumiB = cms.untracked.double(15000.)
lumiC = cms.untracked.double(15000.)
lumiD = cms.untracked.double(15000.)
lumiMu = cms.untracked.double(1)
lumiEle = cms.untracked.double(1)


PileUpSeason = "Summer12"
PileUpSeasonV6 = "Summer12V6"
PileUpSeason53X = "Summer12_53X"

tW_XSec = cms.untracked.double(11.1)
tbarW_XSec = cms.untracked.double(11.1)
ttbar_XSec = cms.untracked.double(245.8)
tChan_XSec = cms.untracked.double(56.4)
tbarChan_XSec = cms.untracked.double(30.7)
sChan_XSec = cms.untracked.double(3.79)
sbarChan_XSec = cms.untracked.double(1.76)
ww_XSec = cms.untracked.double(54.838)
wz_XSec = cms.untracked.double(22.44)
zz_XSec = cms.untracked.double(9.03)
zjets_XSec = cms.untracked.double(3532.8)
zjetslowmll_XSec = cms.untracked.double(860.5)
wjets_XSec = cms.untracked.double(36257.2)

tW_XSecDilep = cms.untracked.double(11.1*0.105)
tbarW_XSecDilep = cms.untracked.double(11.1*0.105)
ttbar_XSecDilep = cms.untracked.double(245.8*0.105)

tW_XSecSemilep = cms.untracked.double(11.1*0.219)
tbarW_XSecSemilep = cms.untracked.double(11.1*0.219)

TWChannel = cms.PSet(
    crossSection = tW_XSec,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(497658),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TbarWChannel = cms.PSet(
    crossSection = tbarW_XSec,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(493460),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar"),
    originalEvents = cms.untracked.double(6923750),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBarSpin = cms.PSet(
    crossSection = ttbar_XSecDilep,
    channel = cms.untracked.string("TTBarSpin"),
    originalEvents = cms.untracked.double(12019013),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBarPowheg = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBarPowheg"),
    originalEvents = cms.untracked.double(6474753),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

    
Data = cms.PSet(
    crossSection = cms.untracked.double(-1),
    channel = cms.untracked.string("Data"),
    originalEvents = cms.untracked.double(-1),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    )



TChannel = cms.PSet(
#    crossSection = cms.untracked.double(56.4),
    crossSection = tChan_XSec,
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(3758227),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )
    
    
TbarChannel = cms.PSet(
#    crossSection = cms.untracked.double(30.7),
    crossSection = tbarChan_XSec,
    channel = cms.untracked.string("TChannel"),
    originalEvents = cms.untracked.double(1935072),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

SChannel = cms.PSet(
#    crossSection = cms.untracked.double(3.79),
    crossSection = sChan_XSec,
    channel = cms.untracked.string("SChannel"),
    originalEvents = cms.untracked.double(259961),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

SbarChannel = cms.PSet(
#    crossSection = cms.untracked.double(1.76),
    crossSection = sbarChan_XSec,
    channel = cms.untracked.string("SChannel"),
    originalEvents = cms.untracked.double(139974),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

ZJets = cms.PSet(
#    crossSection = cms.untracked.double(3503.71),
    crossSection = zjets_XSec,
    channel = cms.untracked.string("ZJets"),
    originalEvents = cms.untracked.double(30459503),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

ZJetsLowMass = cms.PSet(
#    crossSection = cms.untracked.double(3503.71),
    crossSection = zjetslowmll_XSec,
    channel = cms.untracked.string("ZJets"),
    originalEvents = cms.untracked.double(7132223),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )


WJets = cms.PSet(
#    crossSection = cms.untracked.double(36257.2),
    crossSection = wjets_XSec,
    channel = cms.untracked.string("WJets"),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(57509905),
    )

  
WW = cms.PSet(
#    crossSection = cms.untracked.double(57.1097),
    crossSection = ww_XSec,
    channel = cms.untracked.string("WW"),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(10000431),
    )


ZZ = cms.PSet(
#    crossSection = cms.untracked.double(8.25561),
    crossSection = zz_XSec,
    channel = cms.untracked.string("ZZ"),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(9799908),
    )


WZ = cms.PSet(
#    crossSection = cms.untracked.double(32.3161),
    crossSection = wz_XSec,
    channel = cms.untracked.string("WZ"),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    originalEvents = cms.untracked.double(10000283),
    )



#Special Training samples

TWChannelDilepton = cms.PSet(
    crossSection = tW_XSecDilep,
    channel = cms.untracked.string("TWChannelDilepton"),
    originalEvents = cms.untracked.double(2976510),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannelDilepton = cms.PSet(
    crossSection = tbarW_XSecDilep,
    channel = cms.untracked.string("TWChannelDilepton"),
    originalEvents = cms.untracked.double(2971482),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannelDilepton_5 = cms.PSet(
    crossSection = cms.untracked.double(11.1*0.105*1522306./310849.),
    channel = cms.untracked.string("TWChannelDilepton"),
    originalEvents = cms.untracked.double(2976510),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannelDilepton_5 = cms.PSet(
    crossSection = cms.untracked.double(11.1*0.105*1517324./312201.),
    channel = cms.untracked.string("TWChannelDilepton"),
    originalEvents = cms.untracked.double(2971482),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TWChannelSemilepton1 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannelSemilepton"),
    originalEvents = cms.untracked.double(1457622),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )
TWChannelSemilepton2 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannelSemilepton"),
    originalEvents = cms.untracked.double(1490110),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannelSemilepton1 = cms.PSet(
    crossSection = tbarW_XSecSemilep,
    channel = cms.untracked.string("TWChannelSemilepton"),
    originalEvents = cms.untracked.double(1492919),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )
TbarWChannelSemilepton2 = cms.PSet(
    crossSection = tbarW_XSecSemilep,
    channel = cms.untracked.string("TWChannelSemilepton"),
    originalEvents = cms.untracked.double(1466488),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TTBarDilepton = cms.PSet(
    crossSection = ttbar_XSecDilep,
    channel = cms.untracked.string("TTBarDilepton"),
    originalEvents = cms.untracked.double(10783509),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TestSample = cms.PSet(
    crossSection = cms.untracked.double(1.),
    channel = cms.untracked.string("TestSample"),
    originalEvents = cms.untracked.double(1.),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )



#Systs

TWChannel_DS = cms.PSet(
    crossSection = tW_XSecDilep,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(2970011),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_DS = cms.PSet(
    crossSection = tbarW_XSecDilep,
    channel = cms.untracked.string("TWChannel"),
    originalEvents = cms.untracked.double(2940594),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TWChannel_Q2Up = cms.PSet(
    crossSection = tW_XSecDilep,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(1492816),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannel_Q2Down = cms.PSet(
    crossSection = tW_XSecDilep,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(1493130),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2Up = cms.PSet(
    crossSection = tbarW_XSecDilep,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(1492534),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2Down = cms.PSet(
    crossSection = tbarW_XSecDilep,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(1493101),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Q2Up = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Q2Up"),
    originalEvents = cms.untracked.double(5009488),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Q2Down = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Q2Down"),
    originalEvents = cms.untracked.double(5387181),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingUp = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingUp"),
    originalEvents = cms.untracked.double(5415010),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingDown = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingDown"),
    originalEvents = cms.untracked.double(5476728),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_TopMassDown = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_TopMassDown"),
    originalEvents = cms.untracked.double(4469095),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_TopMassUp = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_TopMassUp"),
    originalEvents = cms.untracked.double(4733483),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannel_TopMassDown = cms.PSet(
    crossSection = tW_XSecDilep,
    channel = cms.untracked.string("TWChannel_TopMassDown"),
    originalEvents = cms.untracked.double(1489880),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_TopMassDown = cms.PSet(
    crossSection = tbarW_XSecDilep,
    channel = cms.untracked.string("TWChannel_TopMassDown"),
    originalEvents = cms.untracked.double(1478200),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannel_TopMassUp = cms.PSet(
    crossSection = tW_XSecDilep,
    channel = cms.untracked.string("TWChannel_TopMassUp"),
    originalEvents = cms.untracked.double(1493428),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_TopMassUp = cms.PSet(
    crossSection = tbarW_XSecDilep,
    channel = cms.untracked.string("TWChannel_TopMassUp"),
    originalEvents = cms.untracked.double(1493389),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )


TWChannel_Q2UpSemiLep1 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(442237),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannel_Q2UpSemiLep2 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(455270),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannel_Q2DownSemiLep1 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(453233),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TWChannel_Q2DownSemiLep2 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(496818),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2UpSemiLep1 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(497376),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2UpSemiLep2 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Up"),
    originalEvents = cms.untracked.double(497676),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2DownSemiLep1 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(497674),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TbarWChannel_Q2DownSemiLep2 = cms.PSet(
    crossSection = tW_XSecSemilep,
    channel = cms.untracked.string("TWChannel_Q2Down"),
    originalEvents = cms.untracked.double(497682),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBarNew = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar"),
    originalEvents = cms.untracked.double(62081965),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingDown_New = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingDown"),
    originalEvents = cms.untracked.double(13406551+20596562),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingDown_New1 = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingDown"),
    originalEvents = cms.untracked.double(13406551),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingDown_New2 = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingDown"),
    originalEvents = cms.untracked.double(20596562),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_MatchingUp_New = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_MatchingUp"),
    originalEvents = cms.untracked.double(37083003),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Q2Down_New = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Q2Down"),
    originalEvents = cms.untracked.double(38386663),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_Q2Up_New = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_Q2Up"),
    originalEvents = cms.untracked.double(41858271),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_TopMassDown_New = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_TopMassDown"),
    originalEvents = cms.untracked.double(27078777),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )

TTBar_TopMassUp_New = cms.PSet(
    crossSection = ttbar_XSec,
    channel = cms.untracked.string("TTBar_TopMassUp"),
    originalEvents = cms.untracked.double(24309161),
    finalLumi = cms.untracked.double(1.),
    finalLumiA = lumiA, finalLumiB = lumiB, finalLumiC = lumiC, finalLumiD = lumiD,
    Season = cms.untracked.string(PileUpSeason53X),
    )


