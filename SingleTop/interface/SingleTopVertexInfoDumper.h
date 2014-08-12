#ifndef _VertexInfo_Producer_h
#define _VertexInfo_Producer_h



/**
 *\Class SingleTopVertexInfoDumper
 *
 * \Author A. Orso M. Iorio
 * 
 *
 *\version  $Id: SingleTopVertexInfoDumper.h,v 1.1.2.1 2011/09/21 13:19:38 oiorio Exp $
 *
 *
*/



#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "FWCore/ServiceRegistry/interface/Service.h" 

#include "FWCore/Framework/interface/EDProducer.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
//#include "FWCore/ParameterSet/interface/InputTag.h"
#include "FWCore/Utilities/interface/InputTag.h"

#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"
#include "DataFormats/VertexReco/interface/Vertex.h"

//#include "TLorentzVector.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"


//class JetFlavourIdentifier;


//namespace pat {

class SingleTopVertexInfoDumper : public edm::EDProducer {
public:
  explicit SingleTopVertexInfoDumper(const edm::ParameterSet & iConfig);
  ~SingleTopVertexInfoDumper();
  virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
  //       static void fillDescriptions(edm::ConfigurationDescriptions & descriptions);
private:
  edm::InputTag src_;
  edm::Handle<edm::View<reco::Vertex> > vertices;
  
};
//}


#endif
