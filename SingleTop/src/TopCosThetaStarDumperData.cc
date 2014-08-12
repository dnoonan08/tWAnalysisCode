/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: TopCosThetaStarDumperData.cc,v 1.1 2010/12/10 14:14:30 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

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


#include "TopQuarkAnalysis/SingleTop/interface/TopCosThetaStarDumperData.h"
#include "TopQuarkAnalysis/SingleTop/interface/CandidateBooster.h"


#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"


//using namespace pat;


TopCosThetaStarDumperData::TopCosThetaStarDumperData(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  //  jetsSrc_                 = iConfig.getParameter<edm::InputTag>( "jetsSource" );
  //  topsSrc_                 = iConfig.getParameter<edm::InputTag>( "topsSource" );

tChanSrc_ = iConfig.getParameter<edm::InputTag>( "tChanSource" );
  
produces<std::vector<float> >("cosThetaLJ");
produces<std::vector<float> >("cosThetaStar");
produces<std::vector<float> >("cosThetaBJ");
produces<std::vector<float> >("leptonJetDeltaR");
produces<std::vector<float> >("bJetPt");
produces<std::vector<float> >("topWTransverseMass");

}

void TopCosThetaStarDumperData::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){


  //edm::Handle<edm::View<reco::Candidate> > jets;
//iEvent.getByLabel(jetsSrc_,jets);

//edm::Handle<edm::View<reco::Candidate> > tops;
//iEvent.getByLabel(topsSrc_,tops);


edm::Handle<edm::View<reco::Candidate> > tChan;
iEvent.getByLabel(tChanSrc_,tChan);

 std::vector<float> *cosThetaLJ = new std::vector<float>(), *cosThetaStar = new std::vector<float>(), *topWTransverseMass = new std::vector<float>(), *cosThetaBJ = new std::vector<float>(), *leptonJetDeltaR = new std::vector<float>(), *bJetPt = new std::vector<float>();

 float cosThetaLJTmp(0), cosThetaStarTmp(0),topWTransverseMassTmp(0),cosThetaBJTmp(0),leptonJetDeltaRTmp(0),bJetPtTmp(0);


   for( edm::View<reco::Candidate>::const_iterator it_tChan = tChan->begin();it_tChan != tChan->end();++it_tChan){
     
     CenterOfMassBooster booster(*it_tChan->daughter("Top"));
     //reco::CandidateBaseRef candToBoostRef(edm::Ref<reco::Candidate>(,));
     leptonJetDeltaRTmp = (float)deltaR(*it_tChan->daughter("Top")->daughter("BJet"),*it_tChan->daughter("Top")->daughter("Lepton"));
     bJetPtTmp = (float)(it_tChan->daughter("Top")->daughter("BJet")->pt());
     bJetPt->push_back(bJetPtTmp);

     leptonJetDeltaR->push_back(leptonJetDeltaRTmp);

     reco::Candidate * candToBoost = it_tChan->clone();

     const reco::Candidate * Lepton1 = candToBoost->daughter("Top")->daughter("Lepton"); 
     const reco::Candidate * MET1    = candToBoost->daughter("Top")->daughter("MET");          
     topWTransverseMassTmp = sqrt(pow(Lepton1->et()+MET1->pt(),2) - pow(Lepton1->px()+MET1->px(),2) - pow(Lepton1->py()+MET1->py(),2) );

     topWTransverseMass->push_back(topWTransverseMassTmp);

     
     booster.set(*candToBoost);
     
     const reco::Candidate * Lepton = candToBoost->daughter("Top")->daughter("Lepton"); 
     const reco::Candidate * BJet = candToBoost->daughter("Top")->daughter("BJet"); 
     const reco::Candidate * MET    = candToBoost->daughter("Top")->daughter("MET");          
     
     
     
     //   for( edm::View<reco::Candidate>::const_iterator it_jets = jets->begin();it_jets != jets->end();++it_jets){
     
     const reco::Candidate * Jet = candToBoost->daughter("LightJet");   
     
     cosThetaLJTmp = ((Lepton->px()*Jet->px()) + (Lepton->py()*Jet->py()) + (Lepton->pz()*Jet->pz()))/(Lepton->p()*Jet->p()); 
     cosThetaBJTmp = ((BJet->px()*Jet->px()) + (BJet->py()*Jet->py()) + (BJet->pz()*Jet->pz()))/(BJet->p()*Jet->p()); 

      cosThetaStarTmp = cos(Lepton->theta());
      if(Jet->pz()>0) cosThetaStarTmp = cos(Lepton->theta());
      else cosThetaStarTmp = cos(TMath::Pi() - Lepton->theta());
      
      
      cosThetaStar->push_back(cosThetaStarTmp);
      cosThetaLJ->push_back(cosThetaLJTmp);
      cosThetaBJ->push_back(cosThetaBJTmp);

   }

   
   std::auto_ptr< std::vector< float > > cosThetaLJPoi(cosThetaLJ), cosThetaStarPoi(cosThetaStar),topWTransverseMassPoi(topWTransverseMass), cosThetaBJPoi(cosThetaBJ), leptonJetDeltaRPoi(leptonJetDeltaR), bJetPtPoi(bJetPt);
   
   iEvent.put(cosThetaLJPoi,"cosThetaLJ");
   iEvent.put(cosThetaStarPoi,"cosThetaStar");
   iEvent.put(topWTransverseMassPoi,"topWTransverseMass");
   iEvent.put(cosThetaBJPoi,"cosThetaBJ");
   iEvent.put(leptonJetDeltaRPoi,"leptonJetDeltaR");
   iEvent.put(bJetPtPoi,"bJetPt");

}

TopCosThetaStarDumperData::~TopCosThetaStarDumperData(){;}

DEFINE_FWK_MODULE( TopCosThetaStarDumperData );
