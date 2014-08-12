#ifndef SingleTopDoubleFilter_h
#define SingleTopDoubleFilter_h

// Orso Iorio, INFN Napoli 



#include <FWCore/Framework/interface/Frameworkfwd.h>
#include <FWCore/Framework/interface/EDFilter.h>
#include <FWCore/Framework/interface/Event.h>
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"

//#include "FWCore/ParameterSet/interface/InputTag.h"
#include "FWCore/Utilities/interface/InputTag.h"

class SingleTopDoubleFilter : public edm::EDFilter{

public:

  explicit SingleTopDoubleFilter(const edm::ParameterSet&);
  ~SingleTopDoubleFilter();
  

private:


  virtual bool filter(edm::Event&, const edm::EventSetup&);

  edm::InputTag src_; 
  double min_,max_;

};
#endif
