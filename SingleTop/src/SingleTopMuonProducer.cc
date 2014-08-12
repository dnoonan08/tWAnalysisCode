/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopMuonProducer.cc,v 1.2.12.4.2.1 2012/10/23 21:12:28 dnoonan Exp $ 
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

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopMuonProducer.h"


#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"


#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopMuonProducer::SingleTopMuonProducer(const edm::ParameterSet& iConfig)
{
  src_                 = iConfig.getParameter<edm::InputTag>( "src" );
  cut_ = iConfig.getParameter< std::string >("cut"); 
  rho_ = iConfig.getParameter<edm::InputTag> ("rho");
  deltaR_ = iConfig.getUntrackedParameter<double>         ( "deltaR",0.4 );

  produces<std::vector<pat::Muon> >();
}

void SingleTopMuonProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){

  edm::Handle<edm::View<reco::Vertex> > vertices;
  iEvent.getByLabel("offlinePrimaryVertices",vertices);


  //std::cout << " mark 0 " << std::endl;

  //  edm::Handle<edm::View<pat::Muon> > muons;
  edm::Handle<std::vector<pat::Muon> > muons;
  iEvent.getByLabel(src_,muons);
  iEvent.getByLabel(rho_,rho);
  double energy_ = TMath::Pi()*deltaR_*deltaR_* (*rho);
  
  Selector cut(cut_);
  std::auto_ptr< std::vector< pat::Muon > > initialMuons (new std::vector<pat::Muon>(*muons));
  std::auto_ptr< std::vector< pat::Muon > > finalMuons (new std::vector<pat::Muon>());

  
   //std::cout << " mark 1 " << std::endl;
 
  for(size_t i = 0; i < initialMuons->size(); ++i){



    //std::cout << " mark 2, i: "<< i << std::endl;
    
    pat::Muon & mu = (*initialMuons)[i];
    mu.addUserFloat("DeltaCorrectedIso",(mu.chargedHadronIso() + std::max(0., mu.neutralHadronIso() + mu.photonIso() -0.5*mu.puChargedHadronIso()))/mu.pt());
    mu.addUserFloat("RhoCorrectedIso",(mu.chargedHadronIso() + std::max(0., mu.neutralHadronIso() + mu.photonIso() -energy_))/mu.pt());

    //std::cout << " mark 3, i: "<< i << std::endl;
    
    double dz= 9900;
    double dxy= 9900;

    //std::cout << " mark 4, i: "<< i << std::endl;


    if(vertices->size()>0) {
      //      if(!(el.gsfTrack() == NULL)) 
      //else std::cout << "electron lost track ref!  Distance being set to an unphysical value (99 meters)."<<std::endl;
      
      //std::cout << " mark 5, i: "<< i << std::endl;

      //std::cout << " mark 6, i: "<< i << std::endl;

      if( mu.isGlobalMuon() ){
	
	//std::cout << " mark 7, i: "<< i << std::endl;

	dz = fabs(mu.innerTrack()->dz(vertices->at(0).position()));
	
	//std::cout << " mark 8, i: "<< i << std::endl;
	
	dxy = fabs(mu.innerTrack()->dxy(vertices->at(0).position()));

      }

      
          //else{
      //	dz = fabs(mu.vertex().z()- vertices->at(0).z());
      //	dxy = sqrt( (mu.vertex().x() -vertices->at(0).x())*(mu.vertex().x() -vertices->at(0).x()) +
      //		    (mu.vertex().y() -vertices->at(0).y())*(mu.vertex().y() -vertices->at(0).y()) );
      // }
    }
    else std::cout<< "no offline primary vertex! Check again the collections. Distance DZ,DXY being set to an unphysical value (99 meters)."<<std::endl;    
    //std::cout << " passes cut " << cut_ <<  std::endl;
    
    mu.addUserFloat("VertexDz",dz);
    mu.addUserFloat("VertexDxy",dxy);


    float genPDGId = -99;
    float motherPDGId = -99;
    float grandmotherPDGId = -99;

    int hasTparent = -99;
    int hasBparent = -99;
    int hasWparent = -99;
    int hasZparent = -99;
    int hasHparent = -99;

    const reco::GenParticle * gen_Part = mu.genParticle();

    if (gen_Part){
      hasTparent = 0;
      hasBparent = 0;
      hasWparent = 0;
      hasZparent = 0;
      hasHparent = 0;

      genPDGId = gen_Part->pdgId();
      motherPDGId = gen_Part->mother()->pdgId();
      grandmotherPDGId = gen_Part->mother()->mother()->pdgId();

      const reco::Candidate * motherPart = gen_Part->mother();

      if (abs(motherPart->pdgId())==5)  {hasBparent = motherPart->pdgId()/abs(motherPart->pdgId());}
      if (abs(motherPart->pdgId())==6)  {hasTparent = motherPart->pdgId()/abs(motherPart->pdgId());}
      if (abs(motherPart->pdgId())==23) {hasZparent = motherPart->pdgId()/abs(motherPart->pdgId());}
      if (abs(motherPart->pdgId())==24) {hasWparent = motherPart->pdgId()/abs(motherPart->pdgId());}
      if (abs(motherPart->pdgId())==25) {hasHparent = motherPart->pdgId()/abs(motherPart->pdgId());}
      
      while (motherPart->mother()){
	motherPart = motherPart->mother();
	if (abs(motherPart->pdgId())==5)  {hasBparent = motherPart->pdgId()/abs(motherPart->pdgId());}
	if (abs(motherPart->pdgId())==6)  {hasTparent = motherPart->pdgId()/abs(motherPart->pdgId());}
	if (abs(motherPart->pdgId())==23) {hasZparent = motherPart->pdgId()/abs(motherPart->pdgId());}
	if (abs(motherPart->pdgId())==24) {hasWparent = motherPart->pdgId()/abs(motherPart->pdgId());}
        if (abs(motherPart->pdgId())==25) {hasHparent = motherPart->pdgId()/abs(motherPart->pdgId());}
      }

    }

    mu.addUserFloat("genPDGId",genPDGId);
    mu.addUserFloat("motherPDGId",motherPDGId);
    mu.addUserFloat("grandmotherPDGId",grandmotherPDGId);

    mu.addUserInt("hasBparent",hasBparent);
    mu.addUserInt("hasTparent",hasTparent);
    mu.addUserInt("hasZparent",hasZparent);
    mu.addUserInt("hasWparent",hasWparent);
    mu.addUserInt("hasHparent",hasHparent);
    
    //    std::cout<<" i " <<i << "pt " <<mu.pt()<< " passes cut ? "<< cut(mu) << std::endl; 
    

    if(cut(mu)) finalMuons->push_back(mu);
    //if(!cut(mu)) finalMuons->erase(finalMuons->begin()+i) ; 
    //if(!cut(mu)) finalMuons->pop_back() ; 
  
  } 
 
  //std::cout << " mark 7 " << std::endl;

  //std::auto_ptr< std::vector< pat::Muon > > finalMuonsPtr(finalMuons);
 
  
iEvent.put(finalMuons);

}

SingleTopMuonProducer::~SingleTopMuonProducer(){;}
DEFINE_FWK_MODULE(SingleTopMuonProducer);
