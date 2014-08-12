/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopUnclusteredMETProducer.cc,v 1.1.2.1 2011/09/20 13:36:21 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

#include "DataFormats/Candidate/interface/CandAssociation.h"

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopUnclusteredMETProducer.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopUnclusteredMETProducer::SingleTopUnclusteredMETProducer(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  
  metSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "metSource" );
  jetsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "jetsSource" );
  electronsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "electronsSource" );
  muonsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "muonsSource" );
 
  
  //produces<std::vector< pat::TopLeptonic > >();
  produces< double >("UnclusteredMETPx");
  produces< double >("UnclusteredMETPy");
 
}

void SingleTopUnclusteredMETProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){
  
  
  iEvent.getByLabel(metSrc_,met);
  iEvent.getByLabel(jetsSrc_,jets);
  iEvent.getByLabel(electronsSrc_,electrons);
  iEvent.getByLabel(muonsSrc_,muons);
  
  double px_ = -9999;
  double py_ = -9999;
  
  if(met->size()!=1)std::cout<<" not exactly 1 met: possible problem in configuration, metx mety put to dummy values -9999 "<<std::endl; 
  else {
    px_=met->at(0).px();
    py_=met->at(0).py();
  }

  
  for(size_t j = 0; j < jets->size(); ++j){
    px_ +=jets->at(j).px() ;
    py_ +=jets->at(j).py() ;
  }  

  for(size_t m = 0; m < muons->size(); ++m){
    px_ +=muons->at(m).px() ;
    py_ +=muons->at(m).py() ;
  }
  for(size_t e = 0; e < electrons->size(); ++e){
    px_ +=electrons->at(e).px() ;
    py_ +=electrons->at(e).py() ;
  }
  
  std::auto_ptr< double > px(new double( px_) ), py(new double(py_) );
  
  iEvent.put(px,"UnclusteredMETPx");
  iEvent.put(py,"UnclusteredMETPy");
}

SingleTopUnclusteredMETProducer::~SingleTopUnclusteredMETProducer(){;}


DEFINE_FWK_MODULE( SingleTopUnclusteredMETProducer );
