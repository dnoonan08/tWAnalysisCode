/*
 *\Authors:A.Giammanco, A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopMCProducer.cc,v 1.1.2.1 2012/11/26 10:26:01 oiorio Exp $ 
 */

// Single Top MC producer: 
// Orignial Author: A.Giammanco
// Adapted by: O. Iorio    


#define DEBUG    0 // 0=false

#include "PhysicsTools/PatAlgos/plugins/PATJetProducer.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/Association.h"
#include "DataFormats/Candidate/interface/CandAssociation.h"

#include "DataFormats/JetReco/interface/JetTracksAssociation.h"
#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/BTauReco/interface/TrackProbabilityTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackIPTagInfo.h"
#include "DataFormats/BTauReco/interface/TrackCountingTagInfo.h"
#include "DataFormats/BTauReco/interface/SecondaryVertexTagInfo.h"
#include "DataFormats/BTauReco/interface/SoftLeptonTagInfo.h"

#include "DataFormats/Candidate/interface/CandMatchMap.h"
#include "SimDataFormats/JetMatching/interface/JetFlavourMatching.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleFwd.h"
#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"


#include "FWCore/Framework/interface/Selector.h"



#include "TVector3.h"

////////Part to be made official
#include "../interface/SingleTopMCProducer_tW.h"

#include <vector>
#include <memory>



//using namespace pat;


