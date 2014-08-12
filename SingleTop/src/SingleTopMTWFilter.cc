// Orso Iorio, INFN Napoli 
//
//

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopMTWFilter.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"

SingleTopMTWFilter::SingleTopMTWFilter(const edm::ParameterSet& iConfig){

  cand1_ = iConfig.getParameter<edm::InputTag>("src1");
  cand2_ = iConfig.getParameter<edm::InputTag>("src2");
  cut_ = iConfig.getUntrackedParameter<double>("cut",50); 
  // max_ = iConfig.getUntrackedParameter<double>("max"); 

}


bool SingleTopMTWFilter::filter( edm::Event& iEvent, const edm::EventSetup& iSetup){

edm::Handle<edm::View<reco::Candidate> > cand1;
iEvent.getByLabel(cand1_,cand1);

edm::Handle<edm::View<reco::Candidate> > cand2;
iEvent.getByLabel(cand2_,cand2);

 for(size_t i = 0; i < cand1->size(); ++i){
   for(size_t j = 0; j < cand2->size(); ++j){
     
     double mtw = sqrt((cand1->at(i).pt()+cand2->at(j).pt())*(cand1->at(i).pt()+cand2->at(j).pt())-(cand1->at(i).px()+cand2->at(j).px())*(cand1->at(i).px()+cand2->at(j).px())-(cand1->at(i).py()+cand2->at(j).py())*(cand1->at(i).py()+cand2->at(j).py()) );
     if (mtw > cut_)return true;
		       
   }
 }
   return false;

  return false;

}

SingleTopMTWFilter::~SingleTopMTWFilter(){}

DEFINE_FWK_MODULE(SingleTopMTWFilter);
