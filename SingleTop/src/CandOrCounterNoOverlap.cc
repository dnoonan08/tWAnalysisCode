/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: CandOrCounterNoOverlap.cc,v 1.1 2011/04/28 08:47:55 oiorio Exp $ 
 */


#include "DataFormats/Candidate/interface/Candidate.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "TopQuarkAnalysis/SingleTop/interface/CandOrCounterNoOverlap.h"
#include "DataFormats/Math/interface/deltaR.h"


CandOrCounterNoOverlap::CandOrCounterNoOverlap(const edm::ParameterSet& iConfig){
  cand1_ = iConfig.getParameter<edm::InputTag>("src1");
  cand2_ = iConfig.getParameter<edm::InputTag>("src2");

  candOverlap1_ = iConfig.getParameter<edm::InputTag>("srcOverlap1");
  candOverlap2_ = iConfig.getParameter<edm::InputTag>("srcOverlap2");

  minNum1_ = iConfig.getParameter<int>("minNumberTight");
  maxNum1_ = iConfig.getParameter<int>("maxNumberTight");

  minNum2_ = iConfig.getParameter<int>("minNumberLoose");
  maxNum2_ = iConfig.getParameter<int>("maxNumberLoose");
}


bool CandOrCounterNoOverlap::filter(edm::Event & iEvent, const edm::EventSetup & iSetup){


  iEvent.getByLabel(cand1_,cand1);
  iEvent.getByLabel(cand2_,cand2);

  iEvent.getByLabel(candOverlap1_,candOverlap1);
  iEvent.getByLabel(candOverlap2_,candOverlap2);

  int non_overlapping = 0;
  
  for(size_t j = 0; j<candOverlap1->size();++j){
    bool overlaps= false;
    for(size_t i = 0; i<cand1->size();++i){
      if(deltaR(cand1->at(i),candOverlap1->at(j))<0.01){overlaps = true;break;}
    }
    for(size_t i = 0; i<cand2->size();++i){
      if(deltaR(cand2->at(i),candOverlap1->at(j))<0.01){overlaps = true;break;}
    }
    if (!overlaps) ++non_overlapping;
  }
  
  for(size_t j = 0; j<candOverlap2->size();++j){
    bool overlaps= false;
    for(size_t i = 0; i<cand1->size();++i){
      if(deltaR(cand1->at(i),candOverlap2->at(j))<0.01){overlaps = true;break;}
    }
    for(size_t i = 0; i<cand2->size();++i){
      if(deltaR(cand2->at(i),candOverlap2->at(j))<0.01){overlaps = true;break;}
    }
    if (!overlaps) ++non_overlapping;
  }
  
  
  int num1 = (int)(cand2->size() + cand1->size());  
  int num2 = (int)(non_overlapping);  
  
  return ( (num1 >= minNum1_) && (num1 <= maxNum1_) && ( num2 >= minNum2_ && num2 <= maxNum2_));
}

CandOrCounterNoOverlap::~CandOrCounterNoOverlap(){;}

DEFINE_FWK_MODULE( CandOrCounterNoOverlap );
