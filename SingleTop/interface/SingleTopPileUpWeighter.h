#ifndef _SingleTopPileUp_Weighter_h
#define _SingleTopPileUp_Weighter_h


/**
 *\Class SingleTopPileUpWeighter
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: SingleTopPileUpWeighter.h,v 1.1.2.1 2011/07/11 07:05:49 oiorio Exp $
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

#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

//class JetFlavourIdentifier;


//namespace pat {

class SingleTopPileUpWeighter : public edm::EDProducer {
public:
  explicit SingleTopPileUpWeighter(const edm::ParameterSet & iConfig);
  ~SingleTopPileUpWeighter();
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
  //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
  private:
  
  edm::InputTag syncPU_;
  edm::Handle<int>  syncPU;
 
  edm::LumiReWeighting LumiWeights_;
  
  std::string mcPUFile_,dataPUFile_,puHistoName_;
  bool doPU_;

};
//}


#endif
