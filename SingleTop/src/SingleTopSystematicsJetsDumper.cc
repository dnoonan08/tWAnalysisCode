/*
*\Author:  O.Iorio
*
*
*
*\version  $Id: SingleTopSystematicsJetsDumper.cc,v 1.1.2.2.4.1 2012/09/27 10:13:34 dnoonan Exp $ 
*/
// This analyzer dumps the histograms for all systematics listed in the cfg file 
//
//
//

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopSystematicsJetsDumper.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "FWCore/Common/interface/TriggerNames.h"
//#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"
//#include "FWCore/Framework/interface/TriggerNames.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"
#include "DataFormats/Math/interface/LorentzVector.h"
#include <Math/VectorUtil.h>
//#include "CommonTools/CandUtils/interface/Booster.h"
#include <sstream> //libreria per usare stringstream
//#include "PhysicsTools/Utilities/interface/LumiReWeighting.h"
#include "DataFormats/Math/interface/deltaR.h"

#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"


namespace LHAPDF {
         void initPDFSet(int nset, const std::string& filename, int member=0);
         int numberPDF(int nset);
         void usePDFMember(int nset, int member);
         double xfx(int nset, double x, double Q, int fl);
         double getXmin(int nset, int member);
         double getXmax(int nset, int member);
         double getQ2min(int nset, int member);
         double getQ2max(int nset, int member);
         void extrapolate(bool extrapolate=true);
   }

SingleTopSystematicsJetsDumper::SingleTopSystematicsJetsDumper(const edm::ParameterSet& iConfig)
{
  //MCLightQuarkProducer   = iConfig.getParameter<InputTag>("MCLightQuarkProducer");
  systematics = iConfig.getUntrackedParameter<std::vector<std::string> >("systematics"); 
  rate_systematics = iConfig.getUntrackedParameter<std::vector<std::string> >("rateSystematics"); 
  //Channel information
  
  channelInfo = iConfig.getParameter<edm::ParameterSet>("channelInfo"); 
  //Cross section, name and number of events 
  channel = channelInfo.getUntrackedParameter<string>("channel");
  crossSection = channelInfo.getUntrackedParameter<double>("crossSection");
  originalEvents = channelInfo.getUntrackedParameter<double>("originalEvents");
  finalLumi = channelInfo.getUntrackedParameter<double>("finalLumi");
  MTWCut = channelInfo.getUntrackedParameter<double>("MTWCut",50);


  RelIsoCut = channelInfo.getUntrackedParameter<double>("RelIsoCut",0.1);
  loosePtCut = channelInfo.getUntrackedParameter<double>("loosePtCut",30); 

  maxPtCut = iConfig.getUntrackedParameter<double>("maxPtCut",30);

  //tight leptons 
  leptonsFlavour_ =  iConfig.getUntrackedParameter< std::string >("leptonsFlavour");

  

  //  dataPUFile_ =  iConfig.getUntrackedParameter< std::string >("dataPUFile","pileUpDistr.root");
  //  mcPUFile_ =  iConfig.getUntrackedParameter< std::string >("mcPUFile","pileupdistr_TChannel.root");
  
  leptonsPt_ =  iConfig.getParameter< edm::InputTag >("leptonsPt");
  leptonsPhi_ =  iConfig.getParameter< edm::InputTag >("leptonsPhi");
  leptonsEta_ =  iConfig.getParameter< edm::InputTag >("leptonsEta");
  leptonsEnergy_ =  iConfig.getParameter< edm::InputTag >("leptonsEnergy");
  leptonsCharge_ =  iConfig.getParameter< edm::InputTag >("leptonsCharge");
  leptonsRelIso_ =  iConfig.getParameter< edm::InputTag >("leptonsRelIso");
  leptonsDB_ =  iConfig.getParameter< edm::InputTag >("leptonsDB");
  leptonsID_ =  iConfig.getParameter< edm::InputTag >("leptonsID");

  //qcd leptons

  qcdLeptonsPt_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsPt");
  qcdLeptonsPhi_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsPhi");
  qcdLeptonsEta_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsEta");
  qcdLeptonsEnergy_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsEnergy");
  qcdLeptonsCharge_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsCharge");
  qcdLeptonsRelIso_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsRelIso");
  qcdLeptonsDB_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsDB");
  qcdLeptonsID_ =  iConfig.getParameter< edm::InputTag >("qcdLeptonsID");



  leptonsFlavour_ =  iConfig.getUntrackedParameter< std::string >("leptonsFlavour");
  
  looseMuonsRelIso_ =  iConfig.getParameter< edm::InputTag >("looseMuonsRelIso");
  looseElectronsRelIso_ =  iConfig.getParameter< edm::InputTag >("looseElectronsRelIso");

  //Jets
  
  jetsEta_ =  iConfig.getParameter< edm::InputTag >("jetsEta");
  jetsPt_ =  iConfig.getParameter< edm::InputTag >("jetsPt");
  jetsPhi_ =  iConfig.getParameter< edm::InputTag >("jetsPhi");
  jetsEnergy_ =  iConfig.getParameter< edm::InputTag >("jetsEnergy");
  
  jetsBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsBTagAlgo");
  jetsAntiBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsAntiBTagAlgo");
  jetsFlavour_ =  iConfig.getParameter< edm::InputTag >("jetsFlavour");

  //  genJetsPt_  = iConfig.getParameter< edm::InputTag >("genJetsPt");
  //genJetsEta_  = iConfig.getParameter< edm::InputTag >("genJetsEta");//FIXMEEE

  genJetsPt_  = iConfig.getParameter< edm::InputTag >("genJetsPt");
  genJetsEta_  = iConfig.getParameter< edm::InputTag >("genJetsEta");//FIXMEEE


  METPhi_ =  iConfig.getParameter< edm::InputTag >("METPhi");
  METPt_ =  iConfig.getParameter< edm::InputTag >("METPt");
  
  //  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  //  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  
  
  jetsCorrTotal_ =  iConfig.getParameter< edm::InputTag >("jetsCorrTotal");

  doBScan_  =  iConfig.getUntrackedParameter< bool >("doBScan",false); 
  doQCD_  =  iConfig.getUntrackedParameter< bool >("doQCD",false); 

  doPDF_  =  iConfig.getUntrackedParameter< bool >("doPDF",false); 
  
  //Q2 part
  x1_ = iConfig.getParameter<edm::InputTag>("x1") ;
  x2_ = iConfig.getParameter<edm::InputTag>("x2") ;

  id1_ = iConfig.getParameter<edm::InputTag>("id1") ;
  id2_ = iConfig.getParameter<edm::InputTag>("id2") ;
  
  scalePDF_ = iConfig.getParameter<edm::InputTag>("scalePDF") ;
  
  //Pile Up Part
  np1_ = iConfig.getParameter< edm::InputTag >("nVerticesPlus");//,"PileUpSync"); 
  nm1_ = iConfig.getParameter< edm::InputTag >("nVerticesMinus");//,"PileUpSync"); 
  n0_ = iConfig.getParameter< edm::InputTag >("nVertices");//,"PileUpSync"); 
  
  doPU_ = iConfig.getUntrackedParameter< bool >("doPU",false);
  doResol_ = iConfig.getUntrackedParameter< bool >("doResol",true);
  doTurnOn_ = iConfig.getUntrackedParameter< bool >("doTurnOn",true);

  doReCorrection_ = iConfig.getUntrackedParameter< bool >("doReCorrection",false);
  dataPUFile_ =  channelInfo.getUntrackedParameter< std::string >("Season","Summer11");

  string season = "Summer11";
  season = dataPUFile_;
  //  TString season = "Fall11";
  string distr="pileUpDistr"+season+".root";
  if(doPU_){
    //    //cout << " before lumIweightse "<<endl;

    LumiWeights_ = edm::Lumi3DReWeighting(distr,
					  "pileUpDistr.root",
					  std::string("pileup"),
					  std::string("pileup"),
					  "");
    LumiWeightsUp_ = edm::Lumi3DReWeighting(distr,
					  "pileUpDistr.root",
					  std::string("pileup"),
					  std::string("pileup"),
					  "");
    LumiWeightsDown_ = edm::Lumi3DReWeighting(distr,
					  "pileUpDistr.root",
					  std::string("pileup"),
					  std::string("pileup"),
					  "");
    LumiWeightsUp_.weight3D_init(1.080);
    LumiWeightsDown_.weight3D_init(0.961);
    LumiWeights_.weight3D_init(1.044);

    //    //cout << " built lumiWeights "<<endl;
  }
  
  //  preWeights_ =  iConfig.getParameter< edm::InputTag >("preWeights");
  
  
  Service<TFileService> fs;
  

  bTagThreshold =3.41;


  systematics.insert(systematics.begin(),"noSyst");

  //  for(size_t i = 0; i < systematics.size();++i){
  //  if(systematics.at(i)=="") 
  //}

  std::vector<std::string> all_syst = systematics;



  
  TFileDirectory SingleTopSystematics = fs->mkdir( "systematics_histograms" );
  TFileDirectory SingleTopTrees = fs->mkdir( "systematics_trees" );
  

  for(size_t i = 0; i < rate_systematics.size();++i){
    all_syst.push_back(rate_systematics.at(i));  
  }

  for(size_t i = 0; i < all_syst.size();++i){
    
    string syst = all_syst.at(i);
    
    string treename = (channel+"_"+syst);
    
    
    trees[syst] = new TTree(treename.c_str(),treename.c_str()); 
    
    //quantities for the analysis
    trees[syst]->Branch("eta",&etaTree);
    trees[syst]->Branch("costhetalj",&cosTree);
    trees[syst]->Branch("topMass",&topMassTree);
    trees[syst]->Branch("mtwMass",&mtwMassTree);
    
    trees[syst]->Branch("charge",&chargeTree);
    trees[syst]->Branch("runid",&runTree);
    trees[syst]->Branch("lumiid",&lumiTree);
    trees[syst]->Branch("eventid",&eventTree);
    trees[syst]->Branch("weight",&weightTree);
    //trees[syst]->Branch("weightTmp",&weightTree);
    
    trees[syst]->Branch("totalWeight",&totalWeightTree);
    
    trees[syst]->Branch("nT",&nT);
    trees[syst]->Branch("nJ",&nJ);
    
    trees[syst]->Branch("W1T",&W1T);
    trees[syst]->Branch("WG1T",&WG1T);
    trees[syst]->Branch("W2T",&W2T);
    trees[syst]->Branch("WG2T",&WG2T);
   
    //Systematics b weights
    /*    trees[syst]->Branch("bWeightBTagUp",&bWeightTreeBTagUp);
    trees[syst]->Branch("bWeightBTagDown",&bWeightTreeBTagDown);
    
    trees[syst]->Branch("bWeightMisTagUp",&bWeightTreeMisTagUp);
    trees[syst]->Branch("bWeightMisTagDown",&bWeightTreeMisTagDown);
    */
    //Systematics pile up weights
    trees[syst]->Branch("PUWeight",&PUWeightTree);
    
    /*    trees[syst]->Branch("PUWeightPUUp",&PUWeightTreePUUp);
    trees[syst]->Branch("PUWeightPUDown",&PUWeightTreePUDown);
    */
 
    //Systematics turn on weights
    trees[syst]->Branch("turnOnWeight",&turnOnWeightTree);
    //trees[syst]->Branch("turnOnWeightPt",&turnOnPtWeightTree);
    //trees[syst]->Branch("turnOnWeightBTag",&turnOnBTagWeightTree);
    trees[syst]->Branch("turnOnReWeight",&turnOnReWeightTree);
    
    /*   trees[syst]->Branch("turnOnWeightJetTrig1Up",&turnOnWeightTreeJetTrig1Up);
    trees[syst]->Branch("turnOnWeightJetTrig1Down",&turnOnWeightTreeJetTrig1Down);
    
    trees[syst]->Branch("turnOnWeightJetTrig2Up",&turnOnWeightTreeJetTrig2Up);
    trees[syst]->Branch("turnOnWeightJetTrig2Down",&turnOnWeightTreeJetTrig2Down);
    
    trees[syst]->Branch("turnOnWeightJetTrig3Up",&turnOnWeightTreeJetTrig3Up);
    trees[syst]->Branch("turnOnWeightJetTrig3Down",&turnOnWeightTreeJetTrig3Down);
    
    
    trees[syst]->Branch("turnOnWeightBTagTrig1Up",&turnOnWeightTreeBTagTrig1Up);
    trees[syst]->Branch("turnOnWeightBTagTrig1Down",&turnOnWeightTreeBTagTrig1Down);
    
    trees[syst]->Branch("turnOnWeightBTagTrig2Up",&turnOnWeightTreeBTagTrig2Up);
    trees[syst]->Branch("turnOnWeightBTagTrig2Down",&turnOnWeightTreeBTagTrig2Down);
    
    trees[syst]->Branch("turnOnWeightBTagTrig3Up",&turnOnWeightTreeBTagTrig3Up);
    trees[syst]->Branch("turnOnWeightBTagTrig3Down",&turnOnWeightTreeBTagTrig3Down);
    */

    //other observables
    trees[syst]->Branch("leptonPt",&lepPt);
    trees[syst]->Branch("leptonEta",&lepEta);
    trees[syst]->Branch("leptonPhi",&lepPhi);
    trees[syst]->Branch("leptonRelIso",&lepRelIso);
    
    trees[syst]->Branch("fJetPt",&fJetPt);
    trees[syst]->Branch("fJetE",&fJetE);
    trees[syst]->Branch("fJetEta",&fJetEta);
    trees[syst]->Branch("fJetPhi",&fJetPhi);
    trees[syst]->Branch("fJetBtag",&fJetBTag);
    
    trees[syst]->Branch("bJetPt",&bJetPt);
    trees[syst]->Branch("bJetE",&bJetE);
    trees[syst]->Branch("bJetEta",&bJetEta);
    trees[syst]->Branch("bJetPhi",&bJetPhi);
    trees[syst]->Branch("bJetBtag",&bJetBTag);
    trees[syst]->Branch("bJetFlavour",&bJetFlavourTree);
    
    trees[syst]->Branch("metPt",&metPt);
    trees[syst]->Branch("metPhi",&metPhi);
    
    /*    trees[syst]->Branch("topPt",&topPt);
    trees[syst]->Branch("topPhi",&topPhi);
    trees[syst]->Branch("topEta",&topEta);
    trees[syst]->Branch("topE",&topE);
    */

    trees[syst]->Branch("ID",&electronID);
    trees[syst]->Branch("nVertices",&nVertices);
    /*    
    trees[syst]->Branch("totalEnergy",&totalEnergy);
    trees[syst]->Branch("totalMomentum",&totalMomentum);
    */
    trees[syst]->Branch("lowBTag",&lowBTagTree);
    trees[syst]->Branch("highBTag",&highBTagTree);
  }


  passingLepton=0;
  passingJets=0;
  passingBJets=0;
  passingMET=0;

  //TCHPT
  b_tchpt_1_tag = BTagWeight(1,1);
  b_tchpt_g1_tag = BTagWeight(1,999);
  b_tchpt_2_tags = BTagWeight(2,2);
  b_tchpt_g2_tags = BTagWeight(2,999);
  //TCHEL
//  b_tchel_0_tags = BTagWeight(0,0);

  
  //  JEC_PATH = "CondFormats/JetMETObjects/data/";
  //  JEC_PATH = "./JECs/";
  //  fip = edm::FileInPath(JEC_PATH+"Spring10_Uncertainty_AK5PF.txt");
  //fip = edm::FileInPath(JEC_PATH+"GR_R_42_V19_AK5PF_Uncertainty.txt");
  //jecUnc = new JetCorrectionUncertainty(fip.fullPath());
  
  JEC_PATH = "./";

  jecUnc  = new JetCorrectionUncertainty(JEC_PATH+"GR_R_42_V19_AK5PF_Uncertainty.txt");
  //  jecUnc  = new JetCorrectionUncertainty(JEC_PATH+"JEC11_V12_AK5PF_UncertaintySources.txt");
  //jecUnc  = new JetCorrectionUncertainty(*(new JetCorrectorParameters("JEC11_V12_AK5PF_UncertaintySources.txt", "Total")));
  JES_SW = 0.015;
  JES_b_cut = 0.02;
  JES_b_overCut = 0.03;
  

  //JetResolution part
  string fileResolName = "Spring10_PtResolution_AK5PF.txt";
  bool  doGaussianResol = false;
  //  ptResol = new JetResolution(fileResolName, doGaussianResol);  
  
  leptonRelIsoQCDCutUpper = 0.5,leptonRelIsoQCDCutLower=0.3;  


  topMassMeas = 172.9;
  //  doReCorrection_= false;  
  if(doReCorrection_){//FIXME CURRENTLY NOT WORKING!!!
   /*cout << "jec 1" << endl;
  JetCorrectorParameters *ResJetParData = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L2L3Residual.txt"); 
  cout << "jec 1A" << endl;
  JetCorrectorParameters *L3JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L3Absolute.txt");
  JetCorrectorParameters *L2JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L2Relative.txt");
  JetCorrectorParameters *L1JetParData  = new JetCorrectorParameters(JEC_PATH+"GR_R_42_V23_AK5PF_L1FastJet.txt");
  cout << "jec 1B" << endl;
  vParData->push_back(*L1JetParData);
  cout << "jec 1C" << endl;
  vParData->push_back(*L2JetParData);
  vParData->push_back(*L3JetParData);
  vParData->push_back(*ResJetParData);
    */

  cout << "jec 2" << endl;
  // JetCorrectorParameters *L3JetParMC = new JetCorrectorParameters(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L3Absolute.txt");
  //JetCorrectorParameters *L2JetParMC = new JetCorrectorParameters(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L2Relative.txt");

  //  JetCorrectorParameters L1JetParMC(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L1FastJet.txt");
  cout << "jec 3" << endl;
  //  vector<JetCorrectorParameters > vParTmp;

  //  vParMC.push_back(L1JetParMC);
  //vParTmp.push_back(L1JetParMC);
   //   vParMC->push_back(*L2JetParMC)

   //   vParMC->push_back(*L3JetParMC);
  
  cout << "jec 4" << endl;
  
  //   JetCorrectorData = new FactorizedJetCorrector(*vParData);
  //   JetCorrectorMC  = new FactorizedJetCorrector( vParTmp);
   }
   InitializeEventScaleFactorMap();
   InitializeTurnOnReWeight("CentralJet30BTagIP_2ndSF_mu.root");
   LHAPDF::initPDFSet(1, "cteq66.LHgrid");



  //  //cout<< "I work for now but I do nothing. But again, if you gotta do nothing, you better do it right. To prove my good will I will provide you with somse numbers later."<<endl;
   isFirstEvent = true;
}

