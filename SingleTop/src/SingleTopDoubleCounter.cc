// Orso Iorio, INFN Napoli 
//
//

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopDoubleCounter.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"

SingleTopDoubleCounter::SingleTopDoubleCounter(const edm::ParameterSet& iConfig){

  src_ = iConfig.getParameter<edm::InputTag>("src"); 
  min_ = iConfig.getUntrackedParameter<int>("min"); 
  max_ = iConfig.getUntrackedParameter<int>("max"); 

}


bool SingleTopDoubleCounter::filter( edm::Event& iEvent, const edm::EventSetup& iSetup){

  edm::Handle<std::vector<float> > src ;
  iEvent.getByLabel(src_, src);
  //  
  //  if(src->failedToGet())return false;
  
  if( ((int)src->size() < max_) && ((int)src->size() >= min_))return true;
  
  return false;

}

SingleTopDoubleCounter::~SingleTopDoubleCounter(){}

DEFINE_FWK_MODULE(SingleTopDoubleCounter);
