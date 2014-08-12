/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopTChanProducer.cc,v 1.1 2010/11/11 10:51:41 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

#include "PhysicsTools/PatAlgos/plugins/PATJetProducer.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Candidate/interface/CandAssociation.h"

#include "DataFormats/JetReco/interface/JetTracksAssociation.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/BTauReco/interface/TrackProbabilityTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackCountingTagInfo.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfo.h"

#include "DataFormats/Candidate/interface/CandMatchMap.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourMatching.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"


#include "FWCore/Framework/interface/Selector.h"



#include "TopQuarkAnalysis/SingleTop/interface/SingleTopTChanProducer.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopTChanProducer::SingleTopTChanProducer(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  
  topsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "topsSource" );
  lightJetsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "lightJetsSource" );
  
  
  //produces<std::vector< pat::TopLeptonic > >();
  produces<std::vector< reco::NamedCompositeCandidate > >();
 
}

void SingleTopTChanProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){
  
  
  edm::Handle<edm::View<pat::Jet> > lightJets;
  iEvent.getByLabel(lightJetsSrc_,lightJets);
  
  
  edm::Handle<edm::View<reco::NamedCompositeCandidate> > tops;
  iEvent.getByLabel(topsSrc_,tops);
  
  
  
  
  std::vector< reco::NamedCompositeCandidate > * eventCandidates = new std::vector<reco::NamedCompositeCandidate>();
  
  

  for(size_t i = 0; i < tops->size(); ++i){
    for(size_t j = 0; j < lightJets->size(); ++j){
  
      if(deltaR(*tops->at(i).daughter("BJet"),lightJets->at(j))<0.01)continue;
      
      reco::NamedCompositeCandidate eventCandidate;    
      eventCandidate.addDaughter(tops->at(i),"Top");
      eventCandidate.addDaughter(lightJets->at(j),"LightJet");

     
      eventCandidates->push_back(eventCandidate);
      
    }
  }

 
 std::auto_ptr< std::vector< reco::NamedCompositeCandidate > > finalEventCandidates(eventCandidates);
 
////////

//iEvent.put(newTopLeptonic);

iEvent.put(finalEventCandidates);

}

SingleTopTChanProducer::~SingleTopTChanProducer(){;}


DEFINE_FWK_MODULE( SingleTopTChanProducer );
