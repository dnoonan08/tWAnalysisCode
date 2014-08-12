#ifndef __SINGLETOP_SYNC_DUMPER_H__
#define __SINGLETOP_SYNC_DUMPER_H__

/* \Class SingleTopSystematicsDumper
 *
 * \Authors A. Orso M. Iorio
 * 
 * Produces systematics histograms out of a standard Single Top n-tuple 
 * \ version $Id: SingleTopSyncDumper.h,v 1.1.2.1 2011/09/20 13:36:20 oiorio Exp $
 */


//----------------- system include files
#include <memory>
#include <iostream>
#include <list>
#include <string>
#include <sstream>
#include <map>
#include <vector>
#include <algorithm>

//----------------- cmssw includes

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include <FWCore/Framework/interface/Run.h>

#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Framework/interface/TriggerNamesService.h"

#include "DataFormats/TrackReco/interface/Track.h"
#include "DataFormats/VertexReco/interface/Vertex.h"
#include "JetMETCorrections/JetVertexAssociation/interface/JetVertexMain.h"
#include "DataFormats/HepMCCandidate/interface/PdfInfo.h"

#include "FWCore/Framework/interface/ESHandle.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/JetResolution.h"


//--------------------TQAF includes
/*
#include "AnalysisDataFormats/TopObjects/interface/TopObject.h"
#include "AnalysisDataFormats/TopObjects/interface/TopLepton.h"
#include "AnalysisDataFormats/TopObjects/interface/TopJet.h"
#include "AnalysisDataFormats/TopObjects/interface/TopMET.h"
#include "AnalysisDataFormats/TopObjects/interface/TopElectron.h"
#include "AnalysisDataFormats/TopObjects/interface/TopMuon.h"
*/

//--------------------PAT includes
#include "DataFormats/PatCandidates/interface/Particle.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"


//--------------------ROOT includes
#include "TFile.h"
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH2.h"

//lorentzVector
#include "DataFormats/Math/interface/LorentzVector.h"

//B Tag reading from DB
#include "RecoBTag/Records/interface/BTagPerformanceRecord.h"
#include "CondFormats/PhysicsToolsObjects/interface/BinningPointByMap.h"
#include "RecoBTag/PerformanceDB/interface/BtagPerformance.h"

#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"

using namespace std;
using namespace edm;
using namespace reco;



class SingleTopSyncDumper : public edm::EDAnalyzer {
 public:
  explicit SingleTopSyncDumper(const edm::ParameterSet&);
  //  ~SingleTopSyncDumper();
  
  
 private:
  virtual void analyze(const edm::Event&, const edm::EventSetup&);
  virtual void endJob();
  //void  EventInfo();

  //Find functions descriptions in .cc