void SingleTopSystematicsJetsDumper::analyze(const Event& iEvent, const EventSetup& iSetup)
{

  //cout <<" test 1 "<<endl;
  iEvent.getByLabel(jetsEta_,jetsEta);
  iEvent.getByLabel(jetsPt_,jetsPt);
  //  if(jetsPt->size() < 2)return; 
  if(jetsPt->size() > 25 && channel != "Data")return;  //Crazy events with huge jet multiplicity in mc
  iEvent.getByLabel(jetsPhi_,jetsPhi);

  if(isFirstEvent){
    cout <<  "isfirst " << endl;
    iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfMHP);
    iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPM",perfMHPM);
    iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfMHE);
    
    iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPM",perfBHPM);
    iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPT",perfBHP);
    iSetup.get<BTagPerformanceRecord>().get("BTAGTCHEL",perfBHE);
    isFirstEvent = false;
  }
  //  iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
  // iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);

  //  //cout << "test 0 "<<endl;

  gotLeptons=0;
  gotQCDLeptons=0;
  gotLooseLeptons=0;
  gotJets=0;
  gotMets=0;
  gotPU=0;

  //cout <<" test 2 "<<endl;

  jsfshpt.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jsfshel.clear();//  bjs.clear();cjs.clear();ljs.clear(); 

  jsfshpt_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jsfshpt_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear(); 

  jsfshel_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jsfshel_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear(); 

  jsfshpt_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jsfshpt_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear(); 

  jsfshel_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
  jsfshel_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear(); 




  
  
  iEvent.getByLabel(METPhi_,METPhi);
  iEvent.getByLabel(METPt_,METPt);
  iEvent.getByLabel(leptonsRelIso_,leptonsRelIso);
  
  double PUWeight =1;
  double PUWeightNoSyst =1;
  double bWeightNoSyst =1;
  double turnOnWeightValueNoSyst =1;

  BinningPointByMap measurePoint;
  
  float metPx = 0; 
  float metPy = 0;
  
  metPx = METPt->at(0)*cos(METPhi->at(0));
  metPy = METPt->at(0)*sin(METPhi->at(0));

  float metPxTmp = metPx; 
  float metPyTmp = metPy;

  size_t nLeptons = 0;//leptonsPt->size();
  size_t nQCDLeptons = 0;//leptonsPt->size();
  size_t nJets = 0;
  size_t nJetsNoSyst = 0;
  size_t nBJets = 0;
  size_t nLooseBJets = 0;
  //  size_t nAntiBJets = 0;

  
  double WeightLumi = finalLumi*crossSection/originalEvents;
  double Weight = 1;
  double MTWValue =0;
  double MTWValueQCD =0;
  double RelIsoQCDCut = 0.1;
  
  float ptCut = 30;  

  double myWeight = 1.;

  bool didLeptonLoop = false;
  bool passesLeptonStep = false; 
  bool isQCD = false;


  bool didJetLoop = false;

  if(channel=="Data")WeightLumi=1;

  int lowBTagTreePositionNoSyst=-1;
  int highBTagTreePositionNoSyst=-1;
  int maxPtTreePositionNoSyst=-1;
  int minPtTreePositionNoSyst=-1;
  
  for(size_t s = 0; s < systematics.size();++s){
    string syst_name =  systematics.at(s);
    string syst = syst_name;  

    nLeptons =0;
    nQCDLeptons =0;
    nJets =0;
    //    nBJets =0;
    //    cout <<" syst " << syst << endl;
    //    nAntiBJets =0;

    //Here the weight of the event is the weight
    //to normalize the sample to the luminosity 
    //required in the cfg
    Weight = WeightLumi;
    //    Weight *= PUWeight;
    

    bool is_btag_relevant = ((syst_name=="noSyst" || syst_name == "BTagUp" || syst_name == "BTagDown" 
			           || syst_name == "MisTagUp" || syst_name == "MisTagDown"
			      || syst_name == "JESUp" || syst_name == "JESDown" 
			      || syst_name == "JERUp" || syst_name == "JERDown" 
			      ) && channel != "Data"
			     );


    //Setup for systematics

    //This is done according to old b-tagging prescriptions
    
    //Here we have vectors of weights 
    //to be associated with the 
    //b-jets selection in the sample according to algorythm X: 
    //a b-tag requirement implies a b_weight_tag_algoX,
    //a b-veto requirement implies a b_weight_antitag_algoX
 
    //TCHPT
    b_weight_tchpt_1_tag =1;
    b_weight_tchpt_0_tags =1;
    b_weight_tchpt_2_tags =1;
    //TCHEL
    b_weight_tchel_0_tags =1;
   
    nb =0;
    nc =0;
    nudsg =0;

    
    //Clear the vector of objects to be used in the selection
    
    //Define - initialize some variables
    MTWValue =0;
    
    
    //position of lowest and highest b-tag used to chose the top candidate 
    int lowBTagTreePosition=-1;
    lowBTagTree = 99999;
    
    int highBTagTreePosition=-1;
    highBTagTree = -9999;


    int maxPtTreePosition=-1;
    maxPtTree = -99999;
    
    int minPtTreePosition=-1;
    minPtTree = 99999;

    //Taking the unclustered met previously evaluated 
    //and already present in the n-tuples
    //This is used for syst up and down

    if(syst_name == "UnclusteredMETUp"){
      iEvent.getByLabel(UnclMETPx_,UnclMETPx);
      iEvent.getByLabel(UnclMETPy_,UnclMETPy);
      metPx+= (*UnclMETPx) *0.1;
      metPy+= (*UnclMETPy) *0.1;
    }
    if(syst_name == "UnclusteredMETDown"){
      iEvent.getByLabel(UnclMETPx_,UnclMETPx);
      iEvent.getByLabel(UnclMETPy_,UnclMETPy);
      metPx-= (*UnclMETPx) *0.1;
      metPy-= (*UnclMETPy) *0.1;
    }
    
    
    //Define - initialize some variables
    float eta;
    float ptCorr;
    int flavour;
    double unc =0;
    
    //Loops to apply systematics on jets-leptons


    //    cout << " before leptons "<<endl;
    
    //Lepton loop
    if(!didLeptonLoop){
      for(size_t i = 0;i < leptonsRelIso->size();++i){
	float leptonRelIso = leptonsRelIso->at(i);
	lepRelIso = leptonRelIso;
	
	//Apply isolation cut
	if(leptonRelIso>RelIsoCut)continue;
	if(!gotLeptons){
	  iEvent.getByLabel(leptonsEta_,leptonsEta);
	  iEvent.getByLabel(leptonsPt_,leptonsPt);
	  iEvent.getByLabel(leptonsPhi_,leptonsPhi);
	  iEvent.getByLabel(leptonsEnergy_,leptonsEnergy);
	  iEvent.getByLabel(leptonsCharge_,leptonsCharge);
	  iEvent.getByLabel(leptonsID_,leptonsID);
	  iEvent.getByLabel(leptonsDB_,leptonsDB);
	  gotLeptons=true;
	}
	//if electron apply ID cuts
	if(leptonsFlavour_ == "electron"  ) {
	  if(leptonsID->size()==0)cout<< "warning requiring ele id of collection which has no entries! Check the leptonsFlavour parameter "<<endl;
	  float leptonID = leptonsID->at(i);
	  //Legenda for eleId : 0 fail, 1 ID only, 2 iso Only, 3 ID iso only, 4 conv rej, 5 conv rej and ID, 6 conv rej and iso, 7 all 
	  //Require Full ID selection
	  if ((leptonID !=7)&&leptonID !=5)continue;
	  electronID = leptonID;
	  //This is to require conv rejection and ID but do not make requests on iso from id
	  //	if (!(leptonID==5 || leptonID ==7))continue;
	}
	float leptonDB = leptonsDB->at(i);
	if ( fabs(leptonDB) >0.02) continue;
	
	lepRelIso = leptonRelIso;
	
	float leptonPt = leptonsPt->at(i);
	float leptonPhi = leptonsPhi->at(i);
	float leptonEta = leptonsEta->at(i);
	float leptonE = leptonsEnergy->at(i);
	//Build the lepton 4-momentum
	++nLeptons;
	
	leptons[nLeptons-1]=math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE);
	//  leptons.push_back(math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE));
	if(nLeptons >= 3) break;      
      }
      
      bool passesLeptons = (nLeptons ==1);
      bool passesOneLepton = (nLeptons ==1);
      if(passesLeptons){
	iEvent.getByLabel(looseMuonsRelIso_,looseMuonsRelIso);
	iEvent.getByLabel(looseElectronsRelIso_,looseElectronsRelIso);
	bool passesLooseLeptons = (looseMuonsRelIso->size()+looseElectronsRelIso->size())==1;
	passesLeptons = passesLeptons && passesLooseLeptons;
      }
      if(passesLeptons && syst=="noSyst")++passingLepton;
      
      isQCD = (!passesLeptons);
      //      isQCD = (!passesOneLepton);
      
      //Loop for the qcd leptons
      if(doQCD_ && isQCD){
	iEvent.getByLabel(qcdLeptonsRelIso_,qcdLeptonsRelIso);
	for(size_t i = 0;i<qcdLeptonsRelIso->size();++i){

	  float leptonRelIso = qcdLeptonsRelIso->at(i);
	  //  cout << "qcd lep " << i << "rel iso "<<leptonRelIso<<endl;

	  float leptonQCDRelIso = leptonRelIso;
	  //Use an anti-isolation requirement
	  
	  if(leptonsFlavour_ == "muon"){
	    if( leptonQCDRelIso > leptonRelIsoQCDCutUpper )continue;
	    if( leptonQCDRelIso < leptonRelIsoQCDCutLower )continue;
	    
	    if(!gotQCDLeptons){
	      iEvent.getByLabel(qcdLeptonsEta_,qcdLeptonsEta);
	      iEvent.getByLabel(qcdLeptonsPt_,qcdLeptonsPt);
	      iEvent.getByLabel(qcdLeptonsPhi_,qcdLeptonsPhi);
	      iEvent.getByLabel(qcdLeptonsEnergy_,qcdLeptonsEnergy);
	      iEvent.getByLabel(qcdLeptonsCharge_,qcdLeptonsCharge);
	      iEvent.getByLabel(qcdLeptonsID_,qcdLeptonsID);
	      
	      
	      iEvent.getByLabel(qcdLeptonsDB_,qcdLeptonsDB);
	      gotQCDLeptons=true;
	    }
	  }
	  
	  if(leptonsFlavour_ == "electron"  ) {
	    bool QCDCondition = false;
	    iEvent.getByLabel(qcdLeptonsID_,qcdLeptonsID);
	    iEvent.getByLabel(qcdLeptonsDB_,qcdLeptonsDB);
	    float leptonID = qcdLeptonsID->at(i);
	    float beamspot  = abs(qcdLeptonsDB->at(i));
	    bool isid =	(leptonID ==  1 || leptonID == 3 || leptonID == 5 || leptonID == 7);
	    //Legenda for eleId : 0 fail, 1 ID only, 2 iso Only, 3 ID iso only, 4 conv rej, 5 conv rej and ID, 6 conv rej and iso, 7 all 
	    QCDCondition = (!(leptonRelIso < 0.1) && !(beamspot<0.02))  || (!(leptonRelIso<0.1) && !isid) ||(!isid && !(beamspot<0.02));
	    electronID = leptonID;
	  
	    if(!QCDCondition) continue;
	    if(!gotQCDLeptons){
	      iEvent.getByLabel(qcdLeptonsEta_,qcdLeptonsEta);
	      iEvent.getByLabel(qcdLeptonsPt_,qcdLeptonsPt);
	      iEvent.getByLabel(qcdLeptonsPhi_,qcdLeptonsPhi);
	      iEvent.getByLabel(qcdLeptonsEnergy_,qcdLeptonsEnergy);
	      iEvent.getByLabel(qcdLeptonsCharge_,qcdLeptonsCharge);
	      gotQCDLeptons=true;
	    }
	  } 
	  
	  lepRelIso = leptonRelIso;
	  
	  float qcdLeptonPt = qcdLeptonsPt->at(i);
	  float qcdLeptonPhi = qcdLeptonsPhi->at(i);
	  float qcdLeptonEta = qcdLeptonsEta->at(i);
	  float qcdLeptonE = qcdLeptonsEnergy->at(i);
	  //Create the lepton
	  ++nQCDLeptons;
	  
	  qcdLeptons[nQCDLeptons-1]=math::PtEtaPhiELorentzVector(qcdLeptonPt,qcdLeptonEta,qcdLeptonPhi,qcdLeptonE);
	  //	 leptonsQCD.push_back(math::PtEtaPhiELorentzVector(leptonPt,leptonEta,leptonPhi,leptonE));
	if(nQCDLeptons == 3) break;
	
	}
      }
      didLeptonLoop = true;

      isQCD = (nQCDLeptons == 1 && !passesLeptons);

      passesLeptonStep = (passesLeptons || isQCD);
    }
    if(!passesLeptonStep)continue;
    //Clear the vector of btags //NOT USED NOW 
    //    b_weight_tag_algo1.clear();
   //    b_weight_tag_algo2.clear();
    //    b_weight_antitag_algo1.clear();
    //    b_weight_antitag_algo2.clear();
    //        b_discriminator_value_tag_algo1.clear();
    //    b_discriminator_value_antitag_algo2.clear();
    
    ntchpt_tags=0;
    ntchel_tags=0;

    jsfshpt.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
    jsfshel.clear();//  bjs.clear();cjs.clear();ljs.clear(); 
    
    //Clear the vectors of non-leptons
    //    jets.clear();
    //    bjets.clear();
    //    antibjets.clear();


    
  //  cout << " test 1 "<<endl;

    //    cout << " before met "<<endl;

  bool hasTurnOnWeight = false;
  double turnOnWeightValue =1;
  turnOnReWeightTree=1;
  turnOnWeightTreeJetTrig1Up = 1;
  turnOnWeightTreeJetTrig1Down = 1;
  turnOnWeightTreeJetTrig2Up = 1;
  turnOnWeightTreeJetTrig2Down = 1;
  turnOnWeightTreeJetTrig3Up = 1;
  turnOnWeightTreeJetTrig3Down = 1;
  
  turnOnWeightTreeBTagTrig1Up = 1;
  turnOnWeightTreeBTagTrig1Down = 1;
  turnOnWeightTreeBTagTrig2Up = 1;
  turnOnWeightTreeBTagTrig2Down = 1;
  turnOnWeightTreeBTagTrig3Up = 1;
  turnOnWeightTreeBTagTrig3Down = 1;

  bWeightTree = 1;
  bWeightTreeBTagUp = 1;
  bWeightTreeMisTagUp = 1;
  bWeightTreeBTagDown = 1;
  bWeightTreeMisTagDown = 1;

  //  cout << "test 1 "<<endl;
    if(!gotMets){
      iEvent.getByLabel(METPhi_,METPhi);
      iEvent.getByLabel(METPt_,METPt);
      
      metPx = METPt->at(0)*cos(METPhi->at(0));
      metPy = METPt->at(0)*sin(METPhi->at(0));
      
      metPxTmp = metPx; 
      metPyTmp = metPy;

      metPhi = METPhi->at(0);

      
      gotMets = true;
    }

    metPx = metPxTmp; 
    metPy = metPyTmp;

     
    if(syst_name == "UnclusteredMETUp"){
      iEvent.getByLabel(UnclMETPx_,UnclMETPx);
      iEvent.getByLabel(UnclMETPy_,UnclMETPy);
      metPx+= (*UnclMETPx) *0.1;
      metPy+= (*UnclMETPy) *0.1;
    }
    if(syst_name == "UnclusteredMETDown"){
      iEvent.getByLabel(UnclMETPx_,UnclMETPx);
      iEvent.getByLabel(UnclMETPy_,UnclMETPy);
      metPx-= (*UnclMETPx) *0.1;
      metPy-= (*UnclMETPy) *0.1;
    }


    //    cout << " before jets "<<endl;
   
    if(!gotJets){
      iEvent.getByLabel(jetsEta_,jetsEta);
      iEvent.getByLabel(jetsPhi_,jetsPhi);
      
      iEvent.getByLabel(jetsEnergy_,jetsEnergy);
      iEvent.getByLabel(jetsBTagAlgo_,jetsBTagAlgo);
      iEvent.getByLabel(jetsAntiBTagAlgo_,jetsAntiBTagAlgo);

      iEvent.getByLabel(jetsFlavour_,jetsFlavour);
      iEvent.getByLabel(jetsCorrTotal_,jetsCorrTotal);
      if(doResol_)iEvent.getByLabel(genJetsPt_,genJetsPt);
      
      /*      if(channel != "Data"){
      iEvent.getByLabel(x1_,x1h);
      iEvent.getByLabel(x2_,x2h);
      
      x1 = *x1h;
      x2 = *x2h;
      }
      Q2 = x1 * x2 * 7000*7000;
      */
      gotJets= true;
    }

    if(syst == "noSyst" 
       || syst == "JESUp" || syst == "JESDown"
       || syst == "JERUp" || syst == "JERDown"
       || syst == "BTagUp" || syst == "BTagDown"
       || syst == "MisTagUp" || syst == "MisTagDown"
       ){
      for(size_t i = 0;i<jetsPt->size();++i){
      
      eta = jetsEta->at(i);
      if (fabs(eta )>4.5)continue;
      ptCorr = jetsPt->at(i);
      flavour = jetsFlavour->at(i);
      double energyCorr = jetsEnergy->at(i); 


      
      //      float geneta =genJetsEta->at(i);
      float genpt = -1.;
      if(doResol_)genpt = genJetsPt->at(i);
      float rndm = 0.1;
      
      
      //If systematics JES up/down we need to change the pt of the jet
      //consider if it passes the threshold or not

      if(doResol_ && genpt > 0.0){
	resolScale = resolSF(fabs(eta),syst_name);
	double smear = std::max((double)(0.0),(double)(ptCorr+(ptCorr-genpt)*resolScale)/ptCorr);
	energyCorr = energyCorr * smear;
	ptCorr = ptCorr*smear;
      }
      
      /*      if(doReCorrection_){
	      ptCorr = ptCorr/jetsCorrTotal->at(i);  
	      JetCorrectorMC->setJetPt(ptCorr);
	      JetCorrectorMC->setJetEta(eta);
	      double JECorr = JetCorrectorMC->getCorrection();
	ptCorr = ptCorr*JECorr;
	energyCorr = energyCorr/jetsCorrTotal->at(i)*JECorr;  
	//	JetCorrectorMC.setJetPt(ptCorr);
	//JetCorrectorMC.setJetEta(eta);
	//ptCorr = ptCorr*JetCorrectorMC.getCorrection();
	}*/
      
      if(syst_name == "JESUp"){
	unc = jetUncertainty( eta,  ptCorr, flavour);
	ptCorr = ptCorr * (1+unc);
	energyCorr = energyCorr *(1+unc);
	metPx-=(jetsPt->at(i)*cos(jetsPhi->at(i)))*unc;
	metPy-=(jetsPt->at(i)*sin(jetsPhi->at(i)))*unc;
      }
      if(syst_name == "JESDown"){
	unc = jetUncertainty( eta,  ptCorr, flavour);
	ptCorr = ptCorr * (1-unc);
	energyCorr = energyCorr *(1-unc);
	metPx-=-(jetsPt->at(i)*cos(jetsPhi->at(i)))*unc;
	metPy-=-(jetsPt->at(i)*sin(jetsPhi->at(i)))*unc;
      }
      
      
	//Pt cut
	bool passesPtCut = ptCorr>ptCut;
	if(passesPtCut) {
	  ++nJets;
	  jets[nJets-1]=math::PtEtaPhiELorentzVector(ptCorr,jetsEta->at(i), jetsPhi->at(i), energyCorr);
	  if(syst=="noSyst"){ 
	    ++nJetsNoSyst;
	    jetsNoSyst[nJets-1]=jets[nJets-1]; }
	  //	  cout <<" jet no syst "<< nJets-1<<" pt "  <<jetsNoSyst[nJets-1].pt()<<endl;
	}
    
      //b tag thresholds 
      
      double valueAlgo1 = jetsBTagAlgo->at(i);
      double valueAlgo2 = jetsAntiBTagAlgo->at(i);
      
      bool passesMediumBTag = valueAlgo1  > 1.93;

      bool passesBTag = valueAlgo1  >bTagThreshold;
      bool passesLooseBTag = valueAlgo2 >1.7;

      if(!passesPtCut) continue;
      
      //max pt position:
      int pos =nJets-1;
      if(ptCorr > maxPtTree){ 
	maxPtTreePosition = nJets-1;
	maxPtTree = ptCorr;
      }
      //min pt position:
      if(ptCorr < minPtTree){ 
	minPtTreePosition = nJets-1;
	minPtTree = ptCorr;
      }

      
      //Passes firs algorythm (b tag requirement in the case of t-channel standard selection)
      
      double etaMin =  min(fabs(eta),(float)2.3999);
      double ptMin =  min(ptCorr,(float)239.9);//min(jets.back().pt(),998.0);
      measurePoint.insert(BinningVariables::JetAbsEta,etaMin);
      measurePoint.insert(BinningVariables::JetEt,ptMin);
      //Apply different SFs if it is b,c or light jet
      if(abs(flavour)==4){ 
	++nc;
	  double hptSF=1;
	  double hpteff = EFFMap("TCHPT_C");
	  	  
	  hptSF = BTagSFNew(ptCorr,"TCHPT");
	  jsfshpt.push_back(BTagWeight::JetInfo(hpteff,hptSF));
      }
      else if(abs(flavour)==5){
	++nb;
	
	double hpteff = EFFMap("TCHPT_B");
	double hptSF=1;
	hptSF = BTagSFNew(ptCorr,"TCHPT");
	
	//double hptSFErr=0;
	//hptSFErr = BTagSFErrNew(ptCorr,"TCHPT");
	
	jsfshpt.push_back(BTagWeight::JetInfo(hpteff,hptSF));
	
      }
      else{
	double hptSF=1;
	double hpteff = EFFMap("TCHPT_L");
	hptSF=MisTagSFNew(ptCorr,eta,"TCHPT");
	jsfshpt.push_back(BTagWeight::JetInfo(hpteff,hptSF));
	++nudsg;
      }
      
      //  if(passesMediumBTag){
      //    ++ntchpm_tags;
      //  }
      if(passesLooseBTag){
	++ntchel_tags;
	if(syst== "noSyst")++nLooseBJets;
      }
      if(passesBTag) {
	//Add to b-jet collection
	if(syst=="noSyst" )  ++nBJets;
	bjets[nBJets-1]=jets[nJets-1];
	++ntchpt_tags;
      }
      
      //Condition to find the highest/lowest b-tag 
      //according to algo 1 (tchp) 
      ////cout << " i "<< i <<" jets size "<< jets.size()<< " btag  "<< 
      if(jetsBTagAlgo->at(i) > highBTagTree){
	highBTagTree=jetsBTagAlgo->at(i);
	highBTagTreePosition=nJets-1;
	bJetFlavourTree = jetsFlavour->at(i);
      } 
      if(jetsBTagAlgo->at(i) < lowBTagTree){
	lowBTagTree=jetsBTagAlgo->at(i);
	lowBTagTreePosition=nJets-1;
      }
      if(nJets>=10 )break;
      }
    }
    //  cout << "test 2 "<<endl;
    
    if(syst=="noSyst"){
      highBTagTreePositionNoSyst = highBTagTreePosition;
      lowBTagTreePositionNoSyst = lowBTagTreePosition;
      maxPtTreePositionNoSyst = maxPtTreePosition;
      minPtTreePositionNoSyst = minPtTreePosition;
      nbNoSyst = nb;
      ncNoSyst = nc;
      nudsgNoSyst = nudsg;
      jsfshptNoSyst = jsfshpt; 
      jsfshelNoSyst = jsfshel; 
    }
    if(!(syst == "noSyst" 
       || syst == "JESUp" || syst == "JESDown"
       || syst == "JERUp" || syst == "JERDown"
       || syst == "BTagUp" || syst == "BTagDown"
       || syst == "MisTagUp" || syst == "MisTagDown" )){
      nJets = nJetsNoSyst;
      ntchpt_tags = nBJets; 
      ntchel_tags = nLooseBJets; 
      nb = nbNoSyst;
      nc = ncNoSyst;
      nudsg = nudsgNoSyst;
      for(size_t a =0; a < nJetsNoSyst;++a){
	jets[a] = jetsNoSyst[a];
	//	cout <<" jet no syst "<< a <<" pt "  <<jets[a].pt()<<endl;
      }
      highBTagTreePosition = highBTagTreePositionNoSyst;
      lowBTagTreePosition = lowBTagTreePositionNoSyst;
      maxPtTreePosition = maxPtTreePositionNoSyst;
      minPtTreePosition = minPtTreePositionNoSyst;
      jsfshpt = jsfshptNoSyst;
      jsfshel = jsfshelNoSyst;

    }

    //    cout <<" syst "<< syst<< " njets "<< nJets << " nJetsNoSyst " << nJetsNoSyst << " nBJets "<< ntchpt_tags<< 
    //      " nBJetsNoSyst "<< nBJets<< " nb "<< nb << " nbNoSyst "<<nbNoSyst<< " lowBPos " <<lowBTagTreePosition << " lowBNoSyst " << 
    //      lowBTagTreePositionNoSyst<<endl;

    if( !flavourFilter(channel,nb,nc,nudsg) ) continue;

    /////////
    ///End of the standard lepton-jet loop 
    /////////
    
    int B = ntchpt_tags; 
    nJ = nJets;
    nT = B;
    //    2T_QCD=5;
 
    leptonPFour = leptons[0];
    chargeTree = leptonsCharge->at(0) ; 
    
    if( syst=="noSyst" && nJets ==2 && B ==1 ){	++passingJets;}
    
    //   if( (B==0||B==3 ) && (ntchel_tags !=0  || lowBTagTreePosition<0 || lowBTagTreePosition==highBTagTreePosition) ) continue;//Sample A condition, ok for now
    
    //  cout << "test 3 "<<endl;
    
      if(syst == "noSyst"){ 

	W1T =     b_tchpt_1_tag.weight(jsfshpt,ntchpt_tags);
	WG1T =     b_tchpt_g1_tag.weight(jsfshpt,ntchpt_tags);
	W2T =     b_tchpt_2_tags.weight(jsfshpt,ntchpt_tags);
	WG2T =     b_tchpt_g2_tags.weight(jsfshpt,ntchpt_tags);

      }
      else if(syst == "JESUp" || syst == "JESDown" || 
	      syst == "JERUp" || syst == "JERDown" || 
	      syst == "BTagUp" || syst == "BTagDown" ||
	      syst == "MisTagUp" || syst == "MisTagDown" ) bWeightTree = bTagSF(B);
      else bWeightTree = bWeightNoSyst;

      //    cout << " before npv "<<endl;

      if(doPU_){
	if(!gotPU ){
	  //	      cout << " before npv "<<endl;
	  iEvent.getByLabel(nm1_,nm1);
	  iEvent.getByLabel(n0_,n0);
	  iEvent.getByLabel(np1_,np1);
	  nVertices = *n0;
	  gotPU = true;
	}
	
      }
      else(nVertices = -1);

      if(doPU_){
	if(syst == "noSyst"){ PUWeightNoSyst = pileUpSF(syst); PUWeight = PUWeightNoSyst;
	  //	  PUWeightTreePUUp = pileUpSF("PUUp");
	  //PUWeightTreePUDown = pileUpSF("PUDown");
	}
	else PUWeight = PUWeightNoSyst;
      }
      else PUWeight=1;
      
      if(leptonsFlavour_ == "electron" && doTurnOn_){
	jetprobs.clear();
	for(size_t i = 0;i<jetsEta->size();++i){
	  double eta = jetsEta->at(i);
	  double btag = jetsBTagAlgo->at(i);
	  double pt = jetsPt->at(i);
	  if (fabs(eta)>2.6) jetprobs.push_back(0.);
	  jetprobs.push_back(jetprob(pt,btag,eta,syst));
	}
	turnOnWeightTree = turnOnWeight(jetprobs,1);
	turnOnReWeightTree = turnOnReWeight(turnOnWeightValue,jets[highBTagTreePosition].pt(),highBTagTree);
      }
      
      if(syst== "noSyst" && doPDF_ ){
	
	if(channel != "Data"){
	  iEvent.getByLabel(x1_,x1h);
	  iEvent.getByLabel(x2_,x2h);
	  
	  iEvent.getByLabel(scalePDF_,scalePDFh);
	  iEvent.getByLabel(id1_,id1h);
	  iEvent.getByLabel(id2_,id2h);
	  
	  x1 = *x1h;
	  x2 = *x2h;
	  
	  scalePDF = *scalePDFh;
	  
	  id1 = *id1h;
	  id2 = *id2h;
	  
	}
	//Q2 = x1 * x2 * 7000*7000;
	LHAPDF::usePDFMember(1,0);
	double xpdf1 = LHAPDF::xfx(1, x1, scalePDF, id1);
	double xpdf2 = LHAPDF::xfx(1, x2, scalePDF, id2);
	double w0 = xpdf1 * xpdf2;
	for(int p=1; p <=44; ++p){
	  LHAPDF::usePDFMember(1,p);
	  double xpdf1_new = LHAPDF::xfx(1, x1, scalePDF, id1);
	  double xpdf2_new = LHAPDF::xfx(1, x2, scalePDF, id2);
	  double pweight = xpdf1_new * xpdf2_new / w0;
	  pdf_weights[p-1]=pweight;
	}
      }
      
      //      turnOnWeightTree = turnOnWeightValue;
      PUWeightTree = PUWeight;

      //    cout << " before mtw "<<endl;
      
      metPt = sqrt(metPx*metPx+metPy*metPy);
      MTWValue =  sqrt((leptonPFour.pt()+metPt)*(leptonPFour.pt()+metPt)  -(leptonPFour.px()+metPx)*(leptonPFour.px()+metPx) -(leptonPFour.py()+metPy)*(leptonPFour.py()+metPy));
      bool passesMet= false;
    
      if( syst=="noSyst" && nJets ==2 && B==1){
	//	++passingJets;
	++passingBJets;
	
	if(leptonsFlavour_ == "muon" && MTWValue>40 ) {++passingMET;}//++Passingmet (DD);passesMet= true;}
	if(leptonsFlavour_ == "electron" && metPt>35) {++passingMET;}//passesMet= true;}
	
      }
  
      //  cout << "test  "<<endl;

      /*      math::PtEtaPhiELorentzVector top = top4Momentum(leptonPFour,jets[highBTagTreePosition],metPx,metPy);
      float fCosThetaLJ =  cosThetaLJ(leptonPFour, jets[lowBTagTreePosition], top);
      */

      runTree = iEvent.eventAuxiliary().run();
      lumiTree = iEvent.eventAuxiliary().luminosityBlock();
      eventTree = iEvent.eventAuxiliary().event();
      
      etaTree = fabs(jets[lowBTagTreePosition].eta());
      //      cosTree = fCosThetaLJ;
      /*topMassTree = top.mass();*/
      mtwMassTree = MTWValue;

      lepPt = leptonPFour.pt();
      lepEta = leptonPFour.eta();
      lepPhi = leptonPFour.phi();
      
      bJetPt = jets[highBTagTreePosition].pt();
      bJetE = jets[highBTagTreePosition].energy();
      bJetEta = jets[highBTagTreePosition].eta();
      bJetPhi = jets[highBTagTreePosition].phi();
      
      fJetPt = jets[lowBTagTreePosition].pt();
      fJetE = jets[lowBTagTreePosition].energy();
      fJetEta = jets[lowBTagTreePosition].eta();
      fJetPhi = jets[lowBTagTreePosition].phi();
     
      weightTree = Weight;
      totalWeightTree = bWeightTree*turnOnWeightValue*PUWeight*Weight;
      
      etaTree = fabs(jets[lowBTagTreePosition].eta());
      etaTree2 = fabs(jets[highBTagTreePosition].eta());
      //cosTree = fCosThetaLJ;
      //      topMassTree = top.mass();
      //mtwMassTree = MTWValue;
      
	cout << " B is "<< B<< " syst is "<<syst_name <<endl;
	cout<< " tree name "<< trees[syst_name]->GetName() <<endl;
	trees[syst_name]->Fill();            
    
    //W Sample
    
    
	
	
  }

}
																			
