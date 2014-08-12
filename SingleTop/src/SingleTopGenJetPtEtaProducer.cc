/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopGenJetPtEtaProducer.cc,v 1.1.2.1.8.1 2012/11/21 17:43:50 dnoonan Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

#include "DataFormats/Candidate/interface/CandAssociation.h"

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopGenJetPtEtaProducer.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopGenJetPtEtaProducer::SingleTopGenJetPtEtaProducer(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  
  jetsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "jetsSource" );
 
  
  //produces<std::vector< pat::TopLeptonic > >();
  produces<std::vector< double> >("genJetsPt");
  produces<std::vector< double> >("genJetsEta");
 
}

void SingleTopGenJetPtEtaProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){
  
  
  iEvent.getByLabel(jetsSrc_,jets);
  
  std::vector< double > *pt_ = new std::vector<double>;
  std::vector< double > *eta_ = new std::vector<double>;
  
  
  for(size_t j = 0; j < jets->size(); ++j){
    if(jets->at(j).genJet()!=0){
//       std::cout << "JET PT " << j << "  " <<jets->at(j).pt() << std::endl;  //COMMENT OUT LATER
//       std::cout << "GEN JET PT " << j << "  " <<jets->at(j).genJet()->pt() << std::endl;
//       std::cout << "JET ETA " << j << "  " <<jets->at(j).eta() << std::endl;
//       std::cout << "GEN JET ETA " << j << "  " <<jets->at(j).genJet()->eta() << std::endl;
      pt_->push_back(jets->at(j).genJet()->pt()) ;
      eta_->push_back(jets->at(j).genJet()->eta()) ;
    }
    else{
      pt_->push_back(-1.);//Unphisical value!
      eta_->push_back( -111.);//Unrealistic value outside detector acceptance!
    }

  }  


    
  std::auto_ptr< std::vector<double> > pt( pt_ ), eta(eta_) ;
  
  iEvent.put(pt,"genJetsPt");
  iEvent.put(eta,"genJetsEta");
}

SingleTopGenJetPtEtaProducer::~SingleTopGenJetPtEtaProducer(){;}


DEFINE_FWK_MODULE( SingleTopGenJetPtEtaProducer );
