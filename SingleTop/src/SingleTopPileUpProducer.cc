/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopPileUpProducer.cc,v 1.1.2.1.4.1 2012/06/25 08:27:29 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

#include "DataFormats/Candidate/interface/CandAssociation.h"

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopPileUpProducer.h"
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopPileUpProducer::SingleTopPileUpProducer(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  
 
  //produces<std::vector< pat::TopLeptonic > >();
  produces< int >("PileUpTrue");
  produces< int >("PileUp0");
  produces< int >("PileUpP1");
  produces< int >("PileUpM1");
 
}

void SingleTopPileUpProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){
  
  edm::Handle<std::vector< PileupSummaryInfo > >  PupInfo;
  iEvent.getByLabel(edm::InputTag("addPileupInfo"), PupInfo); 
  
  std::vector<PileupSummaryInfo>::const_iterator PVI;
  
  int n0 = -1, nm1=-1, np1=1, nT;
  for(PVI = PupInfo->begin(); PVI != PupInfo->end(); ++PVI) {
    
    int BX = PVI->getBunchCrossing();

    if(BX == -1) { 
      nm1 = PVI->getPU_NumInteractions();
    }
    if(BX == 0) { 
      n0 = PVI->getPU_NumInteractions();
      nT =  PVI->getTrueNumInteractions();
    }
    if(BX == 1) { 
      np1 = PVI->getPU_NumInteractions();
    }

  }
 
  std::auto_ptr< int > nT_(new int( nT) );
  iEvent.put(nT_,"PileUpTrue");
  std::auto_ptr< int > n0_(new int( n0) );
  iEvent.put(n0_,"PileUp0");
  std::auto_ptr< int > nm1_(new int( nm1) );
  iEvent.put(nm1_,"PileUpM1");
  std::auto_ptr< int > np1_(new int( np1) );
  iEvent.put(np1_,"PileUpP1");
}

SingleTopPileUpProducer::~SingleTopPileUpProducer(){;}


DEFINE_FWK_MODULE( SingleTopPileUpProducer );
