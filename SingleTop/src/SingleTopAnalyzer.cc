/*
*\Authors: M.Merola, O.Iorio
*
*
*
*\version  $Id: SingleTopAnalyzer.cc,v 1.5 2010/04/23 07:06:27 oiorio Exp $ 
*/

// =================================
//   CMS - single top HistoMaker
// =================================
//
//
//
//


#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging


#include "TopQuarkAnalysis/SingleTop/interface/SingleTopAnalyzer.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Common/interface/TriggerNames.h"
//#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
//#include "FWCore/Framework/interface/TriggerNames.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"

SingleTopAnalyzer::SingleTopAnalyzer(const edm::ParameterSet& iConfig)
{
#if DEBUG
  cout << "constructor 1" << endl;
#endif
  
  isMCSingleTop = iConfig.getUntrackedParameter<bool>("isMCSTop",true);
    
  electronProducer = iConfig.getParameter<InputTag>("electronProducer");
  muonProducer = iConfig.getParameter<InputTag>("muonProducer");
  jetProducer = iConfig.getParameter<InputTag>("jetProducer");
  metProducer = iConfig.getParameter<InputTag>("metProducer");

  bJetProducer = iConfig.getParameter<InputTag>("bJetProducer");
  nonBJetProducer = iConfig.getParameter<InputTag>("nonBJetProducer");
  forwardJetProducer = iConfig.getParameter<InputTag>("forwardJetProducer");

  
  topProducer = iConfig.getParameter<InputTag>("topProducer");

  MCLeptonProducer   = iConfig.getParameter<InputTag>("MCLeptonProducer");
  MCJetProducer      = iConfig.getParameter<InputTag>("MCJetProducer");
  MCNeutrinoProducer = iConfig.getParameter<InputTag>("MCNeutrinoProducer");
  MCBQuarkProducer   = iConfig.getParameter<InputTag>("MCBQuarkProducer");
  MCLightQuarkProducer   = iConfig.getParameter<InputTag>("MCLightQuarkProducer");
  


#if DEBUG
  cout << "constructor 2" << endl;
#endif
  
  Service<TFileService> fs;

#if DEBUG
  cout << "constructor 3" << endl;
#endif
  
  TFileDirectory SingleTop_tChannel = fs->mkdir( "SingleTopMC" );
  TFileDirectory SingleTopData = fs->mkdir( "SingleTopData" );
  
  
  h_nJets = SingleTopData.make<TH1F>("JetsNumber",      "number of jets", 21, -0.5, 20.5);
  h_nLeptTop= SingleTopData.make<TH1F>("LeptTopNumber","number of leptons from top",21,-0.5,20.5);
  
  h_nLept = SingleTopData.make<TH1F>("LeptNumber",      "number of leptons", 21, -0.5, 20.5);
  
   h_thetaDiff  = SingleTopData.make<TH1F>("ThetaDifference", "Leptons-Jets theta difference", 70,-3.5, 3.5);
  
  h_wTransverseMass  = SingleTopData.make<TH1F>("WTransverseMass", "transverse mass of the W boson from top decay", 120,0, 120);

  
  h_MCwTransverseMass = SingleTop_tChannel.make<TH1F>("genWTransverseMass", "transverse mass of the true W boson from top decay", 120,0, 120);

  h_eleRelIso = SingleTopData.make<TH1F>("eleRelIso","relative Isolation of the Electron", 50,0, 1);
  h_muRelIso = SingleTopData.make<TH1F>("muRelIso","relative Isolation of the Muon", 50,0, 1);


  h_jetsEta = SingleTopData.make<TH1F>("antiBTaggedJetEta","eta of the anti-bTagged jets",100,-5,5);
  h_bJetsEta = SingleTopData.make<TH1F>("bTaggedJetEta","eta of the bTagged jets",100,-5,5);

  h_jetsPt = SingleTopData.make<TH1F>("jetsPt","pt of the jets",200,0,200);

  h_nBTag = SingleTopData.make<TH1F>("nBTag","number of B Tags",11,-0.5,10.5);

  h_nLepVsNBtag = SingleTopData.make<TH2F>("nLepVsNBTag","number of Leptons vs Number of  B Tags",11,-0.5,10.5,11,-0.5,10.5);

  h_bTagValueInsideEta = SingleTopData.make<TH1F>("bTagValue","Value of BTag algorythm inside its eta range",120,-20,40);
  
  h_nFwdJets = SingleTopData.make<TH1F>("nForwardJets","number of forward jets",21,-0.5,21.5);

  h_MCLeptonPt = SingleTop_tChannel.make<TH1F>("MCLepPt","MC Leptons pt",200,0,200);

  h_MCBQuarkEta = SingleTop_tChannel.make<TH1F>("MCBEta","eta of the mc b quark",100,-5,5);
  h_MCBQuarkPt = SingleTop_tChannel.make<TH1F>("MCBPt","pt of the mc b quark",200,0,200);
  h_MCLightQuarkPt = SingleTop_tChannel.make<TH1F>("MCLightQuarkPt","pt of the mc light quark",200,0,200);
  h_MCLightQuarkEta = SingleTop_tChannel.make<TH1F>("MCLightQuarkEta","eta of the mc light quark",100,-5,5);

  h_lepPt=SingleTopData.make<TH1F>("LepPt"," Leptons pt",200,0,200);

#if Debug 
  cout << "constructor 4 done \n";


#endif
  
}


