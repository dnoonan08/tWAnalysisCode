/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopPileUpWeighter.cc,v 1.1.2.1 2011/07/11 07:05:50 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

#include "DataFormats/Candidate/interface/CandAssociation.h"

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopPileUpWeighter.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopPileUpWeighter::SingleTopPileUpWeighter(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  
  
  syncPU_ =  iConfig.getParameter< edm::InputTag >("syncPU");
  
  dataPUFile_ =  iConfig.getUntrackedParameter< std::string >("dataPUFile","pileUpDistr.root");
  mcPUFile_ = iConfig.getUntrackedParameter< std::string >("mcPUFile","pileupdistr_TChannel.root");
  puHistoName_ = iConfig.getUntrackedParameter< std::string >("puHistoName","pileUpDumper/PileUp");
  
  doPU_ = iConfig.getUntrackedParameter< bool >("doPU",true);

  if(doPU_){
    LumiWeights_ = edm::LumiReWeighting(mcPUFile_,
					dataPUFile_,
					puHistoName_,
					std::string("pileup") );
  }
  
  produces< double >("PUWeight");
}

void SingleTopPileUpWeighter::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){

  double w = 1.;
  
  if(doPU_){
  
    iEvent.getByLabel(syncPU_,syncPU);
    int p = *syncPU;
    
    w = LumiWeights_.weight(p);
  }
  
  std::auto_ptr< double > wn(new double( w) );
  iEvent.put(wn,"PUWeight");

}

SingleTopPileUpWeighter::~SingleTopPileUpWeighter(){;}


DEFINE_FWK_MODULE( SingleTopPileUpWeighter );