//CosThetalj given top quark, lepton and light jet
float SingleTopSystematicsJetsDumper::cosThetaLJ(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top){
  
  math::PtEtaPhiELorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton,top.BoostToCM());
  math::PtEtaPhiELorentzVector boostedJet = ROOT::Math::VectorUtil::boost(jet,top.BoostToCM());

  return  ROOT::Math::VectorUtil::CosTheta(boostedJet.Vect(),boostedLepton.Vect());
  
}

//top quark 4-momentum given lepton, met and b-jet
math::PtEtaPhiELorentzVector SingleTopSystematicsJetsDumper::top4Momentum(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy){
  return top4Momentum(lepton.px(),lepton.py(),lepton.pz(),lepton.energy(),jet.px(),jet.py(),jet.pz(),jet.energy(),metPx,metPy);
}

//top quark 4-momentum original function given the necessary parameters 
math::PtEtaPhiELorentzVector SingleTopSystematicsJetsDumper::top4Momentum(float leptonPx, float leptonPy, float leptonPz, float leptonE, float jetPx, float jetPy, float jetPz,float jetE, float metPx, float metPy){
  float lepton_Pt = sqrt( (leptonPx*leptonPx)+  (leptonPy*leptonPy) );
  
  math::XYZTLorentzVector neutrino = NuMomentum(leptonPx,leptonPy,leptonPz,lepton_Pt,leptonE,metPx,metPy);//.at(0);;
    
  math::XYZTLorentzVector lep(leptonPx,leptonPy,leptonPz,leptonE);
  math::XYZTLorentzVector jet(jetPx,jetPy,jetPz,jetE);
  
  math::XYZTLorentzVector top = lep + jet + neutrino;
  return math::PtEtaPhiELorentzVector(top.pt(),top.eta(),top.phi(),top.E());  
}

