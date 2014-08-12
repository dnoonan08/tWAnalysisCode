/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopJetsProducer.cc,v 1.5.12.3 2012/08/15 09:36:38 oiorio Exp $ 
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
#include "DataFormats/JetReco/interface/JPTJet.h"
#include "DataFormats/JetReco/interface/CaloJet.h"

#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "CMGTools/External/interface/PileupJetIdentifier.h"

#include "CMGTools/External/interface/PileupJetIdentifier.h"

#include "FWCore/Framework/interface/Selector.h"

#include <TLorentzVector.h>


#include "TopQuarkAnalysis/SingleTop/interface/SingleTopJetsProducer.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


SingleTopJetsProducer::SingleTopJetsProducer(const edm::ParameterSet& iConfig) 
{
  src_                 = iConfig.getParameter<edm::InputTag>	      ( "src" );

  PUFullDiscriminant_  = iConfig.getParameter<edm::InputTag>	      ( "puFullDiscriminant" );
  PUFullID_                 = iConfig.getParameter<edm::InputTag>	      ( "puFullID" );

  PUChargedDiscriminant_  = iConfig.getParameter<edm::InputTag>	      ( "puChargedDiscriminant" );
  PUChargedID_                 = iConfig.getParameter<edm::InputTag>	      ( "puChargedID" );

  PUIDVariables_                 = iConfig.getParameter<edm::InputTag>	      ( "puIDVariables" );

  

  cut_ = iConfig.getParameter< std::string >("cut"); 
  
  removeOverlap_ = iConfig.getUntrackedParameter< bool >("removeOverlap",true); 
  electronsSrc_ = iConfig.getParameter<edm::InputTag>("electronsSrc");

  produces<std::vector<pat::Jet> >();
  //produces<std::vector<pat::Jet> >();

 
  //  std::vector<edm::InputTag> names = overlapPSet.getParameterNamesForType< edm::InputTag >

}

void SingleTopJetsProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){
  
  
  
  //  for(std::vector<edm::InputTag>::const_iterator it=names.begin();it != names.end;++it){}

  iEvent.getByLabel(src_,jets);
  iEvent.getByLabel(src_,vjets);

  std::auto_ptr< std::vector< pat::Jet > > initialJets(new std::vector< pat::Jet >(*jets));
  std::auto_ptr< std::vector< pat::Jet > > finalJets(new std::vector< pat::Jet >);


  
  iEvent.getByLabel(PUFullDiscriminant_,puFullJetIdMVA);
  iEvent.getByLabel(PUFullID_,puFullJetIdFlag);  
  iEvent.getByLabel(PUChargedDiscriminant_,puChargedJetIdMVA);
  iEvent.getByLabel(PUChargedID_,puChargedJetIdFlag);  

  iEvent.getByLabel(PUIDVariables_, puIDVariables);  

  if(removeOverlap_)iEvent.getByLabel(electronsSrc_,electrons);


  
  
  for(size_t i = 0; i < jets->size(); ++i){
    //    pat::Jet & jet = (*initialJets)[i];
    pat::Jet & jet = (*initialJets)[i];
    
    bool isOverlapped = false;
    if(removeOverlap_){
      for(size_t e = 0; e < electrons->size(); ++e){
	if(deltaR(jets->at(i),electrons->at(e))<0.3) {
	  isOverlapped = true;
	  break;
	}
      }
    }
    if( isOverlapped)continue;

    Selector cut(cut_);
    if(!cut(jet))continue; 


 
      
    float leadingTrackPt = -9999;      

    std::vector <reco::PFCandidatePtr> constituents = (jets->at(i)).getPFConstituents();
    for (unsigned ic = 0; ic < constituents.size (); ++ic) {
      if ( constituents[ic]->particleId() > 3 ) continue;
      reco::TrackRef trackRef = constituents[ic]->trackRef();
      if ( trackRef.isNonnull() ) { if(trackRef->pt() > leadingTrackPt) leadingTrackPt=trackRef->pt(); }
    }

    edm::Handle<edm::View<reco::Candidate> > eleNoCutsHandle;
    iEvent.getByLabel("gsfElectrons",eleNoCutsHandle);
    edm::View<reco::Candidate> elesNoCuts = *eleNoCutsHandle; 

    edm::Handle<edm::View<reco::Candidate> > muonNoCutsHandle;
    iEvent.getByLabel("muons",muonNoCutsHandle);
    edm::View<reco::Candidate> muonsNoCuts = *muonNoCutsHandle; 

    float softleptPtRel = -99.;
    float softleptPt = -99.;
    float softleptdR = -99.;
    float softleptpdgId = -99;
    float softleptIdlooseMu = 0;
    float softleptId95 = 0;

    int isSemiLept = 0;

    TVector3 jvec ( jets->at(i).p4().Vect().X(), jets->at(i).p4().Vect().Y(), jets->at(i).p4().Vect().Z()  );

    for(edm::View<reco::Candidate>::const_iterator mu = muonsNoCuts.begin(); mu!=muonsNoCuts.end() && isSemiLept!=1; ++mu){
      //      std::cout<< "found a muon with pt " << mu->pt()   << std::endl;
      const pat::Muon& m = static_cast <const pat::Muon&> (*mu); 
      float Smpt = m.pt(); 
      float Smeta = m.eta();
      float Smphi = m.phi();

      float SmJdR = deltaR(Smeta, Smphi, jets->at(i).eta(), jets->at(i).phi());
      if   ( Smpt> 5. && SmJdR <0.5) {
	isSemiLept = 1;

	softleptpdgId =13;
	softleptdR= SmJdR;
	softleptPt=Smpt;
	TVector3 mvec ( m.p4().Vect().X(), m.p4().Vect().Y(), m.p4().Vect().Z()  ); 
	softleptPtRel=  jvec.Perp(  mvec );
	softleptIdlooseMu = m.muonID("TMLastStationLoose");
      }
    }


    for(edm::View<reco::Candidate>::const_iterator ele = elesNoCuts.begin(); ele!=elesNoCuts.end() && isSemiLept!=1; ++ele){
      const pat::Electron& e = static_cast <const pat::Electron&> (*ele); 
      float Smpt = e.pt(); 
      float Smeta = e.eta();
      float Smphi = e.phi();

      float SmJdR = deltaR(Smeta, Smphi, jets->at(i).eta(), jets->at(i).phi());
      if   ( Smpt> 5. && SmJdR <0.5) {
	isSemiLept = 1;

	softleptpdgId =13;
	softleptdR= SmJdR;
	softleptPt=Smpt;
	TVector3 mvec ( e.p4().Vect().X(), e.p4().Vect().Y(), e.p4().Vect().Z()  ); 
	softleptPtRel=  jvec.Perp(  mvec );

	if (( fabs(Smeta)<2.5 && !( abs(Smeta)>1.4442 && abs(Smeta)<1.566))  && 
	    (( abs(Smeta)>1.566  && (e.sigmaIetaIeta()<0.01) && ( e.deltaPhiSuperClusterTrackAtVtx()<0.8  && e.deltaPhiSuperClusterTrackAtVtx()>-0.8) && ( e.deltaEtaSuperClusterTrackAtVtx()<0.007 && e.deltaEtaSuperClusterTrackAtVtx()>-0.007 )  )
	     || ( abs(Smeta)<1.4442  && (e.sigmaIetaIeta()<0.03) && ( e.deltaPhiSuperClusterTrackAtVtx()<0.7 && e.deltaPhiSuperClusterTrackAtVtx()>-0.7 ) && ( e.deltaEtaSuperClusterTrackAtVtx()<0.01 && e.deltaEtaSuperClusterTrackAtVtx()>-0.01 ) )) )
	  softleptId95=1;

      }
    }


    float vtxPt = -99.;
    float vtxMass = -99;
    float vtxNTracks = -99;
    float vtx3dL = -99;
    float vtx3deL = -99;

    const reco::SecondaryVertexTagInfo * tf = jets->at(i).tagInfoSecondaryVertex("secondaryVertex");
    
    if (tf){
      math::XYZTLorentzVectorD vertexSum;
      for(size_t vi=0;vi< tf->nVertices();vi++)
	{
	  vertexSum+=tf->secondaryVertex(vi).p4();
	}
      vtxPt = vertexSum.Pt();

      if (tf->nVertices() >0){
	vtxMass =  tf->secondaryVertex(0).p4().mass();
	vtxNTracks = tf->secondaryVertex(0).nTracks();

	Measurement1D m = tf->flightDistance(0);
	vtx3dL = m.value();
	vtx3deL = m.error();
      }
    }

    float genPDGId = -99;
    float motherPDGId = -99;
    float grandmotherPDGId = -99;

    const reco::GenParticle * gen_Jet = jets->at(i).genParticle();

    int hasTparent = -99;
    int hasBparent = -99;
    int hasWparent = -99;
    int hasZparent = -99;
    int hasHparent = -99;

    if (gen_Jet){
      hasTparent = 0;
      hasBparent = 0;
      hasWparent = 0;
      hasZparent = 0;
      hasHparent = 0;

      genPDGId = gen_Jet->pdgId();
      if (gen_Jet->mother()){ motherPDGId = gen_Jet->mother()->pdgId();}
      if (gen_Jet->mother()->mother()){ grandmotherPDGId = gen_Jet->mother()->mother()->pdgId();}

      const reco::Candidate * motherPart = gen_Jet->mother();

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


    jet.addUserFloat("vtxPt",vtxPt);
    jet.addUserFloat("vtxMass",vtxMass);
    jet.addUserFloat("vtxNTracks",vtxNTracks);
    jet.addUserFloat("vtx3dL",vtx3dL);
    jet.addUserFloat("vtx3deL",vtx3deL);

    jet.addUserFloat("genPDGId",genPDGId);
    jet.addUserFloat("motherPDGId",motherPDGId);
    jet.addUserFloat("grandmotherPDGId",grandmotherPDGId);

    jet.addUserInt("hasBparent",hasBparent);
    jet.addUserInt("hasTparent",hasTparent);
    jet.addUserInt("hasZparent",hasZparent);
    jet.addUserInt("hasWparent",hasWparent);
    jet.addUserInt("hasHparent",hasHparent);
    
    jet.addUserFloat("ptLeadingTrack",leadingTrackPt);
    jet.addUserFloat("ptRaw",(jets->at(i)).correctedJet(0).pt());

    jet.addUserFloat("isSemiLept",isSemiLept);
    jet.addUserFloat("SoftLeptpdgId",softleptpdgId);
    jet.addUserFloat("SoftLeptPt",softleptPt);
    jet.addUserFloat("SoftLeptPtRel",softleptPtRel);
    jet.addUserFloat("SoftLeptdR",softleptdR);
    jet.addUserFloat("SoftLeptIdlooseMu",softleptIdlooseMu);
    jet.addUserFloat("SoftLeptId95",softleptId95);




    jet.addUserFloat("PUFullDiscriminant", (*puFullJetIdMVA)[(vjets->refAt(i))]);
    jet.addUserFloat("PUChargedDiscriminant", (*puChargedJetIdMVA)[(vjets->refAt(i))]);


    jet.addUserFloat("beta", ((*puIDVariables)[(vjets->refAt(i))]).beta());
    jet.addUserFloat("betaStar", ((*puIDVariables)[(vjets->refAt(i))]).betaStar());
    jet.addUserFloat("RMS", ((*puIDVariables)[(vjets->refAt(i))]).RMS());
    jet.addUserFloat("dZ", ((*puIDVariables)[(vjets->refAt(i))]).dZ());
    
    int wp = 0;
    
    int idflag = (*puFullJetIdFlag)[ (vjets->refAt(i))];
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kLoose ) ) {
	  wp =1;
	}
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kMedium )) {
	  wp =2;
	 }
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kTight )) {
	   wp =3;
	 }
	
    
    jet.addUserFloat("PUFullWorkingPoint",wp);

    int wpchs =0; 
    
    int idflagchs = (*puChargedJetIdFlag)[ (vjets->refAt(i))];
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kLoose ) ) {
	  wpchs =1;
	}
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kMedium )) {
	  wpchs =2;
	 }
    if( PileupJetIdentifier::passJetId( idflag, PileupJetIdentifier::kTight )) {
	   wpchs =3;
	 }

    jet.addUserFloat("PUChargedWorkingPoint",wpchs);
    
    
  

    finalJets->push_back(jet);

  }

  //std::cout << "mark 5"<< std::endl;  
  
  iEvent.put(finalJets);
  
  //std::cout << "mark 6"<< std::endl;  

}

SingleTopJetsProducer::~SingleTopJetsProducer(){;}
DEFINE_FWK_MODULE(SingleTopJetsProducer);
