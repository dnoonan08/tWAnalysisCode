#ifndef Cand_Or_Counter_h
#define Cand_Or_Counter_h

/* \Class CandOrCounter
 *
 * \Author A. Orso M. Iorio
 * 
 * \ version $Id: CandOrCounter.h,v 1.2 2011/03/24 15:58:25 oiorio Exp $
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"


class CandOrCounter : public edm::EDFilter{
public:
      explicit CandOrCounter(const edm::ParameterSet & iConfig);
      ~CandOrCounter();
private: 
  virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);
  edm::InputTag cand1_,cand2_;
  edm::InputTag veto1_,veto2_;
  int minNum_,maxNum_;

  edm::Handle<edm::View<reco::Candidate> > cand1;
  edm::Handle<edm::View<reco::Candidate> > cand2;
  edm::Handle<edm::View<reco::Candidate> > veto1;
  edm::Handle<edm::View<reco::Candidate> > veto2;

  bool useVeto_;
};


#endif
