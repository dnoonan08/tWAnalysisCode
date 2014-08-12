/*
 *\Authors:A.Giammanco, A. Orso M. Iorio 
 *
 *
 *\version  $Id: SingleTopTChannelMCProducer.cc,v 1.2 2010/03/26 15:41:27 oiorio Exp $ 
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




////////Part to be made official
#include "../interface/SingleTopTChannelMCProducer.h"

#include <vector>
#include <memory>



//using namespace pat;


SingleTopTChannelMCProducer::SingleTopTChannelMCProducer(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables

  isSingleTopTChan_ =  iConfig.getUntrackedParameter<bool>("isSingleTopTChan",true);  
  
  genParticlesSrc_ = iConfig.getParameter<edm::InputTag>( "genParticlesSource" );
  //GenJets for matching
  //  genJetsSrc_ = iConfig.getParameter<edm::InputTag>( "genJetsSource" );

  genJetsDeltarMatching_ = iConfig.getUntrackedParameter<double> ( "genJetsDeltarMatching", 0.3 );

  produces<std::vector<reco::GenParticle> >("bGenParticles").setBranchAlias("bGenParticles");
  produces<std::vector<reco::GenParticle> >("secondBGenParticles").setBranchAlias("secondBGenParticles");

  produces<std::vector<reco::GenParticle> >("singleTopRecoilQuark").setBranchAlias("singleTopRecoilQuark");
 
  produces<std::vector<reco::GenJet> >("bGenJets").setBranchAlias("bGenJets");

  produces<std::vector<reco::GenParticle> >("topLeptons").setBranchAlias("topLeptons");

  produces<std::vector<reco::GenParticle> >("topNeutrinos").setBranchAlias("topNeutrinos");

  produces<std::vector<reco::GenParticle> >("tops").setBranchAlias("tops");
  produces<std::vector<reco::GenParticle> >("pseudoRecoTops").setBranchAlias("pseudoRecoTops");
  
}

void SingleTopTChannelMCProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){


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

std::auto_ptr< std::vector< reco::GenParticle > > bGenParticles( new std::vector<reco::GenParticle> );

std::auto_ptr< std::vector< reco::GenParticle > > secondBGenParticles( new std::vector<reco::GenParticle> );

std::auto_ptr< std::vector< reco::GenParticle > > singleTopRecoilQuark( new std::vector<reco::GenParticle> );

std::auto_ptr< std::vector< reco::GenJet > > bGenJets( new std::vector<reco::GenJet> );

std::auto_ptr< std::vector< reco::GenParticle > > topLeptons( new std::vector<reco::GenParticle> );

std::auto_ptr< std::vector< reco::GenParticle > > topNeutrinos( new std::vector<reco::GenParticle> );

std::auto_ptr< std::vector< reco::GenParticle > > tops( new std::vector<reco::GenParticle> );

std::auto_ptr< std::vector< reco::GenParticle > > pseudoRecoTops( new std::vector<reco::GenParticle> );

#if DEBUG
  std::cout << "producer 3" << std::endl;
#endif

 if(isSingleTopTChan_){
   try{
/* for(size_t i = 0; i < allParticles->size() ; ++i){
   const reco::GenParticle MCParticle = allParticles->at(i);

   if(abs(MCParticle.pdgId())==5 && MCParticle.status()==3 ){
     for(size_t m = 0; m < MCParticle.numberOfMothers(); ++m){
       if(abs(MCParticle.mother(m)->pdgId())==6 && MCParticle.mother(m)->status()==3){
	 bGenParticles->push_back(MCParticle);
	 break;
      }
     }
   }

   if((abs(MCParticle.pdgId()) < 5 || MCParticle.pdgId() == 21) && MCParticle.status()==3 ){
       std::cout << "non B parton id: " <<  MCParticle.pdgId() << " collision id "<< MCParticle.collisionId()  << std::endl;
     for(size_t m = 0; m < MCParticle.numberOfMothers(); ++m){
       std::cout << " particle mother n " << m + 1 << " mother id " << MCParticle.mother(m)->pdgId() <<std::endl;
     }
   }
 }
*/


  bool debug = false;

  using namespace std;
  using namespace edm;
  using namespace reco;

  //  bool error              = false;
  bool isGluonSplitLQLine = false;
  bool noVtb              = false;
  
  bool top_found  = false;
  bool btop_found = false;
  bool W_found    = false;
  bool lep_found  = false;
  bool nu_found   = false;
  bool lq_found   = false;
  bool secb_found = false;

  bool noW        = true; // MG samples 22x: sometimes no W from top decay listed, build it as sum of lep and nu!
  bool noTop      = true; // MG samples 22x: sometimes no top listed, build it as sum of lep, nu, and btop!

  int idx       = 0;
  int top_id    = 0;
  int secb_id   = 0;
  int btop_id   = 0;

  const Candidate *topMo=NULL, *top=NULL ,*W=NULL, *btop=NULL,
    *lep=NULL, *nu=NULL, *recoilQuark=NULL, *bSecond=NULL, *pseudoRecoTop=NULL;
