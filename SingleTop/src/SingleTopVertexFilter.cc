#ifndef Vertex_Filter_h
#define Vertex_Filter_h


// Orso Iorio, INFN Napoli 
//
//

#include "FWCore/MessageLogger/interface/MessageLogger.h"
//#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/Event.h"

#include "FWCore/Framework/interface/MakerMacros.h"
#include "DataFormats/Common/interface/Handle.h"

#include "CommonTools/Utils/interface/StringObjectFunction.h"
#include "CommonTools/Utils/interface/StringCutObjectSelector.h"

#include "FWCore/Framework/interface/EDFilter.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

class SingleTopVertexFilter : public edm::EDFilter{
public:
  explicit SingleTopVertexFilter(const edm::ParameterSet & iConfig);
  ~SingleTopVertexFilter();
private: 
  typedef StringCutObjectSelector<reco::Vertex> Selector;
  virtual bool filter(edm::Event & iEvent, const edm::EventSetup & iSetup);
  std::string cut_;
};


SingleTopVertexFilter::SingleTopVertexFilter(const edm::ParameterSet& iConfig){

  cut_ = iConfig.getParameter< std::string >("cut"); 

  // max_ = iConfig.getUntrackedParameter<double>("max"); 
}


bool SingleTopVertexFilter::filter( edm::Event& iEvent, const edm::EventSetup& iSetup){
  
  edm::Handle<edm::View<reco::Vertex> > vertices;
  iEvent.getByLabel("offlinePrimaryVertices",vertices);
  
  Selector cut(cut_);
  bool passes = false;  
  if(vertices->size()!=0)passes = cut( vertices->at(0));
  return passes;
}

SingleTopVertexFilter::~SingleTopVertexFilter(){}

DEFINE_FWK_MODULE(SingleTopVertexFilter);

#endif
