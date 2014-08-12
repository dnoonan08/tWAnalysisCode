#ifndef MTW_Filter_h
#define MTW_Filter_h

/* \Class CandOrCounter
 *
 * \Author A. Orso M. Iorio
 * 
 * \ version $Id: SingleTopMTWFilter.h,v 1.1 2010/09/07 15:23:06 oiorio Exp $
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"


class SingleTopMTWFilter : public edm::EDFilter{
public:
      explicit SingleTopMTWFilter(const edm::ParameterSet & iConfig);
      ~SingleTopMTWFilter();
private: 
  virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);
  edm::InputTag cand1_,cand2_;
  double cut_;
};


#endif
