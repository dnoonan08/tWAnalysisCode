#ifndef Cand_Or_Counter_No_Overlap_h
#define Cand_Or_Counter_No_Overlap_h

/* \Class CandOrCounterNoOverlap
 *
 * \Author A. Orso M. Iorio
 * 
 * \ version $Id: CandOrCounterNoOverlap.h,v 1.1 2011/04/28 08:47:55 oiorio Exp $
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"


class CandOrCounterNoOverlap : public edm::EDFilter{
public:
      explicit CandOrCounterNoOverlap(const edm::ParameterSet & iConfig);
      ~CandOrCounterNoOverlap();
private: 
  virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);
  edm::InputTag cand1_,cand2_;
  edm::InputTag candOverlap1_,candOverlap2_;
  int minNum1_,maxNum1_;
  int minNum2_,maxNum2_;

  edm::Handle<edm::View<reco::Candidate> > cand1;
  edm::Handle<edm::View<reco::Candidate> > cand2;
  edm::Handle<edm::View<reco::Candidate> > candOverlap1;
  edm::Handle<edm::View<reco::Candidate> > candOverlap2;

};


#endif
