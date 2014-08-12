/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: CandOrCounter.cc,v 1.3 2011/06/30 15:45:41 oiorio Exp $ 
 */


#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "TopQuarkAnalysis/SingleTop/interface/CandOrCounter.h"
#include "DataFormats/Math/interface/deltaR.h"


CandOrCounter::CandOrCounter(const edm::ParameterSet& iConfig){
  cand1_ = iConfig.getParameter<edm::InputTag>("src1");
  cand2_ = iConfig.getParameter<edm::InputTag>("src2");

  //  veto1_ = iConfig.getParameter<edm::InputTag>("veto1");
  //veto2_ = iConfig.getParameter<edm::InputTag>("veto2");

  //  useVeto_ = iConfig.getUntrackedParameter<bool>("useVeto",true);

  minNum_ = iConfig.getParameter<int>("minNumber");
  maxNum_ = iConfig.getParameter<int>("maxNumber");
}


bool CandOrCounter::filter(edm::Event & iEvent, const edm::EventSetup & iSetup){


  iEvent.getByLabel(cand1_,cand1);
  iEvent.getByLabel(cand2_,cand2);
  //  iEvent.getByLabel(veto1_,veto1);
  // iEvent.getByLabel(veto2_,veto2);
  
  int non_overlapping=0;  

  /*  for(size_t j = 0; j<veto1->size();++j){
    
    bool overlaps= false;
    for(size_t i = 0; i<cand1->size();++i){
    if(deltaR(cand1->at(i),veto1->at(j))<0.01){overlaps = true;break;}
    }
    for(size_t i = 0; i<cand2->size();++i){
    if(deltaR(cand2->at(i),veto1->at(j))<0.01){overlaps = true;break;}
    }
    if (!overlaps) ++non_overlapping;
    }
  */
  /*  for(size_t j = 0; j<veto2->size();++j){
    bool overlaps= false;
    for(size_t i = 0; i<cand1->size();++i){
      if(deltaR(cand1->at(i),veto2->at(j))<0.01){overlaps = true;break;}
    }
    for(size_t i = 0; i<cand2->size();++i){
      if(deltaR(cand2->at(i),veto2->at(j))<0.01){overlaps = true;break;}
    }
    if (!overlaps) ++non_overlapping;
    }*/
  
  
  int num = (int)(cand2->size() + cand1->size());  
  
  //  return ( (num >= minNum_) && (num <= maxNum_) && (non_overlapping == 0));
  return ( (num >= minNum_) && (num <= maxNum_) );
}

CandOrCounter::~CandOrCounter(){;}

DEFINE_FWK_MODULE( CandOrCounter );
