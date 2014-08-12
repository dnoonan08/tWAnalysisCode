/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopBJetsProducer.cc,v 1.2 2010/11/08 08:26:42 oiorio Exp $ 
 */

// Single Top b producer: produces b tagged and anti-b tagged jet collections

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
#include "DataFormats/JetReco/interface/JPTJet.h"
#include "DataFormats/JetReco/interface/CaloJet.h"

#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"


#include "FWCore/Framework/interface/Selector.h"



#include "TopQuarkAnalysis/SingleTop/interface/SingleTopBJetsProducer.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopBJetsProducer::SingleTopBJetsProducer(const edm::ParameterSet& iConfig) 
{
  src_                 = iConfig.getParameter<edm::InputTag>	      ( "src" );

  veto_ = iConfig.getUntrackedParameter<bool>("veto",false); 
  bThreshold_ = iConfig.getUntrackedParameter< double >("bThreshold",-999.); 
 
  produces<std::vector<pat::Jet> >();
}

void SingleTopBJetsProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){
  std::cout << " starting, veto " <<veto_ << std::endl; 


  bThreshold_ = -999;
  double bVetoThreshold_ = -999;
  std::cout << " threshold  start "<<bThreshold_<<std::endl; 
  edm::Handle<edm::View<pat::Jet> > jets;
  iEvent.getByLabel(src_,jets);

  //  std::cout << " threshold  start "<<bThreshold_<<std::endl; 
  std::auto_ptr< std::vector< pat::Jet > > finalJets(new std::vector< pat::Jet >);
    int position=-1;  
    int positionVeto=-1;  
  for(size_t i = 0; i < jets->size(); ++i){
    //std::cout<< " test 0 " << " size " << jets->size() <<" bdiscr "<< jets->at(i).bDiscriminator("trackCountingHighPurBJetTags") << " threshold "<<bThreshold_<<" is ok "<< (jets->at(i).bDiscriminator("trackCountingHighPurBJetTags")>bThreshold_)  << " higeff"<<jets->at(i).bDiscriminator("trackCountingHighEffBJetTags")<<std::endl;
      if(jets->at(i).bDiscriminator("trackCountingHighPurBJetTags")>bThreshold_){
	bThreshold_ = jets->at(i).bDiscriminator("trackCountingHighPurBJetTags");
	if(jets->at(i).bDiscriminator("trackCountingHighPurBJetTags")==-100)continue; 
	position = i; 
      }
    
      if(bVetoThreshold_ == -999)bVetoThreshold_ = jets->at(i).bDiscriminator("trackCountingHighEffBJetTags");                                                              
      if(jets->at(i).bDiscriminator("trackCountingHighEffBJetTags")<=bVetoThreshold_) {
	bVetoThreshold_ = jets->at(i).bDiscriminator("trackCountingHighEffBJetTags");
	if(jets->at(i).bDiscriminator("trackCountingHighEffBJetTags")==-100)if(fabs(jets->at(i).eta())<2.5)continue; 
	positionVeto = i; 
	
      }
      
    
  } 
  if (position >=0 && !veto_ && (position != positionVeto)){
    std::cout <<" final position "<< position << std::endl;
    finalJets->push_back(jets->at(position));
  }
  if (positionVeto >= 0 && veto_ && (position != positionVeto)){
    std::cout <<" final position veto"<< position << std::endl;
    finalJets->push_back(jets->at(positionVeto));
  }
  
  std::cout << " final size "<< finalJets->size() <<std::endl;  
  
  iEvent.put(finalJets);

//std::cout << "mark 6"<< std::endl;  
  
}

SingleTopBJetsProducer::~SingleTopBJetsProducer(){;}
DEFINE_FWK_MODULE(SingleTopBJetsProducer);