//top neutrino 4-momentum function given the parameters
//In brief: 
//Works for top->1l+1neutrino+1bjet
//Assuming all met comes from neutrino
/////What it does:
//w boson mass put to pdg value
//obtained neutrino pz from kinematics
//We get a second order equation 
/////In case of two positive Delta solutions:
//we choose solution with minimum |pz|
/////In case of two negative Delta solutions:
//in such case: mtw > mw
//To solve this: put mtw = mw 
//Solve the equations
//In this way we must
//drop the constraints px_Nu = MET_x and py_Nu = MET_y
//Solve this by chosing the px_Nu and py_Nu that 
//minimize the distance from the MET in the px-py plane
//Such minimization can be done analytically with derivatives
//and much patience. Here we exploit such analytical minimization
/////
//More detailed inline description: work in progress! 
math::XYZTLorentzVector SingleTopSystematicsJetsDumper::NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy ){

  double  mW = 80.399;
  
  math::XYZTLorentzVector result;
  
  //  double Wmt = sqrt(pow(Lepton.et()+MET.pt(),2) - pow(Lepton.px()+metPx,2) - pow(leptonPy+metPy,2) );
    
  double MisET2 = (metPx*metPx + metPy*metPy);
  double mu = (mW*mW)/2 + metPx*leptonPx + metPy*leptonPy;
  double a  = (mu*leptonPz)/(leptonE*leptonE - leptonPz*leptonPz);
  double a2 = TMath::Power(a,2);
  double b  = (TMath::Power(leptonE,2.)*(MisET2) - TMath::Power(mu,2.))/(TMath::Power(leptonE,2) - TMath::Power(leptonPz,2));
  double pz1(0),pz2(0),pznu(0);
  int nNuSol(0);

  math::XYZTLorentzVector p4nu_rec;
  math::XYZTLorentzVector p4W_rec;
  math::XYZTLorentzVector p4b_rec;
  math::XYZTLorentzVector p4Top_rec;
  math::XYZTLorentzVector p4lep_rec;    
  
  p4lep_rec.SetPxPyPzE(leptonPx,leptonPy,leptonPz,leptonE);
  
  math::XYZTLorentzVector p40_rec(0,0,0,0);
  
  if(a2-b > 0 ){
    //if(!usePositiveDeltaSolutions_)
    //  {
    //	result.push_back(p40_rec);
    //	return result;
    //	}
    double root = sqrt(a2-b);
    pz1 = a + root;
    pz2 = a - root;
    nNuSol = 2;     
    
    //    if(usePzPlusSolutions_)pznu = pz1;    
    //    if(usePzMinusSolutions_)pznu = pz2;
    //if(usePzAbsValMinimumSolutions_){
    pznu = pz1;
    if(fabs(pz1)>fabs(pz2)) pznu = pz2;
    //}
    
    
    double Enu = sqrt(MisET2 + pznu*pznu);
    
    p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu);
    
    //    result =.push_back(p4nu_rec);
    result = p4nu_rec;
    
  }
  else{
    
    // if(!useNegativeDeltaSolutions_){
    //result.push_back(p40_rec);
    //  return result;
    //    }
    //    double xprime = sqrt(mW;
    

      double ptlep = leptonPt,pxlep=leptonPx,pylep=leptonPy,metpx=metPx,metpy=metPy;
      
      double EquationA = 1;
      double EquationB = -3*pylep*mW/(ptlep);
      double EquationC = mW*mW*(2*pylep*pylep)/(ptlep*ptlep)+mW*mW-4*pxlep*pxlep*pxlep*metpx/(ptlep*ptlep)-4*pxlep*pxlep*pylep*metpy/(ptlep*ptlep);
      double EquationD = 4*pxlep*pxlep*mW*metpy/(ptlep)-pylep*mW*mW*mW/ptlep;
      
      std::vector<long double> solutions = EquationSolve<long double>((long double)EquationA,(long double)EquationB,(long double)EquationC,(long double)EquationD);
      
      std::vector<long double> solutions2 = EquationSolve<long double>((long double)EquationA,-(long double)EquationB,(long double)EquationC,-(long double)EquationD);
      
      
      double deltaMin = 14000*14000;
      double zeroValue = -mW*mW/(4*pxlep); 
      double minPx=0;
      double minPy=0;
      
      //    std::cout<<"a "<<EquationA << " b " << EquationB  <<" c "<< EquationC <<" d "<< EquationD << std::endl; 
      
   //  if(usePxMinusSolutions_){
	for( int i =0; i< (int)solutions.size();++i){
	  if(solutions[i]<0 ) continue;
	  double p_x = (solutions[i]*solutions[i]-mW*mW)/(4*pxlep); 
	  double p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x -mW*ptlep*solutions[i])/(2*pxlep*pxlep);
	  double Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy); 
	  
      //      std:://cout<<"intermediate solution1 met x "<<metpx << " min px " << p_x  <<" met y "<<metpy <<" min py "<< p_y << std::endl; 

      if(Delta2< deltaMin && Delta2 > 0){deltaMin = Delta2;
      minPx=p_x;
      minPy=p_y;}
      //     std:://cout<<"solution1 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
      }
	
	//    } 
	
	//if(usePxPlusSolutions_){
      for( int i =0; i< (int)solutions2.size();++i){
	if(solutions2[i]<0 ) continue;
	double p_x = (solutions2[i]*solutions2[i]-mW*mW)/(4*pxlep); 
	double p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x +mW*ptlep*solutions2[i])/(2*pxlep*pxlep);
	double Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy); 
	//  std:://cout<<"intermediate solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
	if(Delta2< deltaMin && Delta2 > 0){deltaMin = Delta2;
	  minPx=p_x;
	  minPy=p_y;}
	//	std:://cout<<"solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
      }
      //}
  
    double pyZeroValue= ( mW*mW*pxlep + 2*pxlep*pylep*zeroValue);
    double delta2ZeroValue= (zeroValue-metpx)*(zeroValue-metpx) + (pyZeroValue-metpy)*(pyZeroValue-metpy);
    
    if(deltaMin==14000*14000)return result;    
    //    else std:://cout << " test " << std::endl;

    if(delta2ZeroValue < deltaMin){
      deltaMin = delta2ZeroValue;
      minPx=zeroValue;
      minPy=pyZeroValue;}
  
    //    std:://cout<<" MtW2 from min py and min px "<< sqrt((minPy*minPy+minPx*minPx))*ptlep*2 -2*(pxlep*minPx + pylep*minPy)  <<std::endl;
    ///    ////Y part   

    double mu_Minimum = (mW*mW)/2 + minPx*pxlep + minPy*pylep;
    double a_Minimum  = (mu_Minimum*leptonPz)/(leptonE*leptonE - leptonPz*leptonPz);
    pznu = a_Minimum;
  
    //if(!useMetForNegativeSolutions_){
      double Enu = sqrt(minPx*minPx+minPy*minPy + pznu*pznu);
      p4nu_rec.SetPxPyPzE(minPx, minPy, pznu , Enu);
  
      //    }
      //    else{
      //      pznu = a;
      //      double Enu = sqrt(metpx*metpx+metpy*metpy + pznu*pznu);
      //      p4nu_rec.SetPxPyPzE(metpx, metpy, pznu , Enu);
      //    }
    
      //      result.push_back(p4nu_rec);
      result = p4nu_rec;
  }
  return result;    
}


