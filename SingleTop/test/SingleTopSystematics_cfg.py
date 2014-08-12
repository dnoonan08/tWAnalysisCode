import FWCore.ParameterSet.Config as cms

process = cms.Process("SingleTopSystematics")


process.load("FWCore.MessageLogger.MessageLogger_cfi")

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool(True),
    FailPath = cms.untracked.vstring('ProductNotFound','Type Mismatch')
    )

process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff") ### real data
process.GlobalTag.globaltag = cms.string("START39_V9::All")



#Load B-Tag
#MC measurements from 36X
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDBMC36X")
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDBMC36X")
##Measurements from Fall10
process.load ("RecoBTag.PerformanceDB.BTagPerformanceDB1011")
process.load ("RecoBTag.PerformanceDB.PoolBTagPerformanceDB1011")

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(2000) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.source = cms.Source ("PoolSource",
                             fileNames = cms.untracked.vstring (

'file:/tmp/oiorio/edmntuple_tchannel_big.root',

),
duplicateCheckMode = cms.untracked.string('noDuplicateCheck'),
#eventsToProcess = cms.untracked.VEventRange('1:19517967-1:19517969'),
)




#from TChannel import *
#process.source.fileNames = TChannel_ntuple

process.source.fileNames = cms.untracked.vstring("file:/tmp/oiorio/TChannelMerged.root")
#process.source.fileNames = cms.untracked.vstring("file:/tmp/oiorio/edmntuple_TChannel_noMeta.root")

#Output

process.TFileService = cms.Service("TFileService", fileName = cms.string("/tmp/oiorio/TChannel_a.root"))

process.load("SingleTopAnalyzers_cfi")
process.load("SingleTopRootPlizer_cfi")
process.load("SingleTopFilters_cfi")
from SingleTopPSets_cfi import *

process.TreesEle.channelInfo = TChannelEle
process.TreesMu.channelInfo = TChannelMu
process.PlotsEle.channelInfo = TChannelEle
process.PlotsMu.channelInfo = TChannelMu
#process.TreesMu.systematics = cms.untracked.vstring();


channel_instruction = "channel_instruction" #SWITCH_INSTRUCTION

MC = True #TRIGGER_INSTRUCTION
process.HLTFilterMu.isMC = MC
process.HLTFilterEle.isMC = MC
    
    
if channel_instruction == "all":
    process.PathSys = cms.Path(
        #    process.PlotsMu +
        #    process.PlotsEle +
        process.TreesMu +
        process.TreesEle
        )

if channel_instruction == "mu":
    process.PathSysMu = cms.Path(
        #    process.PlotsMu +
        #    process.PlotsEle +
        process.TreesMu 
        )

if channel_instruction == "ele":
    process.PathSysEle = cms.Path(
        #    process.PlotsMu +
        #    process.PlotsEle +
        process.TreesEle
        )
