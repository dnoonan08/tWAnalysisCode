#ifndef Single_Top_Lepton_Counter_h
#define Single_Top_Lepton_Counter_h

/* \Class SingleTopLeptonCounter
 *
 * \Author A. Orso M. Iorio
 * 
 * \ version $Id: SingleTopLeptonCounter.h,v 1.1.2.1 2011/12/08 21:52:48 oiorio Exp $
 */

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Candidate/interface/Candidate.h"


class SingleTopLeptonCounter : public edm::EDFilter{
public:
      explicit SingleTopLeptonCounter(const edm::ParameterSet & iConfig);
      ~SingleTopLeptonCounter();
private: 
  virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);
  edm::InputTag looseMuons_,looseElectrons_,
    tightMuons_,tightElectrons_,
    qcdMuons_,qcdElectrons_;

  edm::Handle<edm::View<reco::Candidate> > looseMuons,looseElectrons, tightMuons,tightElectrons,qcdMuons,qcdElectrons;

  int minTight_,maxTight_,
    minLoose_,maxLoose_,
    minQCD_,maxQCD_;
  bool doOverlap_,doQCD_;
};


#endif