//B-C weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsJetsDumper::BTagSFNew(double pt, string algo){
  if(algo == "TCHPT")return 0.895596*((1.+(9.43219e-05*pt))/(1.+(-4.63927e-05*pt)));
  if(algo == "TCHEL")return 0.603913*((1.+(0.286361*pt))/(1.+(0.170474*pt)));
  return 1;
}


double SingleTopSystematicsJetsDumper::BTagSFErrNew(double pt, string algo){
  if(algo == "TCHPT"){
    if (pt > 30 && pt < 40)return 0.0543376;
    if (pt > 40 && pt < 50)return 0.0534339;
    if (pt > 50 && pt < 60)return 0.0266156;
    if (pt > 60 && pt < 70)return 0.0271337;
    if (pt > 70 && pt < 80)return 0.0276364;
    if (pt > 80 && pt <100)return 0.0308838;
    if (pt >100 && pt <120)return 0.0381656;
    if (pt >120 && pt <160)return 0.0336979;
    if (pt >160 && pt <210)return 0.0336773;
    if (pt >210 && pt <260)return 0.0347688;
    if (pt >260 && pt <320)return 0.0376865;
    if (pt >320 && pt <400)return 0.0556052;
    if (pt >400 && pt <500)return 0.0598105;
    if (pt >500 && pt <670)return 0.0861122;
  }
  if(algo == "TCHEL"){
    if (pt > 30 && pt < 40)return 0.0244956;
    if (pt > 40 && pt < 50)return 0.0237293;
    if (pt > 50 && pt < 60)return 0.0180131;
    if (pt > 60 && pt < 70)return 0.0182411;
    if (pt > 70 && pt < 80)return 0.0184592;
    if (pt > 80 && pt <100)return 0.0106444;
    if (pt >100 && pt <120)return 0.0110736;
    if (pt >120 && pt <160)return 0.0106296;
    if (pt >160 && pt <210)return 0.0175259;
    if (pt >210 && pt <260)return 0.0161566;
    if (pt >260 && pt <320)return 0.0158973;
    if (pt >320 && pt <400)return 0.0186782;
    if (pt >400 && pt <500)return 0.0371113;
    if (pt >500 && pt <670)return 0.0289788;
  }
  return 0;
}

