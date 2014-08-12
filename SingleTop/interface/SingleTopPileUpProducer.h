#ifndef _SingleTopPileUp_Producer_h
#define _SingleTopPileUp_Producer_h


/**
 *\Class SingleTopPileUpProducer
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: SingleTopPileUpProducer.h,v 1.1 2011/07/04 00:56:21 oiorio Exp $
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
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 


//class JetFlavourIdentifier;


//namespace pat {

class SingleTopPileUpProducer : public edm::EDProducer {
public:
  explicit SingleTopPileUpProducer(const edm::ParameterSet & iConfig);
  ~SingleTopPileUpProducer();
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
  //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
  private:
   
  
};
//}


#endif
