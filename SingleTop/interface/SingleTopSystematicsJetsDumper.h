#ifndef __SINGLETOP_SYST_JETS_DUMPER_H__
#define __SINGLETOP_SYST_JETS_DUMPER_H__

/* \Class SingleTopSystematicsDumper
 *
 * \Authors A. Orso M. Iorio
 * 
 * Produces systematics histograms out of a standard Single Top n-tuple 
 * \ version $Id: SingleTopSystematicsJetsDumper.h,v 1.1.2.2.2.1 2012/06/05 10:57:11 oiorio Exp $
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
//#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"

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

//#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "PhysicsTools/Utilities/interface/Lumi3DReWeighting.h"
                                           

using namespace std;
using namespace edm;
using namespace reco;



class SingleTopSystematicsJetsDumper : public edm::EDAnalyzer {
 public:
  explicit SingleTopSystematicsJetsDumper(const edm::ParameterSet&);
  //  ~SingleTopSystematicsJetsDumper();
  
  
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

  //B-weight generating functions
  double BScaleFactor(string algo,string syst_name); 
  double MisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr);
  double AntiBScaleFactor(string algo,string syst_name); 
  double AntiMisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr);
  double resolSF(double eta,string syst);
  double pileUpSF(string syst);
  double bTagSF(int B);
  double bTagSF(int B, string syst);

  double EventAntiScaleFactor(string algo,string syst_name );
  double EventScaleFactor(string algo,string syst_name );
  double SFMap(string);   double SFErrMap(string);   double EFFMap(string);   double EFFErrMap(string); 

  void InitializeEventScaleFactorMap();
  void InitializeTurnOnReWeight(string SFFile);
  double EventScaleFactorMap(string, string);
  
  //Jet uncertainty as a function of eta pt and jet flavour
  double jetUncertainty(double eta, double ptCorr, int flavour);

  double BTagSFNew(double pt, string algo);
  double MisTagSFNew(double pt,double eta, string algo);

  double BTagSFErrNew(double pt, string algo);
  double MisTagSFErrNewUp(double pt, double eta, string algo);
  double MisTagSFErrNewDown(double pt, double eta, string algo);
  double EFFMapNew(double btag,string algo);

  
  //  int nsrc;// = 16;
  //  std::vector<JetCorrectionUncertainty*> vsrc(16);



  bool flavourFilter(string c,int nb, int nc, int nl);


  //Weight and probabilities for TurnOn curves
  double turnOnWeight (std::vector<double> probs, int njets_req);
  double turnOnReWeight (double preWeight, double pt, double tchpt);
  double jetprob(double pt,double tchp); 
  double jetprob(double pt,double tchp,double eta, string syst); 
  double jetprobpt(double pt); 
  double jetprobbtag(double tchp); 
 
  double turnOnProbs (string syst, int njets_req);
  void pushJetProbs (double pt, double btag, double eta);
  void resetWeightsDoubles();

  
  //Define vector of required systematics to loop on
  std::vector<std::string> systematics,rate_systematics;


  //Define parameterSet to change from channel to channel
  edm::ParameterSet channelInfo;
  std::string channel;
  double crossSection,originalEvents,finalLumi,MTWCut,RelIsoCut; 
  edm::Event*   iEvent;
  
  //  std::vector<float> leptonsPt,leptonsPhi,leptonsPz,leptonsEta,jetsPt,jetsPx,jetsPy,jetsPz,jetsEta,jetEnergy,jetsBTagAlgo,jetsAntiBTagAlgo,METPt,METPhi;
  
  //InputTags
  edm::InputTag leptonsPt_,
    leptonsPhi_,
    leptonsEta_,
    leptonsEnergy_,
    leptonsCharge_,
    leptonsRelIso_,
    leptonsID_,
    leptonsDB_,
    
    qcdLeptonsPt_,
    qcdLeptonsPhi_,
    qcdLeptonsEta_,
    qcdLeptonsEnergy_,
    qcdLeptonsCharge_,
    qcdLeptonsRelIso_,
   qcdLeptonsID_,
    qcdLeptonsDB_,

    looseElectronsRelIso_,
    looseMuonsRelIso_,

    genJetsPt_,
    genJetsEta_,
    jetsPt_,
    jetsPhi_,
    jetsEta_,
    jetsEnergy_,
    jetsBTagAlgo_,
    jetsCorrTotal_,
    jetsAntiBTagAlgo_,
    METPt_,
    METPhi_,
    jetsFlavour_,
    UnclMETPx_,
    UnclMETPy_,
    npv_,
    n0_,
    np1_,
    nm1_,
    preWeights_,
    x1_,
    x2_,
    id1_,
    id2_,
    scalePDF_ ;



  // Handles
  edm::Handle<std::vector<float> >  leptonsPt,
    leptonsPhi,
    leptonsEta,
    leptonsEnergy,
    leptonsCharge,
    leptonsRelIso,
   leptonsID,
   leptonsDB,
    
    qcdLeptonsPt,
    qcdLeptonsPhi,
    qcdLeptonsEta,
    qcdLeptonsEnergy,
    qcdLeptonsCharge,
    qcdLeptonsRelIso,
   qcdLeptonsID,
   qcdLeptonsDB,
   looseElectronsRelIso,
   looseMuonsRelIso,
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
 
  edm::Handle<int > npv,n0,nm1,np1;

  int passingPreselection, passingLepton, passingJets, passingBJets,passingMET;
  

  int nVertices;

  //Unclustered MET to take from the event
  edm::Handle< double > UnclMETPx,UnclMETPy,preWeights;
  edm::Handle< std::vector<double> > genJetsPt;
  edm::Handle< float > x1h,x2h,scalePDFh;
  edm::Handle< int > id1h,id2h;
  std::string leptonsFlavour_,mode_;  


  //Part for BTagging payloads
  edm::ESHandle<BtagPerformance> perfMHP;
  edm::ESHandle<BtagPerformance> perfMHPM;
  edm::ESHandle<BtagPerformance> perfMHE;
  edm::ESHandle<BtagPerformance> perfBHP;
  edm::ESHandle<BtagPerformance> perfBHPM;
  edm::ESHandle<BtagPerformance> perfBHE;


  //Part for JEC and JES
  //Part for JEC and JES
  string JEC_PATH;
  //  JetResolution *ptResol;
  edm::FileInPath fip;
  JetCorrectionUncertainty *jecUnc;
  double JES_SW, JES_b_cut, JES_b_overCut;



  //4-momenta vectors definition  
  /*  std::vector<math::PtEtaPhiELorentzVector> 
    jets,
    loosejets,
    bjets,
    antibjets;*/
  math::PtEtaPhiELorentzVector leptons[3],
    qcdLeptons[3],
    jets[10],
    jetsNoSyst[10],
    bjets[10],
    antibjets[10]; 
  
  float pdf_weights[44];
  //  float recorrection_weights[7][7];
  //  float pt_bin_extremes[8];
  //  float tchpt_bin_extremes[8];
  TH2D histoSFs; 

  math::PtEtaPhiELorentzVector leptonPFour;
  
  //Definition of trees
  
  map<string, TTree*> trees;
  

  
  //Other variables definitions
  double bTagThreshold,maxPtCut;
  size_t bScanSteps;
  bool doBScan_,doQCD_,doPDF_;
  //To be changed in 1 tree, now we keep 
  //because we have no time to change and debug
  //Vectors of b-weights
  vector< double > b_weight_tag_algo1,
    b_weight_tag_algo2,
    b_weight_antitag_algo1,
    b_weight_antitag_algo2,
    b_discriminator_value_tag_algo1,
    b_discriminator_value_antitag_algo2;

  //Variables to use as trees references

  //Variables to use as trees references
  double etaTree,etaTree2,cosTree,topMassTree,totalWeightTree,weightTree,mtwMassTree,lowBTagTree,highBTagTree,maxPtTree,minPtTree,topMassLowBTagTree,topMassBestTopTree,topMassMeas,bWeightTree,PUWeightTree,turnOnWeightTree,limuWeightTree,turnOnReWeightTree,miscWeightTree,W1T,W2T,WG1T,WG2T;
  //Weights for systematics
  double bWeightTreeBTagUp,
    bWeightTreeMisTagUp,
    bWeightTreeBTagDown,
    bWeightTreeMisTagDown,
    PUWeightTreePUUp,
    PUWeightTreePUDown,
    turnOnWeightTreeJetTrig1Up,
    turnOnWeightTreeJetTrig2Up,
    turnOnWeightTreeJetTrig3Up,
    turnOnWeightTreeJetTrig1Down,
    turnOnWeightTreeJetTrig2Down,
    turnOnWeightTreeJetTrig3Down,
    turnOnWeightTreeBTagTrig1Up,
    turnOnWeightTreeBTagTrig2Up,
    turnOnWeightTreeBTagTrig3Up,
    turnOnWeightTreeBTagTrig1Down,
    turnOnWeightTreeBTagTrig2Down,
    turnOnWeightTreeBTagTrig3Down;
  
  int runTree, eventTree,lumiTree,chargeTree,electronID,bJetFlavourTree, puZero, nJ, nT;
  double lepPt,lepEta,lepPhi,lepRelIso,fJetPhi,fJetPt,fJetEta,fJetE,bJetPt,bJetEta,bJetPhi,bJetE,metPt,metPhi,topPt,topPhi,topEta,topE,totalEnergy,totalMomentum,fJetBTag,bJetBTag;

  
  //Not used anymore:
  double loosePtCut,resolScale ;
  bool doPU_,doTurnOn_, doResol_ ; 
 
  edm::Lumi3DReWeighting LumiWeights_,LumiWeightsUp_,LumiWeightsDown_;
  std::string mcPUFile_,dataPUFile_,puHistoName_;

  std::vector<double> jetprobs,
    jetprobs_j1up,
    jetprobs_j2up,
    jetprobs_j3up,
    jetprobs_b1up,
    jetprobs_b2up,
    jetprobs_b3up,
    jetprobs_j1down,
    jetprobs_j2down,
    jetprobs_j3down,
    jetprobs_b1down,
    jetprobs_b2down,
    jetprobs_b3down ;

  double leptonRelIsoQCDCutUpper,leptonRelIsoQCDCutLower;  
  bool gotLeptons,gotJets,gotMets,gotLooseLeptons,gotPU,gotQCDLeptons;

  int nb,nc,nudsg,ntchpt_tags,
    nbNoSyst,ncNoSyst,nudsgNoSyst,
    ntchpt_antitags,ntchpm_tags,ntchel_tags,ntche_antitags;

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

  vector<BTagWeight::JetInfo> jsfshpt,jsfshel,
    jsfshpt_b_tag_up,jsfshel_b_tag_up,
    jsfshpt_mis_tag_up,jsfshel_mis_tag_up,
    jsfshpt_b_tag_down,jsfshel_b_tag_down,
    jsfshpt_mis_tag_down,jsfshel_mis_tag_down,
    jsfshptNoSyst,jsfshelNoSyst;// bjs,cjs,ljs;

 
  BTagWeight b_tchpt_0_tags,
    b_tchpt_1_tag,
    b_tchpt_g1_tag,
    b_tchpt_2_tags,
    b_tchpt_g2_tags,
    b_tchel_0_tags;
  double b_weight_tchpt_0_tags, 
    b_weight_tchpt_1_tag, 
    b_weight_tchpt_2_tags, 
    b_weight_tchel_0_tags; 
  
  float x1,x2,Q2,scalePDF;
  int id1,id2;

  bool isFirstEvent,doReCorrection_;

  vector<JetCorrectorParameters > *vParData;
  FactorizedJetCorrector *JetCorrectorData;
  vector<JetCorrectorParameters > vParMC;
  FactorizedJetCorrector *JetCorrectorMC;
  
};

#endif