double SingleTopSystematicsJetsDumper::MisTagSFNew(double pt, double eta, string algo){
  if(algo == "TCHPT")return ((1.20711+(0.000681067*pt))+(-1.57062e-06*(pt*pt)))+(2.83138e-10*(pt*(pt*pt)));
  if(algo == "TCHEL") return (1.10649*((1+(-9.00297e-05*pt))+(2.32185e-07*(pt*pt))))+(-4.04925e-10*(pt*(pt*(pt/(1+(-0.00051036*pt))))));
  return 0;
}

double SingleTopSystematicsJetsDumper::MisTagSFErrNewUp(double pt, double eta, string algo){
  if(algo == "TCHPT")return ((1.38002+(0.000933875*pt))+(-2.59821e-06*(pt*pt)))+(1.18434e-09*(pt*(pt*pt)));
  if(algo == "TCHEL")return (1.19751*((1+(-0.000114197*pt))+(3.08558e-07*(pt*pt))))+(-5.27598e-10*(pt*(pt*(pt/(1+(-0.000422372*pt)))))) ;
  return 0;
}

double SingleTopSystematicsJetsDumper::MisTagSFErrNewDown(double pt, double eta, string algo){
  if(algo == "TCHPT")return ((1.03418+(0.000428273*pt))+(-5.43024e-07*(pt*pt)))+(-6.18061e-10*(pt*(pt*pt)));
  if(algo == "TCHEL")return (1.01541*((1+(-6.04627e-05*pt))+(1.38195e-07*(pt*pt))))+(-2.83043e-10*(pt*(pt*(pt/(1+(-0.000633609*pt))))));
  return 0;
}


double SingleTopSystematicsJetsDumper::EFFMapNew(double btag, string algo){
  if(algo == "TCHP_B")return 1.26119661124e-05*btag*btag*btag*btag +  -0.000683198597977*btag*btag*btag +  0.0145106168149*btag*btag +  -0.159575511553*btag +  0.887707865272;
  if(algo == "TCHP_C"){
    if(btag<0.54) return 0.451288118581*exp(-0.0213290505241*btag*btag*btag + 0.356020789904*btag*btag + -2.20158883207*btag + 1.84838018633 );
    else return 0.99;
  }
  if(algo == "TCHP_L")return (-0.00101+(4.70405e-05*btag))+(8.3338e-09*(btag*btag));

  if(algo == "TCHE_B")return 3.90732786802e-06*btag*btag*btag*btag +  -0.000239934437355*btag*btag*btag +  0.00664986827287*btag*btag +  -0.112578996016*btag +  1.00775721404;
  if(algo == "TCHE_C"){
    if(btag>0.46 ) return 0.343760640168*exp(-0.00315525164823*btag*btag*btag + 0.0805427315196*btag*btag + -0.867625139194*btag + 1.44815935164 );
    else return 0.99;//EFFMap("TCHEL_C");
  }

  if(algo == "TCHE_L")return(((-0.0276197+(0.00291907*btag))+(-7.51594e-06*(btag*btag)))+(9.82128e-09*(btag*(btag*btag))))+(-5.33759e-12*(btag*(btag*(btag*btag))));
  return 1;
}

//JES uncertainty as a function of pt, eta and jet flavour 
double SingleTopSystematicsJetsDumper::jetUncertainty(double eta, double ptCorr, int flavour){
  jecUnc->setJetEta(eta); 
  jecUnc->setJetPt(ptCorr);
  double JetCorrection = jecUnc->getUncertainty(true); // In principle, boolean controls if uncertainty on +ve or -ve side is returned (asymmetric errors) but not yet implemented.
  bool cut = ptCorr> 50 && ptCorr < 200 && fabs(eta) < 2.0;
  // JES_SW = 0.015;                                                                                                                                 
  //  double JES_PU=0.75*0.8*2.2/ptCorr;
  double JES_PU=0.; //We are using pfNoPU must understand what value to put there
  double JES_b=0;
  if(abs(flavour)==5){
    if(cut) JES_b = JES_b_cut;
    else JES_b = JES_b_overCut;
  }
  //    float JESUncertaintyTmp = sqrt(JESUncertainty*JESUncertainty + JetCorrection*JetCorrection);                                                 
  return sqrt(JES_b*JES_b + JES_PU*JES_PU +JES_SW*JES_SW + JetCorrection*JetCorrection);
}

//EndJob filling rate systematics trees
void SingleTopSystematicsJetsDumper::endJob(){
  
  //part for rate systematics

  cout <<endl<< passingLepton<< " | "<< passingJets <<" | "<< passingMET <<" | "<< passingBJets << endl<<endl;

  resetWeightsDoubles();
  /*  for(size_t i = 0; i < rate_systematics.size();++i){
    string syst = rate_systematics[i];
    string treename = (channel+"_"+syst);

    cout<< " endjob"  << syst<< " 0 "<<endl;
    int bj =0;
    trees[bj][syst]->CopyAddresses(trees[bj]["noSyst"]);
    

        cout<< " endjob"  << syst<< " 1 "<<endl;

    
    //modify the weight by a constant factor    
    double tmpWeight = 0;
    double weightSF = 1.;
    
    TBranch * b = trees[bj]["noSyst"]->GetBranch("weight");
    int entries = b->GetEntries();
    b->SetAddress(&tmpWeight);    


    cout<< " endjob"  << syst<< " 2 "<<endl;
    
    trees[bj][syst]->GetBranch("weight")->Reset();
    trees[bj][syst]->GetBranch("weight")->SetAddress(&tmpWeight);
    

    cout<< " endjob"  << syst<< " 3 "<<endl;
    
    for(int t =0; t < entries ; ++t){
      b->GetEntry(t);
      tmpWeight*=weightSF;
      trees[bj][syst]->GetBranch("weight")->Fill();
      
    }
    

    
    b->SetAddress(&weightTree);
    trees[bj][syst]->GetBranch("weight")->SetAddress(&weightTree);
    

    
    //    cout<< " syst "<< syst<< " weights entries "<<  entries <<endl;

  }*/
}
  
//B-C weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsJetsDumper::BScaleFactor(string algo,string syst_name){
  
  double bcentral =0.9;  
  double berr = 0.15*bcentral;
  double cerr =0.3*bcentral;
  double tcheeff =0.7;
  
  if(syst_name == "BTagUp"){
    if(algo == "TCHP_B"){
      return bcentral+berr;
    }
    if(algo == "TCHP_C"){
      return bcentral+cerr;
    }
    
    if(algo == "TCHE_B"){
      return bcentral+berr;
    }
    
    if(algo == "TCHE_C"){
      return bcentral+cerr;
    }
    
  }
  
  if(syst_name == "BTagDown"){
    if(algo == "TCHP_B"){
      return bcentral-berr;
    }
    if(algo == "TCHP_C"){
      return bcentral-cerr;
    }
  
    if(algo == "TCHE_B"){
      return bcentral-berr;
    }
    if(algo == "TCHE_C"){
      return bcentral-berr;
    }
  }

  if(algo == "TCHP_B"){
    return bcentral;
  }
  if(algo == "TCHP_C"){
    return bcentral;
  }
  if(algo == "TCHE_B"){
    return bcentral;
  }
  if(algo == "TCHE_C"){
    return bcentral;
  }
    
  return 0.9;
}

//Mistag weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsJetsDumper::MisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr){
  double mistagcentral = sf;  
  double mistagerr = sferr;
  double tcheeff = eff;

  
  if(syst_name == "MisTagUp"){
    if(algo == "TCHP_L"){
      return mistagcentral+mistagerr;
    }
    if(algo == "TCHE_L"){
      return mistagcentral+mistagerr;
    }
    
  }
  
  if(syst_name == "MisTagDown"){
    if(algo == "TCHP_L"){
      return mistagcentral-mistagerr;
    }
    if(algo == "TCHE_L"){
      return mistagcentral-mistagerr;
    }
  }

  if(algo == "TCHP_L"){
    return mistagcentral;
  }
  if(algo == "TCHE_L"){
    return mistagcentral;
  }
  
  return 0.9;


}



//B-C veto weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsJetsDumper::AntiBScaleFactor(string algo,string syst_name){
  
  double bcentral =0.9;  
  double berr = 0.15*bcentral;
  double cerr =0.3*bcentral;
  double tcheeff =0.7;
  double tchpeff =0.26;
  
  if(syst_name == "BTagUp"){
    if(algo == "TCHP_B"){
      return (1-tchpeff*(bcentral+berr))/(1-tchpeff);
    }
    if(algo == "TCHP_C"){
      return (1-tchpeff*(bcentral+cerr))/(1-tchpeff);
    }
    
    if(algo == "TCHE_B"){
      return (1-tcheeff*(bcentral+berr))/(1-tcheeff);
    }
    
    if(algo == "TCHE_C"){
      return (1-tcheeff*(bcentral+cerr))/(1-tcheeff);
    }
  }
  
  if(syst_name == "BTagDown"){
    if(algo == "TCHP_B"){
      return (1-tchpeff*(bcentral-berr))/(1-tchpeff);
    }
    if(algo == "TCHP_C"){
      return (1-tchpeff*(bcentral-cerr))/(1-tchpeff);
    }
  
    if(algo == "TCHE_B"){
      return (1-tcheeff*(bcentral-berr))/(1-tcheeff);
    }
    if(algo == "TCHE_C"){
      return (1-tcheeff*(bcentral-cerr))/(1-tcheeff);
    }
  }

  if(algo == "TCHP_B"){
    return (1-tchpeff*(bcentral))/(1-tchpeff);
  }
  if(algo == "TCHP_C"){
    return (1-tchpeff*(bcentral))/(1-tchpeff);
  }
  if(algo == "TCHE_B"){
    return (1-tcheeff*(bcentral))/(1-tcheeff);
  }
  if(algo == "TCHE_C"){
    return (1-tcheeff*(bcentral))/(1-tcheeff);
  }
    
  return 0.9;
}

void SingleTopSystematicsJetsDumper::InitializeEventScaleFactorMap(){

  TCHPT_B = EventScaleFactor("TCHPT_B","noSyst");
  TCHPT_C = EventScaleFactor("TCHPT_C","noSyst");
  TCHPT_L = EventScaleFactor("TCHPT_L","noSyst");
    
  
  TCHPT_BBTagUp = EventScaleFactor("TCHPT_B","BTagUp");
  TCHPT_BBTagDown = EventScaleFactor("TCHPT_B","BTagDown");
  TCHPT_CBTagUp = EventScaleFactor("TCHPT_C","BTagUp");
  TCHPT_CBTagDown = EventScaleFactor("TCHPT_C","BTagDown");
  TCHPT_LMisTagUp = EventScaleFactor("TCHPT_L","MisTagUp");
  TCHPT_LMisTagDown = EventScaleFactor("TCHPT_L","MisTagDown");
    

  TCHPT_BAnti = EventAntiScaleFactor("TCHPT_B","noSyst");
  TCHPT_CAnti = EventAntiScaleFactor("TCHPT_C","noSyst");
  TCHPT_LAnti = EventAntiScaleFactor("TCHPT_L","noSyst");

  TCHPT_BAntiBTagUp = EventAntiScaleFactor("TCHPT_B","BTagUp");
  TCHPT_BAntiBTagDown = EventAntiScaleFactor("TCHPT_B","BTagDown");
  TCHPT_CAntiBTagUp = EventAntiScaleFactor("TCHPT_C","BTagUp");
  TCHPT_CAntiBTagDown = EventAntiScaleFactor("TCHPT_C","BTagDown");
  TCHPT_LAntiMisTagUp = EventAntiScaleFactor("TCHPT_L","MisTagUp");
  TCHPT_LAntiMisTagDown = EventAntiScaleFactor("TCHPT_L","MisTagDown");


  //  TCHP_LAntiMisTagDown = EventAntiScaleFactor("TCHP_L","MisTagDown");

  TCHPM_B = EventScaleFactor("TCHPM_B","noSyst");
  TCHPM_C = EventScaleFactor("TCHPM_C","noSyst");
  TCHPM_L = EventScaleFactor("TCHPM_L","noSyst");
    
  
  TCHPM_BBTagUp = EventScaleFactor("TCHPM_B","BTagUp");
  TCHPM_BBTagDown = EventScaleFactor("TCHPM_B","BTagDown");
  TCHPM_CBTagUp = EventScaleFactor("TCHPM_C","BTagUp");
  TCHPM_CBTagDown = EventScaleFactor("TCHPM_C","BTagDown");
  TCHPM_LMisTagUp = EventScaleFactor("TCHPM_L","MisTagUp");
  TCHPM_LMisTagDown = EventScaleFactor("TCHPM_L","MisTagDown");
    

  TCHPM_BAnti = EventAntiScaleFactor("TCHPM_B","noSyst");
  TCHPM_CAnti = EventAntiScaleFactor("TCHPM_C","noSyst");
  TCHPM_LAnti = EventAntiScaleFactor("TCHPM_L","noSyst");

  TCHPM_BAntiBTagUp = EventAntiScaleFactor("TCHPM_B","BTagUp");
  TCHPM_BAntiBTagDown = EventAntiScaleFactor("TCHPM_B","BTagDown");
  TCHPM_CAntiBTagUp = EventAntiScaleFactor("TCHPM_C","BTagUp");
  TCHPM_CAntiBTagDown = EventAntiScaleFactor("TCHPM_C","BTagDown");
  TCHPM_LAntiMisTagUp = EventAntiScaleFactor("TCHPM_L","MisTagUp");
  TCHPM_LAntiMisTagDown = EventAntiScaleFactor("TCHPM_L","MisTagDown");

  /////

  TCHEL_B = EventScaleFactor("TCHEL_B","noSyst");
  TCHEL_C = EventScaleFactor("TCHEL_C","noSyst");
  TCHEL_L = EventScaleFactor("TCHEL_L","noSyst");
    
  TCHEL_BBTagUp = EventScaleFactor("TCHEL_B","BTagUp");
  TCHEL_BBTagDown = EventScaleFactor("TCHEL_B","BTagDown");
  TCHEL_CBTagUp = EventScaleFactor("TCHEL_C","BTagUp");
  TCHEL_CBTagDown = EventScaleFactor("TCHEL_C","BTagDown");
  TCHEL_LMisTagUp = EventScaleFactor("TCHEL_L","MisTagUp");
  TCHEL_LMisTagDown = EventScaleFactor("TCHEL_L","MisTagDown");

  TCHEL_BAnti = EventAntiScaleFactor("TCHEL_B","noSyst");
  TCHEL_CAnti = EventAntiScaleFactor("TCHEL_C","noSyst");
  TCHEL_LAnti = EventAntiScaleFactor("TCHEL_L","noSyst");
   
  TCHEL_BAntiBTagUp = EventAntiScaleFactor("TCHEL_B","BTagUp");
  TCHEL_BAntiBTagDown = EventAntiScaleFactor("TCHEL_B","BTagDown");
  TCHEL_CAntiBTagUp = EventAntiScaleFactor("TCHEL_C","BTagUp");
  TCHEL_CAntiBTagDown = EventAntiScaleFactor("TCHEL_C","BTagDown");
  TCHEL_LAntiMisTagUp = EventAntiScaleFactor("TCHEL_L","MisTagUp");
  TCHEL_LAntiMisTagDown = EventAntiScaleFactor("TCHEL_L","MisTagDown");
}