SingleTopMCProducer_tW::SingleTopMCProducer_tW(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables

  
  genParticlesSrc_ = iConfig.getParameter<edm::InputTag>( "genParticlesSource" );
  //GenJets for matching
  //  genJetsSrc_ = iConfig.getParameter<edm::InputTag>( "genJetsSource" );

  genJetsDeltarMatching_ = iConfig.getUntrackedParameter<double> ( "genJetsDeltarMatching", 0.3 );

  produces<std::vector<reco::GenParticle> >("MCtops").setBranchAlias("MCtops");

  produces<std::vector< int> >("MCtopsMotherID").setBranchAlias("MCtopsMotherID");
  produces<std::vector< int> >("MCtopsGrannyID").setBranchAlias("MCtopsGrannyID");
  produces<std::vector< float> >("MCtopsVertexX").setBranchAlias("MCtopsVertexX");
  produces<std::vector< float> >("MCtopsVertexY").setBranchAlias("MCtopsVertexY");
  produces<std::vector< float> >("MCtopsVertexZ").setBranchAlias("MCtopsVertexZ");
  produces<std::vector< int> >("MCtopsNDau").setBranchAlias("MCtopsNDau");
  produces<std::vector< int> >("MCtopsDauOneID").setBranchAlias("MCtopsDauOneID");
  produces<std::vector< int> >("MCtopsDauTwoID").setBranchAlias("MCtopsDauTwoID");
  produces<std::vector< int> >("MCtopsDauThreeID").setBranchAlias("MCtopsDauThreeID");
  produces<std::vector< int> >("MCtopsDauFourID").setBranchAlias("MCtopsDauFourID");

  produces<std::vector<reco::GenParticle> >("MCleptons").setBranchAlias("MCleptons");

  produces<std::vector< int> >("MCleptonsMotherID").setBranchAlias("MCleptonsMotherID");
  produces<std::vector< int> >("MCleptonsGrannyID").setBranchAlias("MCleptonsGrannyID");
  produces<std::vector< float> >("MCleptonsVertexX").setBranchAlias("MCleptonsVertexX");
  produces<std::vector< float> >("MCleptonsVertexY").setBranchAlias("MCleptonsVertexY");
  produces<std::vector< float> >("MCleptonsVertexZ").setBranchAlias("MCleptonsVertexZ");
  produces<std::vector< int> >("MCleptonsNDau").setBranchAlias("MCleptonsNDau");
  produces<std::vector< int> >("MCleptonsDauOneID").setBranchAlias("MCleptonsDauOneID");
  produces<std::vector< int> >("MCleptonsDauTwoID").setBranchAlias("MCleptonsDauTwoID");
  produces<std::vector< int> >("MCleptonsDauThreeID").setBranchAlias("MCleptonsDauThreeID");
  produces<std::vector< int> >("MCleptonsDauFourID").setBranchAlias("MCleptonsDauFourID");

  produces<std::vector<reco::GenParticle> >("MCquarks").setBranchAlias("MCquarks");

  produces<std::vector< int> >("MCquarksMotherID").setBranchAlias("MCquarksMotherID");
  produces<std::vector< int> >("MCquarksGrannyID").setBranchAlias("MCquarksGrannyID");
  produces<std::vector< float> >("MCquarksVertexX").setBranchAlias("MCquarksVertexX");
  produces<std::vector< float> >("MCquarksVertexY").setBranchAlias("MCquarksVertexY");
  produces<std::vector< float> >("MCquarksVertexZ").setBranchAlias("MCquarksVertexZ");
  produces<std::vector< int> >("MCquarksNDau").setBranchAlias("MCquarksNDau");
  produces<std::vector< int> >("MCquarksDauOneID").setBranchAlias("MCquarksDauOneID");
  produces<std::vector< int> >("MCquarksDauTwoID").setBranchAlias("MCquarksDauTwoID");
  produces<std::vector< int> >("MCquarksDauThreeID").setBranchAlias("MCquarksDauThreeID");
  produces<std::vector< int> >("MCquarksDauFourID").setBranchAlias("MCquarksDauFourID");

  produces<std::vector<reco::GenParticle> >("MCbquarks").setBranchAlias("MCbquarks");

  produces<std::vector< int> >("MCbquarksMotherID").setBranchAlias("MCbquarksMotherID");
  produces<std::vector< int> >("MCbquarksGrannyID").setBranchAlias("MCbquarksGrannyID");
  produces<std::vector< float> >("MCbquarksVertexX").setBranchAlias("MCbquarksVertexX");
  produces<std::vector< float> >("MCbquarksVertexY").setBranchAlias("MCbquarksVertexY");
  produces<std::vector< float> >("MCbquarksVertexZ").setBranchAlias("MCbquarksVertexZ");
  produces<std::vector< int> >("MCbquarksNDau").setBranchAlias("MCbquarksNDau");
  produces<std::vector< int> >("MCbquarksDauOneID").setBranchAlias("MCbquarksDauOneID");
  produces<std::vector< int> >("MCbquarksDauTwoID").setBranchAlias("MCbquarksDauTwoID");
  produces<std::vector< int> >("MCbquarksDauThreeID").setBranchAlias("MCbquarksDauThreeID");
  produces<std::vector< int> >("MCbquarksDauFourID").setBranchAlias("MCbquarksDauFourID");

  produces<std::vector<reco::GenParticle> >("MCneutrinos").setBranchAlias("MCneutrinos");

  produces<std::vector< int> >("MCneutrinosMotherID").setBranchAlias("MCneutrinosMotherID");
  produces<std::vector< int> >("MCneutrinosGrannyID").setBranchAlias("MCneutrinosGrannyID");
  produces<std::vector< float> >("MCneutrinosVertexX").setBranchAlias("MCneutrinosVertexX");
  produces<std::vector< float> >("MCneutrinosVertexY").setBranchAlias("MCneutrinosVertexY");
  produces<std::vector< float> >("MCneutrinosVertexZ").setBranchAlias("MCneutrinosVertexZ");
  produces<std::vector< int> >("MCneutrinosNDau").setBranchAlias("MCneutrinosNDau");
  produces<std::vector< int> >("MCneutrinosDauOneID").setBranchAlias("MCneutrinosDauOneID");
  produces<std::vector< int> >("MCneutrinosDauTwoID").setBranchAlias("MCneutrinosDauTwoID");
  produces<std::vector< int> >("MCneutrinosDauThreeID").setBranchAlias("MCneutrinosDauThreeID");
  produces<std::vector< int> >("MCneutrinosDauFourID").setBranchAlias("MCneutrinosDauFourID");

  produces<std::vector<reco::GenParticle> >("MCtopsLepton").setBranchAlias("MCtopsLepton");

  produces<std::vector< int> >("MCtopsLeptonMotherID").setBranchAlias("MCtopsLeptonMotherID");
  produces<std::vector< int> >("MCtopsLeptonGrannyID").setBranchAlias("MCtopsLeptonGrannyID");
  produces<std::vector< float> >("MCtopsLeptonVertexX").setBranchAlias("MCtopsLeptonVertexX");
  produces<std::vector< float> >("MCtopsLeptonVertexY").setBranchAlias("MCtopsLeptonVertexY");
  produces<std::vector< float> >("MCtopsLeptonVertexZ").setBranchAlias("MCtopsLeptonVertexZ");
  produces<std::vector< int> >("MCtopsLeptonNDau").setBranchAlias("MCtopsLeptonNDau");
  produces<std::vector< int> >("MCtopsLeptonDauOneID").setBranchAlias("MCtopsLeptonDauOneID");
  produces<std::vector< int> >("MCtopsLeptonDauTwoID").setBranchAlias("MCtopsLeptonDauTwoID");
  produces<std::vector< int> >("MCtopsLeptonDauThreeID").setBranchAlias("MCtopsLeptonDauThreeID");
  produces<std::vector< int> >("MCtopsLeptonDauFourID").setBranchAlias("MCtopsLeptonDauFourID");

  produces<std::vector<reco::GenParticle> >("MCtopsNeutrino").setBranchAlias("MCtopsNeutrino");

  produces<std::vector< int> >("MCtopsNeutrinoMotherID").setBranchAlias("MCtopsNeutrinoMotherID");
  produces<std::vector< int> >("MCtopsNeutrinoGrannyID").setBranchAlias("MCtopsNeutrinoGrannyID");
  produces<std::vector< float> >("MCtopsNeutrinoVertexX").setBranchAlias("MCtopsNeutrinoVertexX");
  produces<std::vector< float> >("MCtopsNeutrinoVertexY").setBranchAlias("MCtopsNeutrinoVertexY");
  produces<std::vector< float> >("MCtopsNeutrinoVertexZ").setBranchAlias("MCtopsNeutrinoVertexZ");
  produces<std::vector< int> >("MCtopsNeutrinoNDau").setBranchAlias("MCtopsNeutrinoNDau");
  produces<std::vector< int> >("MCtopsNeutrinoDauOneID").setBranchAlias("MCtopsNeutrinoDauOneID");
  produces<std::vector< int> >("MCtopsNeutrinoDauTwoID").setBranchAlias("MCtopsNeutrinoDauTwoID");
  produces<std::vector< int> >("MCtopsNeutrinoDauThreeID").setBranchAlias("MCtopsNeutrinoDauThreeID");
  produces<std::vector< int> >("MCtopsNeutrinoDauFourID").setBranchAlias("MCtopsNeutrinoDauFourID");

  produces<std::vector<reco::GenParticle> >("MCtopsBQuark").setBranchAlias("MCtopsBQuark");

  produces<std::vector< int> >("MCtopsBQuarkMotherID").setBranchAlias("MCtopsBQuarkMotherID");
  produces<std::vector< int> >("MCtopsBQuarkGrannyID").setBranchAlias("MCtopsBQuarkGrannyID");
  produces<std::vector< float> >("MCtopsBQuarkVertexX").setBranchAlias("MCtopsBQuarkVertexX");
  produces<std::vector< float> >("MCtopsBQuarkVertexY").setBranchAlias("MCtopsBQuarkVertexY");
  produces<std::vector< float> >("MCtopsBQuarkVertexZ").setBranchAlias("MCtopsBQuarkVertexZ");
  produces<std::vector< int> >("MCtopsBQuarkNDau").setBranchAlias("MCtopsBQuarkNDau");
  produces<std::vector< int> >("MCtopsBQuarkDauOneID").setBranchAlias("MCtopsBQuarkDauOneID");
  produces<std::vector< int> >("MCtopsBQuarkDauTwoID").setBranchAlias("MCtopsBQuarkDauTwoID");
  produces<std::vector< int> >("MCtopsBQuarkDauThreeID").setBranchAlias("MCtopsBQuarkDauThreeID");
  produces<std::vector< int> >("MCtopsBQuarkDauFourID").setBranchAlias("MCtopsBQuarkDauFourID");

  produces<std::vector<reco::GenParticle> >("MCtopsQuark").setBranchAlias("MCtopsQuark");

  produces<std::vector< int> >("MCtopsQuarkMotherID").setBranchAlias("MCtopsQuarkMotherID");
  produces<std::vector< int> >("MCtopsQuarkGrannyID").setBranchAlias("MCtopsQuarkGrannyID");
  produces<std::vector< float> >("MCtopsQuarkVertexX").setBranchAlias("MCtopsQuarkVertexX");
  produces<std::vector< float> >("MCtopsQuarkVertexY").setBranchAlias("MCtopsQuarkVertexY");
  produces<std::vector< float> >("MCtopsQuarkVertexZ").setBranchAlias("MCtopsQuarkVertexZ");
  produces<std::vector< int> >("MCtopsQuarkNDau").setBranchAlias("MCtopsQuarkNDau");
  produces<std::vector< int> >("MCtopsQuarkDauOneID").setBranchAlias("MCtopsQuarkDauOneID");
  produces<std::vector< int> >("MCtopsQuarkDauTwoID").setBranchAlias("MCtopsQuarkDauTwoID");
  produces<std::vector< int> >("MCtopsQuarkDauThreeID").setBranchAlias("MCtopsQuarkDauThreeID");
  produces<std::vector< int> >("MCtopsQuarkDauFourID").setBranchAlias("MCtopsQuarkDauFourID");

  produces<std::vector<reco::GenParticle> >("MCtopsQuarkBar").setBranchAlias("MCtopsQuarkBar");

  produces<std::vector< int> >("MCtopsQuarkBarMotherID").setBranchAlias("MCtopsQuarkBarMotherID");
  produces<std::vector< int> >("MCtopsQuarkBarGrannyID").setBranchAlias("MCtopsQuarkBarGrannyID");
  produces<std::vector< float> >("MCtopsQuarkBarVertexX").setBranchAlias("MCtopsQuarkBarVertexX");
  produces<std::vector< float> >("MCtopsQuarkBarVertexY").setBranchAlias("MCtopsQuarkBarVertexY");
  produces<std::vector< float> >("MCtopsQuarkBarVertexZ").setBranchAlias("MCtopsQuarkBarVertexZ");
  produces<std::vector< int> >("MCtopsQuarkBarNDau").setBranchAlias("MCtopsQuarkBarNDau");
  produces<std::vector< int> >("MCtopsQuarkBarDauOneID").setBranchAlias("MCtopsQuarkBarDauOneID");
  produces<std::vector< int> >("MCtopsQuarkBarDauTwoID").setBranchAlias("MCtopsQuarkBarDauTwoID");
  produces<std::vector< int> >("MCtopsQuarkBarDauThreeID").setBranchAlias("MCtopsQuarkBarDauThreeID");
  produces<std::vector< int> >("MCtopsQuarkBarDauFourID").setBranchAlias("MCtopsQuarkBarDauFourID");

  produces<std::vector<reco::GenParticle> >("MCtopsW").setBranchAlias("MCtopsW");

  produces<std::vector< int> >("MCtopsWMotherID").setBranchAlias("MCtopsWMotherID");
  produces<std::vector< int> >("MCtopsWGrannyID").setBranchAlias("MCtopsWGrannyID");
  produces<std::vector< float> >("MCtopsWVertexX").setBranchAlias("MCtopsWVertexX");
  produces<std::vector< float> >("MCtopsWVertexY").setBranchAlias("MCtopsWVertexY");
  produces<std::vector< float> >("MCtopsWVertexZ").setBranchAlias("MCtopsWVertexZ");
  produces<std::vector< int> >("MCtopsWNDau").setBranchAlias("MCtopsWNDau");
  produces<std::vector< int> >("MCtopsWDauOneID").setBranchAlias("MCtopsWDauOneID");
  produces<std::vector< int> >("MCtopsWDauTwoID").setBranchAlias("MCtopsWDauTwoID");
  produces<std::vector< int> >("MCtopsWDauThreeID").setBranchAlias("MCtopsWDauThreeID");
  produces<std::vector< int> >("MCtopsWDauFourID").setBranchAlias("MCtopsWDauFourID");


  //  produces<std::vector<reco::GenParticle> >("MCstops").setBranchAlias("MCstops");
//  produces<std::vector<reco::GenParticle> >("MCgluinos").setBranchAlias("MCgluinos");

}

