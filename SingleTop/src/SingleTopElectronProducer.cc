/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopElectronProducer.cc,v 1.7.12.4.2.2 2012/11/21 17:43:50 dnoonan Exp $ 
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

#include "DataFormats/EgammaCandidates/interface/Conversion.h"
#include "DataFormats/RecoCandidate/interface/IsoDeposit.h"


//#include "EGamma/EGammaAnalysisTools/interface/EGammaCutBasedEleId.h"
#include "RecoEgamma/EgammaTools/interface/ConversionTools.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "DataFormats/VertexReco/interface/VertexFwd.h"
#include "DataFormats/Common/interface/ValueMap.h"


#include "DataFormats/Math/interface/deltaR.h"

#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"

#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"


#include "FWCore/Framework/interface/Selector.h"

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopElectronProducer.h"


#include "DataFormats/Scalers/interface/DcsStatus.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "RecoEgamma/EgammaTools/interface/ConversionFinder.h"
#include "PhysicsTools/SelectorUtils/interface/SimpleCutBasedElectronIDSelectionFunctor.h"


#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;

typedef std::vector< edm::Handle< edm::ValueMap<reco::IsoDeposit> > >   IsoDepositMaps;
typedef std::vector< edm::Handle< edm::ValueMap<double> > >             IsoDepositVals;


SingleTopElectronProducer::SingleTopElectronProducer(const edm::ParameterSet& iConfig)
{
  src_                 = iConfig.getParameter<edm::InputTag>( "src" );
  cut_ = iConfig.getParameter< std::string >("cut"); 
  rho_ = iConfig.getParameter<edm::InputTag> ("rho");
  deltaR_ = iConfig.getUntrackedParameter<double>         ( "deltaR",0.3 );
  //  category_ = iConfig.getUntrackedParameter<std::string>         ( "category","none");
  
  

  produces<std::vector<pat::Electron> >();
}

void SingleTopElectronProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){

  edm::Handle<edm::View<reco::Vertex> > vertices;
  iEvent.getByLabel("offlinePrimaryVertices",vertices);


  ////std::cout << " mark 0 " << std::endl;

  ////std::cout << " mark 1 " << std::endl;
  //  edm::Handle<edm::View<pat::Electron> > electrons;
  edm::Handle<std::vector<pat::Electron> > electrons;
  iEvent.getByLabel(src_,electrons);
  iEvent.getByLabel(rho_,rho);
  double rhoD = *rho; 

  double Aeff = 1.;



  double energy_ = TMath::Pi()*deltaR_*deltaR_* (*rho);
  

  edm::Handle<reco::ConversionCollection> conversions;
  iEvent.getByLabel("allConversions", conversions);

  // iso deposits
  //IsoDepositVals isoVals(isoVals_.size());
  //for (size_t j = 0; j < isoVals_.size(); ++j) {
  //  iEvent.getByLabel(isoVals_[j], isoVals[j]);
  //}

  edm::Handle<reco::BeamSpot> beamspot;
  iEvent.getByLabel("offlineBeamSpot", beamspot);
  const reco::BeamSpot &beamSpot = *(beamspot.product());


  Selector cut(cut_);
  std::auto_ptr< std::vector< pat::Electron > > initialElectrons (new std::vector<pat::Electron>(*electrons));
  std::auto_ptr< std::vector< pat::Electron > > finalElectrons (new std::vector<pat::Electron>());

  ////std::cout << " mark 2 " << std::endl;
    
  //  std::cout << "size before "<< initialElectrons->size()<< std::endl;
  
  for(size_t i = 0; i < initialElectrons->size(); ++i){
    
    bool passes = true;
    
    pat::Electron & el = (*initialElectrons)[i];

    Aeff = 1.;

    //NEWEST Data2012 nubmers
    //https://twiki.cern.ch/twiki/bin/view/CMS/EgammaEARhoCorrection#Isolation_cone_R_0_3

    if (abs(el.superCluster()->eta() < 1.0)){ Aeff = 0.13;}
    else if (abs(el.superCluster()->eta() < 1.479)){ Aeff = 0.14;}
    else if (abs(el.superCluster()->eta() < 2.0)){ Aeff = 0.07;}
    else if (abs(el.superCluster()->eta() < 2.2)){ Aeff = 0.09;}
    else if (abs(el.superCluster()->eta() < 2.3)){ Aeff = 0.11;}
    else if (abs(el.superCluster()->eta() < 2.4)){ Aeff = 0.11;}
    else { Aeff = 0.14;}



    float genPDGId = -99;
    float motherPDGId = -99;
    float grandmotherPDGId = -99;

    int hasTparent = -99;
    int hasBparent = -99;
    int hasWparent = -99;
    int hasZparent = -99;
    int hasHparent = -99;

    const reco::GenParticle * gen_Part = el.genParticle();

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

    el.addUserFloat("genPDGId",genPDGId);
    el.addUserFloat("motherPDGId",motherPDGId);
    el.addUserFloat("grandmotherPDGId",grandmotherPDGId);

    el.addUserInt("hasBparent",hasBparent);
    el.addUserInt("hasTparent",hasTparent);
    el.addUserInt("hasZparent",hasZparent);
    el.addUserInt("hasWparent",hasWparent);
    el.addUserInt("hasHparent",hasHparent);
    
    
    el.addUserFloat("DeltaCorrectedIso",(el.chargedHadronIso() + std::max(0., el.neutralHadronIso() + el.photonIso() -0.5*el.puChargedHadronIso()))/el.et());
    el.addUserFloat("RhoCorrectedIso",(el.chargedHadronIso() + std::max(0., el.neutralHadronIso() + el.photonIso() -rhoD*Aeff))/el.et());
    
    double dxy= 9900;
    double dz= 9900;
    if(vertices->size()>0) {
      //      if(!(el.gsfTrack() == NULL)) 
      //else std::cout << "electron lost track ref!  Distance being set to an unphysical value (99 meters)."<<std::endl;
      dz = fabs(el.gsfTrack()->dz(vertices->at(0).position()));
      dxy = fabs(el.gsfTrack()->dxy(vertices->at(0).position()));
    }
    //    else std::cout<< "no offline primary vertex! Check again the collections. Distance being set to an unphysical value (99 meters)."<<std::endl;
    
    el.addUserFloat("VertexDz",dz);
    el.addUserFloat("VertexDxy",dxy);
    
    if(!cut(el)) passes = false;

//     // get the mask value
//     if(category_ == "veto" || category_ == "tight" || category_ == "loose" ){
//     double iso_ch = el.chargedHadronIso();
//     double iso_em = el.photonIso();
//     double iso_nh =  el.neutralHadronIso();
    
//     bool isEB           = el.isEB() ? true : false;
//     float pt            = el.pt();
//     float eta           = el.superCluster()->eta();

//     // id variables                                                                                                                                                    
//     float dEtaIn        = el.deltaEtaSuperClusterTrackAtVtx();
//     float dPhiIn        = el.deltaPhiSuperClusterTrackAtVtx();
//     float sigmaIEtaIEta = el.sigmaIetaIeta();
//     float hoe           = el.hadronicOverEm();
//     float ooemoop       = (1.0/el.ecalEnergy() - el.eSuperClusterOverP()/el.ecalEnergy());
//     // conversion rejection variables
//     bool vtxFitConversion = ConversionTools::hasMatchedConversion(el, conversions, beamSpot.position());
//     float mHits = el.gsfTrack()->trackerExpectedHitsInner().numberOfHits(); 
    
//     //    std::cout << " test id: category "<< category_ << " isEB " << isEB << " pt " << pt << " eta "<< eta << 
//     //  " dEtaIn " << dEtaIn << " dPhiIn " << dPhiIn << " sigmaIEtaIEta " << sigmaIEtaIEta << " hoe "<< hoe <<
//     //  " ooemoop " << ooemoop << " dxy " << dxy  << " dz " << dz << " iso_ch " << iso_ch<< " iso_em " << iso_em<< " iso_nh "<< iso_nh <<
//     //  " vtxFitConversion " << vtxFitConversion << " mHits " << mHits << " rhoD " <<rhoD <<  std::endl;
    
//     if(category_ == "tight"){
//       bool id = EgammaCutBasedEleId::PassWP(EgammaCutBasedEleId::TIGHT, isEB, pt, eta, dEtaIn, dPhiIn, sigmaIEtaIEta, hoe, ooemoop, dxy, dz, iso_ch, iso_em, iso_nh, vtxFitConversion, mHits, rhoD);
//       passes = passes && id;
//     }
//     if(category_ == "loose"){
//       bool id = EgammaCutBasedEleId::PassWP(EgammaCutBasedEleId::LOOSE, isEB, pt, eta, dEtaIn, dPhiIn, sigmaIEtaIEta, hoe, ooemoop, dxy, dz, iso_ch, iso_em, iso_nh, vtxFitConversion, mHits, rhoD);
//       passes = passes && id;
//     }
//     if(category_ == "veto"){
//       bool id = EgammaCutBasedEleId::PassWP(EgammaCutBasedEleId::VETO, isEB, pt, eta, dEtaIn, dPhiIn, sigmaIEtaIEta, hoe, ooemoop, dxy, dz, iso_ch, iso_em, iso_nh, vtxFitConversion, mHits, rhoD);
//       passes = passes && id;
//     }
   
//     }
    
    if(passes)finalElectrons->push_back(el);
    
    //std::cout << " passes cut " << cut_ <<  std::endl;
    
    //    finalElectrons->push_back(electrons->at(i));
  } 
 
  //  std::cout << "size after "<< finalElectrons->size()<< std::endl;
  ////std::cout << " mark 7 " << std::endl;

  //std::auto_ptr< std::vector< pat::Electron > > finalElectronsPtr(finalElectrons);
 

iEvent.put(finalElectrons);

}

SingleTopElectronProducer::~SingleTopElectronProducer(){;}
DEFINE_FWK_MODULE(SingleTopElectronProducer);