double SingleTopSystematicsJetsDumper::SFMap(string algo ){
  if(algo == "TCHPT_B")return 0.89;
  if(algo == "TCHPT_C")return 0.89;
  if(algo == "TCHPT_L")return 1.17;

  if(algo == "TCHPM_B")return 0.91;
  if(algo == "TCHPM_C")return 0.91;
  if(algo == "TCHPM_L")return 0.91;

  if(algo == "TCHEL_B")return 0.95;
  if(algo == "TCHEL_C")return 0.95;
  if(algo == "TCHEL_L")return 1.11;


  return 0.9;
}

double SingleTopSystematicsJetsDumper::SFErrMap(string algo ){
  if(algo == "TCHPT_B")return 0.092;
  if(algo == "TCHPT_C")return 0.092;
  if(algo == "TCHPT_L")return 0.18;

  if(algo == "TCHPM_B")return 0.10;
  if(algo == "TCHPM_C")return 0.10;
  if(algo == "TCHPM_L")return 0.11;

  if(algo == "TCHEL_B")return 0.10;
  if(algo == "TCHEL_C")return 0.10;
  if(algo == "TCHEL_L")return 0.11;

  return 0.1;
}

double SingleTopSystematicsJetsDumper::EFFMap(string algo ){
  if(algo == "TCHPT_B")return 0.365;
  if(algo == "TCHPT_C")return 0.365;
  if(algo == "TCHPT_L")return 0.0017;

  if(algo == "TCHEL_B")return 0.765;
  if(algo == "TCHEL_C")return 0.765;
  if(algo == "TCHEL_L")return 0.13;

  if(algo == "TCHPM_B")return 0.48;
  if(algo == "TCHPM_C")return 0.48;
  if(algo == "TCHPM_L")return 0.0177;

  return 0.36;
}



double SingleTopSystematicsJetsDumper::EFFErrMap(string algo ){
  if(algo == "TCHPT_B")return 0.05;
  if(algo == "TCHPT_C")return 0.05;
  if(algo == "TCHPT_L")return 0.0004;

  if(algo == "TCHEL_B")return 0.05;
  if(algo == "TCHEL_C")return 0.05;
  if(algo == "TCHEL_L")return 0.03;

  if(algo == "TCHEL_B")return 0.05;
  if(algo == "TCHEL_C")return 0.05;
  if(algo == "TCHEL_L")return 0.004;

  return 0.05;
}
double SingleTopSystematicsJetsDumper::EventScaleFactor(string algo,string syst_name){//,double sf, double eff, double sferr){

  //  double mistagcentral = sf;  
  //double mistagerr = sferr;
  //double tcheeff = eff;

  double mistagcentral = SFMap(algo);  
  double mistagerr = SFErrMap(algo);
  double tcheeff = EFFMap(algo);

  
  if(syst_name == "MisTagUp" || syst_name == "BTagUp"){
    return mistagcentral+mistagerr;
  }

  if(syst_name == "MisTagDown" || syst_name == "BTagDown"){
    return mistagcentral-mistagerr;
  }

  return mistagcentral;
}

//EventAntiScaleFactor

double SingleTopSystematicsJetsDumper::EventAntiScaleFactor(string algo,string syst_name ){
  //,double sf, double eff, double sferr){

  
  //double mistagcentral = sf;  
  //double mistagerr = sferr;
  //double tcheeff = eff;

  double mistagcentral = SFMap(algo);  
  double mistagerr = SFErrMap(algo);
  double tcheeff = EFFMap(algo);

  
  if(syst_name == "MisTagUp" || syst_name == "BTagUp"){
    return (1-tcheeff)/(1-tcheeff/(mistagcentral+mistagerr));
  }
  
  if(syst_name == "MisTagDown" || syst_name == "BTagDown"){
    return (1-tcheeff)/(1-tcheeff/(mistagcentral-mistagerr));
    
  }

  return (1-tcheeff)/(1-tcheeff/(mistagcentral));
  
}


//MisTag veto weight as function of jet flavour, systematics and scale factors: 
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS 
double SingleTopSystematicsJetsDumper::AntiMisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr){
  double mistagcentral = sf;  
  double mistagerr = sferr;
  double tcheeff = eff;
  double tchpeff =eff;
  
  if(syst_name == "MisTagUp"){
    if(algo == "TCHP_L"){
      return (1-tchpeff)/(1-tchpeff/(mistagcentral+mistagerr));
      }
    if(algo == "TCHE_L"){
      return (1-tcheeff)/(1-tcheeff/(mistagcentral+mistagerr));
    }
    
  }
  
  if(syst_name == "MisTagDown"){
    if(algo == "TCHP_L"){
      return (1-tchpeff)/(1-tchpeff/(mistagcentral-mistagerr));
    }
    if(algo == "TCHE_L"){
      return (1-tcheeff)/(1-tcheeff/(mistagcentral-mistagerr));
    }
  }

  if(algo == "TCHP_L"){
    return (1-tchpeff)/(1-tchpeff/(mistagcentral));
  }
  if(algo == "TCHE_L"){
    return (1-tcheeff)/(1-tcheeff/(mistagcentral));
  }
  
  return 0.9;


}


double SingleTopSystematicsJetsDumper::turnOnWeight (std::vector<double> probabilities, int njets_req =1){
  double prob =0;
  for(unsigned int i=0; i<pow(2,probabilities.size());++i){
    //at least njets_req objects for trigger required
    int ntrigobj=0;
    for(unsigned int j=0; j<probabilities.size();++j){
      if((int)(i/pow(2,j))%2) ntrigobj++;
    }
    if(ntrigobj<njets_req) continue;  
    double newprob=1;
    for(unsigned int j=0; j<probabilities.size();++j){
      if((int)(i/pow(2,j))%2) newprob*=probabilities[j];
      else newprob*=1-probabilities[j];
    }
    prob+=newprob;
  }
  return prob;
}


bool SingleTopSystematicsJetsDumper::flavourFilter(string ch, int nb, int nc, int nl){
  
  if(ch == "WJets_wbb" || ch == "ZJets_wbb") return (nb>0 );
  if(ch == "WJets_wcc" || ch == "ZJets_wcc") return (nb==0 && nc>0);
  if(ch == "WJets_wlight" || ch == "ZJets_wlight") return (nb==0 && nc==0);
   
  return true;
}

/*double SingleTopSystematicsJetsDumper::jetprob(double pt, double btag){
  double prob=0.993*(exp(-51.0*exp(-0.160*pt)));
  prob*=0.902*exp((-5.995*exp(-0.604*btag)));
  return prob;
  }*/

double SingleTopSystematicsJetsDumper::jetprob(double pt, double btag){
  double prob=0.982*exp(-30.6*exp(-0.151*pt));//PT turnOn
  prob*=0.844*exp((-6.72*exp(-0.720*btag)));//BTag turnOn
  return prob;
}


double SingleTopSystematicsJetsDumper::jetprobpt(double pt){
  double prob=0.982*exp(-30.6*exp(-0.151*pt));//PT turnOn
  return prob;
}

double SingleTopSystematicsJetsDumper::jetprobbtag(double btag){
  double prob =0.844*exp((-6.72*exp(-0.720*btag)));//BTag turnOn
  return prob;
}

double SingleTopSystematicsJetsDumper::turnOnProbs(string syst, int n){
  if(syst=="JetTrig1Up"){
    return turnOnWeight(jetprobs_j1up,1)
    ;  } 
  else if (syst=="JetTrig2Up"){
    return turnOnWeight(jetprobs_j2up,1)
    ;  }
  else if (syst=="JetTrig3Up"){
    return turnOnWeight(jetprobs_j3up,1)
    ;  }

  if(syst=="JetTrig1Down"){
    return turnOnWeight(jetprobs_j1down,1)
    ;  } 
  else if (syst=="JetTrig2Down"){
    return turnOnWeight(jetprobs_j2down,1)
    ;  }
  else if (syst=="JetTrig3Down"){
    return turnOnWeight(jetprobs_j3down,1)
    ;  }

  if(syst=="BTagTrig1Up"){
    return turnOnWeight(jetprobs_b1up,1)
    ;  } 
  else if (syst=="BTagTrig2Up"){
    return turnOnWeight(jetprobs_b2up,1)
    ;  }
  else if (syst=="BTagTrig3Up"){
    return turnOnWeight(jetprobs_b3up,1)
    ;  }

  if(syst=="BTagTrig1Down"){
    return turnOnWeight(jetprobs_b1down,1)
    ;  } 
  else if (syst=="BTagTrig2Down"){
    return turnOnWeight(jetprobs_b2down,1)
    ;  }
  else if (syst=="BTagTrig3Down"){
    return turnOnWeight(jetprobs_b3down,1)
    ;  }

  return turnOnWeight(jetprobs,1);


}

void SingleTopSystematicsJetsDumper::pushJetProbs(double pt, double btag, double eta){

jetprobs.push_back(jetprob(pt,btag,eta,"noSyst"));

jetprobs_j1up.push_back(jetprob(pt,btag,eta,"JetTrig1Up"));
jetprobs_j1down.push_back(jetprob(pt,btag,eta,"JetTrig1Down"));

jetprobs_j2up.push_back(jetprob(pt,btag,eta,"JetTrig2Up"));
jetprobs_j2down.push_back(jetprob(pt,btag,eta,"JetTrig2Down"));

jetprobs_j3up.push_back(jetprob(pt,btag,eta,"JetTrig3Up"));
jetprobs_j3down.push_back(jetprob(pt,btag,eta,"JetTrig3Down"));


jetprobs_b1up.push_back(jetprob(pt,btag,eta,"BTagTrig1Up"));
jetprobs_b1down.push_back(jetprob(pt,btag,eta,"BTagTrig1Down"));

jetprobs_b2up.push_back(jetprob(pt,btag,eta,"BTagTrig2Up"));
jetprobs_b2down.push_back(jetprob(pt,btag,eta,"BTagTrig2Down"));

jetprobs_b3up.push_back(jetprob(pt,btag,eta,"BTagTrig3Up"));
jetprobs_b3down.push_back(jetprob(pt,btag,eta,"BTagTrig3Down"));




}