void SingleTopMCProducer_tW::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){


  //edm::Handle<edm::View<reco::genParticle> > looseJets;
  //iEvent.getByLabel(looseJetsSrc_, looseJets);


#if DEBUG
  std::cout << "producer 1" << std::endl;
#endif


edm::Handle<std::vector<reco::GenParticle> > genParticles;
iEvent.getByLabel(genParticlesSrc_, genParticles);


#if DEBUG
  std::cout << "producer 2" << std::endl;
#endif

  std::auto_ptr< std::vector< reco::GenParticle > > MCtops( new std::vector<reco::GenParticle> );

  std::auto_ptr< std::vector< int > > MCtopsMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCtopsNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCtopsVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsVertexZ( new std::vector<float> );


  std::auto_ptr< std::vector< reco::GenParticle > > MCleptons( new std::vector<reco::GenParticle> );

  std::auto_ptr< std::vector< int > > MCleptonsMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCleptonsGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCleptonsNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCleptonsDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCleptonsDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCleptonsDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCleptonsDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCleptonsVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCleptonsVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCleptonsVertexZ( new std::vector<float> );

  std::auto_ptr< std::vector< reco::GenParticle > > MCquarks( new std::vector<reco::GenParticle> );

  std::auto_ptr< std::vector< int > > MCquarksMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCquarksGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCquarksNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCquarksDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCquarksDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCquarksDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCquarksDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCquarksVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCquarksVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCquarksVertexZ( new std::vector<float> );

  std::auto_ptr< std::vector< reco::GenParticle > > MCbquarks( new std::vector<reco::GenParticle> );

  std::auto_ptr< std::vector< int > > MCbquarksMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCbquarksGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCbquarksNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCbquarksDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCbquarksDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCbquarksDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCbquarksDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCbquarksVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCbquarksVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCbquarksVertexZ( new std::vector<float> );

  std::auto_ptr< std::vector< reco::GenParticle > > MCneutrinos( new std::vector<reco::GenParticle> );

  std::auto_ptr< std::vector< int > > MCneutrinosMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCneutrinosGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCneutrinosNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCneutrinosDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCneutrinosDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCneutrinosDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCneutrinosDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCneutrinosVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCneutrinosVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCneutrinosVertexZ( new std::vector<float> );

  std::auto_ptr< std::vector< reco::GenParticle > > MCtopsLepton( new std::vector<reco::GenParticle> );


  std::auto_ptr< std::vector< int > > MCtopsLeptonMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsLeptonGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCtopsLeptonNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsLeptonDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsLeptonDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsLeptonDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsLeptonDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCtopsLeptonVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsLeptonVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsLeptonVertexZ( new std::vector<float> );



  std::auto_ptr< std::vector< reco::GenParticle > > MCtopsW( new std::vector<reco::GenParticle> );

  std::auto_ptr< std::vector< int > > MCtopsWMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsWGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCtopsWNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsWDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsWDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsWDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsWDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCtopsWVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsWVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsWVertexZ( new std::vector<float> );

  std::auto_ptr< std::vector< reco::GenParticle > > MCtopsNeutrino( new std::vector<reco::GenParticle> );


  std::auto_ptr< std::vector< int > > MCtopsNeutrinoMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsNeutrinoGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCtopsNeutrinoNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsNeutrinoDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsNeutrinoDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsNeutrinoDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsNeutrinoDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCtopsNeutrinoVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsNeutrinoVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsNeutrinoVertexZ( new std::vector<float> );

  std::auto_ptr< std::vector< reco::GenParticle > > MCtopsBQuark( new std::vector<reco::GenParticle> );


  std::auto_ptr< std::vector< int > > MCtopsBQuarkMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsBQuarkGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCtopsBQuarkNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsBQuarkDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsBQuarkDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsBQuarkDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsBQuarkDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCtopsBQuarkVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsBQuarkVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsBQuarkVertexZ( new std::vector<float> );

  std::auto_ptr< std::vector< reco::GenParticle > > MCtopsQuark( new std::vector<reco::GenParticle> );


  std::auto_ptr< std::vector< int > > MCtopsQuarkMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCtopsQuarkNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCtopsQuarkVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsQuarkVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsQuarkVertexZ( new std::vector<float> );


  std::auto_ptr< std::vector< reco::GenParticle > > MCtopsQuarkBar( new std::vector<reco::GenParticle> );


  std::auto_ptr< std::vector< int > > MCtopsQuarkBarMotherID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkBarGrannyID( new std::vector<int> );

  std::auto_ptr< std::vector< int > > MCtopsQuarkBarNDau( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkBarDauOneID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkBarDauTwoID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkBarDauThreeID( new std::vector<int> );
  std::auto_ptr< std::vector< int > > MCtopsQuarkBarDauFourID( new std::vector<int> );

  std::auto_ptr< std::vector< float > > MCtopsQuarkBarVertexX( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsQuarkBarVertexY( new std::vector<float> );
  std::auto_ptr< std::vector< float > > MCtopsQuarkBarVertexZ( new std::vector<float> );



  int nDau =0;
  int dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
  
  int verbosity_= 0;

  using namespace std;
  using namespace edm;
  using namespace reco;
  
  bool isNewPhysics_= false;
  
  const Candidate *top_=NULL, *stop_=NULL, * lepton_=NULL, *quark_=NULL, *bquark_=NULL, *gluino_=NULL, *neutrino_=NULL;
  const Candidate *W_=NULL, *quarkBar_=NULL; 

  for (reco::GenParticleCollection::const_iterator t = genParticles->begin (); t != genParticles->end (); ++t)
    {
      if(verbosity_>4) cout<<t->p4()<<" "<<t->pdgId()<<" "<<t->status()<<endl;
      if (t->status () == 3)
	{
	  if (t->pdgId () > 100000)
	    {
	      isNewPhysics_ = true;
	    }
	  if ((abs (t->pdgId ()) == 11 || abs (t->pdgId ()) == 13 || abs (t->pdgId ()) == 15) &&
	      ((abs (t->mother ()->pdgId ()) > 22 && abs (t->mother ()->pdgId ()) < 40) || (abs (t->mother ()->pdgId ()) > 999999 && abs (t->mother ()->pdgId ()) < 2999999)))
	    {	
	      MCleptons->push_back ( (*t));
	      if(t->mother()) MCleptonsMotherID->push_back( t->mother()->pdgId());
	      if(t->mother() && t->mother()->mother())MCleptonsGrannyID->push_back(t->mother()->mother()->pdgId());
	      MCleptonsVertexX->push_back(t->vertex().x());
	      MCleptonsVertexY->push_back(t->vertex().y());
	      MCleptonsVertexZ->push_back(t->vertex().z());
	      nDau =0;
	      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
	      for (reco::GenParticle::const_iterator td = t->begin (); td != t->end (); ++td){
		nDau++;
		if(nDau==1) dauOneId = td->pdgId();
		if(nDau==2) dauTwoId = td->pdgId();
		if(nDau==3) dauThreeId = td->pdgId();
		if(nDau==4) dauFourId = td->pdgId();
	      }
	      MCleptonsNDau->push_back(nDau);
	      MCleptonsDauOneID->push_back(dauOneId);
	      MCleptonsDauTwoID->push_back(dauTwoId);
	      MCleptonsDauThreeID->push_back(dauThreeId);
	      MCleptonsDauFourID->push_back(dauFourId);

	    }
	      if ((abs (t->pdgId ()) == 12 || abs (t->pdgId ()) == 14 || abs (t->pdgId ()) == 16) &&
	      ((abs (t->mother ()->pdgId ()) > 22 && abs (t->mother ()->pdgId ()) < 40) || (abs (t->mother ()->pdgId ()) > 999999 && abs (t->mother ()->pdgId ()) < 2999999)))
		{
		  MCneutrinos->push_back( (*t));
	      if(t->mother()) MCneutrinosMotherID->push_back( t->mother()->pdgId());
	      if(t->mother() && t->mother()->mother())MCneutrinosGrannyID->push_back(t->mother()->mother()->pdgId());
	      MCneutrinosVertexX->push_back(t->vertex().x());
	      MCneutrinosVertexY->push_back(t->vertex().y());
	      MCneutrinosVertexZ->push_back(t->vertex().z());
	      nDau =0;
	      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
	      for (reco::GenParticle::const_iterator td = t->begin (); td != t->end (); ++td){
		nDau++;
		if(nDau==1) dauOneId = td->pdgId();
		if(nDau==2) dauTwoId = td->pdgId();
		if(nDau==3) dauThreeId = td->pdgId();
		if(nDau==4) dauFourId = td->pdgId();
	      }
	      MCneutrinosNDau->push_back(nDau);
	      MCneutrinosDauOneID->push_back(dauOneId);
	      MCneutrinosDauTwoID->push_back(dauTwoId);
	      MCneutrinosDauThreeID->push_back(dauThreeId);
	      MCneutrinosDauFourID->push_back(dauFourId);

		}
	  if (abs (abs (t->pdgId ())) == 1000022 || abs (abs (t->pdgId ())) == 1000023 || abs (abs (t->pdgId ())) == 1000025 || abs (abs (t->pdgId ())) == 1000035)
	    {
	      int nofd = 0;
	      for (reco::GenParticle::const_iterator td = t->begin (); td != t->end (); ++td)
		nofd++;
	      if (nofd < 2)
		;		//		invisibleParticles_.push_back (ConvertMCPart(t));
	    }
	  if (abs (t->pdgId ()) < 6){
	    MCquarks->push_back (*t);
	    if(t->mother()) MCquarksMotherID->push_back( t->mother()->pdgId());
	    if(t->mother() && t->mother()->mother())MCquarksGrannyID->push_back(t->mother()->mother()->pdgId());
	    MCquarksVertexX->push_back(t->vertex().x());
	    MCquarksVertexY->push_back(t->vertex().y());
	    MCquarksVertexZ->push_back(t->vertex().z());
	    nDau =0;
	    dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
	    for (reco::GenParticle::const_iterator td = t->begin (); td != t->end (); ++td){
	      nDau++;
	      if(nDau==1) dauOneId = td->pdgId();
	      if(nDau==2) dauTwoId = td->pdgId();
	      if(nDau==3) dauThreeId = td->pdgId();
	      if(nDau==4) dauFourId = td->pdgId();
	    }
	    MCquarksNDau->push_back(nDau);
	    MCquarksDauOneID->push_back(dauOneId);
	    MCquarksDauTwoID->push_back(dauTwoId);
	    MCquarksDauThreeID->push_back(dauThreeId);
	    MCquarksDauFourID->push_back(dauFourId);
	  }
	  if (abs (t->pdgId ()) == 5){
	    MCbquarks->push_back (*t);
	    if(t->mother()) MCbquarksMotherID->push_back( t->mother()->pdgId());
	    if(t->mother() && t->mother()->mother())MCbquarksGrannyID->push_back(t->mother()->mother()->pdgId());
	    MCbquarksVertexX->push_back(t->vertex().x());
	    MCbquarksVertexY->push_back(t->vertex().y());
	    MCbquarksVertexZ->push_back(t->vertex().z());
	    nDau =0;
	    dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
	    for (reco::GenParticle::const_iterator td = t->begin (); td != t->end (); ++td){
	      nDau++;
	      if(nDau==1) dauOneId = td->pdgId();
	      if(nDau==2) dauTwoId = td->pdgId();
	      if(nDau==3) dauThreeId = td->pdgId();
	      if(nDau==4) dauFourId = td->pdgId();
	    }
	    MCbquarksNDau->push_back(nDau);
	    MCbquarksDauOneID->push_back(dauOneId);
	    MCbquarksDauTwoID->push_back(dauTwoId);
	    MCbquarksDauThreeID->push_back(dauThreeId);
	    MCbquarksDauFourID->push_back(dauFourId);
	  }
	  if (abs (t->pdgId ()) == 1000021)
	    ;//	    MCgluinos->push_back (*t);
	  if (abs (t->pdgId ()) == 1000006 || abs (t->pdgId ()) == 2000006)
	    ;//  MCstops->push_back (*t);
	  if (abs (t->pdgId ()) == 6)
	    {
	      bool isLeptonic_ = false;
	      //TRootMCParticle top_;
	      //TRootMCParticle W_;
	      //TRootMCParticle bquark_;
	      //TRootMCParticle quark_;
	      //TRootMCParticle quarkBar_;
	      //TRootMCParticle lepton_;
	      //TRootMCParticle neutrino_;
	      
	      top_ = (&(*t));
	      reco::GenParticle::const_iterator td = t->begin ();
	      MCtops->push_back(*t);
	      if(t->mother()) MCtopsMotherID->push_back( t->mother()->pdgId());
	      if(t->mother() && t->mother()->mother())MCtopsGrannyID->push_back(t->mother()->mother()->pdgId());
	      MCtopsVertexX->push_back(t->vertex().x());
	      MCtopsVertexY->push_back(t->vertex().y());
	      MCtopsVertexZ->push_back(t->vertex().z());
	      nDau =0;
	      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
	      for (reco::GenParticle::const_iterator td = t->begin (); td != t->end (); ++td){
		nDau++;
		if(nDau==1) dauOneId = td->pdgId();
		if(nDau==2) dauTwoId = td->pdgId();
		if(nDau==3) dauThreeId = td->pdgId();
		if(nDau==4) dauFourId = td->pdgId();
	      }
	      MCtopsNDau->push_back(nDau);
	      MCtopsDauOneID->push_back(dauOneId);
	      MCtopsDauTwoID->push_back(dauTwoId);
	      MCtopsDauThreeID->push_back(dauThreeId);
	      MCtopsDauFourID->push_back(dauFourId);
	      for (; td != t->end (); ++td)
		{
		  if (abs (td->pdgId ()) == 24)
		    {
		      W_  = (&(*td));
		      MCtopsW->push_back( *(dynamic_cast< const reco::GenParticle *> (&(*td))) );
		      if(td->mother()) MCtopsWMotherID->push_back( td->mother()->pdgId());
		      if(td->mother() && td->mother()->mother())MCtopsWGrannyID->push_back(td->mother()->mother()->pdgId());
		      MCtopsWVertexX->push_back(td->vertex().x());
		      MCtopsWVertexY->push_back(td->vertex().y());
		      MCtopsWVertexZ->push_back(td->vertex().z());
		      nDau =0;
		      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
		      for (reco::GenParticle::const_iterator tdd = td->begin (); tdd != td->end (); ++tdd){
			nDau++;
			if(nDau==1) dauOneId = tdd->pdgId();
			if(nDau==2) dauTwoId = tdd->pdgId();
			if(nDau==3) dauThreeId = tdd->pdgId();
			if(nDau==4) dauFourId = tdd->pdgId();
		      }
		      MCtopsWNDau->push_back(nDau);
		      MCtopsWDauOneID->push_back(dauOneId);
		      MCtopsWDauTwoID->push_back(dauTwoId);
		      MCtopsWDauThreeID->push_back(dauThreeId);
		      MCtopsWDauFourID->push_back(dauFourId);
		    reco:GenParticle::const_iterator Wd = td->begin ();
		      
		      
		      
		      for (; Wd != td->end (); ++Wd)
			{
			  if (Wd->pdgId () > 0 && Wd->pdgId () < 6)
			    {
			      quark_  = &(*Wd);
			      MCtopsQuark->push_back( *(dynamic_cast< const reco::GenParticle *> (&(*Wd))) );
			      
			      if(Wd->mother()) MCtopsQuarkMotherID->push_back( Wd->mother()->pdgId());
			      if(Wd->mother() && Wd->mother()->mother())MCtopsQuarkGrannyID->push_back(Wd->mother()->mother()->pdgId());
			      MCtopsQuarkVertexX->push_back(Wd->vertex().x());
			      MCtopsQuarkVertexY->push_back(Wd->vertex().y());
			      MCtopsQuarkVertexZ->push_back(Wd->vertex().z());
			      nDau =0;
			      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
			      for (reco::GenParticle::const_iterator Wdd = Wd->begin (); Wdd != Wd->end (); ++Wdd){
				nDau++;
				if(nDau==1) dauOneId = Wdd->pdgId();
				if(nDau==2) dauTwoId = Wdd->pdgId();
				if(nDau==3) dauThreeId = Wdd->pdgId();
				if(nDau==4) dauFourId = Wdd->pdgId();
			      }
			      MCtopsQuarkNDau->push_back(nDau);
			      MCtopsQuarkDauOneID->push_back(dauOneId);
			      MCtopsQuarkDauTwoID->push_back(dauTwoId);
			      MCtopsQuarkDauThreeID->push_back(dauThreeId);
			      MCtopsQuarkDauFourID->push_back(dauFourId);
			      
			      
			    }
			  if (Wd->pdgId () < 0 && Wd->pdgId () > -6)
			    {
			      quarkBar_  = &(*Wd);
			      MCtopsQuarkBar->push_back( *(dynamic_cast< const reco::GenParticle *> (&(*Wd))) );
			      
			      if(Wd->mother()) MCtopsQuarkBarMotherID->push_back( Wd->mother()->pdgId());
			      if(Wd->mother() && Wd->mother()->mother())MCtopsQuarkBarGrannyID->push_back(Wd->mother()->mother()->pdgId());
			      MCtopsQuarkBarVertexX->push_back(Wd->vertex().x());
			      MCtopsQuarkBarVertexY->push_back(Wd->vertex().y());
			      MCtopsQuarkBarVertexZ->push_back(Wd->vertex().z());
			      nDau =0;
			      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
			      for (reco::GenParticle::const_iterator Wdd = Wd->begin (); Wdd != Wd->end (); ++Wdd){
				nDau++;
				if(nDau==1) dauOneId = Wdd->pdgId();
				if(nDau==2) dauTwoId = Wdd->pdgId();
				if(nDau==3) dauThreeId = Wdd->pdgId();
				if(nDau==4) dauFourId = Wdd->pdgId();
			      }
			      MCtopsQuarkBarNDau->push_back(nDau);
			      MCtopsQuarkBarDauOneID->push_back(dauOneId);
			      MCtopsQuarkBarDauTwoID->push_back(dauTwoId);
			      MCtopsQuarkBarDauThreeID->push_back(dauThreeId);
			      MCtopsQuarkBarDauFourID->push_back(dauFourId);
			    }
			  if (abs (Wd->pdgId ()) == 11 || abs (Wd->pdgId ()) == 13 || abs (Wd->pdgId ()) == 15)
			    {
			      lepton_  = &(*Wd);
			      MCtopsLepton->push_back( *(dynamic_cast< const reco::GenParticle *> (&(*Wd))) );

			      if(Wd->mother()) MCtopsLeptonMotherID->push_back( Wd->mother()->pdgId());
			      if(Wd->mother() && Wd->mother()->mother())MCtopsLeptonGrannyID->push_back(Wd->mother()->mother()->pdgId());
			      MCtopsLeptonVertexX->push_back(Wd->vertex().x());
			      MCtopsLeptonVertexY->push_back(Wd->vertex().y());
			      MCtopsLeptonVertexZ->push_back(Wd->vertex().z());
			      nDau =0;
			      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
			      for (reco::GenParticle::const_iterator Wdd = Wd->begin (); Wdd != Wd->end (); ++Wdd){
				nDau++;
				if(nDau==1) dauOneId = Wdd->pdgId();
				if(nDau==2) dauTwoId = Wdd->pdgId();
				if(nDau==3) dauThreeId = Wdd->pdgId();
				if(nDau==4) dauFourId = Wdd->pdgId();
			      }
			      MCtopsLeptonNDau->push_back(nDau);
			      MCtopsLeptonDauOneID->push_back(dauOneId);
			      MCtopsLeptonDauTwoID->push_back(dauTwoId);
			      MCtopsLeptonDauThreeID->push_back(dauThreeId);
			      MCtopsLeptonDauFourID->push_back(dauFourId);
			      isLeptonic_ = true;
			    }
			  if (abs (Wd->pdgId ()) == 12 || abs (Wd->pdgId ()) == 14 || abs (Wd->pdgId ()) == 16)
			    {
			      neutrino_  = &(*Wd);
			      MCtopsNeutrino->push_back( *(dynamic_cast< const reco::GenParticle *> (&(*Wd))) );

			      if(Wd->mother()) MCtopsNeutrinoMotherID->push_back( Wd->mother()->pdgId());
			      if(Wd->mother() && Wd->mother()->mother())MCtopsNeutrinoGrannyID->push_back(Wd->mother()->mother()->pdgId());
			      MCtopsNeutrinoVertexX->push_back(Wd->vertex().x());
			      MCtopsNeutrinoVertexY->push_back(Wd->vertex().y());
			      MCtopsNeutrinoVertexZ->push_back(Wd->vertex().z());
			      nDau =0;
			      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
			      for (reco::GenParticle::const_iterator Wdd = Wd->begin (); Wdd != Wd->end (); ++Wdd){
				nDau++;
				if(nDau==1) dauOneId = Wdd->pdgId();
				if(nDau==2) dauTwoId = Wdd->pdgId();
				if(nDau==3) dauThreeId = Wdd->pdgId();
				if(nDau==4) dauFourId = Wdd->pdgId();
			      }
			      MCtopsNeutrinoNDau->push_back(nDau);
			      MCtopsNeutrinoDauOneID->push_back(dauOneId);
			      MCtopsNeutrinoDauTwoID->push_back(dauTwoId);
			      MCtopsNeutrinoDauThreeID->push_back(dauThreeId);
			      MCtopsNeutrinoDauFourID->push_back(dauFourId);

			    }
			}
		    }
		  else if (abs (td->pdgId ()) == 5){   bquark_  = &(*td);
		    MCtopsBQuark->push_back( *(dynamic_cast< const reco::GenParticle *> (&(*td))) );
		    if(td->mother()) MCtopsBQuarkMotherID->push_back( td->mother()->pdgId());
		    if(td->mother() && td->mother()->mother())MCtopsBQuarkGrannyID->push_back(td->mother()->mother()->pdgId());
		    MCtopsBQuarkVertexX->push_back(td->vertex().x());
		      MCtopsBQuarkVertexY->push_back(td->vertex().y());
		      MCtopsBQuarkVertexZ->push_back(td->vertex().z());
		      nDau =0;
		      dauOneId=-9999, dauTwoId =-9999, dauThreeId=-9999,dauFourId=-9999 ;
		      for (reco::GenParticle::const_iterator tdd = td->begin (); tdd != td->end (); ++tdd){
			nDau++;
			if(nDau==1) dauOneId = tdd->pdgId();
			if(nDau==2) dauTwoId = tdd->pdgId();
			if(nDau==3) dauThreeId = tdd->pdgId();
			if(nDau==4) dauFourId = tdd->pdgId();
		      }
		      MCtopsBQuarkNDau->push_back(nDau);
		      MCtopsBQuarkDauOneID->push_back(dauOneId);
		      MCtopsBQuarkDauTwoID->push_back(dauTwoId);
		      MCtopsBQuarkDauThreeID->push_back(dauThreeId);
		      MCtopsBQuarkDauFourID->push_back(dauFourId);
		  }
		}
	      //cout<<"TopGenPart"<<endl;
	      //
	      char cprod[1000];
	      char cprodTemp[1000];
	      sprintf(cprod,"%d->",t->motherRef()->pdgId());
	      GenParticle::const_iterator tm = t->motherRef()->begin();
	      for( ; tm!=t->motherRef()->end(); ++tm){
		sprintf(cprodTemp,"%s %d",cprod,tm->pdgId());
		sprintf(cprod,"%s",cprodTemp);
	      }
	      string production_ = string(cprod);  
	      //	      MCtops->push_back (top);

	      if(isLeptonic_){
		//		TRootGenTop top (isLeptonic_, top_, W_, bquark_, lepton_, neutrino_, production_);
		;
	      }
	      else{
		//		TRootGenTop top (isLeptonic_, top_, W_, bquark_, quark_, quarkBar_, production_);
		//		tops_.push_back (top);
		;
	      }
	      //cout<<"End TopGenPart"<<endl;
	    }
	}
  }
  //cout<<"AT THE END"<<endl;

  //  TRootNPGenEvent TRootgenEvt (isNewPhysics_, tops_, leptons_, quarks_, bquarks_, invisibleParticles_, neutrinos_, gluinos_, stops_);

  //cout<<"AT THE END"<<endl;
  //  iEvent.put(MCstops,"MCstops");
  iEvent.put(MCtops,"MCtops");
  iEvent.put(MCtopsMotherID,"MCtopsMotherID");
  iEvent.put(MCtopsGrannyID,"MCtopsGrannyID");
  iEvent.put(MCtopsVertexX,"MCtopsVertexX");
  iEvent.put(MCtopsVertexY,"MCtopsVertexY");
  iEvent.put(MCtopsVertexZ,"MCtopsVertexZ");

  iEvent.put(MCtopsNDau,"MCtopsNDau");
  iEvent.put(MCtopsDauOneID,"MCtopsDauOneID");
  iEvent.put(MCtopsDauTwoID,"MCtopsDauTwoID");
  iEvent.put(MCtopsDauThreeID,"MCtopsDauThreeID");
  iEvent.put(MCtopsDauFourID,"MCtopsDauFourID");


  iEvent.put(MCtopsW,"MCtopsW");
  iEvent.put(MCtopsWMotherID,"MCtopsWMotherID");
  iEvent.put(MCtopsWGrannyID,"MCtopsWGrannyID");
  iEvent.put(MCtopsWVertexX,"MCtopsWVertexX");
  iEvent.put(MCtopsWVertexY,"MCtopsWVertexY");
  iEvent.put(MCtopsWVertexZ,"MCtopsWVertexZ");

  iEvent.put(MCtopsWNDau,"MCtopsWNDau");
  iEvent.put(MCtopsWDauOneID,"MCtopsWDauOneID");
  iEvent.put(MCtopsWDauTwoID,"MCtopsWDauTwoID");
  iEvent.put(MCtopsWDauThreeID,"MCtopsWDauThreeID");
  iEvent.put(MCtopsWDauFourID,"MCtopsWDauFourID");

  iEvent.put(MCtopsBQuark,"MCtopsBQuark");
  iEvent.put(MCtopsBQuarkMotherID,"MCtopsBQuarkMotherID");
  iEvent.put(MCtopsBQuarkGrannyID,"MCtopsBQuarkGrannyID");
  iEvent.put(MCtopsBQuarkVertexX,"MCtopsBQuarkVertexX");
  iEvent.put(MCtopsBQuarkVertexY,"MCtopsBQuarkVertexY");
  iEvent.put(MCtopsBQuarkVertexZ,"MCtopsBQuarkVertexZ");

  iEvent.put(MCtopsBQuarkNDau,"MCtopsBQuarkNDau");
  iEvent.put(MCtopsBQuarkDauOneID,"MCtopsBQuarkDauOneID");
  iEvent.put(MCtopsBQuarkDauTwoID,"MCtopsBQuarkDauTwoID");
  iEvent.put(MCtopsBQuarkDauThreeID,"MCtopsBQuarkDauThreeID");
  iEvent.put(MCtopsBQuarkDauFourID,"MCtopsBQuarkDauFourID");



  iEvent.put(MCtopsLepton,"MCtopsLepton");
  iEvent.put(MCtopsLeptonMotherID,"MCtopsLeptonMotherID");
  iEvent.put(MCtopsLeptonGrannyID,"MCtopsLeptonGrannyID");
  iEvent.put(MCtopsLeptonVertexX,"MCtopsLeptonVertexX");
  iEvent.put(MCtopsLeptonVertexY,"MCtopsLeptonVertexY");
  iEvent.put(MCtopsLeptonVertexZ,"MCtopsLeptonVertexZ");

  iEvent.put(MCtopsLeptonNDau,"MCtopsLeptonNDau");
  iEvent.put(MCtopsLeptonDauOneID,"MCtopsLeptonDauOneID");
  iEvent.put(MCtopsLeptonDauTwoID,"MCtopsLeptonDauTwoID");
  iEvent.put(MCtopsLeptonDauThreeID,"MCtopsLeptonDauThreeID");
  iEvent.put(MCtopsLeptonDauFourID,"MCtopsLeptonDauFourID");

  iEvent.put(MCtopsNeutrino,"MCtopsNeutrino");
  iEvent.put(MCtopsNeutrinoMotherID,"MCtopsNeutrinoMotherID");
  iEvent.put(MCtopsNeutrinoGrannyID,"MCtopsNeutrinoGrannyID");
  iEvent.put(MCtopsNeutrinoVertexX,"MCtopsNeutrinoVertexX");
  iEvent.put(MCtopsNeutrinoVertexY,"MCtopsNeutrinoVertexY");
  iEvent.put(MCtopsNeutrinoVertexZ,"MCtopsNeutrinoVertexZ");

  iEvent.put(MCtopsNeutrinoNDau,"MCtopsNeutrinoNDau");
  iEvent.put(MCtopsNeutrinoDauOneID,"MCtopsNeutrinoDauOneID");
  iEvent.put(MCtopsNeutrinoDauTwoID,"MCtopsNeutrinoDauTwoID");
  iEvent.put(MCtopsNeutrinoDauThreeID,"MCtopsNeutrinoDauThreeID");
  iEvent.put(MCtopsNeutrinoDauFourID,"MCtopsNeutrinoDauFourID");

  iEvent.put(MCtopsQuark,"MCtopsQuark");
  iEvent.put(MCtopsQuarkMotherID,"MCtopsQuarkMotherID");
  iEvent.put(MCtopsQuarkGrannyID,"MCtopsQuarkGrannyID");
  iEvent.put(MCtopsQuarkVertexX,"MCtopsQuarkVertexX");
  iEvent.put(MCtopsQuarkVertexY,"MCtopsQuarkVertexY");
  iEvent.put(MCtopsQuarkVertexZ,"MCtopsQuarkVertexZ");

  iEvent.put(MCtopsQuarkNDau,"MCtopsQuarkNDau");
  iEvent.put(MCtopsQuarkDauOneID,"MCtopsQuarkDauOneID");
  iEvent.put(MCtopsQuarkDauTwoID,"MCtopsQuarkDauTwoID");
  iEvent.put(MCtopsQuarkDauThreeID,"MCtopsQuarkDauThreeID");
  iEvent.put(MCtopsQuarkDauFourID,"MCtopsQuarkDauFourID");

  iEvent.put(MCtopsQuarkBar,"MCtopsQuarkBar");
  iEvent.put(MCtopsQuarkBarMotherID,"MCtopsQuarkBarMotherID");
  iEvent.put(MCtopsQuarkBarGrannyID,"MCtopsQuarkBarGrannyID");
  iEvent.put(MCtopsQuarkBarVertexX,"MCtopsQuarkBarVertexX");
  iEvent.put(MCtopsQuarkBarVertexY,"MCtopsQuarkBarVertexY");
  iEvent.put(MCtopsQuarkBarVertexZ,"MCtopsQuarkBarVertexZ");

  iEvent.put(MCtopsQuarkBarNDau,"MCtopsQuarkBarNDau");
  iEvent.put(MCtopsQuarkBarDauOneID,"MCtopsQuarkBarDauOneID");
  iEvent.put(MCtopsQuarkBarDauTwoID,"MCtopsQuarkBarDauTwoID");
  iEvent.put(MCtopsQuarkBarDauThreeID,"MCtopsQuarkBarDauThreeID");
  iEvent.put(MCtopsQuarkBarDauFourID,"MCtopsQuarkBarDauFourID");

  iEvent.put(MCleptons,"MCleptons");
  iEvent.put(MCleptonsMotherID,"MCleptonsMotherID");
  iEvent.put(MCleptonsGrannyID,"MCleptonsGrannyID");
  iEvent.put(MCleptonsVertexX,"MCleptonsVertexX");
  iEvent.put(MCleptonsVertexY,"MCleptonsVertexY");
  iEvent.put(MCleptonsVertexZ,"MCleptonsVertexZ");

  iEvent.put(MCleptonsNDau,"MCleptonsNDau");
  iEvent.put(MCleptonsDauOneID,"MCleptonsDauOneID");
  iEvent.put(MCleptonsDauTwoID,"MCleptonsDauTwoID");
  iEvent.put(MCleptonsDauThreeID,"MCleptonsDauThreeID");
  iEvent.put(MCleptonsDauFourID,"MCleptonsDauFourID");

  iEvent.put(MCquarks,"MCquarks");
  iEvent.put(MCquarksMotherID,"MCquarksMotherID");
  iEvent.put(MCquarksGrannyID,"MCquarksGrannyID");
  iEvent.put(MCquarksVertexX,"MCquarksVertexX");
  iEvent.put(MCquarksVertexY,"MCquarksVertexY");
  iEvent.put(MCquarksVertexZ,"MCquarksVertexZ");

  iEvent.put(MCquarksNDau,"MCquarksNDau");
  iEvent.put(MCquarksDauOneID,"MCquarksDauOneID");
  iEvent.put(MCquarksDauTwoID,"MCquarksDauTwoID");
  iEvent.put(MCquarksDauThreeID,"MCquarksDauThreeID");
  iEvent.put(MCquarksDauFourID,"MCquarksDauFourID");

  iEvent.put(MCbquarks,"MCbquarks");
  iEvent.put(MCbquarksMotherID,"MCbquarksMotherID");
  iEvent.put(MCbquarksGrannyID,"MCbquarksGrannyID");
  iEvent.put(MCbquarksVertexX,"MCbquarksVertexX");
  iEvent.put(MCbquarksVertexY,"MCbquarksVertexY");
  iEvent.put(MCbquarksVertexZ,"MCbquarksVertexZ");

  iEvent.put(MCbquarksNDau,"MCbquarksNDau");
  iEvent.put(MCbquarksDauOneID,"MCbquarksDauOneID");
  iEvent.put(MCbquarksDauTwoID,"MCbquarksDauTwoID");
  iEvent.put(MCbquarksDauThreeID,"MCbquarksDauThreeID");
  iEvent.put(MCbquarksDauFourID,"MCbquarksDauFourID");

  iEvent.put(MCneutrinos,"MCneutrinos");
  iEvent.put(MCneutrinosMotherID,"MCneutrinosMotherID");
  iEvent.put(MCneutrinosGrannyID,"MCneutrinosGrannyID");
  iEvent.put(MCneutrinosVertexX,"MCneutrinosVertexX");
  iEvent.put(MCneutrinosVertexY,"MCneutrinosVertexY");
  iEvent.put(MCneutrinosVertexZ,"MCneutrinosVertexZ");

  iEvent.put(MCneutrinosNDau,"MCneutrinosNDau");
  iEvent.put(MCneutrinosDauOneID,"MCneutrinosDauOneID");
  iEvent.put(MCneutrinosDauTwoID,"MCneutrinosDauTwoID");
  iEvent.put(MCneutrinosDauThreeID,"MCneutrinosDauThreeID");
  iEvent.put(MCneutrinosDauFourID,"MCneutrinosDauFourID");
}



SingleTopMCProducer_tW::~SingleTopMCProducer_tW(){;}

DEFINE_FWK_MODULE( SingleTopMCProducer_tW );

//  LocalWords:  MCtopsQuarkBar
