// Orso Iorio, INFN Napoli 
//
//

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopDoubleFilter.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"

SingleTopDoubleFilter::SingleTopDoubleFilter(const edm::ParameterSet& iConfig){

  src_ = iConfig.getParameter<edm::InputTag>("src"); 
  min_ = iConfig.getUntrackedParameter<double>("min"); 
  max_ = iConfig.getUntrackedParameter<double>("max"); 

}


bool SingleTopDoubleFilter::filter( edm::Event& iEvent, const edm::EventSetup& iSetup){

  edm::Handle<std::vector<double> > src ;
  iEvent.getByLabel(src_, src);
  
  
  for(std::vector<double>::const_iterator it = src->begin();it != src->end();++it){
    if( (*it < max_) && (*it > min_))return true;
  }
  return false;

}

SingleTopDoubleFilter::~SingleTopDoubleFilter(){}

DEFINE_FWK_MODULE(SingleTopDoubleFilter);