#if DEBUG
  std::cout << "producer 4" << std::endl;
#endif
  
  // get event weight 
  //  double wgt = 0;
  //  wgt = (weight > 0) ? 1. : -1.; // take only sign of event weigth!
  
  //mcST->eventWeight = wgt;
  
  //   h["eventWeightSign"]->Fill(wgt);
  //   h["eventWeight"]->Fill(weight);
  
  for(std::vector<reco::GenParticle> ::const_iterator p=genParticles->begin(); p != genParticles->end(); ++p){
    

#if DEBUG
  std::cout << "producer 5" << std::endl;
#endif

    

    if((abs(p->pdgId()) == 11 
	|| abs(p->pdgId()) == 13 
	|| abs(p->pdgId()) == 15) && !lep_found){  // charged lepton found ...first one in list
      lep = &(*p);
      lep_found = true;
      
      //mcST->mcLepID = p->pdgId();

      // lep info  -------------------------------------------------------------
      if(lep->pdgId() == -11 || lep->pdgId() == -13 || lep->pdgId() == -15){
	top_id = 6;
	secb_id = -5;
	btop_id = 5;
	//mcST->QLep_gen = 1;
      }
      else 
	if(lep->pdgId() == 11 || lep->pdgId() == 13 || lep->pdgId() == 15){
	  top_id = -6;
	  secb_id = 5;
	  btop_id = -5;
	  //mcST->QLep_gen = -1;
	}
      


      if(p->numberOfMothers()>= 1){
#if DEBUG
  std::cout << "producer 6" << std::endl;
#endif
	for (unsigned int ilepM=0; ilepM<p->numberOfMothers(); ilepM++){       // check lep mothers ...
	  if(abs(p->mother(ilepM)->pdgId()) == 24){                            // yes, we found the W!!
	    W=p->mother(ilepM);
	    W_found = true;
	    noW = false;
	    // set neutrino ...
	    for (unsigned int iWD=0; iWD<W->numberOfDaughters(); iWD++){
	      if(abs(W->daughter(iWD)->pdgId()) == 12 
		 || abs(W->daughter(iWD)->pdgId()) == 14 
		 || abs(W->daughter(iWD)->pdgId()) == 16){
		nu=W->daughter(iWD);
		nu_found = true;
	      }
	    }
	    for (unsigned int iWM=0; iWM<W->numberOfMothers(); iWM++){   //check W mothers ...
	      if(abs(W->mother(iWM)->pdgId()) == 6){                     // yes, we found the top via the W!!
		top=W->mother(iWM);
		top_found = true;
		noTop = false;
	      }
	    }
	    if(!top_found){                                                                    // no top found in list -> need to get btop as daughter of W mother
	      for (unsigned int iWM=0; iWM<W->numberOfMothers(); iWM++){                       // check W mothers
		for (unsigned int iWMD=0; iWMD<(W->mother(iWM))->numberOfDaughters(); iWMD++){ // check daughters of W mothers
		  if((W->mother(iWM))->daughter(iWMD)->pdgId() == btop_id){                    // btop found
		    btop_found = true;
		    btop = (W->mother(iWM))->daughter(iWMD);
		  }
		}
	      }
	    }
	    else{                                                                 // top was found, we are able to check directly the top daughters to find btop
	      for (unsigned int itop=0; itop<top->numberOfDaughters(); itop++){   //check top daughters ...
		if(abs(top->daughter(itop)->pdgId()) == 5){                       // btop found
		  btop = top->daughter(itop);
		  btop_found = true;
		}
	      }
	    }
	  }
	  else{                                                      // no W found ... 
	    noW = true;
	    W_found = true;
	    if(abs(p->mother(ilepM)->pdgId()) == 6){                 //  ... but we found top directly as mother of lep ...-> no W in list!
#if DEBUG
  std::cout << "producer 7" << std::endl;
#endif

	      top=p->mother(ilepM);
	      top_found = true;
	      noTop=false;
	      for (unsigned int itopD=0; itopD<top->numberOfDaughters(); itopD++){   // loop daughters of top to get neutrino:
		if(abs(top->daughter(itopD)->pdgId()) == 12 
		   || abs(top->daughter(itopD)->pdgId()) == 14 
		   || abs(top->daughter(itopD)->pdgId()) == 16){                     // neutrino found ...
		  nu = top->daughter(itopD);
		  nu_found = true;
		}
		if(abs(top->daughter(itopD)->pdgId()) == 5){                         // btop found
		  btop = top->daughter(itopD);
		  btop_found = true;
		}
	      }
	    }
	  }
	}
	
	// special case: neither top nor W are in the list!
	if(noW)
	  if(noTop){
#if DEBUG
  std::cout << "producer 8" << std::endl;
#endif
	    for (unsigned int ilepM=0; ilepM<lep->numberOfMothers(); ilepM++){                           // check mothers of lepton
	      for (unsigned int ilepMD=0; ilepMD<(lep->mother(ilepM))->numberOfDaughters(); ilepMD++){   // check daughters of lepton mothers
		if((lep->mother(ilepM))->daughter(ilepMD)->pdgId() == btop_id){                          // found btop
		  btop_found = true;
		  btop = (lep->mother(ilepM))->daughter(ilepMD);
		}
		if(abs((lep->mother(ilepM))->daughter(ilepMD)->pdgId()) == 12 
		   || abs((lep->mother(ilepM))->daughter(ilepMD)->pdgId()) == 14 
		   || abs((lep->mother(ilepM))->daughter(ilepMD)->pdgId()) == 16){
		  nu_found = true;                                                                       // found neutrino 
		  nu = (lep->mother(ilepM))->daughter(ilepMD);
		}
	      }
	    }
	  }
      }
      

#if DEBUG
  std::cout << "producer 9" << std::endl;
#endif
      // decay channel:
      if(abs(lep->pdgId()) == 11 || abs(lep->pdgId()) == 13)
	//mcST->DecChan = 0;
      if(abs(lep->pdgId()) == 15)
	//mcST->DecChan = 1;
      
      
      // --------------------- DEBUG INFO ----------------------------------------
      if(debug)cout << "after first finding stuff .. let's summarize:" << endl;
      
      if(noW && !noTop)
	if(debug) cout << "there is no W from top decay!" << endl;
      if(noTop && !noW)
	if(debug) cout << "there is no top!" << endl;
      if(noW && noTop)
	if(debug) cout << "there is neither top nor W in list!" << endl;
      
      if(!noTop) if(debug) cout << "this is my new top: " << top->pdgId() << "\t" << top->status() << "\t" << top->px() << endl;
      if(!noTop && !noW) if(debug) cout << "this is my new btop: " << btop->pdgId() << "\t" << btop->status() << "\t" << btop->px() << endl;		      
      if(!noW) if(debug) cout << "this is my new W boson: " << W->pdgId() << "\t" << W->status() << "\t" << W->px() << endl;
      if(debug) cout << "this is my new neutrino: " << nu->pdgId() << "\t" << nu->status() << "\t" << nu->px() << endl;		
      if(debug) cout << "this is my new lepton: " << lep->pdgId() << "\t" << lep->status() << "\t" << lep->px() << endl;		
      // --------------------- DEBUG INFO END ----------------------------------------
      
     
      // --- light quark ----------------------
      
      const Candidate *p_=NULL; // pointer to "earliest" parton in process chain after the hard scattering 
                                //             (which has initial state partons as mothers)
                                // ideal: top is in list
                                // if not: set it on W
                                // if no W: set it on lepton

#if DEBUG
	std::cout << "producer 10" << std::endl;
#endif
      
      if(!noTop){
                             // top was found!
	p_ = &(*top);      
      }
      else{
	if(noTop && !noW)                      // not top, but we have a W
	  p_ = &(*W);
	else if(noTop && noW) p_ = &(*lep);    // we have neither top nor W in the list ... 
      }
      
#if DEBUG
      std::cout << "producer 10.5" << std::endl;
#endif


      // ---------------------------------- OLD MCatNLO STUFF ------------------------------------------

      if(p_->numberOfMothers() < 2 )continue;

      // check if we have gluon splitting in the light quark line:
      if( ( p_->mother(0)->pdgId() == 21 && abs( p_->mother(1)->pdgId() ) == 5 ) 
	  || ( p_->mother(1)->pdgId() == 21 && abs( p_->mother(0)->pdgId() ) == 5 )){

	isGluonSplitLQLine = true;
      }
      // check if we have a Vtb vertex (for events w/o gluon splitting!):
      if(abs(p_->mother(0)->pdgId()) < 5 && abs(p_->mother(1)->pdgId()) < 5){
	noVtb = true;
      }
      // --------------------------------- END OLD MCatNLO STUFF ----------------------------------------
      
      
      // choose light quark as topMother:               // "top mother" is now (more general) 
      if( abs( p_->mother(0)->pdgId() ) < 5 )           //  the mother of the starting paticle (top, W, or lep) 
	topMo = p_->mother(0);
      else
	topMo = p_->mother(1);
     
#if DEBUG
      std::cout << "producer 11" << std::endl;
#endif

      // if the incoming light quark comes directly from the proton:
      if(!noVtb && !isGluonSplitLQLine){
	// top mother:
	int nd = topMo->numberOfDaughters();
	for (int j = 0; j<nd; j++){
	  if(abs( topMo->daughter(j)->pdgId() ) < 5 
	     && topMo->daughter(j)->pdgId() != topMo->pdgId()){
	    const Candidate *lq = topMo->daughter(j);
	    // mcST->p4_q2_gen.SetCoordinates(lq->px(), lq->py(), lq->pz(), lq->energy());
	    lq_found = true;
	    if(debug) cout << "this is my new light quark: " << lq->pdgId() 
			   << "\t" << lq->status() << "\t" << lq->px() << endl;
	    recoilQuark = lq;

	  }
	}
      }
    }
    
   
#if DEBUG
	std::cout << "producer 12" << std::endl;
#endif

  } // END: particle loop  

 