  //Kinematic functions: 
  math::PtEtaPhiELorentzVector top4Momentum(float leptonPx, float leptonPy, float leptonPz,float leptonE, float jetPx, float jetPy, float jetPz,float jetE, float metPx, float metPy);
  math::PtEtaPhiELorentzVector top4Momentum(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy);
  math::XYZTLorentzVector NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy );
  float cosThetaLJ(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top);

  bool flavourFilter(string c,int nb, int nc, int nl);

  //B-weight generating functions
  double BScaleFactor(string algo,string syst_name); 
  double MisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr);
  double AntiBScaleFactor(string algo,string syst_name); 
  double AntiMisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr);

  double EventAntiScaleFactor(string algo,string syst_name );
  double EventScaleFactor(string algo,string syst_name );
  double SFMap(string);   double SFErrMap(string);   double EFFMap(string);   double EFFErrMap(string); 

  void InitializeEventScaleFactorMap();
  double EventScaleFactorMap(string, string);
  
  //Jet uncertainty as a function of eta pt and jet flavour
  double jetUncertainty(double eta, double ptCorr, int flavour);
  
  //Weight and probabilities for TurnOn curves
  double turnOnWeight (std::vector<double> probs, int njets_req);
  double jetprob(double pt,double tchp); 

  //Define vector of required systematics to loop on
  std::vector<std::string> systematics,rate_systematics, all_syst;

  //Define parameterSet to change from channel to channel
  edm::ParameterSet channelInfo;
  std::string channel;
  double crossSection,originalEvents,finalLumi,MTWCut,RelIsoCut,resolScale; 
  edm::Event*   iEvent;
  
  int nVertices;
  //  std::vector<float> leptonsPt,leptonsPhi,leptonsPz,leptonsEta,jetsPt,jetsPx,jetsPy,jetsPz,jetsEta,jetEnergy,jetsBTagAlgo,jetsAntiBTagAlgo,METPt,METPhi;
  
  //InputTags
  edm::InputTag leptonsPt_,
    leptonsPhi_,
    leptonsEta_,
    leptonsEnergy_,
    leptonsCharge_,
    leptonsRelIso_,
    leptonsQCDRelIso_,
    leptonsID_,
    leptonsDB_,
    looseElectronsRelIso_,
    looseMuonsRelIso_,
    leptonsConvDcot_,
    leptonsLostHits_,
    leptonsConvDist_, 
    jetsPt_,
    jetsPhi_,
    jetsEta_,
    jetsEnergy_,
    jetsBTagAlgo_,
    jetsCorrTotal_,
    jetsAntiBTagAlgo_,
    genJetsPt_,
    genJetsEta_,
    METPt_,
    METPhi_,
    jetsFlavour_,
    UnclMETPx_,
    UnclMETPy_,
    npv_,
    preWeights_;


  // Handles
  edm::Handle<std::vector<float> > leptonsPt,
   leptonsPhi,
   leptonsEta,
   leptonsEnergy,
   leptonsCharge,
   leptonsRelIso,
   leptonsQCDRelIso,
   looseElectronsRelIso,
   looseMuonsRelIso,
   leptonsConvDist,
   leptonsConvDcot,
   leptonsLostHits,
   leptonsID,
   leptonsDB,
   jetsEta,
   jetsPt,
   jetsPhi,
   jetsEnergy,
   jetsBTagAlgo,
   jetsAntiBTagAlgo,
   jetsFlavour,
   jetsCorrTotal,
   METPhi,
   METPt;
 
  edm::Handle<int > npv;
  
  //Unclustered MET to take from the event
  edm::Handle< double > UnclMETPx,UnclMETPy,preWeights;
  edm::Handle< std::vector<double> > genJetsPt;
  std::string leptonsFlavour_,mode_;  

  //Part for BTagging payloads
  edm::ESHandle<BtagPerformance> perfMHP;
  edm::ESHandle<BtagPerformance> perfMHE;
  edm::ESHandle<BtagPerformance> perfBHP;
  edm::ESHandle<BtagPerformance> perfBHE;

  //Part for JEC and JES
  string JEC_PATH;
  JetResolution *ptResol;
  edm::FileInPath fip;
  JetCorrectionUncertainty *jecUnc;
  double JES_SW, JES_b_cut, JES_b_overCut;

  //4-momenta vectors definition  
  std::vector<math::PtEtaPhiELorentzVector> leptons,
    leptonsQCD,
    jets,
    loosejets,
    bjets,
    antibjets;
  
  std::vector<double> btags;

  //Definition of trees
  map<string, TTree*> trees;
  map<string, TTree*> treesWSample;
  map<string, TTree*> treesQCD;
  map<string, TTree*> treesWSampleQCD;
  
  //Other variables definitions
  double bTagThreshold,maxPtCut;
  size_t bScanSteps;
  bool doBScan_,doQCD_,isControlSample_;
  //To be changed in 1 tree, now we keep 
  //because we have no time to change and debug
  map<string, TTree*> treesScan;
  map<string, TTree*> treesScanQCD;
  //Vectors of b-weights
  vector< double > b_weight_tag_algo1,
    b_weight_tag_algo2,
    b_weight_antitag_algo1,
    b_weight_antitag_algo2,
    b_discriminator_value_tag_algo1,
    b_discriminator_value_antitag_algo2;

  //Variables to use as trees references
  double etaTree,etaTree2,cosTree,topMassTree,weightTree,mtwMassTree,lowBTagTree,highBTagTree,maxPtTree,minPtTree,topMassLowBTagTree,topMassBestTopTree,topMassMeas,bWeightTree,PUWeightTree,turnOnWeightTree,limuWeightTree;
  int runTree, eventTree,lumiTree,chargeTree,electronID,bJetFlavourTree;
  double lepPt,lepEta,lepPhi,lepRelIso,fJetPhi,fJetPt,fJetEta,fJetE,bJetPt,bJetEta,bJetPhi,bJetE,metPt,metPhi,topPt,topPhi,topEta,topE,totalEnergy,totalMomentum;

  
  //Not used anymore:
  double loosePtCut ;
  bool doPU_,doTurnOn_, doResol_ ; 
 
  edm::LumiReWeighting LumiWeights_;
  std::string mcPUFile_,dataPUFile_,puHistoName_;

  std::vector<double> jetprobs;

  double leptonRelIsoQCDCutUpper,leptonRelIsoQCDCutLower;  
 
  bool gotLeptons,gotJets,gotMets,gotLooseLeptons,gotPU;

  int nb,nc,nudsg,ntchp_tags,ntchp_antitags,ntche_tags,ntche_antitags;

  double TCHPM_LMisTagUp,  TCHPM_BBTagUp, TCHPM_CBTagUp, TCHPM_LMisTagDown, TCHPM_BBTagDown, TCHPM_CBTagDown;
  double TCHPM_LAntiMisTagUp,  TCHPM_BAntiBTagUp, TCHPM_CAntiBTagUp, TCHPM_LAntiMisTagDown, TCHPM_BAntiBTagDown, TCHPM_CAntiBTagDown;
  double TCHPM_C,  TCHPM_B, TCHPM_L;
  double TCHPM_CAnti,  TCHPM_BAnti, TCHPM_LAnti;

  double TCHPT_LMisTagUp,  TCHPT_BBTagUp, TCHPT_CBTagUp, TCHPT_LMisTagDown, TCHPT_BBTagDown, TCHPT_CBTagDown;
  double TCHPT_LAntiMisTagUp,  TCHPT_BAntiBTagUp, TCHPT_CAntiBTagUp, TCHPT_LAntiMisTagDown, TCHPT_BAntiBTagDown, TCHPT_CAntiBTagDown;
  double TCHPT_C,  TCHPT_B, TCHPT_L;
  double TCHPT_CAnti,  TCHPT_BAnti, TCHPT_LAnti;


  double TCHEL_LMisTagUp,  TCHEL_BBTagUp, TCHEL_CBTagUp, TCHEL_LMisTagDown, TCHEL_BBTagDown, TCHEL_CBTagDown;
  double TCHEL_LAntiMisTagUp,  TCHEL_BAntiBTagUp, TCHEL_CAntiBTagUp, TCHEL_LAntiMisTagDown, TCHEL_BAntiBTagDown, TCHEL_CAntiBTagDown;
  double TCHEL_C,  TCHEL_B, TCHEL_L;
  double TCHEL_CAnti,  TCHEL_BAnti, TCHEL_LAnti;

  long int nprecut, nlepton, nlepton2, njets, nbtag, nmtw;

  class BTagWeight 
  {
  public:
    struct JetInfo {
      JetInfo(float mceff,float datasf) : eff(mceff), sf(datasf) {}
      float eff;
      float sf;
    };
    BTagWeight():
      minTags(0),maxTags(0){;}
    BTagWeight(int jmin, int jmax) : 
      maxTags(jmax), minTags(jmin) {}
    
    bool filter(int t);
    float weight(vector<JetInfo> jets, int tags);
  private:
    int maxTags;
    int minTags;
    
    
  };

  vector<BTagWeight::JetInfo> jsfshpt,jsfshel;// bjs,cjs,ljs;
  
  BTagWeight b_tchpt_signal_region, b_tchel_sample_A, b_tchel_sample_B, b_tchpt_sample_B;
  double b_weight_signal_region, b_weight_sample_A, b_weight_sample_B; 


  bool isFirstEvent;
};

#endif
