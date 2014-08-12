#ifndef _SingleTopGenJetPtEta_Producer_h
#define _SingleTopGenJetPtEta_Producer_h



/**
 *\Class SingleTopGenJetPtEtaProducer
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: SingleTopGenJetPtEtaProducer.h,v 1.1.2.1 2011/09/21 13:26:31 oiorio Exp $
 *
 *
*/



#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h" 

#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "FWCore/ParameterSet/interface/InputTag.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"

//#include "TLorentzVector.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

//class JetFlavourIdentifier;


//namespace pat {

class SingleTopGenJetPtEtaProducer : public edm::EDProducer {
public:
  explicit SingleTopGenJetPtEtaProducer(const edm::ParameterSet & iConfig);
  ~SingleTopGenJetPtEtaProducer();
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
  //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
private:
  edm::InputTag   metSrc_,  jetsSrc_,  electronsSrc_, muonsSrc_;

  edm::Handle<edm::View<pat::Jet> >    jets;



  
  
  
};
//}


#endif
