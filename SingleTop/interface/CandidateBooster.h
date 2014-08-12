#ifndef _Candidate_Booster_h
#define _Candidate_Booster_h



/**
 *\Class CandidateBooster 
 *
 *
 * \Author A. Orso M. Iorio
 *
 *Produces a candidate collection boosted in the center of mass given by another collection 
 *
 *\version  $Id: CandidateBooster.h,v 1.3 2010/11/09 14:38:28 oiorio Exp $
 *
 *
*/



#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"
#include "FWCore/ServiceRegistry/interface/Service.h" 


#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "FWCore/ParameterSet/interface/InputTag.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "DataFormats/PatCandidates/interface/UserData.h"
#include "PhysicsTools/PatAlgos/interface/PATUserDataHelper.h"


#include "DataFormats/PatCandidates/interface/Lepton.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/CompositeCandidate.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PATObject.h"

#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"


#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"
#include "PhysicsTools/CandUtils/interface/CenterOfMassBooster.h"

template < typename T >
class CandidateBooster : public edm::EDProducer {
  
public:
  
  explicit CandidateBooster(const edm::ParameterSet & iConfig);
  ~CandidateBooster();
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);

private:
  edm::InputTag src_, boostSrc_;
};

template< typename T > 
CandidateBooster<T>::CandidateBooster(const edm::ParameterSet & iConfig){
  
  src_ =  iConfig.template getParameter<edm::InputTag>("src");    
  boostSrc_ = iConfig.getParameter<edm::InputTag>("boostSrc")  ;
  produces< reco::CandidateCollection >();
}

template< typename T >
CandidateBooster<T>::~CandidateBooster(){
}

template< typename T >
void CandidateBooster<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup){
  edm::Handle<reco::CandidateView> boost;
  iEvent.getByLabel(boostSrc_,boost);
  edm::Handle<T> src;
  iEvent.getByLabel(src_,src);
  
  std::auto_ptr<reco::CandidateCollection> boostedCollection(new reco::CandidateCollection);  
  for(size_t i = 0;i< src->size();++i){
    reco::CandidateBaseRef candToBoostRef(edm::Ref<T>(src,i));
    //reco::Candidate * candToBoost = src->at(i).clone();
    //    if(boost->size()==1){
    for(size_t s = 0;s< boost->size();++s){
    CenterOfMassBooster booster(boost->at(s));
      reco::Candidate * candToBoost = candToBoostRef->clone();
      booster.set(*candToBoost);
      boostedCollection->push_back(candToBoost->clone());
    }
    //    else if( boost->size()>1 )std::cout << " warning: input collection for the boost doesn't  have exactly element! It has "<< boost->size() << " elements! Empty boosted collection produced. "<<std::endl;
  }
  iEvent.put(boostedCollection);
}
#endif
