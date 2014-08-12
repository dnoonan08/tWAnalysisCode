#ifndef _SingleTopUnclusteredMET_Producer_h
#define _SingleTopUnclusteredMET_Producer_h



/**
 *\Class SingleTopUnclusteredMETProducer
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: SingleTopUnclusteredMETProducer.h,v 1.1 2011/03/24 15:58:25 oiorio Exp $
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


//class JetFlavourIdentifier;


//namespace pat {

class SingleTopUnclusteredMETProducer : public edm::EDProducer {
public:
  explicit SingleTopUnclusteredMETProducer(const edm::ParameterSet & iConfig);
  ~SingleTopUnclusteredMETProducer();
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
  //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
private:
  edm::InputTag   metSrc_,  jetsSrc_,  electronsSrc_, muonsSrc_;

  edm::Handle<edm::View<reco::Candidate> > met,
    jets,
    electrons,
    muons;



  
  
  
};
//}


#endif