//SingleTopAnalyzer::~SingleTopAnalyzer()
//{
//}

void SingleTopAnalyzer::analyze(const Event& iEvent, const EventSetup& iSetup)
{

#if DEBUG
  cout << "analyzer 1" << endl;
#endif
    
  // Electrons ----------------------------------------------------------------
  Handle<vector<pat::Electron> > elHa;
  iEvent.getByLabel(electronProducer, elHa);
  
  // Muons --------------------------------------------------------------------
  Handle<vector<pat::Muon> > muHa;
  iEvent.getByLabel(muonProducer, muHa);
  
  // MC Leptons ---------------------------------------
    Handle<vector<reco::GenParticle> > MCLepHa;
   iEvent.getByLabel(MCLeptonProducer, MCLepHa);
  

  
  // MET ----------------- 
  Handle<vector<pat::MET> > metHa;
  iEvent.getByLabel(metProducer, metHa);
  
  // MC Neutrinos ---------------------------------------
  Handle<vector<reco::GenParticle> > MCNuHa;
  iEvent.getByLabel(MCNeutrinoProducer, MCNuHa);


  
  // Jets ------------------
  Handle<vector<pat::Jet> > jetHa;
  iEvent.getByLabel(jetProducer, jetHa);

  //BJets
  Handle<vector<pat::Jet> > bJetHa;
  iEvent.getByLabel(bJetProducer, bJetHa);

  //nonBJets
  Handle<vector<pat::Jet> > nonBJetHa;
  iEvent.getByLabel(nonBJetProducer, nonBJetHa);

  //Forward Jets
  Handle<vector<pat::Jet> > fwdJetHa;
  iEvent.getByLabel(forwardJetProducer, fwdJetHa);

  vector<pat::Jet> const & bJet = *bJetHa;
  vector<pat::Jet>::const_iterator iter_bJet;

  vector<pat::Jet> const & nonBJet = *nonBJetHa;
  vector<pat::Jet>::const_iterator iter_nonBJet;

  vector<pat::Jet> const & fwdJet = *fwdJetHa;
  vector<pat::Jet>::const_iterator iter_fwdJet;



  // MC Jets ------------------
  Handle<vector<reco::GenParticle> > MCJetHa;
  iEvent.getByLabel(MCJetProducer, MCJetHa);
  
  
  // Tops ------------------
  Handle<vector<reco::NamedCompositeCandidate> > topHa;
  iEvent.getByLabel(topProducer, topHa);


  //MC b quarks
  Handle<vector<reco::GenParticle> > MCBHa;
  iEvent.getByLabel(MCBQuarkProducer, MCBHa);

  //MC light quarks   
  Handle<vector<reco::GenParticle> > MCLQHa;
  iEvent.getByLabel(MCLightQuarkProducer,MCLQHa);
  

#if DEBUG
  cout << "analyzer 2" << endl;
#endif

  //  Handle<double> GenEventWeight;
  // iEvent.getByLabel("genEventWeight",GenEventWeight);
  
  
  double weight = 1;//*GenEventWeight;
  
  
  vector<pat::Jet> const & Jet = *jetHa;
  vector<pat::Jet>::const_iterator iter_jet;
    
  vector<pat::Electron> const & El = *elHa;
  vector<pat::Electron>::const_iterator iter_el;
    
  vector<pat::Muon> const & Mu = *muHa;
  vector<pat::Muon>::const_iterator iter_mu;
    
  vector<reco::NamedCompositeCandidate> const & Top = *topHa;
  vector<reco::NamedCompositeCandidate>::const_iterator iter_top;
  


  vector<reco::GenParticle> const & MCLep = *MCLepHa;
  vector<reco::GenParticle>::const_iterator iter_MCLep;
  
  vector<reco::GenParticle> const & MCNu = *MCNuHa;
  vector<reco::GenParticle>::const_iterator iter_MCNu;

  vector<reco::GenParticle> const & MCB = *MCBHa;
  vector<reco::GenParticle>::const_iterator iter_MCB;

  vector<reco::GenParticle> const & MCLQ = *MCLQHa;
  vector<reco::GenParticle>::const_iterator iter_MCLQ;


#if DEBUG
  cout << "analyzer 3" << endl;
#endif

  for (iter_top=Top.begin(); iter_top!=Top.end(); iter_top++){
    
    const Candidate * Lepton = iter_top->daughter("Lepton"); 
    const Candidate * MET    = iter_top->daughter("MET");          
    //    const Candidate * BJet   = iter_top->daughter("BJet");
    
    double Wmt = sqrt(pow(Lepton->et()+MET->pt(),2) - pow(Lepton->px()+MET->px(),2) - pow(Lepton->py()+MET->py(),2) );
    h_wTransverseMass->Fill(Wmt,weight);
  }
  
  for (iter_MCLep=MCLep.begin(); iter_MCLep!=MCLep.end(); iter_MCLep++){
    
    const GenParticle  MCLepton   = *(iter_MCLep);
   


     

#if DEBUG
     cout << "analyzer leptonpt" << MCLepton.pt() <<" n bins x "<< h_MCLeptonPt->GetNbinsX() << " content bin 3 should be 10: " << h_MCLeptonPt->GetBinContent(3) <<endl;
#endif

    
    for(iter_MCNu=MCNu.begin(); iter_MCNu!=MCNu.end(); iter_MCNu++){
      
      
      const GenParticle  MCNeutrino = *(iter_MCNu);
      double MCWmt = sqrt(pow(MCLepton.et()+MCNeutrino.pt(),2) - pow(MCLepton.px()+MCNeutrino.px(),2) - pow(MCLepton.py()+MCNeutrino.py(),2) );
      h_MCwTransverseMass->Fill(MCWmt,weight);
      
    }
    
  }
  
  
  
#if DEBUG
  cout << "analyzer 4" << endl;
#endif
  
  //  h_nLeptTop -> Fill(Lepton->size());  
  
  
  for (iter_el=El.begin(); iter_el!=El.end(); iter_el++){
    double relIso = iter_el->pt()/(iter_el->pt() + iter_el->trackIso()+ iter_el->caloIso());
    h_eleRelIso->Fill(relIso,weight);
    h_lepPt->Fill(iter_el->pt(),weight);
  }
  
  
  for (iter_mu=Mu.begin(); iter_mu!=Mu.end(); iter_mu++){
    double relIso = iter_mu->pt()/(iter_mu->pt() + iter_mu->trackIso()+ iter_mu->caloIso());
    h_muRelIso->Fill(relIso,weight);
    h_lepPt->Fill(iter_mu->pt(),weight);
  }
  

  for (iter_MCB=MCB.begin(); iter_MCB!=MCB.end(); iter_MCB++){
    h_MCBQuarkPt->Fill(iter_MCB->pt());
    h_MCBQuarkEta->Fill(iter_MCB->eta());
    
  }
  
  for (iter_MCLQ=MCLQ.begin(); iter_MCLQ!=MCLQ.end(); iter_MCLQ++){
    h_MCLightQuarkPt->Fill(iter_MCLQ->pt());
    h_MCLightQuarkEta->Fill(iter_MCLQ->eta());
    
  }
  
#if DEBUG
  cout << "analyzer 4 mc" << endl;
#endif
  
  
  std::string balgo="trackCountingHighPurBJetTags";
  for (iter_jet=Jet.begin(); iter_jet!=Jet.end(); iter_jet++){
    h_bTagValueInsideEta->Fill(iter_jet->bDiscriminator(balgo),weight);
    h_jetsPt->Fill(iter_jet->pt(),weight);      
  }
  
  h_nBTag->Fill(bJet.size(),weight);
  h_nFwdJets->Fill(fwdJet.size(),weight);
  
  for (iter_bJet=bJet.begin(); iter_bJet!=bJet.end(); iter_bJet++){
    h_bJetsEta->Fill(iter_bJet->eta());   
  }
  for (iter_nonBJet=nonBJet.begin(); iter_nonBJet!=nonBJet.end(); iter_nonBJet++){
    h_jetsEta->Fill(iter_nonBJet->eta(),weight);   
  }
  
  for (iter_fwdJet=fwdJet.begin(); iter_fwdJet!=fwdJet.end(); iter_fwdJet++){
  }
  
  h_nLepVsNBtag->Fill(elHa->size() + muHa->size(),bJet.size(),weight);


  /// Jets and leptons number distributions
  
  h_nJets-> Fill(jetHa->size());

#if DEBUG
  cout << "analyzer 5" << endl;
#endif
  
  h_nLept-> Fill(elHa->size() + muHa->size()); 


#if DEBUG
  cout << "analyzer 6" << endl;
#endif
  
  //cout<<" n tops " << topHa->size() << " n jets: " <<jetHa->size()<<endl;
  
  
  
}




//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopAnalyzer);

