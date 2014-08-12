import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTopSystematics")


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data
process.GlobalTag.globaltag = cms.string("START53_V7::All")



#Load B-Tag
#MC measurements from 36X
#process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDBMC36X")
#process.load ("RecoBTag.PerformanceDB.BTagPerformanceDBMC36X")
##Measurements from Fall10
#process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1011")
#process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1011")

#Spring11
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1107")
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1107")


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
# Process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(20000))

process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (*(
                             'file:INSERTFILENAME',
                             )),
                             duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
)


#Output
process.TFileService = cms.Service("TFileService", fileName = cms.string("output/ntuple_SysTrees_REPLACEROOTFILENAME.root"))
#process.TFileService = cms.Service("TFileService", fileName = cms.string("/mnt/hadoop/user/uscms01/pnfs/unl.edu/data4/cms/store/user/dnoonan/tW_8TeV/Ntuples/ntuple_SysTrees_REPLACEROOTFILENAME.root"))

process.load("SingleTopRootPlizer_tW_cfi")
process.load("SingleTopFilters_tW_cfi")
#from SingleTopPSets_cfi import *
#from SingleTopPSetsFall11_cfi import *
from SingleTopPSetsSummer_tW_cfi import *

process.TreesDileptontW.dataPUFile = cms.untracked.string("pileUpDistr.root")

process.TreesDileptontW.channelInfo = REPLACECHANNELNAME

channelName = 'REPLACECHANNELNAME'

# if 'Dilepton' in channelName:
#     process.TreesDileptontW.systematics = cms.untracked.vstring()

if 'TestSample' in channelName:
    process.TreesDileptontW.systematics = cms.untracked.vstring()


#doPU = cms.untracked.bool(False)

#process.WeightProducer.doPU = cms.untracked.bool(False)
#process.TreesMu.doQCD = cms.untracked.bool(False)
#process.TreesEle.doQCD = cms.untracked.bool(False)
#process.TreesMu.doResol = cms.untracked.bool(False)
#process.TreesEle.doResol = cms.untracked.bool(False)

#process.TreesMu.doPU = cms.untracked.bool(False)
#process.TreesEle.doPU = cms.untracked.bool(False)


#channel_instruction = "channel_instruction" #SWITCH_INSTRUCTION

channel_instruction = "allmc" #SWITCH_INSTRUCTION

MC_instruction = True # False #TRIGGER_INSTRUCTION

process.HLTFilterTWEleMu2012.isMC = MC_instruction
process.HLTFilterTWDoubleEle2012.isMC = MC_instruction
process.HLTFilterTWDoubleMu2012.isMC = MC_instruction
process.HLTFilterTWDilepton2012.isMC = MC_instruction
    

#process.PUWeightsPath = cms.Path(
#    process.WeightProducer 
#)

if channel_instruction == "allmc":
    #    process.TreesMu.doResol = cms.untracked.bool(True)
    #    process.TreesEle.doResol = cms.untracked.bool(True)
    #    process.TreesEle.doTurnOn = cms.untracked.bool(True) 
    process.PathSysAllTW = cms.Path(
    process.HLTFilterTWDilepton2012 *
    process.TreesDileptontW
    )

if channel_instruction == "data":
    process.TreesDileptontW.doResol = cms.untracked.bool(False)
    process.TreesDileptontW.doPU = cms.untracked.bool(False)
    process.TreesDileptontW.doGen = cms.untracked.bool(False)
    process.TreesDileptontW.systematics = cms.untracked.vstring()

    process.PathSysAllTW = cms.Path(
    process.HLTFilterTWDilepton2012 *
    process.TreesDileptontW
    )

if channel_instruction == "systSample":
    process.TreesDileptontW.doResol = cms.untracked.bool(True)
    process.TreesDileptontW.doPU = cms.untracked.bool(True)
    process.TreesDileptontW.systematics = cms.untracked.vstring()

    process.PathSysAllTW = cms.Path(
    process.HLTFilterTWDilepton2012 *
    process.TreesDileptontW
    )

