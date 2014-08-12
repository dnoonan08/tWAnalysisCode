/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: PDFInfoDumper.cc,v 1.1 2011/03/24 17:08:23 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

#include "PhysicsTools/PatAlgos/plugins/PATJetProducer.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "TopQuarkAnalysis/SingleTop/interface/PDFInfoDumper.h"

//using namespace pat;


PDFInfoDumper::PDFInfoDumper(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  //  jetsSrc_                 = iConfig.getParameter<edm::InputTag>( "jetsSource" );
  //  topsSrc_                 = iConfig.getParameter<edm::InputTag>( "topsSource" );

 
produces< float >("x1");
produces< float >("x2");
produces< float >("scalePDF");
produces< int >("id1");
produces< int >("id2");
}

void PDFInfoDumper::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){


  //edm::Handle<edm::View<reco::Candidate> > jets;
//iEvent.getByLabel(jetsSrc_,jets);

//edm::Handle<edm::View<reco::Candidate> > tops;
//iEvent.getByLabel(topsSrc_,tops);

  edm::Handle<GenEventInfoProduct> genprod;
  iEvent.getByLabel("generator",genprod);
  

 std::auto_ptr< float > scalePDF_(new float),x1_(new float),x2_(new float);
 std::auto_ptr<int> id1_(new int),id2_(new int);

 *scalePDF_ = genprod->pdf()->scalePDF;
 *x1_ =  genprod->pdf()->x.first;
 *x2_ =  genprod->pdf()->x.second;
 *id1_ =  genprod->pdf()->id.first;
 *id2_ =  genprod->pdf()->id.second;
 
   iEvent.put(scalePDF_,"scalePDF");
   iEvent.put(x1_,"x1");
   iEvent.put(x2_,"x2");
   iEvent.put(id1_,"id1");
   iEvent.put(id2_,"id2");

 
}

PDFInfoDumper::~PDFInfoDumper(){;}

DEFINE_FWK_MODULE( PDFInfoDumper );