void SingleTopSystematicsJetsDumper::InitializeTurnOnReWeight(string rootFile = "CentralJet30BTagIP_2ndSF_mu.root"){
  
  TFile f("CentralJet30BTagIP_2ndSF_mu.root");
  TH2D *histSF = dynamic_cast<TH2D *>(f.Get("ScaleFactor"));
  
  histoSFs = *histSF;
  

  //  for 
  //  recorrection_weights[7][7];

  //  float pt_bin_extremes[8];
  //float tchpt_bin_extremes[8];

  ;}

double SingleTopSystematicsJetsDumper::turnOnReWeight (double preWeight, double pt, double tchpt){
  cout << "reweight pt"<<  pt << " tchpt "<<tchpt << " sf " ; 
  cout << histoSFs.GetBinContent(histoSFs.FindFixBin(pt,tchpt))<<endl;

  return histoSFs.GetBinContent(histoSFs.FindFixBin(pt,tchpt));
  //  return 1;//preWeight;
}


double SingleTopSystematicsJetsDumper::jetprob(double pt, double btag, double eta, string syst){
  double prob=1.;

  if (fabs(eta)>2.6) return 0.;
  //PT turnOn
  if(syst=="JetTrig1Up"){

    if(eta<-1.4)prob = 0.981*exp(-37.49*exp(-0.158*pt));
    if(eta>-1.4&&eta<0)prob = 0.982*exp(-27.51*exp(-0.146*pt));
    if(eta<1.4&&eta>0)prob =0.982*exp(-26.63*exp(-0.145*pt));
    if(eta>1.4)prob =0.984*exp(-42.17*exp(-0.158*pt));
    ;  } 
  else if (syst=="JetTrig2Up"){
    if(eta<-1.4)prob =0.982*exp(-41.17*exp(-0.161*pt));
    if(eta>-1.4&&eta<0)prob =0.983*exp(-27.03*exp(-0.147*pt));
    if(eta<1.4&&eta>0)prob =0.983*exp(-26.18*exp(-0.146*pt));
    if(eta>1.4)prob =0.986*exp(-45.11*exp(-0.161*pt));
    ;  }
  else if (syst=="JetTrig3Up"){
    if(eta<-1.4)prob =0.981*exp(-41.17*exp(-0.162*pt));
    if(eta>-1.4&&eta<0)prob =0.982*exp(-27.03*exp(-0.146*pt));
    if(eta<1.4&&eta>0)prob =0.982*exp(-26.18*exp(-0.146*pt));
    if(eta>1.4)prob =0.985*exp(-45.11*exp(-0.161*pt));

    prob=0.982*exp(-30.6*exp(-0.151*pt));
    ;  }
  else if(syst=="JetTrig1Down"){
    if(eta<-1.4)prob = 0.981*exp(-44.84*exp(-0.164*pt));
    if(eta>-1.4&&eta<0)prob =0.982*exp(-26.56*exp(-0.147*pt));
    if(eta<1.4&&eta>0)prob =0.983*exp(-25.72*exp(-0.147*pt));
    if(eta>1.4)prob =0.985*exp(-48.05*exp(-0.164*pt))
      ;  } 
  else if (syst=="JetTrig2Down"){
    if(eta<-1.4)prob = 0.98*exp(-41.17*exp(-0.161*pt));
    if(eta>-1.4&&eta<0)prob = 0.982*exp(-27.03*exp(-0.147*pt));
    if(eta<1.4&&eta>0)prob = 0.982*exp(-26.18*exp(-0.146*pt));
    if(eta>1.4)prob = 0.984*exp(-45.11*exp(-0.161*pt));

    ;  }
  else if (syst=="JetTrig3Down"){
    if(eta<-1.4)prob =0.981*exp(-41.17*exp(-0.161*pt));
    if(eta>-1.4&&eta<0)prob =0.982*exp(-27.03*exp(-0.147*pt));
    if(eta<1.4&&eta>0)prob =0.982*exp(-26.18*exp(-0.146*pt));
    if(eta>1.4)prob =0.985*exp(-45.11*exp(-0.16*pt));

    ;  }
  else prob=0.982*exp(-30.6*exp(-0.151*pt));
 
  //BTag turnOn
  if(syst=="BTagTrig1Up"){
    prob*=0.85*exp(-6.35*exp(-0.681*btag));  }
  else if(syst=="BTagTrig1Down"){
  prob*= 0.839*exp(-7.1*exp(-0.759*btag));  } 
  else if (syst=="BTagTrig2Up"){
    prob*= 0.824*exp(-6.72*exp(-0.733*btag));  }
  else if (syst=="BTagTrig2Down"){
     prob*= 0.865*exp(-6.73*exp(-0.707*btag));  }
  else if (syst=="BTagTrig3Up"){
    prob*=0.838*exp(-6.73*exp(-0.71*btag));  }
  else if (syst=="BTagTrig3Down"){
      prob*=0.851*exp(-6.72*exp(-0.73*btag));  }
  else prob*=0.844*exp((-6.72*exp(-0.720*btag)));
  
  return prob;

}

double SingleTopSystematicsJetsDumper::bTagSF(int B){
  //  cout<< " B " << " ntchhpt "<<   ntchpt_tags << " jsfshpt size "<<
  //  jsfshpt.size() << " ntchel " << ntchel_tags<< " jsfshel size " << jsfshel.size()<<endl;

  if (B==0 || B==3){
    return b_tchpt_0_tags.weight(jsfshpt,ntchpt_tags)*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
  }
  if (B==1 || B==4){
    return b_tchpt_1_tag.weight(jsfshpt,ntchpt_tags);
  }
  if (B==2 || B==5){
    return b_tchpt_2_tags.weight(jsfshpt,ntchpt_tags);
  }
  return 1.;
}

double SingleTopSystematicsJetsDumper::bTagSF(int B, string syst){
  //  cout<< " B " << " ntchhpt "<<   ntchpt_tags << " jsfshpt size "<<
  // jsfshpt.size() << " ntchel " << ntchel_tags<< " jsfshel size " << jsfshel.size()<<endl;

  if (B==0 || B==3){
    if(syst == "BTagUp")    return b_tchpt_0_tags.weight(jsfshpt_b_tag_up,ntchpt_tags)*b_tchel_0_tags.weight(jsfshel_b_tag_up,ntchel_tags);
    if(syst == "BTagDown")    return b_tchpt_0_tags.weight(jsfshpt_b_tag_down,ntchpt_tags)*b_tchel_0_tags.weight(jsfshel_b_tag_down,ntchel_tags);
    if(syst == "MisTagUp")    return b_tchpt_0_tags.weight(jsfshpt_mis_tag_up,ntchpt_tags)*b_tchel_0_tags.weight(jsfshel_mis_tag_up,ntchel_tags);
    if(syst == "MisTagDown")    return b_tchpt_0_tags.weight(jsfshpt_mis_tag_down,ntchpt_tags)*b_tchel_0_tags.weight(jsfshel_mis_tag_down,ntchel_tags);
    return b_tchpt_0_tags.weight(jsfshpt,ntchpt_tags)*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
  }
  if (B==1 || B==4){

    if(syst == "BTagUp")    return b_tchpt_1_tag.weight(jsfshpt_b_tag_up,ntchpt_tags);
    if(syst == "BTagDown")    return b_tchpt_1_tag.weight(jsfshpt_b_tag_down,ntchpt_tags);
    if(syst == "MisTagUp")    return b_tchpt_1_tag.weight(jsfshpt_mis_tag_up,ntchpt_tags);
    if(syst == "MisTagDown")    return b_tchpt_1_tag.weight(jsfshpt_mis_tag_down,ntchpt_tags);

    return b_tchpt_1_tag.weight(jsfshpt,ntchpt_tags);
  }
  if (B==2 || B==5){

    if(syst == "BTagUp")    return b_tchpt_2_tags.weight(jsfshpt_b_tag_up,ntchpt_tags);
    if(syst == "BTagDown")    return b_tchpt_2_tags.weight(jsfshpt_b_tag_down,ntchpt_tags);
    if(syst == "MisTagUp")    return b_tchpt_2_tags.weight(jsfshpt_mis_tag_up,ntchpt_tags);
    if(syst == "MisTagDown")    return b_tchpt_2_tags.weight(jsfshpt_mis_tag_down,ntchpt_tags);

    return b_tchpt_2_tags.weight(jsfshpt,ntchpt_tags);
  }
  return 1.;
}


double SingleTopSystematicsJetsDumper::pileUpSF(string syst){

  if(syst=="PUUp" )return LumiWeightsUp_.weight3D( *nm1,*n0,*np1);
  if(syst=="PUDown" )return LumiWeightsDown_.weight3D( *nm1,*n0,*np1);
  return LumiWeights_.weight3D( *nm1,*n0,*np1);
  

  
}

double SingleTopSystematicsJetsDumper::resolSF(double eta,string syst){
  double fac = 0.;
  if(syst== "JERUp")fac=1.;
  if(syst== "JERDown")fac=-1.;
  if(eta<=0.5) return 0.05+0.06*fac;
  else if( eta>0.5 && eta<=1.1 ) return 0.06+0.06*fac;
  else if( eta>1.1 && eta<=1.7 ) return 0.1+0.06*fac;
  else if( eta>1.7 && eta<=2.3 ) return 0.13+0.1*fac;
  else if( eta>2.3 && eta<=5. ) return 0.29+0.2*fac;
  return 0.1;
}


//BTag weighter
bool SingleTopSystematicsJetsDumper::BTagWeight::filter(int t)
{
  return (t >= minTags && t <= maxTags);
}

float SingleTopSystematicsJetsDumper::BTagWeight::weight(vector<JetInfo> jets, int tags)
{
  if(!filter(tags))
    {
      //   std::cout << "nThis event should not pass the selection, what is it doing here?" << std::endl;
      return 0;
    }
  int njets=jets.size();
  int comb= 1 << njets;
  float pMC=0;
  float pData=0;
  for(int i=0;i < comb; i++)
    {
      float mc=1.;
      float data=1.;
      int ntagged=0;
      for(int j=0;j<njets;j++)
	{
	  bool tagged = ((i >> j) & 0x1) == 1;
	  if(tagged) 
	    {
	      ntagged++;
	      mc*=jets[j].eff;
	      data*=jets[j].eff*jets[j].sf;
	    }
	  else
	    {
	      mc*=(1.-jets[j].eff);
	      data*=(1.-jets[j].eff*jets[j].sf);
	    }
	}       
   
      if(filter(ntagged))
	{
	  //  std::cout << mc << " " << data << endl;
	  pMC+=mc;
	  pData+=data;
	}
    }

  if(pMC==0) return 0; 
  return pData/pMC;
}

void SingleTopSystematicsJetsDumper::resetWeightsDoubles(){
  /*  cout << "start doubles removal...";

  for(int bj = 0; bj<=5;++bj){
    for (size_t j = 0; j < systematics.size();++j){
      string syst = systematics[j];
	
      trees[bj][syst]->Branch("weightDoubles",&miscWeightTree);
      int nentries =  trees[bj][syst]->GetEntries();
	
      if(bj==1|| bj==4){
	
	int idtmp, runtmp; 
	map<long int,int> ids;
	
	for (int i =0; i< nentries;++i){
	  trees[bj][syst]->GetEntry(i);
	  idtmp = eventTree;
	  runtmp = runTree;
	  stringstream s,s2;
	  s<<idtmp ;
	  s2<<runtmp;
	  string ss = s.str();
	  string ss2 = s2.str();
	  string cond = "eventid == "+ss;
	  miscWeightTree= 1.;
	  if (channel == "Data") cond = "eventid=="+ss +"&& runid == "+ss2  ;
	  //cout << "entries " << trees[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  << " weight"<< miscWeightTree<< endl;
	  if(trees[bj][syst]->GetEntries(cond.c_str())>1){
	    ids[idtmp]+=1;
	    if(ids[idtmp]>1)miscWeightTree=0;
	    //	cout << " found cond "<<endl;
	  }
	  //cout << "entries after" << trees[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  << " weight"<< miscWeightTree<< endl;
	  trees[bj][syst]->GetBranch("weightDoubles")->Fill();
	  //      cout << cond << endl;
	  //     cout << "entries " << trees[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  <<endl;
	}
      }
      else{
	for (int i =0; i< nentries;++i){
	  trees[bj][syst]->GetEntry(i);
	  miscWeightTree = 1.;
	  trees[bj][syst]->GetBranch("weightDoubles")->Fill();
	}
	
      }
    }
  }
  */;
}


//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopSystematicsJetsDumper);