if(top!= NULL)tops->push_back(*(dynamic_cast<const reco::GenParticle *>(top)));
if(btop!= NULL)bGenParticles->push_back(*(dynamic_cast<const reco::GenParticle *>(btop)));
if(lep!= NULL)topLeptons->push_back(*(dynamic_cast<const reco::GenParticle *>(lep)));
if(nu!= NULL)topNeutrinos->push_back(*(dynamic_cast<const reco::GenParticle *>(nu)));
if(recoilQuark!= NULL)singleTopRecoilQuark->push_back(*(dynamic_cast<const reco::GenParticle *>(recoilQuark)));

 if(top!= NULL&&btop!= NULL&&lep!= NULL&&nu!= NULL){
   //reco::GenParticle * tmp = (dynamic_cast<const reco::GenParticle *>(top));
   //tmp->setP4((nu->p4()+lep->p4())+btop->p4());
   pseudoRecoTop = new GenParticle();
   //*pseudoRecoTop = *top;
   //top;// *(dynamic_cast<const reco::GenParticle *>(top));
   //pseudoRecoTop->setP4((nu->p4()+lep->p4())+btop.p4());
   pseudoRecoTops->push_back(*(dynamic_cast<const reco::GenParticle *>(pseudoRecoTop)));
}

  //Const reco::GenParticle * btopPart =  dynamic_cast<const reco::GenParticle *>(btop);
  //bGenParticles->push_back( * btopPart);
  
  // second particle loop for second b quark, since charge is not determined before lep was found, 
  // but 2ndb is often listed above the lepton (23 process)!  
  for(std::vector<reco::GenParticle> ::const_iterator p=genParticles->begin(); p != genParticles->end(); ++p){
    // second b quark:
#if DEBUG
	std::cout << "producer 13" << std::endl;
#endif
    if(!secb_found && p->pdgId() == secb_id){
      const Candidate * mom = p->mother(0);
      if(abs(mom->pdgId()) < 6 || mom->pdgId() == 21){
	secb_found = true;
	//mcST->p4_2ndb_gen.SetCoordinates(p->px(), p->py(), p->pz(), p->energy());
	//if(p->status() == 2)
	  //mcST->procID = 22;
	//else{
	// if(p->status() == 3)
	    //mcST->procID = 23;

	//}

#if DEBUG
	std::cout << "producer 14" << std::endl;
#endif
	secondBGenParticles->push_back(*p);
	if(debug) cout << "secb found in line " << idx << endl;
      }
    }
    idx++;
    if(secb_found)
      break;
  } // END: particle loop
  //if(bSecond != NULL)secondBGenParticles->push_back(*(dynamic_cast<const reco::GenParticle *>(bSecond)));
   }catch(...){;}
 }

 
 iEvent.put(bGenParticles,"bGenParticles");
 iEvent.put(secondBGenParticles,"secondBGenParticles");

 iEvent.put(singleTopRecoilQuark,"singleTopRecoilQuark");

 iEvent.put(bGenJets,"bGenJets");
 iEvent.put(topLeptons,"topLeptons");
 iEvent.put(topNeutrinos,"topNeutrinos");
 iEvent.put(tops,"tops");
 iEvent.put(pseudoRecoTops,"pseudoRecoTops");

}



SingleTopTChannelMCProducer::~SingleTopTChannelMCProducer(){;}

DEFINE_FWK_MODULE( SingleTopTChannelMCProducer );
