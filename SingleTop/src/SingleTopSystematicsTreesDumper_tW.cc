/*
*\Author:  O.Iorio
*
*
*
*\version  $Id: SingleTopSystematicsTreesDumper_tW.cc,v 1.1.2.6 2013/07/05 17:54:20 dnoonan Exp $
*/
// This analyzer dumps the histograms for all systematics listed in the cfg file
//
//
//

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopSystematicsTreesDumper_tW.h"
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



#include "../interface/ReWeighting.h"

namespace LHAPDF
{
void initPDFSet(int nset, const std::string &filename, int member = 0);
int numberPDF(int nset);
void usePDFMember(int nset, int member);
double xfx(int nset, double x, double Q, int fl);
double getXmin(int nset, int member);
double getXmax(int nset, int member);
double getQ2min(int nset, int member);
double getQ2max(int nset, int member);
void extrapolate(bool extrapolate = true);
}

SingleTopSystematicsTreesDumper_tW::SingleTopSystematicsTreesDumper_tW(const edm::ParameterSet &iConfig)
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
    finalLumiA = channelInfo.getUntrackedParameter<double>("finalLumiA");
    finalLumiB = channelInfo.getUntrackedParameter<double>("finalLumiB");
    finalLumiC = channelInfo.getUntrackedParameter<double>("finalLumiC");
    finalLumiD = channelInfo.getUntrackedParameter<double>("finalLumiD");

    //  dataPUFile_ =  iConfig.getUntrackedParameter< std::string >("dataPUFile","pileUpDistr.root");
    //  mcPUFile_ =  iConfig.getUntrackedParameter< std::string >("mcPUFile","pileupdistr_TChannel.root");

    //Electrons
    electronsPt_ =  iConfig.getParameter< edm::InputTag >("electronsPt");
    electronsPhi_ =  iConfig.getParameter< edm::InputTag >("electronsPhi");
    electronsEta_ =  iConfig.getParameter< edm::InputTag >("electronsEta");
    electronsEnergy_ =  iConfig.getParameter< edm::InputTag >("electronsEnergy");
    electronsCharge_ =  iConfig.getParameter< edm::InputTag >("electronsCharge");
    electronsDB_ =  iConfig.getParameter< edm::InputTag >("electronsDB");
    electronsDZ_ =  iConfig.getParameter< edm::InputTag >("electronsDZ");
    electronsDXY_ =  iConfig.getParameter< edm::InputTag >("electronsDXY");
    electronsMVAID_ =  iConfig.getParameter< edm::InputTag >("electronsMVAID");
    electronsMVAIDNonTrig_ =  iConfig.getParameter< edm::InputTag >("electronsMVAIDNonTrig");
    electronsRelIso_ =  iConfig.getParameter< edm::InputTag >("electronsRelIso");
    electronsDeltaCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("electronsDeltaCorrectedRelIso");
    electronsRhoCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("electronsRhoCorrectedRelIso");
    electronsEleId70cIso_ =  iConfig.getParameter< edm::InputTag >("electronsEleId70cIso");
    electronsEleId80cIso_ =  iConfig.getParameter< edm::InputTag >("electronsEleId80cIso");
    electronsEleId90cIso_ =  iConfig.getParameter< edm::InputTag >("electronsEleId90cIso");
    electronsEleId95cIso_ =  iConfig.getParameter< edm::InputTag >("electronsEleId95cIso");
    electronsTrackerExpectedInnerHits_ =  iConfig.getParameter< edm::InputTag >("electronsTrackerExpectedInnerHits");
    electronsSuperClusterEta_ =  iConfig.getParameter< edm::InputTag >("electronsSuperClusterEta");
    electronsECALPt_ =  iConfig.getParameter< edm::InputTag >("electronsECALPt");
    electronsChargedHadronIso_ =  iConfig.getParameter< edm::InputTag >("electronsChargedHadronIso");
    electronsPUChargedHadronIso_ =  iConfig.getParameter< edm::InputTag >("electronsPUChargedHadronIso");
    electronsNeutralHadronIso_ =  iConfig.getParameter< edm::InputTag >("electronsNeutralHadronIso");
    electronsPhotonIso_ =  iConfig.getParameter< edm::InputTag >("electronsPhotonIso");
    electronsPassConversionVeto_ =  iConfig.getParameter< edm::InputTag >("electronsPassConversionVeto");

    electronsGenPDGId_ =  iConfig.getParameter< edm::InputTag >("electronsGenPDGId");
    electronsHasBParent_ =  iConfig.getParameter< edm::InputTag >("electronsHasBParent");
    electronsHasTParent_ =  iConfig.getParameter< edm::InputTag >("electronsHasTParent");
    electronsHasZParent_ =  iConfig.getParameter< edm::InputTag >("electronsHasZParent");
    electronsHasWParent_ =  iConfig.getParameter< edm::InputTag >("electronsHasWParent");
    electronsHasHParent_ =  iConfig.getParameter< edm::InputTag >("electronsHasHParent");


    //Muons
    muonsPt_ =  iConfig.getParameter< edm::InputTag >("muonsPt");
    muonsPhi_ =  iConfig.getParameter< edm::InputTag >("muonsPhi");
    muonsEta_ =  iConfig.getParameter< edm::InputTag >("muonsEta");
    muonsEnergy_ =  iConfig.getParameter< edm::InputTag >("muonsEnergy");
    muonsCharge_ =  iConfig.getParameter< edm::InputTag >("muonsCharge");
    muonsDB_ =  iConfig.getParameter< edm::InputTag >("muonsDB");
    muonsDZ_ =  iConfig.getParameter< edm::InputTag >("muonsDZ");
    muonsDXY_ =  iConfig.getParameter< edm::InputTag >("muonsDXY");
    muonsRelIso_ =  iConfig.getParameter< edm::InputTag >("muonsRelIso");
    muonsDeltaCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("muonsDeltaCorrectedRelIso");
    muonsRhoCorrectedRelIso_ =  iConfig.getParameter< edm::InputTag >("muonsRhoCorrectedRelIso");
    muonsChargedHadronIso_ =  iConfig.getParameter< edm::InputTag >("muonsChargedHadronIso");
    muonsPUChargedHadronIso_ =  iConfig.getParameter< edm::InputTag >("muonsPUChargedHadronIso");
    muonsNeutralHadronIso_ =  iConfig.getParameter< edm::InputTag >("muonsNeutralHadronIso");
    muonsPhotonIso_ =  iConfig.getParameter< edm::InputTag >("muonsPhotonIso");
    muonsSumChargedHadronPtR03_ = iConfig.getParameter< edm::InputTag >("muonsSumChargedHadronPtR03");
    muonsSumChargedParticlePtR03_ = iConfig.getParameter< edm::InputTag >("muonsSumChargedParticlePtR03");
    muonsSumNeutralHadronEtR03_ = iConfig.getParameter< edm::InputTag >("muonsSumNeutralHadronEtR03");
    muonsSumPhotonEtR03_ = iConfig.getParameter< edm::InputTag >("muonsSumPhotonEtR03");
    muonsSumNeutralHadronEtHighThresholdR03_ = iConfig.getParameter< edm::InputTag >("muonsSumNeutralHadronEtHighThresholdR03");
    muonsSumPhotonEtHighThresholdR03_ = iConfig.getParameter< edm::InputTag >("muonsSumPhotonEtHighThresholdR03");
    muonsSumPUPtR03_ = iConfig.getParameter< edm::InputTag >("muonsSumPUPtR03");
    muonsSumChargedHadronPtR04_ = iConfig.getParameter< edm::InputTag >("muonsSumChargedHadronPtR04");
    muonsSumChargedParticlePtR04_ = iConfig.getParameter< edm::InputTag >("muonsSumChargedParticlePtR04");
    muonsSumNeutralHadronEtR04_ = iConfig.getParameter< edm::InputTag >("muonsSumNeutralHadronEtR04");
    muonsSumPhotonEtR04_ = iConfig.getParameter< edm::InputTag >("muonsSumPhotonEtR04");
    muonsSumNeutralHadronEtHighThresholdR04_ = iConfig.getParameter< edm::InputTag >("muonsSumNeutralHadronEtHighThresholdR04");
    muonsSumPhotonEtHighThresholdR04_ = iConfig.getParameter< edm::InputTag >("muonsSumPhotonEtHighThresholdR04");
    muonsSumPUPtR04_ = iConfig.getParameter< edm::InputTag >("muonsSumPUPtR04");

    muonsGenPDGId_ =  iConfig.getParameter< edm::InputTag >("muonsGenPDGId");
    muonsHasBParent_ =  iConfig.getParameter< edm::InputTag >("muonsHasBParent");
    muonsHasTParent_ =  iConfig.getParameter< edm::InputTag >("muonsHasTParent");
    muonsHasZParent_ =  iConfig.getParameter< edm::InputTag >("muonsHasZParent");
    muonsHasWParent_ =  iConfig.getParameter< edm::InputTag >("muonsHasWParent");
    muonsHasHParent_ =  iConfig.getParameter< edm::InputTag >("muonsHasHParent");


    //Vertices
    vertexX_ = iConfig.getParameter< edm::InputTag >("vertexX");//,"PileUpSync");
    vertexY_ = iConfig.getParameter< edm::InputTag >("vertexY");//,"PileUpSync");
    vertexZ_ = iConfig.getParameter< edm::InputTag >("vertexZ");//,"PileUpSync");
    vertexrho_ = iConfig.getParameter< edm::InputTag >("vertexrho");//,"PileUpSync");
    vertexchi_ = iConfig.getParameter< edm::InputTag >("vertexchi");//,"PileUpSync");
    vertexNDOF_ = iConfig.getParameter< edm::InputTag >("vertexNDOF");//,"PileUpSync");
    vertexIsFake_ = iConfig.getParameter< edm::InputTag >("vertexIsFake");//,"PileUpSync");

    //Jets
    jetsPt_ =  iConfig.getParameter< edm::InputTag >("jetsPt");
    jetsPhi_ =  iConfig.getParameter< edm::InputTag >("jetsPhi");
    jetsEta_ =  iConfig.getParameter< edm::InputTag >("jetsEta");
    jetsEnergy_ =  iConfig.getParameter< edm::InputTag >("jetsEnergy");
    jetsCSV_ =  iConfig.getParameter< edm::InputTag >("jetsCSV");
    jetsTCHP_ =  iConfig.getParameter< edm::InputTag >("jetsTCHP");
    jetsRMS_ =  iConfig.getParameter< edm::InputTag >("jetsRMS");
    jetsNumDaughters_ = iConfig.getParameter< edm::InputTag >("jetsNumDaughters");
    jetsCHEmEn_ = iConfig.getParameter< edm::InputTag >("jetsCHEmEn");
    jetsCHHadEn_ = iConfig.getParameter< edm::InputTag >("jetsCHHadEn");
    jetsCHMult_ = iConfig.getParameter< edm::InputTag >("jetsCHMult");
    jetsNeuEmEn_ = iConfig.getParameter< edm::InputTag >("jetsNeuEmEn");
    jetsNeuHadEn_ = iConfig.getParameter< edm::InputTag >("jetsNeuHadEn");
    jetsNeuMult_ = iConfig.getParameter< edm::InputTag >("jetsNeuMult");
    jetsPUChargedDiscr_ =  iConfig.getParameter< edm::InputTag >("jetsPUChargedDiscr");
    jetsPUChargedWP_ =  iConfig.getParameter< edm::InputTag >("jetsPUChargedWP");
    jetsPUFullDiscr_ =  iConfig.getParameter< edm::InputTag >("jetsPUFullDiscr");
    jetsPUFullWP_ =  iConfig.getParameter< edm::InputTag >("jetsPUFullWP");
    jetsBeta_ =  iConfig.getParameter< edm::InputTag >("jetsBeta");
    jetsBetaStar_ =  iConfig.getParameter< edm::InputTag >("jetsBetaStar");
    jetsFlavour_ =  iConfig.getParameter< edm::InputTag >("jetsFlavour");
    jetsDZ_ =  iConfig.getParameter< edm::InputTag >("jetsDZ");

    genjetsPt_ =  iConfig.getParameter< edm::InputTag >("genjetsPt");
    genjetsEta_ =  iConfig.getParameter< edm::InputTag >("genjetsEta");
    
    jetsGenPDGId_ =  iConfig.getParameter< edm::InputTag >("jetsGenPDGId");
    jetsHasBParent_ =  iConfig.getParameter< edm::InputTag >("jetsHasBParent");
    jetsHasTParent_ =  iConfig.getParameter< edm::InputTag >("jetsHasTParent");
    jetsHasZParent_ =  iConfig.getParameter< edm::InputTag >("jetsHasZParent");
    jetsHasWParent_ =  iConfig.getParameter< edm::InputTag >("jetsHasWParent");
    jetsHasHParent_ =  iConfig.getParameter< edm::InputTag >("jetsHasHParent");
    
    genPartPt_ = iConfig.getParameter< edm::InputTag >("genPartPt");
    genPartPdgId_ = iConfig.getParameter< edm::InputTag >("genPartPdgId");

    ktJetsForIsoRho_ =  iConfig.getParameter< edm::InputTag >("ktJetsForIsoRho");

    METPhi_ =  iConfig.getParameter< edm::InputTag >("METPhi");
    METPt_ =  iConfig.getParameter< edm::InputTag >("METPt");
    UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
    UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");

    doQCD_  =  iConfig.getUntrackedParameter< bool >("doQCD", true);

    doPDF_  =  iConfig.getUntrackedParameter< bool >("doPDF", true);

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
    

    doPU_ = iConfig.getUntrackedParameter< bool >("doPU", false);
    doResol_ = iConfig.getUntrackedParameter< bool >("doResol", false);
    doTurnOn_ = iConfig.getUntrackedParameter< bool >("doTurnOn", true);
    doGen_ = iConfig.getUntrackedParameter< bool >("doGen", true);

    doReCorrection_ = iConfig.getUntrackedParameter< bool >("doReCorrection", false);
    dataPUFile_ =  channelInfo.getUntrackedParameter< std::string >("Season", "SummerMean11");
    
    PUFileNew_ =  channelInfo.getUntrackedParameter< std::string >("PUFileNew", "pileUpDistrNewWJets");
    
    takeBTagSFFromDB_ = iConfig.getUntrackedParameter< bool >("takeBTagSFFromDB", true);

    algo_ = iConfig.getUntrackedParameter< std::string >("algo", "CSVT");
    doLooseBJetVeto_ = iConfig.getUntrackedParameter< bool >("doLooseBJetVeto", false);

    string season = "Summer11";
    season = dataPUFile_;
    //  TString season = "Fall11";
    string distr = "pileUpDistr" + season + ".root";
    if (doPU_)
    {
        //    //cout << " before lumIweightse "<<endl;
      LumiWeightsA_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012A_Jan22ReReco.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsB_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012B_Jan22ReReco.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsC_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012C_Jan22ReReco.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsD_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012D_Jan22ReReco.root",
					   std::string("pileup"),
					   std::string("pileup"));
      

      LumiWeightsAUp_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012A_Jan22ReReco_Up.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsBUp_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012B_Jan22ReReco_Up.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsCUp_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012C_Jan22ReReco_Up.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsDUp_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012D_Jan22ReReco_Up.root",
					   std::string("pileup"),
					   std::string("pileup"));
      

      LumiWeightsADown_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012A_Jan22ReReco_Down.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsBDown_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012B_Jan22ReReco_Down.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsCDown_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012C_Jan22ReReco_Down.root",
					   std::string("pileup"),
					   std::string("pileup"));
      LumiWeightsDDown_ = edm::LumiReWeighting("PileUpHistos/pileup_MC_Summer12.root",
					   "PileUpHistos/run2012D_Jan22ReReco_Down.root",
					   std::string("pileup"),
					   std::string("pileup"));
      
    }
    
    


    Service<TFileService> fs;


    bTagThreshold = 3.41;
    facBTagErr = 1.5;

    systematics.insert(systematics.begin(), "noSyst");

    //  for(size_t i = 0; i < systematics.size();++i){
    //  if(systematics.at(i)=="")
    //}

    std::vector<std::string> all_syst = systematics;


    //TFileDirectory SingleTopSystematics = fs->mkdir( "systematics_histograms" );
    TFileDirectory SingleTopTrees = fs->mkdir( "systematics_trees" );


    for (size_t i = 0; i < rate_systematics.size(); ++i)
    {
      //      all_syst.push_back(rate_systematics.at(i));
    }


    for (size_t i = 0; i < all_syst.size(); ++i)
    {


        string syst = all_syst[i];

	string treename = (channel +"_"+ syst);
// 	cout << "-----------------------------------------------------" << endl;
// 	cout << "-----------------------------------------------------" << endl;
// 	cout << "-----------------------------------------------------" << endl;
// 	cout << "-----------------------------------------------------" << endl;
// 	cout << "-----------------------------------------------------" << endl;
// 	cout << "-----------------------------------------------------" << endl;
// 	cout << "-----------------------------------------------------" << endl;

// 	cout << treename << endl << endl << endl;

	trees[syst] = new TTree(treename.c_str(), treename.c_str());

	trees[syst]->Branch("muonPt", &_muonPt_);
	trees[syst]->Branch("muonEta", &_muonEta_);
	trees[syst]->Branch("muonPhi", &_muonPhi_);
	trees[syst]->Branch("muonE", &_muonEnergy_);
	trees[syst]->Branch("muonCharge", &_muonCharge_);
	trees[syst]->Branch("muonRelIso", &_muonRelIso_);
	trees[syst]->Branch("muonRhoCorrectedRelIso", &_muonRhoCorrectedRelIso_);
	trees[syst]->Branch("muonDeltaCorrectedRelIso", &_muonDeltaCorrectedRelIso_);
	trees[syst]->Branch("muonPVDz", &_muonPVDz_);
	trees[syst]->Branch("muonPVDxy", &_muonPVDxy_);
	trees[syst]->Branch("muonDB", &_muonDB_);
	trees[syst]->Branch("muonChargedHadronIso", &_muonChargedHadronIso_);
	trees[syst]->Branch("muonPUChargedHadronIso", &_muonPUChargedHadronIso_);
	trees[syst]->Branch("muonNeutralHadronIso", &_muonNeutralHadronIso_);
	trees[syst]->Branch("muonPhotonIso", &_muonPhotonIso_);
	trees[syst]->Branch("muonSumChargedHadronPtR03", &_muonSumChargedHadronPtR03_);
	trees[syst]->Branch("muonSumChargedParticlePtR03", &_muonSumChargedParticlePtR03_);
	trees[syst]->Branch("muonSumNeutralHadronEtR03", &_muonSumNeutralHadronEtR03_);
	trees[syst]->Branch("muonSumPhotonEtR03", &_muonSumPhotonEtR03_);
	trees[syst]->Branch("muonSumNeutralHadronEtHighThresholdR03", &_muonSumNeutralHadronEtHighThresholdR03_);
	trees[syst]->Branch("muonSumPhotonEtHighThresholdR03", &_muonSumPhotonEtHighThresholdR03_);
	trees[syst]->Branch("muonSumPUPtR03", &_muonSumPUPtR03_);
	trees[syst]->Branch("muonSumChargedHadronPtR04", &_muonSumChargedHadronPtR04_);
	trees[syst]->Branch("muonSumChargedParticlePtR04", &_muonSumChargedParticlePtR04_);
	trees[syst]->Branch("muonSumNeutralHadronEtR04", &_muonSumNeutralHadronEtR04_);
	trees[syst]->Branch("muonSumPhotonEtR04", &_muonSumPhotonEtR04_);
	trees[syst]->Branch("muonSumNeutralHadronEtHighThresholdR04", &_muonSumNeutralHadronEtHighThresholdR04_);
	trees[syst]->Branch("muonSumPhotonEtHighThresholdR04", &_muonSumPhotonEtHighThresholdR04_);
	trees[syst]->Branch("muonSumPUPtR04", &_muonSumPUPtR04_);
	

	trees[syst]->Branch("muonGenPDGId" 	,&_muonGenPDGId_   );
	trees[syst]->Branch("muonHasBParent" 	,&_muonHasBParent_   );
	trees[syst]->Branch("muonHasTParent" 	,&_muonHasTParent_   );
	trees[syst]->Branch("muonHasZParent" 	,&_muonHasZParent_   );
	trees[syst]->Branch("muonHasWParent" 	,&_muonHasWParent_   );
	trees[syst]->Branch("muonHasHParent" 	,&_muonHasHParent_   );


	trees[syst]->Branch("electronPt", &_electronPt_);
	trees[syst]->Branch("electronEta", &_electronEta_);
	trees[syst]->Branch("electronPhi", &_electronPhi_);
	trees[syst]->Branch("electronE", &_electronEnergy_);
	trees[syst]->Branch("electronCharge", &_electronCharge_);
	trees[syst]->Branch("electronRelIso", &_electronRelIso_);
	trees[syst]->Branch("electronRhoCorrectedRelIso", &_electronRhoCorrectedRelIso_);
	trees[syst]->Branch("electronDeltaCorrectedRelIso", &_electronDeltaCorrectedRelIso_);
	trees[syst]->Branch("electronPVDz", &_electronPVDz_);
	trees[syst]->Branch("electronPVDxy", &_electronPVDxy_);
	trees[syst]->Branch("electronDB", &_electronDB_);
	trees[syst]->Branch("electronMVATrigV0", &_electronMVAID_);
	trees[syst]->Branch("electronMVANonTrigV0", &_electronMVAIDNonTrig_);
	trees[syst]->Branch("electronEleId70cIso", &_electronEleId70cIso_);
	trees[syst]->Branch("electronEleId80cIso", &_electronEleId80cIso_);
	trees[syst]->Branch("electronEleId90cIso", &_electronEleId90cIso_);
	trees[syst]->Branch("electronEleId95cIso", &_electronEleId95cIso_);
	trees[syst]->Branch("electronTrackerExpectedInnerHits", &_electronTrackerExpectedInnerHits_);
	trees[syst]->Branch("electronSuperClusterEta", &_electronSuperClusterEta_);
	trees[syst]->Branch("electronECALPt", &_electronECALPt_);
	trees[syst]->Branch("electronChargedHadronIso", &_electronChargedHadronIso_);
	trees[syst]->Branch("electronPUChargedHadronIso", &_electronPUChargedHadronIso_);
	trees[syst]->Branch("electronNeutralHadronIso", &_electronNeutralHadronIso_);
	trees[syst]->Branch("electronPhotonIso", &_electronPhotonIso_);
	trees[syst]->Branch("electronPassConversionVeto", &_electronPassConversionVeto_);

	trees[syst]->Branch("electronGenPDGId"  	,&_electronGenPDGId_   );
	trees[syst]->Branch("electronHasBParent" 	,&_electronHasBParent_   );
	trees[syst]->Branch("electronHasTParent" 	,&_electronHasTParent_   );
	trees[syst]->Branch("electronHasZParent" 	,&_electronHasZParent_   );
	trees[syst]->Branch("electronHasWParent" 	,&_electronHasWParent_   );
	trees[syst]->Branch("electronHasHParent" 	,&_electronHasHParent_   );

	trees[syst]->Branch("jetPt", &_jetPt_);
	trees[syst]->Branch("jetEta", &_jetEta_);
	trees[syst]->Branch("jetPhi", &_jetPhi_);
	trees[syst]->Branch("jetE", &_jetEnergy_);
	trees[syst]->Branch("jetNumDaughters", &_jetNumDaughters_);
	trees[syst]->Branch("jetCHEmEn", &_jetCHEmEn_);
	trees[syst]->Branch("jetCHHadEn", &_jetCHHadEn_);
	trees[syst]->Branch("jetCHMult", &_jetCHMult_);
	trees[syst]->Branch("jetNeuEmEn", &_jetNeuEmEn_);
	trees[syst]->Branch("jetNeuHadEn", &_jetNeuHadEn_);
	trees[syst]->Branch("jetNeuMult", &_jetNeuMult_);
	trees[syst]->Branch("jetCSV", &_jetCSV_);
	trees[syst]->Branch("jetTCHP", &_jetTCHP_);
	trees[syst]->Branch("jetRMS", &_jetRMS_);
	trees[syst]->Branch("jetPUChargedDiscr", &_jetPUChargedDiscr_);
	trees[syst]->Branch("jetPUChargedWP", &_jetPUChargedWP_);
	trees[syst]->Branch("jetPUFullDiscr", &_jetPUFullDiscr_);
	trees[syst]->Branch("jetPUFullWP", &_jetPUFullWP_);
	trees[syst]->Branch("jetBeta", &_jetBeta_);
	trees[syst]->Branch("jetBetaStar", &_jetBetaStar_);
	trees[syst]->Branch("jetFlavour", &_jetFlavour_);
	trees[syst]->Branch("jetDZ", &_jetDZ_);
	trees[syst]->Branch("jetUncorrPt", &_jetUncorrPt_);


	trees[syst]->Branch("genjetPt", &_genjetPt_);
	trees[syst]->Branch("genjetEta", &_genjetEta_);

	trees[syst]->Branch("jetGenPDGId" 	,&_jetGenPDGId_   );
	trees[syst]->Branch("jetHasBParent" 	,&_jetHasBParent_   );
	trees[syst]->Branch("jetHasTParent" 	,&_jetHasTParent_   );
	trees[syst]->Branch("jetHasZParent" 	,&_jetHasZParent_   );
	trees[syst]->Branch("jetHasWParent" 	,&_jetHasWParent_   );
	trees[syst]->Branch("jetHasHParent" 	,&_jetHasHParent_   );

	trees[syst]->Branch("ktJetsForIsoRho", &_ktJetsForIsoRho_);

	trees[syst]->Branch("MetPhi", &_MetPhi_);
	trees[syst]->Branch("MetPt", &_MetPt_);
	trees[syst]->Branch("UncorrMetPt", &_UncorrMetPt_);
	trees[syst]->Branch("UnclMETPx", &_UnclMETPx_);
	trees[syst]->Branch("UnclMETPy", &_UnclMETPy_);

	trees[syst]->Branch("vertexX", &_vertexX_);
	trees[syst]->Branch("vertexY", &_vertexY_);
	trees[syst]->Branch("vertexZ", &_vertexZ_);
	trees[syst]->Branch("vertexrho", &_vertexrho_);
	trees[syst]->Branch("vertexchi", &_vertexchi_);
	trees[syst]->Branch("vertexNDOF", &_vertexNDOF_);
	trees[syst]->Branch("vertexIsFake", &_vertexIsFake_);

	trees[syst]->Branch("runNum", &_runNum_);
	trees[syst]->Branch("lumiNum", &_lumiNum_);
	trees[syst]->Branch("eventNum", &_eventNum_);
	trees[syst]->Branch("weightA", &_weightA_);
	trees[syst]->Branch("weightB", &_weightB_);
	trees[syst]->Branch("weightC", &_weightC_);
	trees[syst]->Branch("weightD", &_weightD_);
	trees[syst]->Branch("PUWeightA", &_PUWeightA_);
	trees[syst]->Branch("PUWeightB", &_PUWeightB_);
	trees[syst]->Branch("PUWeightC", &_PUWeightC_);
	trees[syst]->Branch("PUWeightD", &_PUWeightD_);
	//	trees[syst]->Branch("PUWeightNew", &_PUWeightNew_);
	trees[syst]->Branch("TopPtweight", &_TopPtweight_);
	trees[syst]->Branch("scalePDF", &_scalePDF_);
	trees[syst]->Branch("PDF_x1", &_PDF_x1_);
	trees[syst]->Branch("PDF_x2", &_PDF_x2_);
	trees[syst]->Branch("PDF_id1", &_PDF_id1_);
	trees[syst]->Branch("PDF_id2", &_PDF_id2_);
	trees[syst]->Branch("PDF_weights", &_PDF_weights_);
	trees[syst]->Branch("PDF_weights_alternate_set_1", &pdf_weights_alternate_set_1);
	trees[syst]->Branch("PDF_weights_alternate_set_2", &pdf_weights_alternate_set_2);



    }

    passingLepton = 0;
    passingMuonVeto = 0;
    passingLeptonVeto = 0;
    passingJets = 0;
    passingBJets = 0;
    passingMET = 0;

    //TCHPT
    b_tchpt_0_tags = BTagWeight(0, 0);
    b_tchpt_1_tag = BTagWeight(1, 1);
    b_tchpt_2_tags = BTagWeight(2, 2);
    //CSVT
    b_csvt_0_tags = BTagWeight(0, 0);
    b_csvt_1_tag = BTagWeight(1, 1);
    b_csvt_2_tags = BTagWeight(2, 2);
    //CSVM
    b_csvm_0_tags = BTagWeight(0, 0);
    b_csvm_1_tag = BTagWeight(1, 1);
    b_csvm_2_tags = BTagWeight(2, 2);




    //  JEC_PATH = "CondFormats/JetMETObjects/data/";
    //  JEC_PATH = "./JECs/";
    //  fip = edm::FileInPath(JEC_PATH+"Spring10_Uncertainty_AK5PF.txt");
    //fip = edm::FileInPath(JEC_PATH+"GR_R_42_V19_AK5PF_Uncertainty.txt");
    //jecUnc = new JetCorrectionUncertainty(fip.fullPath());

    JEC_PATH = "./";


    //Latest JEC uncertainties from Dec 5
//     jecUnc  = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Fall12_V6_DATA_UncertaintySources_AK5PFchs.txt", "Total")));
//    jecUnc  = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Fall12_V6_DATA_UncertaintySources_AK5PFchs.txt", "Total")));

    jecUnc  = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Summer13_V5_DATA_UncertaintySources_AK5PFchs.txt", "Total")));

    jecUncCorrelationGroupInSitu            = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Summer13_V5_DATA_UncertaintySources_AK5PFchs.txt", "CorrelationGroupMPFInSitu")));
    jecUncCorrelationGroupFlavor            = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Summer13_V5_DATA_UncertaintySources_AK5PFchs.txt", "CorrelationGroupFlavor")));
    jecUncCorrelationGroupIntercalibration  = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Summer13_V5_DATA_UncertaintySources_AK5PFchs.txt", "CorrelationGroupIntercalibration")));
    jecUncCorrelationGroupUncorrelated      = new JetCorrectionUncertainty(*(new JetCorrectorParameters("Summer13_V5_DATA_UncertaintySources_AK5PFchs.txt", "CorrelationGroupUncorrelated")));

    JES_SW = 0.015;
    JES_b_cut = 0.02;
    JES_b_overCut = 0.03;


    //JetResolution part
    string fileResolName = "Spring10_PtResolution_AK5PF.txt";
    //    bool  doGaussianResol = false;
    //  ptResol = new JetResolution(fileResolName, doGaussianResol);

    leptonRelIsoQCDCutUpper = 0.9, leptonRelIsoQCDCutLower = 0.2;


    topMassMeas = 172.9;
    //  doReCorrection_= false;
    if (doReCorrection_) //FIXME CURRENTLY NOT WORKING!!!
    {
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

        //cout << "jec 2" << endl;
        // JetCorrectorParameters *L3JetParMC = new JetCorrectorParameters(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L3Absolute.txt");
        //JetCorrectorParameters *L2JetParMC = new JetCorrectorParameters(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L2Relative.txt");

        //  JetCorrectorParameters L1JetParMC(JEC_PATH+"JECs/STARTv17/START42_V17_AK5PF_L1FastJet.txt");
        //cout << "jec 3" << endl;
        //  vector<JetCorrectorParameters > vParTmp;

        //  vParMC.push_back(L1JetParMC);
        //vParTmp.push_back(L1JetParMC);
        //   vParMC->push_back(*L2JetParMC)

        //   vParMC->push_back(*L3JetParMC);

        //cout << "jec 4" << endl;

        //   JetCorrectorData = new FactorizedJetCorrector(*vParData);
        //   JetCorrectorMC  = new FactorizedJetCorrector( vParTmp);
    }
    InitializeEventScaleFactorMap();
    InitializeTurnOnReWeight("CentralJet30BTagIP_2ndSF_mu.root");

    LHAPDF::initPDFSet(1, "cteq66.LHgrid"); //This is the one listed on the TopRefSyst twiki
    //    LHAPDF::initPDFSet(1, "CT10.LHgrid");  //This is the one Orso had 
    LHAPDF::initPDFSet(2, "MSTW2008nlo68cl.LHgrid");
    LHAPDF::initPDFSet(3, "MSTW2008nlo68cl.LHgrid");
    //   LHAPDF::initPDFSet(3, "NNPDF21_100.LHgrid");


    //  //cout<< "I work for now but I do nothing. But again, if you gotta do nothing, you better do it right. To prove my good will I will provide you with somse numbers later."<<endl;
    isFirstEvent = true;
}

void SingleTopSystematicsTreesDumper_tW::initBranchVars()
{
#define INT_NAN 9999
#define FLOAT_NAN 9999.0
#define DOUBLE_NAN 9999.0

    _muonPt_.clear();
    _muonEta_.clear();
    _muonPhi_.clear();
    _muonEnergy_.clear();
    _muonCharge_.clear();
    _muonRelIso_.clear();
    _muonRhoCorrectedRelIso_.clear();
    _muonDeltaCorrectedRelIso_.clear();
    _muonPVDz_.clear();
    _muonPVDxy_.clear();
    _muonDB_.clear();
    _muonChargedHadronIso_.clear();
    _muonPUChargedHadronIso_.clear();
    _muonNeutralHadronIso_.clear();
    _muonPhotonIso_.clear();
    _muonSumChargedHadronPtR03_.clear();
    _muonSumChargedParticlePtR03_.clear();
    _muonSumNeutralHadronEtR03_.clear();
    _muonSumPhotonEtR03_.clear();
    _muonSumNeutralHadronEtHighThresholdR03_.clear();
    _muonSumPhotonEtHighThresholdR03_.clear();
    _muonSumPUPtR03_.clear();
    _muonSumChargedHadronPtR04_.clear();
    _muonSumChargedParticlePtR04_.clear();
    _muonSumNeutralHadronEtR04_.clear();
    _muonSumPhotonEtR04_.clear();
    _muonSumNeutralHadronEtHighThresholdR04_.clear();
    _muonSumPhotonEtHighThresholdR04_.clear();
    _muonSumPUPtR04_.clear();
    _muonGenPDGId_.clear();
    _muonHasBParent_.clear();
    _muonHasTParent_.clear();
    _muonHasZParent_.clear();
    _muonHasWParent_.clear();
    _muonHasHParent_.clear();
    
    _electronPt_.clear();
    _electronEta_.clear();
    _electronPhi_.clear();
    _electronEnergy_.clear();
    _electronCharge_.clear();
    _electronRelIso_.clear();
    _electronRhoCorrectedRelIso_.clear();
    _electronDeltaCorrectedRelIso_.clear();
    _electronPVDz_.clear();
    _electronPVDxy_.clear();
    _electronDB_.clear();
    _electronMVAID_.clear();
    _electronMVAIDNonTrig_.clear();
    _electronEleId70cIso_.clear();
    _electronEleId80cIso_.clear();
    _electronEleId90cIso_.clear();
    _electronEleId95cIso_.clear();
    _electronTrackerExpectedInnerHits_.clear();
    _electronSuperClusterEta_.clear();
    _electronECALPt_.clear();
    _electronChargedHadronIso_.clear();
    _electronPUChargedHadronIso_.clear();
    _electronNeutralHadronIso_.clear();
    _electronPhotonIso_.clear();
    _electronPassConversionVeto_.clear();
    
    _electronGenPDGId_.clear();
    _electronHasBParent_.clear();
    _electronHasTParent_.clear();
    _electronHasZParent_.clear();
    _electronHasWParent_.clear();
    _electronHasHParent_.clear();

    _jetPt_.clear();
    _jetEta_.clear();
    _jetPhi_.clear();
    _jetEnergy_.clear();
    _jetNumDaughters_.clear();
    _jetCHEmEn_.clear();
    _jetCHHadEn_.clear();
    _jetCHMult_.clear();
    _jetNeuEmEn_.clear();
    _jetNeuHadEn_.clear();
    _jetNeuMult_.clear();
    _jetCSV_.clear();
    _jetTCHP_.clear();
    _jetRMS_.clear();
    _jetPUChargedDiscr_.clear();
    _jetPUChargedWP_.clear();
    _jetPUFullDiscr_.clear();
    _jetPUFullWP_.clear();
    _jetBeta_.clear();
    _jetBetaStar_.clear();
    _jetFlavour_.clear();
    _jetDZ_.clear();
    _genjetPt_.clear();
    _genjetEta_.clear();
    _jetUncorrPt_.clear();

    _jetGenPDGId_.clear();
    _jetHasBParent_.clear();
    _jetHasTParent_.clear();
    _jetHasZParent_.clear();
    _jetHasWParent_.clear();
    _jetHasHParent_.clear();

    _ktJetsForIsoRho_ = DOUBLE_NAN;

    _MetPhi_ = DOUBLE_NAN;
    _MetPt_ = DOUBLE_NAN;
    _UncorrMetPt_ = DOUBLE_NAN;
    _UnclMETPx_ = DOUBLE_NAN;
    _UnclMETPy_ = DOUBLE_NAN;

    _vertexX_ = DOUBLE_NAN;
    _vertexY_ = DOUBLE_NAN;
    _vertexZ_ = DOUBLE_NAN;
    _vertexrho_ = DOUBLE_NAN;
    _vertexchi_ = DOUBLE_NAN;
    _vertexNDOF_ = DOUBLE_NAN;
    _vertexIsFake_ = false;

    _runNum_ = INT_NAN;
    _lumiNum_ = INT_NAN;
    _eventNum_ = INT_NAN;
    _weight_ = DOUBLE_NAN;
    _weightA_ = DOUBLE_NAN;
    _weightB_ = DOUBLE_NAN;
    _weightC_ = DOUBLE_NAN;
    _weightD_ = DOUBLE_NAN;
    _TopPtweight_ = DOUBLE_NAN;
    _scalePDF_ = DOUBLE_NAN;
    _PDF_x1_ = DOUBLE_NAN;
    _PDF_x2_ = DOUBLE_NAN;
    _PDF_id1_ = INT_NAN;
    _PDF_id2_ = INT_NAN;
    _PDF_weights_.clear();



    //ints
    chargeTree = INT_NAN;
    runTree = INT_NAN;
    lumiTree = INT_NAN;
    eventTree = INT_NAN;
    eventFlavourTree = INT_NAN;
    firstJetFlavourTree = INT_NAN;
    secondJetFlavourTree = INT_NAN;
    thirdJetFlavourTree = INT_NAN;
    nJ = INT_NAN;
    nJNoPU = INT_NAN;
    nJCentral = INT_NAN;
    nJCentralNoPU = INT_NAN;
    nJForward = INT_NAN;
    nJForwardNoPU = INT_NAN;
    nVertices = INT_NAN;
    npv = INT_NAN;
    ntchpt_tags = INT_NAN;
    ncsvt_tags = INT_NAN;
    ncsvm_tags = INT_NAN;

    //doubles
    weightTree = DOUBLE_NAN;
    w1TCHPT = DOUBLE_NAN;
    w2TCHPT = DOUBLE_NAN;
    w1CSVT = DOUBLE_NAN;
    w2CSVT = DOUBLE_NAN;
    w1CSVM = DOUBLE_NAN;
    w2CSVM = DOUBLE_NAN;
    PUWeightTree = DOUBLE_NAN;
    PUWeightTreeNew = DOUBLE_NAN;
    turnOnWeightTree = DOUBLE_NAN;
    turnOnReWeightTree = DOUBLE_NAN;
    lepPt = DOUBLE_NAN;
    lepEta = DOUBLE_NAN;
    lepPhi = DOUBLE_NAN;
    lepDeltaCorrectedRelIso = DOUBLE_NAN;
    lepRhoCorrectedRelIso = DOUBLE_NAN;
    lepEff = DOUBLE_NAN;
    mtwMassTree = DOUBLE_NAN;
    metPt = DOUBLE_NAN;
    firstJetPt = DOUBLE_NAN;
    firstJetEta = DOUBLE_NAN;
    firstJetPhi = DOUBLE_NAN;
    firstJetE = DOUBLE_NAN;
    secondJetPt = DOUBLE_NAN;
    secondJetEta = DOUBLE_NAN;
    secondJetPhi = DOUBLE_NAN;
    secondJetE = DOUBLE_NAN;
    thirdJetPt = DOUBLE_NAN;
    thirdJetEta = DOUBLE_NAN;
    thirdJetPhi = DOUBLE_NAN;
    thirdJetE = DOUBLE_NAN;
    bJetPt = DOUBLE_NAN;
    fJetPt = DOUBLE_NAN;
    bJetEta = DOUBLE_NAN;
    fJetEta = DOUBLE_NAN;
    fJetPUID = DOUBLE_NAN;
    fJetPUWP = DOUBLE_NAN;
    //58 lines

    etaTree = DOUBLE_NAN;
    cosTree = DOUBLE_NAN;
    cosBLTree = DOUBLE_NAN;
    mtwMassTree = DOUBLE_NAN;

    chargeTree = INT_NAN;
    runTree = INT_NAN;
    lumiTree = INT_NAN;
    eventTree = INT_NAN;

    weightTree = DOUBLE_NAN;

    fJetFlavourTree = INT_NAN;
    bJetFlavourTree = INT_NAN;
    eventFlavourTree = INT_NAN;
    nVertices = INT_NAN;
    npv = INT_NAN;
    firstJetFlavourTree = INT_NAN;
    secondJetFlavourTree = INT_NAN;
    thirdJetFlavourTree = INT_NAN;

    bWeightTreeBTagUp = DOUBLE_NAN;
    bWeightTreeBTagDown = DOUBLE_NAN;
    bWeightTreeMisTagUp = DOUBLE_NAN;
    bWeightTreeMisTagDown = DOUBLE_NAN;
    PUWeightTree = DOUBLE_NAN;
    PUWeightTreePUUp = DOUBLE_NAN;
    PUWeightTreePUDown = DOUBLE_NAN;
    turnOnWeightTree = DOUBLE_NAN;
    turnOnReWeightTree = DOUBLE_NAN;
    turnOnWeightTreeJetTrig1Up = DOUBLE_NAN;
    turnOnWeightTreeJetTrig1Down = DOUBLE_NAN;
    turnOnWeightTreeJetTrig2Up = DOUBLE_NAN;
    turnOnWeightTreeJetTrig2Down = DOUBLE_NAN;
    turnOnWeightTreeJetTrig3Up = DOUBLE_NAN;
    turnOnWeightTreeJetTrig3Down = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig1Up = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig1Down = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig2Up = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig2Down = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig3Up = DOUBLE_NAN;
    turnOnWeightTreeBTagTrig3Down = DOUBLE_NAN;
    lepPt = DOUBLE_NAN;
    lepEta = DOUBLE_NAN;
    lepPhi = DOUBLE_NAN;
    lepDeltaCorrectedRelIso = DOUBLE_NAN;
    lepRhoCorrectedRelIso = DOUBLE_NAN;
    lepEff = DOUBLE_NAN;
    lepEffB = DOUBLE_NAN;
    fJetPt = DOUBLE_NAN;
    fJetE = DOUBLE_NAN;
    fJetEta = DOUBLE_NAN;
    fJetPhi = DOUBLE_NAN;
    fJetBTag = DOUBLE_NAN;
    fJetPUID = DOUBLE_NAN;
    fJetPUWP = DOUBLE_NAN;
    bJetPt = DOUBLE_NAN;
    bJetE = DOUBLE_NAN;
    bJetEta = DOUBLE_NAN;
    bJetPhi = DOUBLE_NAN;
    bJetBTag = DOUBLE_NAN;
    bJetPUID = DOUBLE_NAN;
    bJetPUWP = DOUBLE_NAN;
    firstJetPt = DOUBLE_NAN;
    firstJetEta = DOUBLE_NAN;
    firstJetPhi = DOUBLE_NAN;
    firstJetE = DOUBLE_NAN;
    secondJetPt = DOUBLE_NAN;
    secondJetEta = DOUBLE_NAN;
    secondJetPhi = DOUBLE_NAN;
    secondJetE = DOUBLE_NAN;
    thirdJetPt = DOUBLE_NAN;
    thirdJetEta = DOUBLE_NAN;
    thirdJetPhi = DOUBLE_NAN;
    thirdJetE = DOUBLE_NAN;
    metPt = DOUBLE_NAN;
    metPhi = DOUBLE_NAN;
    topMassTree = DOUBLE_NAN;
    topMtwTree = DOUBLE_NAN;
    topPt = DOUBLE_NAN;
    topPhi = DOUBLE_NAN;
    topEta = DOUBLE_NAN;
    topE = DOUBLE_NAN;
    electronID = DOUBLE_NAN;
    totalEnergy = DOUBLE_NAN;
    totalMomentum = DOUBLE_NAN;
    lowBTagTree = DOUBLE_NAN;
    highBTagTree = DOUBLE_NAN;

    pdf_weights_alternate_set_1 = FLOAT_NAN;
    pdf_weights_alternate_set_2 = FLOAT_NAN;

}

void SingleTopSystematicsTreesDumper_tW::analyze(const Event &iEvent, const EventSetup &iSetup)
{

  //  if()
  //

    initBranchVars();

    //    cout << "GetByLabelSection" << endl;

    iEvent.getByLabel(muonsPt_, muonsPt);
    iEvent.getByLabel(muonsPhi_, muonsPhi);
    iEvent.getByLabel(muonsEta_, muonsEta);		 
    iEvent.getByLabel(muonsEnergy_,  muonsEnergy);		 
    iEvent.getByLabel(muonsCharge_,  muonsCharge);		 
    iEvent.getByLabel(muonsDB_,	  muonsDB);			 
    iEvent.getByLabel(muonsDZ_,	  muonsDZ);			 
    iEvent.getByLabel(muonsDXY_,  muonsDXY);		 
    iEvent.getByLabel(muonsRelIso_,  muonsRelIso);
    iEvent.getByLabel(muonsDeltaCorrectedRelIso_, muonsDeltaCorrectedRelIso);
    iEvent.getByLabel(muonsRhoCorrectedRelIso_,   muonsRhoCorrectedRelIso);;
    iEvent.getByLabel(muonsChargedHadronIso_, muonsChargedHadronIso);
    iEvent.getByLabel(muonsPUChargedHadronIso_, muonsPUChargedHadronIso);
    iEvent.getByLabel(muonsNeutralHadronIso_, muonsNeutralHadronIso);
    iEvent.getByLabel(muonsPhotonIso_, muonsPhotonIso);
    iEvent.getByLabel(muonsSumChargedHadronPtR03_, muonsSumChargedHadronPtR03);
    iEvent.getByLabel(muonsSumChargedParticlePtR03_, muonsSumChargedParticlePtR03);
    iEvent.getByLabel(muonsSumNeutralHadronEtR03_, muonsSumNeutralHadronEtR03);
    iEvent.getByLabel(muonsSumPhotonEtR03_, muonsSumPhotonEtR03);
    iEvent.getByLabel(muonsSumNeutralHadronEtHighThresholdR03_, muonsSumNeutralHadronEtHighThresholdR03);
    iEvent.getByLabel(muonsSumPhotonEtHighThresholdR03_, muonsSumPhotonEtHighThresholdR03);
    iEvent.getByLabel(muonsSumPUPtR03_, muonsSumPUPtR03);
    iEvent.getByLabel(muonsSumChargedHadronPtR04_, muonsSumChargedHadronPtR04);
    iEvent.getByLabel(muonsSumChargedParticlePtR04_, muonsSumChargedParticlePtR04);
    iEvent.getByLabel(muonsSumNeutralHadronEtR04_, muonsSumNeutralHadronEtR04);
    iEvent.getByLabel(muonsSumPhotonEtR04_, muonsSumPhotonEtR04);
    iEvent.getByLabel(muonsSumNeutralHadronEtHighThresholdR04_, muonsSumNeutralHadronEtHighThresholdR04);
    iEvent.getByLabel(muonsSumPhotonEtHighThresholdR04_, muonsSumPhotonEtHighThresholdR04);
    iEvent.getByLabel(muonsSumPUPtR04_, muonsSumPUPtR04);

    if (doGen_){
      iEvent.getByLabel(muonsGenPDGId_,  muonsGenPDGId);
      iEvent.getByLabel(muonsHasBParent_,  muonsHasBParent);
      iEvent.getByLabel(muonsHasTParent_,  muonsHasTParent);
      iEvent.getByLabel(muonsHasZParent_,  muonsHasZParent);
      iEvent.getByLabel(muonsHasWParent_,  muonsHasWParent);
      iEvent.getByLabel(muonsHasHParent_,  muonsHasHParent);
    }

    iEvent.getByLabel(electronsPt_, electronsPt);
    iEvent.getByLabel(electronsPhi_, electronsPhi);
    iEvent.getByLabel(electronsEta_, electronsEta);
    iEvent.getByLabel(electronsEnergy_, electronsEnergy);
    iEvent.getByLabel(electronsCharge_, electronsCharge);
    iEvent.getByLabel(electronsDB_, electronsDB);
    iEvent.getByLabel(electronsDZ_, electronsDZ);
    iEvent.getByLabel(electronsDXY_, electronsDXY);
    iEvent.getByLabel(electronsRelIso_, electronsRelIso);
    iEvent.getByLabel(electronsDeltaCorrectedRelIso_, electronsDeltaCorrectedRelIso);
    iEvent.getByLabel(electronsRhoCorrectedRelIso_, electronsRhoCorrectedRelIso);
    iEvent.getByLabel(electronsMVAID_, electronsMVAID);
    iEvent.getByLabel(electronsMVAIDNonTrig_, electronsMVAIDNonTrig);
    iEvent.getByLabel(electronsEleId70cIso_, electronsEleId70cIso);
    iEvent.getByLabel(electronsEleId80cIso_, electronsEleId80cIso);
    iEvent.getByLabel(electronsEleId90cIso_, electronsEleId90cIso);
    iEvent.getByLabel(electronsEleId95cIso_, electronsEleId95cIso);
    iEvent.getByLabel(electronsTrackerExpectedInnerHits_, electronsTrackerExpectedInnerHits);
    iEvent.getByLabel(electronsSuperClusterEta_, electronsSuperClusterEta);
    iEvent.getByLabel(electronsECALPt_, electronsECALPt);
    iEvent.getByLabel(electronsChargedHadronIso_, electronsChargedHadronIso);
    iEvent.getByLabel(electronsPUChargedHadronIso_, electronsPUChargedHadronIso);
    iEvent.getByLabel(electronsNeutralHadronIso_, electronsNeutralHadronIso);
    iEvent.getByLabel(electronsPhotonIso_, electronsPhotonIso);
    iEvent.getByLabel(electronsPassConversionVeto_, electronsPassConversionVeto);

    if (doGen_){
      iEvent.getByLabel(electronsGenPDGId_,    electronsGenPDGId);
      iEvent.getByLabel(electronsHasBParent_,  electronsHasBParent);
      iEvent.getByLabel(electronsHasTParent_,  electronsHasTParent);
      iEvent.getByLabel(electronsHasZParent_,  electronsHasZParent);
      iEvent.getByLabel(electronsHasWParent_,  electronsHasWParent);
      iEvent.getByLabel(electronsHasHParent_,  electronsHasHParent);
    }

    iEvent.getByLabel(vertexX_,vertexX);
    iEvent.getByLabel(vertexY_,vertexY);
    iEvent.getByLabel(vertexZ_,vertexZ);
    iEvent.getByLabel(vertexrho_,vertexrho);
    iEvent.getByLabel(vertexchi_,vertexchi);
    iEvent.getByLabel(vertexNDOF_,vertexNDOF);
    iEvent.getByLabel(vertexIsFake_,vertexIsFake);


    if (doGen_){
      iEvent.getByLabel(genPartPt_,genPartPt);
      iEvent.getByLabel(genPartPdgId_,genPartPdgId);
    }

    iEvent.getByLabel(jetsPt_,		   jetsPt);		  
    iEvent.getByLabel(jetsEta_,		   jetsEta);		  
    iEvent.getByLabel(jetsPhi_,		   jetsPhi);		  
    iEvent.getByLabel(jetsEnergy_,	   jetsEnergy);	  
    iEvent.getByLabel(jetsCSV_,		   jetsCSV);		  
    iEvent.getByLabel(jetsTCHP_,	   jetsTCHP);		  
    iEvent.getByLabel(jetsRMS_,		   jetsRMS);		  
    iEvent.getByLabel(jetsNumDaughters_,   jetsNumDaughters);	 
    iEvent.getByLabel(jetsCHEmEn_,	   jetsCHEmEn);	  
    iEvent.getByLabel(jetsCHHadEn_,	   jetsCHHadEn);	  
    iEvent.getByLabel(jetsCHMult_,	   jetsCHMult);	  
    iEvent.getByLabel(jetsNeuEmEn_,	   jetsNeuEmEn);	  
    iEvent.getByLabel(jetsNeuHadEn_,	   jetsNeuHadEn);	  
    iEvent.getByLabel(jetsNeuMult_,	   jetsNeuMult);	  
    iEvent.getByLabel(jetsPUChargedDiscr_, jetsPUChargedDiscr); 
    iEvent.getByLabel(jetsPUChargedWP_,	   jetsPUChargedWP);	  
    iEvent.getByLabel(jetsPUFullDiscr_,	   jetsPUFullDiscr);	  
    iEvent.getByLabel(jetsPUFullWP_,	   jetsPUFullWP);	  
    iEvent.getByLabel(jetsBeta_,	   jetsBeta);		  
    iEvent.getByLabel(jetsBetaStar_,	   jetsBetaStar);	  
    iEvent.getByLabel(jetsFlavour_,	   jetsFlavour);	  
    iEvent.getByLabel(jetsDZ_,             jetsDZ);

    if (doGen_){
      iEvent.getByLabel(jetsGenPDGId_,    jetsGenPDGId);
      iEvent.getByLabel(jetsHasBParent_,  jetsHasBParent);
      iEvent.getByLabel(jetsHasTParent_,  jetsHasTParent);
      iEvent.getByLabel(jetsHasZParent_,  jetsHasZParent);
      iEvent.getByLabel(jetsHasWParent_,  jetsHasWParent);
      iEvent.getByLabel(jetsHasHParent_,  jetsHasHParent);
    }

    if (doResol_)iEvent.getByLabel(genjetsPt_,	   genjetsPt);		  
    if (doResol_)iEvent.getByLabel(genjetsEta_,	   genjetsEta);		  

    iEvent.getByLabel(ktJetsForIsoRho_,	   ktJetsForIsoRho);

    iEvent.getByLabel(METPt_, METPt);
    iEvent.getByLabel(METPhi_, METPhi);
    iEvent.getByLabel(UnclMETPx_, UnclMETPx);
    iEvent.getByLabel(UnclMETPy_, UnclMETPy);


    if (doPU_){
      //  //cout << " before npv "<<endl;
      //iEvent.getByLabel(nm1_,nm1);
      iEvent.getByLabel(n0_, n0);
      //iEvent.getByLabel(np1_,np1);
      nVertices = *n0;

    }
    else(nVertices = -1);

    //if (jetsPt->size() > 25 && channel != "Data")return; //Crazy events with huge jet multiplicity in mc

    if (isFirstEvent && takeBTagSFFromDB_)
    {
        //cout <<  "isfirst " << endl;
        iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT", perfMHP);
        iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPM", perfMHPM);
        iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL", perfMHE);

        iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPM", perfBHPM);
        iSetup.get<BTagPerformanceRecord>().get("BTAGTCHPT", perfBHP);
        iSetup.get<BTagPerformanceRecord>().get("BTAGTCHEL", perfBHE);
        isFirstEvent = false;
    }
    //  iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
    // iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);

    //  //cout << "test 0 "<<endl;

    gotLeptons = 0;
    gotPV = 0;
    gotQCDLeptons = 0;
    gotLooseLeptons = 0;
    gotJets = 0;
    gotMets = 0;
    gotPU = 0;

    //cout <<" test 2 "<<endl;

    jsfshpt.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfshpt_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfshpt_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfshpt_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfshpt_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvt.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvt_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvt_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvt_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvt_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvm.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvm_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvm_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();

    jsfscsvm_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    jsfscsvm_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();


    //No second tagger: uncomment it to add one

    //  jsfshel.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_b_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_b_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_mis_tag_up.clear();//  bjs.clear();cjs.clear();ljs.clear();
    //jsfshel_mis_tag_down.clear();//  bjs.clear();cjs.clear();ljs.clear();


    double PUWeight = 1;
    double PUWeightA = 1;
    double PUWeightB = 1;
    double PUWeightC = 1;
    double PUWeightD = 1;
    double PUWeightNoSyst = 1;
    //    double bWeightNoSyst = 1;
    //    double turnOnWeightValueNoSyst = 1;
    //    double turnOnReWeightTreeNoSyst = 1;

    double PUWeightNew = 1;
    double PUWeightNewNoSyst = 1;

    BinningPointByMap measurePoint;

    float metPx = 0;
    float metPy = 0;

    _UncorrMetPt_ = METPt->at(0);   
    float OrigmetPx = METPt->at(0) * cos(METPhi->at(0));
    float OrigmetPy = METPt->at(0) * sin(METPhi->at(0));

//     size_t nLeptons = 0;//leptonsPt->size();
//     size_t nQCDLeptons = 0;//leptonsPt->size();
//     size_t nJets = 0;
//     size_t nJetsNoPU = 0;
//     size_t nJetsCentralNoPU = 0;
//     size_t nJetsCentral = 0;
//     size_t nJetsForwardNoPU = 0;
//     size_t nJetsForward = 0;
    //    size_t nJetsNoSyst = 0;
    //    size_t nBJets = 0;
    //    size_t nLooseBJets = 0;
    //  size_t nAntiBJets = 0;


    double WeightLumiA = finalLumiA * crossSection / originalEvents;
    double WeightLumiB = finalLumiB * crossSection / originalEvents;
    double WeightLumiC = finalLumiC * crossSection / originalEvents;
    double WeightLumiD = finalLumiD * crossSection / originalEvents;

    //double Weight = 1;
    //double MTWValue = 0;
    //    double MTWValueQCD = 0;
    //    double RelIsoQCDCut = 0.1;

    //    float ptCut = 40;

    //    double myWeight = 1.;

    //    bool didLeptonLoop = false;
    //    bool passesLeptonStep = false;
    //    bool isQCD = false;


    //    bool didJetLoop = false;

    if (channel == "Data"){
      WeightLumiA = 1;
      WeightLumiB = 1;
      WeightLumiC = 1;
      WeightLumiD = 1;
    }
//     int secondPtPosition = -1;
//     int thirdPtPosition = -1;

//     double secondPt = -1;
//     double thirdPt = -1;

//     int lowBTagTreePositionNoSyst = -1;
//     int highBTagTreePositionNoSyst = -1;
//     int maxPtTreePositionNoSyst = -1;
//     int minPtTreePositionNoSyst = -1;

    //    cout << "Get Objects Section" << endl;

    //    cout << "Muons" << endl;
    // Get Muons
    for(size_t i = 0; i < muonsPt->size(); i++){
      _muonPt_.push_back(muonsPt->at(i));
      _muonEta_.push_back(muonsEta->at(i));
      _muonPhi_.push_back(muonsPhi->at(i));
      _muonEnergy_.push_back(muonsEnergy->at(i));
      _muonCharge_.push_back(muonsCharge->at(i));
      _muonRelIso_.push_back(muonsRelIso->at(i));
      _muonDeltaCorrectedRelIso_.push_back(muonsDeltaCorrectedRelIso->at(i));
      _muonRhoCorrectedRelIso_.push_back(muonsRhoCorrectedRelIso->at(i));
      _muonDB_.push_back(muonsDB->at(i));
      _muonPVDz_.push_back(muonsDZ->at(i));
      _muonPVDxy_.push_back(muonsDXY->at(i));
      _muonChargedHadronIso_.push_back(muonsChargedHadronIso->at(i)); 
      _muonPUChargedHadronIso_.push_back(muonsPUChargedHadronIso->at(i)); 
      _muonNeutralHadronIso_.push_back(muonsNeutralHadronIso->at(i));
      _muonPhotonIso_.push_back(muonsPhotonIso->at(i));
      _muonSumChargedHadronPtR03_.push_back(muonsSumChargedHadronPtR03->at(i));
      _muonSumChargedParticlePtR03_.push_back(muonsSumChargedParticlePtR03->at(i));
      _muonSumNeutralHadronEtR03_.push_back(muonsSumNeutralHadronEtR03->at(i));
      _muonSumPhotonEtR03_.push_back(muonsSumPhotonEtR03->at(i));
      _muonSumNeutralHadronEtHighThresholdR03_.push_back(muonsSumNeutralHadronEtHighThresholdR03->at(i));
      _muonSumPhotonEtHighThresholdR03_.push_back(muonsSumPhotonEtHighThresholdR03->at(i));
      _muonSumPUPtR03_.push_back(muonsSumPUPtR03->at(i));
      _muonSumChargedHadronPtR04_.push_back(muonsSumChargedHadronPtR04->at(i));
      _muonSumChargedParticlePtR04_.push_back(muonsSumChargedParticlePtR04->at(i));
      _muonSumNeutralHadronEtR04_.push_back(muonsSumNeutralHadronEtR04->at(i));
      _muonSumPhotonEtR04_.push_back(muonsSumPhotonEtR04->at(i));
      _muonSumNeutralHadronEtHighThresholdR04_.push_back(muonsSumNeutralHadronEtHighThresholdR04->at(i));
      _muonSumPhotonEtHighThresholdR04_.push_back(muonsSumPhotonEtHighThresholdR04->at(i));
      _muonSumPUPtR04_.push_back(muonsSumPUPtR04->at(i));

      if (doGen_){
	_muonGenPDGId_.push_back(muonsGenPDGId->at(i));
	_muonHasBParent_.push_back(muonsHasBParent->at(i));
	_muonHasTParent_.push_back(muonsHasTParent->at(i));
	_muonHasZParent_.push_back(muonsHasZParent->at(i));
	_muonHasWParent_.push_back(muonsHasWParent->at(i));
	_muonHasHParent_.push_back(muonsHasHParent->at(i));
      }
    }

    //    cout << "Electrons" << endl;

    // Get Electrons
    for(size_t i = 0; i < electronsPt->size(); i++){
      _electronPt_.push_back(electronsPt->at(i));
      _electronEta_.push_back(electronsEta->at(i));
      _electronPhi_.push_back(electronsPhi->at(i));
      _electronEnergy_.push_back(electronsEnergy->at(i));
      _electronCharge_.push_back(electronsCharge->at(i));
      _electronRelIso_.push_back(electronsRelIso->at(i));
      _electronDeltaCorrectedRelIso_.push_back(electronsDeltaCorrectedRelIso->at(i));
      _electronRhoCorrectedRelIso_.push_back(electronsRhoCorrectedRelIso->at(i));
      _electronDB_.push_back(electronsDB->at(i));
      _electronPVDz_.push_back(electronsDZ->at(i));
      _electronPVDxy_.push_back(electronsDXY->at(i));
      _electronMVAID_.push_back(electronsMVAID->at(i));
      _electronMVAIDNonTrig_.push_back(electronsMVAIDNonTrig->at(i));
      _electronEleId70cIso_.push_back(electronsEleId70cIso->at(i));
      _electronEleId80cIso_.push_back(electronsEleId80cIso->at(i));
      _electronEleId90cIso_.push_back(electronsEleId90cIso->at(i));
      _electronEleId95cIso_.push_back(electronsEleId95cIso->at(i));
      _electronTrackerExpectedInnerHits_.push_back(electronsTrackerExpectedInnerHits->at(i));
      _electronSuperClusterEta_.push_back(electronsSuperClusterEta->at(i));
      _electronECALPt_.push_back(electronsECALPt->at(i)); 
      _electronChargedHadronIso_.push_back(electronsChargedHadronIso->at(i)); 
      _electronPUChargedHadronIso_.push_back(electronsPUChargedHadronIso->at(i)); 
      _electronNeutralHadronIso_.push_back(electronsNeutralHadronIso->at(i));
      _electronPhotonIso_.push_back(electronsPhotonIso->at(i));
      _electronPassConversionVeto_.push_back(electronsPassConversionVeto->at(i));

      if (doGen_){
	_electronGenPDGId_.push_back(electronsGenPDGId->at(i));
	_electronHasBParent_.push_back(electronsHasBParent->at(i));
	_electronHasTParent_.push_back(electronsHasTParent->at(i));
	_electronHasZParent_.push_back(electronsHasZParent->at(i));
	_electronHasWParent_.push_back(electronsHasWParent->at(i));
	_electronHasHParent_.push_back(electronsHasHParent->at(i));
      }
  }

    //    cout << "Jets" << endl;

    // Get Jets
    for (size_t i = 0; i < jetsPt->size(); i++){
      _jetEta_.push_back(jetsEta->at(i));
      _jetPhi_.push_back(jetsPhi->at(i));
      _jetNumDaughters_.push_back(jetsNumDaughters->at(i));
      _jetCHEmEn_.push_back(jetsCHEmEn->at(i));
      _jetCHHadEn_.push_back(jetsCHHadEn->at(i));
      _jetCHMult_.push_back(jetsCHMult->at(i));
      _jetNeuEmEn_.push_back(jetsNeuEmEn->at(i));
      _jetNeuHadEn_.push_back(jetsNeuHadEn->at(i));
      _jetNeuMult_.push_back(jetsNeuMult->at(i));
      _jetCSV_.push_back(jetsCSV->at(i));
      _jetTCHP_.push_back(jetsTCHP->at(i));
      _jetRMS_.push_back(jetsRMS->at(i));
      _jetPUChargedDiscr_.push_back(jetsPUChargedDiscr->at(i));
      _jetPUChargedWP_.push_back(jetsPUChargedWP->at(i));
      _jetPUFullDiscr_.push_back(jetsPUFullDiscr->at(i));
      _jetPUFullWP_.push_back(jetsPUFullWP->at(i));
      _jetBeta_.push_back(jetsBeta->at(i));
      _jetBetaStar_.push_back(jetsBetaStar->at(i));
      _jetFlavour_.push_back(jetsFlavour->at(i));
      _jetDZ_.push_back(jetsDZ->at(i));
      if (doResol_)_genjetPt_.push_back(genjetsPt->at(i));
      if (doResol_)_genjetEta_.push_back(genjetsEta->at(i));
      if (doGen_){
	_jetGenPDGId_.push_back(jetsGenPDGId->at(i));
	_jetHasBParent_.push_back(jetsHasBParent->at(i));
	_jetHasTParent_.push_back(jetsHasTParent->at(i));
	_jetHasZParent_.push_back(jetsHasZParent->at(i));
	_jetHasWParent_.push_back(jetsHasWParent->at(i));
	_jetHasHParent_.push_back(jetsHasHParent->at(i));
      }

    }

    _ktJetsForIsoRho_ = (*ktJetsForIsoRho);

    //    cout << "Other" << endl;
    
    // Get Vertex
    _vertexX_ = vertexX->at(0);
    _vertexY_ = vertexY->at(0);
    _vertexZ_ = vertexZ->at(0);
    _vertexrho_ = vertexrho->at(0);
    _vertexchi_ = vertexchi->at(0);
    _vertexNDOF_ = vertexNDOF->at(0);
    _vertexIsFake_ = vertexIsFake->at(0);

    // Get Event Info
    _runNum_ = iEvent.eventAuxiliary().run();
    _lumiNum_ = iEvent.eventAuxiliary().luminosityBlock();
    _eventNum_ = iEvent.eventAuxiliary().event();
    _weightA_ = WeightLumiA;
    _weightB_ = WeightLumiB;
    _weightC_ = WeightLumiC;
    _weightD_ = WeightLumiD;


    double ptTop = 0;
    double ptAntiTop = 0;

    if (doGen_){
      for (size_t i = 0; i < genPartPt->size(); i++){
	if (genPartPdgId->at(i) == 6)
	{
	  ptTop = genPartPt->at(i);
	}
	if (genPartPdgId->at(i) == -6)
	{
	  ptAntiTop = genPartPt->at(i);
	}
      }
    }

    //scale factor values from the top pt reweighting twiki for 8 TeV dilepton

    double a = 0.148;
    double b = -0.00129;

    if (ptTop == 0 || ptAntiTop == 0)
    {
      _TopPtweight_ = 1.;
    }
    else if (ptTop > 400 || ptAntiTop > 400)
    {
      _TopPtweight_ = 1.;
    }
    else
    {
      double sfTop = exp(a + b*ptTop);
      double sfAntiTop = exp(a + b*ptAntiTop);
      _TopPtweight_ = sqrt(sfTop * sfAntiTop);
    }


    //    cout << "Systematics Section" << endl;

    for (size_t s = 0; s < systematics.size(); ++s)
    {
      _jetPt_.clear();
      _jetUncorrPt_.clear();
      _jetEnergy_.clear();
      metPx = OrigmetPx;
      metPy = OrigmetPy;

      string syst_name =  systematics.at(s);
      string syst = syst_name;

      if (syst == "noSyst" && doPDF_ ){
	if (channel != "Data"){
	  iEvent.getByLabel(x1_, x1h);
	  iEvent.getByLabel(x2_, x2h);
	  
	  iEvent.getByLabel(scalePDF_, scalePDFh);
	  iEvent.getByLabel(id1_, id1h);
	  iEvent.getByLabel(id2_, id2h);
	  
	  x1 = *x1h;
	  x2 = *x2h;
	  
	  scalePDF = *scalePDFh;
	  
	  id1 = *id1h;
	  id2 = *id2h;
	  
	  //Q2 = x1 * x2 * 7000*7000;
	  LHAPDF::usePDFMember(1, 0);
	  double xpdf1 = LHAPDF::xfx(1, x1, scalePDF, id1);
	  double xpdf2 = LHAPDF::xfx(1, x2, scalePDF, id2);
	  double w0 = xpdf1 * xpdf2;
	  for (int p = 1; p <= 44; ++p) {
	    LHAPDF::usePDFMember(1, p);
	    double xpdf1_new = LHAPDF::xfx(1, x1, scalePDF, id1);
	    double xpdf2_new = LHAPDF::xfx(1, x2, scalePDF, id2);
	    double pweight = xpdf1_new * xpdf2_new / w0;
	    _PDF_weights_.push_back(pweight);
	  }
	  LHAPDF::usePDFMember(2, 0);
	  double xpdf1_new = LHAPDF::xfx(2, x1, scalePDF, id1);
	  double xpdf2_new = LHAPDF::xfx(2, x2, scalePDF, id2);
	  pdf_weights_alternate_set_1 = xpdf1_new * xpdf2_new / w0;
	  xpdf1_new = LHAPDF::xfx(3, x1, scalePDF, id1);
	  xpdf2_new = LHAPDF::xfx(3, x2, scalePDF, id2);
	  pdf_weights_alternate_set_2 = xpdf1_new * xpdf2_new / w0;
	  //    pdf_weights_alternate_set_1 =pweight1;
	  //    pdf_weights_alternate_set_2 =pweight2;
	
	}
      }

      
//         nLeptons = 0;
//         nQCDLeptons = 0;
//         nJets = 0;
//         nJetsNoPU = 0;
//         nJetsCentral = 0;
//         nJetsCentralNoPU = 0;
//         nJetsForward = 0;
//         nJetsForwardNoPU = 0;
        //    nBJets =0;
        //cout <<" syst " << syst << endl;
        //    nAntiBJets =0;

        //Here the weight of the event is the weight
        //to normalize the sample to the luminosity
        //required in the cfg
      //        Weight = WeightLumi;
        //    Weight *= PUWeight;

//         bool is_btag_relevant = ((syst_name == "noSyst" || syst_name == "BTagUp" || syst_name == "BTagDown"
//                                   || syst_name == "MisTagUp" || syst_name == "MisTagDown"
//                                   || syst_name == "JESUp" || syst_name == "JESDown"
//                                   || syst_name == "JERUp" || syst_name == "JERDown"
//                                  ) && channel != "Data"
//                                 );

	_UnclMETPx_ = (*UnclMETPx);
	_UnclMETPy_ = (*UnclMETPy);

        if (syst_name == "UnclusteredMETUp")
        {
	  metPx += (*UnclMETPx) * 0.1;
	  metPy += (*UnclMETPy) * 0.1;
        }
        if (syst_name == "UnclusteredMETDown")
        {
	  metPx -= (*UnclMETPx) * 0.1;
	  metPy -= (*UnclMETPy) * 0.1;
        }


        //Setup for systematics

        //This is done according to old b-tagging prescriptions

        //Here we have vectors of weights
        //to be associated with the
        //b-jets selection in the sample according to algorythm X:
        //a b-tag requirement implies a b_weight_tag_algoX,
        //a b-veto requirement implies a b_weight_antitag_algoX

        //TCHPT
        b_weight_tchpt_1_tag = 1;
        b_weight_tchpt_0_tags = 1;
        b_weight_tchpt_2_tags = 1;
        //CSVT
        b_weight_csvm_1_tag = 1;
        b_weight_csvm_0_tags = 1;
        b_weight_csvm_2_tags = 1;
        //CSVT
        b_weight_csvt_1_tag = 1;
        b_weight_csvt_0_tags = 1;
        b_weight_csvt_2_tags = 1;

        nb = 0;
        nc = 0;
        nudsg = 0;


        //Clear the vector of objects to be used in the selection

        //Define - initialize some variables
	//        MTWValue = 0;


        //position of lowest and highest b-tag used to chose the top candidate
	//        int lowBTagTreePosition = -1;
	//        lowBTagTree = 99999;

	//        int highBTagTreePosition = -1;
	//        highBTagTree = -9999;


	//        int maxPtTreePosition = -1;
	//        maxPtTree = -99999;

	//        int minPtTreePosition = -1;
	//        minPtTree = 99999;

//         secondPt = -1;
//         thirdPt = -1;
//         secondPtPosition = -1;
//         thirdPtPosition = -1;

        //Taking the unclustered met previously evaluated
        //and already present in the n-tuples
        //This is used for syst up and down



        //Define - initialize some variables
	//        float eta;
	//        float ptCorr;
	int flavour;
        double unc = 0;

        //Loops to apply systematics on jets-leptons


        //cout << " before leptons "<<endl;

        ntchpt_tags = 0;
        ncsvl_tags = 0;
        ncsvt_tags = 0;
        ncsvm_tags = 0;

        ntight_tags = 0;

        jsfshpt.clear();//  bjs.clear();cjs.clear();ljs.clear();
        jsfscsvt.clear();//  bjs.clear();cjs.clear();ljs.clear();
        jsfscsvm.clear();//  bjs.clear();cjs.clear();ljs.clear();
        //    jsfshel.clear();//  bjs.clear();cjs.clear();ljs.clear();

        //Clear the vectors of non-leptons
        //    jets.clear();
        //    bjets.clear();
        //    antibjets.clear();



        //  cout << " test 1 "<<endl;

        //cout << " before met "<<endl;

	//        bool hasTurnOnWeight = false;
	//        double turnOnWeightValue = 1;
        turnOnReWeightTree = 1;
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
	TVector2 met;
	TVector2 tmpjet;
	met.SetMagPhi(METPt->at(0), METPhi->at(0));

	for (size_t i = 0; i < jetsPt->size(); i++){
	  double ptCorr = jetsPt->at(i);
	  double energyCorr = jetsEnergy->at(i);
	  double eta = jetsEta->at(i);
	  flavour = jetsFlavour->at(i);
	  double genpt;
	  if (doResol_){
	    genpt = genjetsPt->at(i);
	    tmpjet.SetMagPhi(ptCorr,jetsPhi->at(i));
	    //	  cout << "MET " << met.Mod() << endl;
	    met += tmpjet;
	  }
	  
	  if (doResol_ && genpt > 15.0){
	    resolScale = resolSF(fabs(eta), syst_name);
	    double smear = std::max((double)(0.0), (double)(ptCorr + (ptCorr - genpt) * resolScale) / ptCorr);
// 	    metPx -= (jetsPt->at(i) * cos(jetsPhi->at(i)))*(smear-1);
// 	    metPy -= (jetsPt->at(i) * sin(jetsPhi->at(i)))*(smear-1);
//	    std::cout << ptCorr << "\t" << genpt << "\t" << smear << std::endl;
	    energyCorr = energyCorr * smear;	    
	    ptCorr = ptCorr * smear;
	  }

	  if (syst_name == "JESUp" ||
	      syst_name == "JESUpCorrelationGroupInSitu" ||
	      syst_name == "JESUpCorrelationGroupFlavor" ||
	      syst_name == "JESUpCorrelationGroupIntercalibration" ||
	      syst_name == "JESUpCorrelationGroupUncorrelated"
	      ){
	    if (ptCorr > 15.){
	      unc = jetUncertaintyNew( eta,  ptCorr, syst_name);
	      ptCorr = ptCorr * (1 + unc);
	      energyCorr = energyCorr * (1 + unc);
	      //	    metPx -= (jetsPt->at(i) * cos(jetsPhi->at(i))) * unc;
	      //	    metPy -= (jetsPt->at(i) * sin(jetsPhi->at(i))) * unc;
	    }
	  }
	  if (syst_name == "JESDown" || 
	      syst_name == "JESDownCorrelationGroupInSitu" ||
	      syst_name == "JESDownCorrelationGroupFlavor" ||
	      syst_name == "JESDownCorrelationGroupIntercalibration" ||
	      syst_name == "JESDownCorrelationGroupUncorrelated"
	      ){
	    if (ptCorr > 15.){
	      unc = jetUncertaintyNew( eta,  ptCorr, syst_name);
	      ptCorr = ptCorr * (1 - unc);
	      energyCorr = energyCorr * (1 - unc);
	      //	    metPx -= -(jetsPt->at(i) * cos(jetsPhi->at(i))) * unc;
	      //	    metPy -= -(jetsPt->at(i) * sin(jetsPhi->at(i))) * unc;
	    }
	  }

	  if (doResol_){
	    tmpjet.SetMagPhi(ptCorr,jetsPhi->at(i));
	    met -= tmpjet;
	  }
	  
	  _jetPt_.push_back(ptCorr);
	  _jetEnergy_.push_back(energyCorr);
	  _jetUncorrPt_.push_back(jetsPt->at(i));

	}

	//Do lepton energy scale correction systematics
	if (syst_name == "LESUp" || syst_name == "LESDown"){

	  TVector2 tmplep;
	  double eleScale = 1.;
	  double muonScale = 1.;
	  
	  if (syst_name == "LESUp"){
	    muonScale = 1.002;
	  }
	  if (syst_name == "LESDown"){
	    muonScale = 0.998;
	  }

	  for (size_t i = 0; i < _electronPt_.size(); i++){
	    //WHAT IS THE ETA RANGE NEEDED FOR THIS
	    if (abs(_electronEta_[i]) < 1.5){
	      if (syst_name == "LESUp"){
		eleScale = 1.005;
	      }
	      if (syst_name == "LESDown"){
		eleScale = 0.995;
	      }
	    }	      
	    else if (abs(_electronEta_[i]) < 2.5){
	      if (syst_name == "LESUp"){
		eleScale = 1.01;
	      }
	      if (syst_name == "LESDown"){
		eleScale = 0.99;
	      }
	    }	      

	    //Add on lepton vector to met (will be subtracted again after correction)
	    tmplep.SetMagPhi(_electronPt_[i],_electronPhi_[i]);
	    met += tmplep;

	    _electronPt_[i] *= eleScale;
	    _electronEnergy_[i] *= eleScale;
	    _electronECALPt_[i] *= eleScale;
	    _electronRelIso_[i] *= 1./eleScale;
	    _electronRhoCorrectedRelIso_[i] *= 1./eleScale;
	    _electronDeltaCorrectedRelIso_[i] *= 1./eleScale;
	    
	    //Subtract off lepton vector to met (to get net effect from correction)
	    tmplep.SetMagPhi(_electronPt_[i],_electronPhi_[i]);
	    met -= tmplep;
	  }

	  for (size_t i = 0; i < _muonPt_.size(); i++){
	    //Add on lepton vector to met (will be subtracted again after correction)
	    tmplep.SetMagPhi(_muonPt_[i],_muonPhi_[i]);
	    met += tmplep;

	    _muonPt_[i] *= muonScale;
	    _muonEnergy_[i] *= muonScale;
	    _muonRelIso_[i] *= 1./muonScale;
	    _muonRhoCorrectedRelIso_[i] *= 1./muonScale;
	    _muonDeltaCorrectedRelIso_[i] *=1./ muonScale;

	    //Subtract off lepton vector to met (to get net effect from correction)
	    tmplep.SetMagPhi(_muonPt_[i],_muonPhi_[i]);
	    met -= tmplep;

	  }
	}

        /////////
        ///End of the standard lepton-jet loop
        /////////


	double PUWeightPUUp = 1.;
	double PUWeightPUDown = 1.;

        if (doPU_)
        {
	  string run = "A";
	  PUWeightA = pileUpSF(syst,run); 
	  run = "B";
	  PUWeightB = pileUpSF(syst,run); 
	  run = "C";
	  PUWeightC = pileUpSF(syst,run); 
	  run = "D";
	  PUWeightD = pileUpSF(syst,run); 

	  PUWeightPUUp = pileUpSF("PUUp",run);
	  PUWeightPUDown = pileUpSF("PUDown",run);
	  //    cout<< "n0 " << nVertices <<   " weight = "<< PUWeightNoSyst<< " cross-check "  <<endl;
                
	  //	  PUWeightNewNoSyst = pileUpSFNew(); PUWeightNew = PUWeightNewNoSyst;
	}
        else {
	  PUWeight = 1;
	  PUWeightA = 1;
	  PUWeightB = 1;
	  PUWeightC = 1;
	  PUWeightD = 1;
	  PUWeightNew = 1;
        }

        _PUWeight_ = PUWeight;
        _PUWeightA_ = PUWeightA;
        _PUWeightB_ = PUWeightB;
        _PUWeightC_ = PUWeightC;
        _PUWeightD_ = PUWeightD;

	if (syst_name == "PUUp") _PUWeight_ = PUWeightPUUp;
	if (syst_name == "PUDown") _PUWeight_ = PUWeightPUDown;

        _PUWeightNew_ = PUWeightNew;
        //Jet trees:

//         _MetPt_ = sqrt(metPx * metPx + metPy * metPy);
// 	_MetPhi_ = METPhi->at(0);

	_MetPt_ = met.Mod();
	_MetPhi_ = met.Phi();
	
	trees[syst]->Fill();
    }

}

//CosThetalj given top quark, lepton and light jet
float SingleTopSystematicsTreesDumper_tW::cosThetaLJ(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top)
{

    math::PtEtaPhiELorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton, top.BoostToCM());
    math::PtEtaPhiELorentzVector boostedJet = ROOT::Math::VectorUtil::boost(jet, top.BoostToCM());

    return  ROOT::Math::VectorUtil::CosTheta(boostedJet.Vect(), boostedLepton.Vect());

}

//CosTheta-lepton-beam-line, implementation by Joosep Pata
float SingleTopSystematicsTreesDumper_tW::cosTheta_eta_bl(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, math::PtEtaPhiELorentzVector top)
{

    double eta = jet.eta();
    double z;
    if (eta > 0)
    {
        z = 1.0;
    }
    else
    {
        z = -1.0;
    }
    math::XYZTLorentzVector beamLine = math::XYZTLorentzVector(0.0, 0.0, z, 1.0);
    math::PtEtaPhiELorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton, top.BoostToCM());
    math::XYZTLorentzVector boostedBeamLine = ROOT::Math::VectorUtil::boost(beamLine, top.BoostToCM());

    return ROOT::Math::VectorUtil::CosTheta(boostedBeamLine.Vect(), boostedLepton.Vect());

}


double SingleTopSystematicsTreesDumper_tW::topMtw(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy)
{
    math::PtEtaPhiELorentzVector lb = lepton + jet;
    double mlb2 = lb.mass() * lb.mass();
    double etlb = sqrt(mlb2 + lb.pt() * lb.pt());
    double metPT = sqrt(metPx * metPx + metPy * metPy);

    return sqrt( mlb2 + 2 * ( etlb * metPT - lb.px() * metPx - lb.py() * metPy ) );
}

//top quark 4-momentum given lepton, met and b-jet
math::PtEtaPhiELorentzVector SingleTopSystematicsTreesDumper_tW::top4Momentum(math::PtEtaPhiELorentzVector lepton, math::PtEtaPhiELorentzVector jet, float metPx, float metPy)
{
    return top4Momentum(lepton.px(), lepton.py(), lepton.pz(), lepton.energy(), jet.px(), jet.py(), jet.pz(), jet.energy(), metPx, metPy);
}

//top quark 4-momentum original function given the necessary parameters
math::PtEtaPhiELorentzVector SingleTopSystematicsTreesDumper_tW::top4Momentum(float leptonPx, float leptonPy, float leptonPz, float leptonE, float jetPx, float jetPy, float jetPz, float jetE, float metPx, float metPy)
{
    float lepton_Pt = sqrt( (leptonPx * leptonPx) +  (leptonPy * leptonPy) );

    math::XYZTLorentzVector neutrino = NuMomentum(leptonPx, leptonPy, leptonPz, lepton_Pt, leptonE, metPx, metPy); //.at(0);;

    math::XYZTLorentzVector lep(leptonPx, leptonPy, leptonPz, leptonE);
    math::XYZTLorentzVector jet(jetPx, jetPy, jetPz, jetE);

    math::XYZTLorentzVector top = lep + jet + neutrino;
    return math::PtEtaPhiELorentzVector(top.pt(), top.eta(), top.phi(), top.E());
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
math::XYZTLorentzVector SingleTopSystematicsTreesDumper_tW::NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy )
{

    double  mW = 80.399;

    math::XYZTLorentzVector result;

    //  double Wmt = sqrt(pow(Lepton.et()+MET.pt(),2) - pow(Lepton.px()+metPx,2) - pow(leptonPy+metPy,2) );

    double MisET2 = (metPx * metPx + metPy * metPy);
    double mu = (mW * mW) / 2 + metPx * leptonPx + metPy * leptonPy;
    double a  = (mu * leptonPz) / (leptonE * leptonE - leptonPz * leptonPz);
    double a2 = TMath::Power(a, 2);
    double b  = (TMath::Power(leptonE, 2.) * (MisET2) - TMath::Power(mu, 2.)) / (TMath::Power(leptonE, 2) - TMath::Power(leptonPz, 2));
    double pz1(0), pz2(0), pznu(0);
    int nNuSol(0);

    math::XYZTLorentzVector p4nu_rec;
    math::XYZTLorentzVector p4W_rec;
    math::XYZTLorentzVector p4b_rec;
    math::XYZTLorentzVector p4Top_rec;
    math::XYZTLorentzVector p4lep_rec;

    p4lep_rec.SetPxPyPzE(leptonPx, leptonPy, leptonPz, leptonE);

    math::XYZTLorentzVector p40_rec(0, 0, 0, 0);

    if (a2 - b > 0 )
    {
        //if(!usePositiveDeltaSolutions_)
        //  {
        //  result.push_back(p40_rec);
        //  return result;
        //  }
        double root = sqrt(a2 - b);
        pz1 = a + root;
        pz2 = a - root;
        nNuSol = 2;

        //    if(usePzPlusSolutions_)pznu = pz1;
        //    if(usePzMinusSolutions_)pznu = pz2;
        //if(usePzAbsValMinimumSolutions_){
        pznu = pz1;
        if (fabs(pz1) > fabs(pz2)) pznu = pz2;
        //}


        double Enu = sqrt(MisET2 + pznu * pznu);

        p4nu_rec.SetPxPyPzE(metPx, metPy, pznu, Enu);

        //    result =.push_back(p4nu_rec);
        result = p4nu_rec;

    }
    else
    {

        // if(!useNegativeDeltaSolutions_){
        //result.push_back(p40_rec);
        //  return result;
        //    }
        //    double xprime = sqrt(mW;


        double ptlep = leptonPt, pxlep = leptonPx, pylep = leptonPy, metpx = metPx, metpy = metPy;

        double EquationA = 1;
        double EquationB = -3 * pylep * mW / (ptlep);
        double EquationC = mW * mW * (2 * pylep * pylep) / (ptlep * ptlep) + mW * mW - 4 * pxlep * pxlep * pxlep * metpx / (ptlep * ptlep) - 4 * pxlep * pxlep * pylep * metpy / (ptlep * ptlep);
        double EquationD = 4 * pxlep * pxlep * mW * metpy / (ptlep) - pylep * mW * mW * mW / ptlep;

        std::vector<long double> solutions = EquationSolve<long double>((long double)EquationA, (long double)EquationB, (long double)EquationC, (long double)EquationD);

        std::vector<long double> solutions2 = EquationSolve<long double>((long double)EquationA, -(long double)EquationB, (long double)EquationC, -(long double)EquationD);


        double deltaMin = 14000 * 14000;
        double zeroValue = -mW * mW / (4 * pxlep);
        double minPx = 0;
        double minPy = 0;

        //    std::cout<<"a "<<EquationA << " b " << EquationB  <<" c "<< EquationC <<" d "<< EquationD << std::endl;

        //  if(usePxMinusSolutions_){
        for ( int i = 0; i < (int)solutions.size(); ++i)
        {
            if (solutions[i] < 0 ) continue;
            double p_x = (solutions[i] * solutions[i] - mW * mW) / (4 * pxlep);
            double p_y = ( mW * mW * pylep + 2 * pxlep * pylep * p_x - mW * ptlep * solutions[i]) / (2 * pxlep * pxlep);
            double Delta2 = (p_x - metpx) * (p_x - metpx) + (p_y - metpy) * (p_y - metpy);

            //      std:://cout<<"intermediate solution1 met x "<<metpx << " min px " << p_x  <<" met y "<<metpy <<" min py "<< p_y << std::endl;

            if (Delta2 < deltaMin && Delta2 > 0)
            {
                deltaMin = Delta2;
                minPx = p_x;
                minPy = p_y;
            }
            //     std:://cout<<"solution1 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl;
        }

        //    }

        //if(usePxPlusSolutions_){
        for ( int i = 0; i < (int)solutions2.size(); ++i)
        {
            if (solutions2[i] < 0 ) continue;
            double p_x = (solutions2[i] * solutions2[i] - mW * mW) / (4 * pxlep);
            double p_y = ( mW * mW * pylep + 2 * pxlep * pylep * p_x + mW * ptlep * solutions2[i]) / (2 * pxlep * pxlep);
            double Delta2 = (p_x - metpx) * (p_x - metpx) + (p_y - metpy) * (p_y - metpy);
            //  std:://cout<<"intermediate solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl;
            if (Delta2 < deltaMin && Delta2 > 0)
            {
                deltaMin = Delta2;
                minPx = p_x;
                minPy = p_y;
            }
            //  std:://cout<<"solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl;
        }
        //}

        double pyZeroValue = ( mW * mW * pxlep + 2 * pxlep * pylep * zeroValue);
        double delta2ZeroValue = (zeroValue - metpx) * (zeroValue - metpx) + (pyZeroValue - metpy) * (pyZeroValue - metpy);

        if (deltaMin == 14000 * 14000)return result;
        //    else std:://cout << " test " << std::endl;

        if (delta2ZeroValue < deltaMin)
        {
            deltaMin = delta2ZeroValue;
            minPx = zeroValue;
            minPy = pyZeroValue;
        }

        //    std:://cout<<" MtW2 from min py and min px "<< sqrt((minPy*minPy+minPx*minPx))*ptlep*2 -2*(pxlep*minPx + pylep*minPy)  <<std::endl;
        ///    ////Y part

        double mu_Minimum = (mW * mW) / 2 + minPx * pxlep + minPy * pylep;
        double a_Minimum  = (mu_Minimum * leptonPz) / (leptonE * leptonE - leptonPz * leptonPz);
        pznu = a_Minimum;

        //if(!useMetForNegativeSolutions_){
        double Enu = sqrt(minPx * minPx + minPy * minPy + pznu * pznu);
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



//JES uncertainty as a function of pt, eta and jet flavour
double SingleTopSystematicsTreesDumper_tW::jetUncertainty(double eta, double ptCorr, int flavour)
{
    jecUnc->setJetEta(eta);
    jecUnc->setJetPt(ptCorr);
    double JetCorrection = jecUnc->getUncertainty(true); // In principle, boolean controls if uncertainty on +ve or -ve side is returned (asymmetric errors) but not yet implemented.
    bool cut = ptCorr > 50 && ptCorr < 200 && fabs(eta) < 2.0;
    // JES_SW = 0.015;
    //  double JES_PU=0.75*0.8*2.2/ptCorr;
    double JES_PU = 0.; //We are using pfNoPU must understand what value to put there
    double JES_b = 0;
    if (abs(flavour) == 5)
    {
        if (cut) JES_b = JES_b_cut;
        else JES_b = JES_b_overCut;
    }
    //    float JESUncertaintyTmp = sqrt(JESUncertainty*JESUncertainty + JetCorrection*JetCorrection);
    //    return sqrt(JES_b * JES_b + JES_PU * JES_PU + JES_SW * JES_SW + JetCorrection * JetCorrection);
    return JetCorrection;
}



double SingleTopSystematicsTreesDumper_tW::jetUncertaintyNew(double eta, double ptCorr, string systematic)
{
  if (systematic == "JESUp"      			    || systematic == "JESDown")                                {jecUnc__ = jecUnc;}
  if (systematic == "JESUpCorrelationGroupInSitu" 	    || systematic == "JESDownCorrelationGroupInSitu")          {jecUnc__ = jecUncCorrelationGroupInSitu;}
  if (systematic == "JESUpCorrelationGroupFlavor" 	    || systematic == "JESDownCorrelationGroupFlavor")          {jecUnc__ = jecUncCorrelationGroupFlavor;}
  if (systematic == "JESUpCorrelationGroupIntercalibration" || systematic == "JESDownCorrelationGroupIntercalibration"){jecUnc__ = jecUncCorrelationGroupIntercalibration;}
  if (systematic == "JESUpCorrelationGroupUncorrelated"     || systematic == "JESDownCorrelationGroupUncorrelated")    {jecUnc__ = jecUncCorrelationGroupUncorrelated;}

  jecUnc__->setJetEta(eta);
  jecUnc__->setJetPt(ptCorr);
  double JetCorrection = jecUnc__->getUncertainty(true); // In principle, boolean controls if uncertainty on +ve or -ve side is returned (asymmetric errors) but not yet implemented.

  return JetCorrection;
}




float SingleTopSystematicsTreesDumper_tW::muonHLTEff(float eta, string period)
{
    float eff = 0.87;

    /*    if(period == "Mu2012A"){
    if (eta < -1.1 && eta > -2.1) eff = 0.81;
    if (eta > -1.1 && eta < -0.9) eff = 0.835;
    if (eta > -0.9 && eta < -0.0) eff = 0.919;
    if (eta > 0.0 && eta < 0.9) eff = 0.921;
    if (eta > 0.9 && eta < 1.1) eff = 0.83;
    if (eta > 1.1 && eta < 2.1) eff = 0.815;
    }


    if(period == "Mu2012B"){
    if (eta < -1.1 && eta > -2.1) eff = 0.81;
    if (eta > -1.1 && eta < -0.9) eff = 0.841;
    if (eta > -0.9 && eta < -0.0) eff = 0.938;
    if (eta > 0.0 && eta < 0.9) eff = 0.940;
    if (eta > 0.9 && eta < 1.1) eff = 0.84;
    if (eta > 1.1 && eta < 2.1) eff = 0.821;
    }OLD
    */


    if(period == "Mu2012A"){
      if (eta < -1.2 && eta > -2.1) eff = 0.8083;
      if (eta > -1.2 && eta < -0.9) eff = 0.8339;
      if (eta > -0.9 && eta < -0.0) eff = 0.9151;
      if (eta > 0.0 && eta < 0.9) eff = 0.9151;
      if (eta > 0.9 && eta < 1.2) eff = 0.8339;
      if (eta > 1.2 && eta < 2.1) eff = 0.8083;
    }
    
    
    if(period == "Mu2012B"){
      if (eta < -1.2 && eta > -2.1) eff = 0.8047;
      if (eta > -1.2 && eta < -0.9) eff = 0.8394;
      if (eta > -0.9 && eta < -0.0) eff = 0.9326;
      if (eta > 0.0 && eta < 0.9) eff = 0.9326;
      if (eta > 0.9 && eta < 1.2) eff = 0.8394;
      if (eta > 1.2 && eta < 2.1) eff = 0.8047;
    }
    
    return eff;
}

//EndJob filling rate systematics trees
void SingleTopSystematicsTreesDumper_tW::endJob()
{

    //part for rate systematics

    cout << endl << passingLepton << " | " << passingMuonVeto << " | " << passingLeptonVeto << " | "  << passingJets << " | " << passingMET << " | " << passingBJets << endl << endl;

    //  resetWeightsDoubles();
    /*  for(size_t i = 0; i < rate_systematics.size();++i){
      string syst = rate_systematics[i];
      string treename = (channel+"_"+syst);

      cout<< " endjob"  << syst<< " 0 "<<endl;
      int bj =0;
      trees2J[bj][syst]->CopyAddresses(trees2J[bj]["noSyst"]);


          cout<< " endjob"  << syst<< " 1 "<<endl;


      //modify the weight by a constant factor
      double tmpWeight = 0;
      double weightSF = 1.;

      TBranch * b = trees2J[bj]["noSyst"]->GetBranch("weight");
      int entries = b->GetEntries();
      b->SetAddress(&tmpWeight);


      cout<< " endjob"  << syst<< " 2 "<<endl;

      trees2J[bj][syst]->GetBranch("weight")->Reset();
      trees2J[bj][syst]->GetBranch("weight")->SetAddress(&tmpWeight);


      cout<< " endjob"  << syst<< " 3 "<<endl;

      for(int t =0; t < entries ; ++t){
        b->GetEntry(t);
        tmpWeight*=weightSF;
        trees2J[bj][syst]->GetBranch("weight")->Fill();

      }



      b->SetAddress(&weightTree);
      trees2J[bj][syst]->GetBranch("weight")->SetAddress(&weightTree);



      //    cout<< " syst "<< syst<< " weights entries "<<  entries <<endl;

    }*/
}

//B-C weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper_tW::BTagSFNew(double pt, string algo)
{
    if (algo == "CSVM")return 0.6981 * ((1. + (0.414063 * pt)) / (1. + (0.300155 * pt)));
    if (algo == "CSVT")return 0.901615 * ((1. + (0.552628 * pt)) / (1. + (0.547195 * pt)));
    if (algo == "TCHPT")return 0.895596 * ((1. + (9.43219e-05 * pt)) / (1. + (-4.63927e-05 * pt)));
    if (algo == "CSVL") return 1.02658 * ((1. + (0.0195388 * pt)) / (1. + (0.0209145 * pt)));


    return 1;
}


double SingleTopSystematicsTreesDumper_tW::BTagSFErrNew(double pt, string algo)
{
    if (algo == "TCHPT")
    {
        if (pt > 30 && pt < 40)return 0.0543376;
        if (pt > 40 && pt < 50)return 0.0534339;
        if (pt > 50 && pt < 60)return 0.0266156;
        if (pt > 60 && pt < 70)return 0.0271337;
        if (pt > 70 && pt < 80)return 0.0276364;
        if (pt > 80 && pt < 100)return 0.0308838;
        if (pt > 100 && pt < 120)return 0.0381656;
        if (pt > 120 && pt < 160)return 0.0336979;
        if (pt > 160 && pt < 210)return 0.0336773;
        if (pt > 210 && pt < 260)return 0.0347688;
        if (pt > 260 && pt < 320)return 0.0376865;
        if (pt > 320 && pt < 400)return 0.0556052;
        if (pt > 400 && pt < 500)return 0.0598105;
        if (pt > 500 && pt < 670)return 0.0861122;
    }
    if (algo == "TCHEL")
    {
        if (pt > 30 && pt < 40)return 0.0244956;
        if (pt > 40 && pt < 50)return 0.0237293;
        if (pt > 50 && pt < 60)return 0.0180131;
        if (pt > 60 && pt < 70)return 0.0182411;
        if (pt > 70 && pt < 80)return 0.0184592;
        if (pt > 80 && pt < 100)return 0.0106444;
        if (pt > 100 && pt < 120)return 0.0110736;
        if (pt > 120 && pt < 160)return 0.0106296;
        if (pt > 160 && pt < 210)return 0.0175259;
        if (pt > 210 && pt < 260)return 0.0161566;
        if (pt > 260 && pt < 320)return 0.0158973;
        if (pt > 320 && pt < 400)return 0.0186782;
        if (pt > 400 && pt < 500)return 0.0371113;
        if (pt > 500 && pt < 670)return 0.0289788;
    }
    if (algo == "CSVM")
    {
        if (pt > 30 && pt < 40)return 0.0295675;
        if (pt > 40 && pt < 50)return 0.0295095;
        if (pt > 50 && pt < 60)return 0.0210867;
        if (pt > 60 && pt < 70)return 0.0219349;
        if (pt > 70 && pt < 80)return 0.0227033;
        if (pt > 80 && pt < 100)return 0.0204062;
        if (pt > 100 && pt < 120)return 0.0185857;
        if (pt > 120 && pt < 160)return 0.0256242;
        if (pt > 160 && pt < 210)return 0.0383341;
        if (pt > 210 && pt < 260)return 0.0409675;
        if (pt > 260 && pt < 320)return 0.0420284;
        if (pt > 320 && pt < 400)return 0.0541299;
        if (pt > 400 && pt < 500)return 0.0578761;
        if (pt > 500 && pt < 670)return 0.0655432;
    }

    if (algo == "CSVT")
    {
        if (pt > 30 && pt < 40)return 0.0364717;
        if (pt > 40 && pt < 50)return 0.0362281;
        if (pt > 50 && pt < 60)return 0.0232876;
        if (pt > 60 && pt < 70)return 0.0249618;
        if (pt > 70 && pt < 80)return 0.0261482;
        if (pt > 80 && pt < 100)return 0.0290466;
        if (pt > 100 && pt < 120)return 0.0300033;
        if (pt > 120 && pt < 160)return 0.0453252;
        if (pt > 160 && pt < 210)return 0.0685143;
        if (pt > 210 && pt < 260)return 0.0653621;
        if (pt > 260 && pt < 320)return 0.0712586;
        if (pt > 320 && pt < 400)return 0.0945892;
        if (pt > 400 && pt < 500)return 0.0777011;
        if (pt > 500 && pt < 670)return 0.0866563;
    }
















    if (algo == "CSVL")
    {
        if (pt > 30 && pt < 40)return     0.0188743;
        if (pt > 40 && pt < 50)return     0.0161816;
        if (pt > 50 && pt < 60)return     0.0139824;
        if (pt > 60 && pt < 70)return     0.0152644;
        if (pt > 70 && pt < 80)return     0.0161226;
        if (pt > 80 && pt < 100)return     0.0157396;
        if (pt > 100 && pt < 120)return     0.0161619;
        if (pt > 120 && pt < 160)return     0.0168747;
        if (pt > 160 && pt < 210)return     0.0257175;
        if (pt > 210 && pt < 260)return     0.026424;
        if (pt > 260 && pt < 320)return     0.0264928;
        if (pt > 320 && pt < 400)return     0.0315127;
        if (pt > 400 && pt < 500)return     0.030734;
        if (pt > 500 && pt < 670)return     0.0438259 ;
    }


    return 0;

}

double SingleTopSystematicsTreesDumper_tW::MisTagSFNew(double pt, double eta, string algo)
{
    if (algo == "TCHPT")return ((1.20711 + (0.000681067 * pt)) + (-1.57062e-06 * (pt * pt))) + (2.83138e-10 * (pt * (pt * pt))) * (1.08376 + -0.000666189 * pt + 1.01272e-06 * pt * pt);
    if (algo == "CSVM")return ((1.20711 + (0.000681067 * pt)) + (-1.57062e-06 * (pt * pt))) + (2.83138e-10 * (pt * (pt * pt))) * (1.10422 + -0.000523856 * pt + 1.14251e-06 * pt * pt);
    if (algo == "CSVT") return (1.10649 * ((1 + (-9.00297e-05 * pt)) + (2.32185e-07 * (pt * pt)))) + (-4.04925e-10 * (pt * (pt * (pt / (1 + (-0.00051036 * pt)))))) * (1.19275 + -0.00191042 * pt + 2.92205e-06 * pt * pt);

    if (algo == "CSVL")return ((1.0344 + (0.000962994 * pt)) + (-3.65392e-06 * (pt * pt))) + (3.23525e-09 * (pt * (pt * pt))) * (0.979396 + 0.000205898 * pt + 2.49868e-07 * pt * pt);

    return 0;
}

double SingleTopSystematicsTreesDumper_tW::MisTagSFErrNewUp(double pt, double eta, string algo)
{
    double x = pt;

    if (algo == "TCHPT")return ((1.38002 + (0.000933875 * pt)) + (-2.59821e-06 * (pt * pt))) + (1.18434e-09 * (pt * (pt * pt)));
    if (algo == "TCHEL")return (1.19751 * ((1 + (-0.000114197 * pt)) + (3.08558e-07 * (pt * pt)))) + (-5.27598e-10 * (pt * (pt * (pt / (1 + (-0.000422372 * pt)))))) ;

    if (algo == "CSVT") return ((0.997077 + (0.00473953 * x)) + (-1.34985e-05 * (x * x))) + (1.0032e-08 * (x * (x * x)));
    if (algo == "CSVL")return ((1.11272 + (0.00110104 * x)) + (-4.11956e-06 * (x * x))) + (3.65263e-09 * (x * (x * x)));

    return 0;
}

double SingleTopSystematicsTreesDumper_tW::MisTagSFErrNewDown(double pt, double eta, string algo)
{
    double x = pt;
    if (algo == "TCHPT")return ((1.03418 + (0.000428273 * pt)) + (-5.43024e-07 * (pt * pt))) + (-6.18061e-10 * (pt * (pt * pt)));
    if (algo == "TCHEL")return (1.01541 * ((1 + (-6.04627e-05 * pt)) + (1.38195e-07 * (pt * pt)))) + (-2.83043e-10 * (pt * (pt * (pt / (1 + (-0.000633609 * pt))))));

    if (algo == "CSVT") return ((0.899715 + (0.00102278 * x)) + (-2.46335e-06 * (x * x))) + (9.71143e-10 * (x * (x * x)));
    if (algo == "CSVL")return ((0.956023 + (0.000825106 * x)) + (-3.18828e-06 * (x * x))) + (2.81787e-09 * (x * (x * x)));

    return 0;
}


double SingleTopSystematicsTreesDumper_tW::EFFMapNew(double btag, string algo)
{
    if (algo == "TCHP_B")return 1.26119661124e-05 * btag * btag * btag * btag +  -0.000683198597977 * btag * btag * btag +  0.0145106168149 * btag * btag +  -0.159575511553 * btag +  0.887707865272;
    if (algo == "TCHP_C")
    {
        if (btag < 0.54) return 0.451288118581 * exp(-0.0213290505241 * btag * btag * btag + 0.356020789904 * btag * btag + -2.20158883207 * btag + 1.84838018633 );
        else return 0.99;
    }
    if (algo == "TCHP_L")return (-0.00101 + (4.70405e-05 * btag)) + (8.3338e-09 * (btag * btag));

    if (algo == "TCHE_B")return 3.90732786802e-06 * btag * btag * btag * btag +  -0.000239934437355 * btag * btag * btag +  0.00664986827287 * btag * btag +  -0.112578996016 * btag +  1.00775721404;
    if (algo == "TCHE_C")
    {
        if (btag > 0.46 ) return 0.343760640168 * exp(-0.00315525164823 * btag * btag * btag + 0.0805427315196 * btag * btag + -0.867625139194 * btag + 1.44815935164 );
        else return 0.99;//EFFMap("TCHEL_C");
    }

    if (algo == "TCHE_L")return(((-0.0276197 + (0.00291907 * btag)) + (-7.51594e-06 * (btag * btag))) + (9.82128e-09 * (btag * (btag * btag)))) + (-5.33759e-12 * (btag * (btag * (btag * btag))));
    return 1;
}

double SingleTopSystematicsTreesDumper_tW::BScaleFactor(string algo, string syst_name)
{

    double bcentral = 0.9;
    double berr = 0.15 * bcentral;
    double cerr = 0.3 * bcentral;
    double tcheeff = 0.7;

    if (syst_name == "BTagUp")
    {
        if (algo == "TCHP_B")
        {
            return bcentral + berr;
        }
        if (algo == "TCHP_C")
        {
            return bcentral + cerr;
        }

        if (algo == "TCHE_B")
        {
            return bcentral + berr;
        }

        if (algo == "TCHE_C")
        {
            return bcentral + cerr;
        }

    }

    if (syst_name == "BTagDown")
    {
        if (algo == "TCHP_B")
        {
            return bcentral - berr;
        }
        if (algo == "TCHP_C")
        {
            return bcentral - cerr;
        }

        if (algo == "TCHE_B")
        {
            return bcentral - berr;
        }
        if (algo == "TCHE_C")
        {
            return bcentral - berr;
        }
    }

    if (algo == "TCHP_B")
    {
        return bcentral;
    }
    if (algo == "TCHP_C")
    {
        return bcentral;
    }
    if (algo == "TCHE_B")
    {
        return bcentral;
    }
    if (algo == "TCHE_C")
    {
        return bcentral;
    }

    return 0.9;
}

//Mistag weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper_tW::MisTagScaleFactor(string algo, string syst_name, double sf, double eff, double sferr)
{
    double mistagcentral = sf;
    double mistagerr = sferr;
    double tcheeff = eff;


    if (syst_name == "MisTagUp")
    {
        if (algo == "TCHP_L")
        {
            return mistagcentral + mistagerr;
        }
        if (algo == "TCHE_L")
        {
            return mistagcentral + mistagerr;
        }

    }

    if (syst_name == "MisTagDown")
    {
        if (algo == "TCHP_L")
        {
            return mistagcentral - mistagerr;
        }
        if (algo == "TCHE_L")
        {
            return mistagcentral - mistagerr;
        }
    }

    if (algo == "TCHP_L")
    {
        return mistagcentral;
    }
    if (algo == "TCHE_L")
    {
        return mistagcentral;
    }

    return 0.9;


}



//B-C veto weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper_tW::AntiBScaleFactor(string algo, string syst_name)
{

    double bcentral = 0.9;
    double berr = 0.15 * bcentral;
    double cerr = 0.3 * bcentral;
    double tcheeff = 0.7;
    double tchpeff = 0.26;

    if (syst_name == "BTagUp")
    {
        if (algo == "TCHP_B")
        {
            return (1 - tchpeff * (bcentral + berr)) / (1 - tchpeff);
        }
        if (algo == "TCHP_C")
        {
            return (1 - tchpeff * (bcentral + cerr)) / (1 - tchpeff);
        }

        if (algo == "TCHE_B")
        {
            return (1 - tcheeff * (bcentral + berr)) / (1 - tcheeff);
        }

        if (algo == "TCHE_C")
        {
            return (1 - tcheeff * (bcentral + cerr)) / (1 - tcheeff);
        }
    }

    if (syst_name == "BTagDown")
    {
        if (algo == "TCHP_B")
        {
            return (1 - tchpeff * (bcentral - berr)) / (1 - tchpeff);
        }
        if (algo == "TCHP_C")
        {
            return (1 - tchpeff * (bcentral - cerr)) / (1 - tchpeff);
        }

        if (algo == "TCHE_B")
        {
            return (1 - tcheeff * (bcentral - berr)) / (1 - tcheeff);
        }
        if (algo == "TCHE_C")
        {
            return (1 - tcheeff * (bcentral - cerr)) / (1 - tcheeff);
        }
    }

    if (algo == "TCHP_B")
    {
        return (1 - tchpeff * (bcentral)) / (1 - tchpeff);
    }
    if (algo == "TCHP_C")
    {
        return (1 - tchpeff * (bcentral)) / (1 - tchpeff);
    }
    if (algo == "TCHE_B")
    {
        return (1 - tcheeff * (bcentral)) / (1 - tcheeff);
    }
    if (algo == "TCHE_C")
    {
        return (1 - tcheeff * (bcentral)) / (1 - tcheeff);
    }

    return 0.9;
}

void SingleTopSystematicsTreesDumper_tW::InitializeEventScaleFactorMap()
{

    TCHPT_B = EventScaleFactor("TCHPT_B", "noSyst");
    TCHPT_C = EventScaleFactor("TCHPT_C", "noSyst");
    TCHPT_L = EventScaleFactor("TCHPT_L", "noSyst");


    TCHPT_BBTagUp = EventScaleFactor("TCHPT_B", "BTagUp");
    TCHPT_BBTagDown = EventScaleFactor("TCHPT_B", "BTagDown");
    TCHPT_CBTagUp = EventScaleFactor("TCHPT_C", "BTagUp");
    TCHPT_CBTagDown = EventScaleFactor("TCHPT_C", "BTagDown");
    TCHPT_LMisTagUp = EventScaleFactor("TCHPT_L", "MisTagUp");
    TCHPT_LMisTagDown = EventScaleFactor("TCHPT_L", "MisTagDown");


    TCHPT_BAnti = EventAntiScaleFactor("TCHPT_B", "noSyst");
    TCHPT_CAnti = EventAntiScaleFactor("TCHPT_C", "noSyst");
    TCHPT_LAnti = EventAntiScaleFactor("TCHPT_L", "noSyst");

    TCHPT_BAntiBTagUp = EventAntiScaleFactor("TCHPT_B", "BTagUp");
    TCHPT_BAntiBTagDown = EventAntiScaleFactor("TCHPT_B", "BTagDown");
    TCHPT_CAntiBTagUp = EventAntiScaleFactor("TCHPT_C", "BTagUp");
    TCHPT_CAntiBTagDown = EventAntiScaleFactor("TCHPT_C", "BTagDown");
    TCHPT_LAntiMisTagUp = EventAntiScaleFactor("TCHPT_L", "MisTagUp");
    TCHPT_LAntiMisTagDown = EventAntiScaleFactor("TCHPT_L", "MisTagDown");


    //  TCHP_LAntiMisTagDown = EventAntiScaleFactor("TCHP_L","MisTagDown");

    TCHPM_B = EventScaleFactor("TCHPM_B", "noSyst");
    TCHPM_C = EventScaleFactor("TCHPM_C", "noSyst");
    TCHPM_L = EventScaleFactor("TCHPM_L", "noSyst");


    TCHPM_BBTagUp = EventScaleFactor("TCHPM_B", "BTagUp");
    TCHPM_BBTagDown = EventScaleFactor("TCHPM_B", "BTagDown");
    TCHPM_CBTagUp = EventScaleFactor("TCHPM_C", "BTagUp");
    TCHPM_CBTagDown = EventScaleFactor("TCHPM_C", "BTagDown");
    TCHPM_LMisTagUp = EventScaleFactor("TCHPM_L", "MisTagUp");
    TCHPM_LMisTagDown = EventScaleFactor("TCHPM_L", "MisTagDown");


    TCHPM_BAnti = EventAntiScaleFactor("TCHPM_B", "noSyst");
    TCHPM_CAnti = EventAntiScaleFactor("TCHPM_C", "noSyst");
    TCHPM_LAnti = EventAntiScaleFactor("TCHPM_L", "noSyst");

    TCHPM_BAntiBTagUp = EventAntiScaleFactor("TCHPM_B", "BTagUp");
    TCHPM_BAntiBTagDown = EventAntiScaleFactor("TCHPM_B", "BTagDown");
    TCHPM_CAntiBTagUp = EventAntiScaleFactor("TCHPM_C", "BTagUp");
    TCHPM_CAntiBTagDown = EventAntiScaleFactor("TCHPM_C", "BTagDown");
    TCHPM_LAntiMisTagUp = EventAntiScaleFactor("TCHPM_L", "MisTagUp");
    TCHPM_LAntiMisTagDown = EventAntiScaleFactor("TCHPM_L", "MisTagDown");

    /////

    TCHEL_B = EventScaleFactor("TCHEL_B", "noSyst");
    TCHEL_C = EventScaleFactor("TCHEL_C", "noSyst");
    TCHEL_L = EventScaleFactor("TCHEL_L", "noSyst");

    TCHEL_BBTagUp = EventScaleFactor("TCHEL_B", "BTagUp");
    TCHEL_BBTagDown = EventScaleFactor("TCHEL_B", "BTagDown");
    TCHEL_CBTagUp = EventScaleFactor("TCHEL_C", "BTagUp");
    TCHEL_CBTagDown = EventScaleFactor("TCHEL_C", "BTagDown");
    TCHEL_LMisTagUp = EventScaleFactor("TCHEL_L", "MisTagUp");
    TCHEL_LMisTagDown = EventScaleFactor("TCHEL_L", "MisTagDown");

    TCHEL_BAnti = EventAntiScaleFactor("TCHEL_B", "noSyst");
    TCHEL_CAnti = EventAntiScaleFactor("TCHEL_C", "noSyst");
    TCHEL_LAnti = EventAntiScaleFactor("TCHEL_L", "noSyst");

    TCHEL_BAntiBTagUp = EventAntiScaleFactor("TCHEL_B", "BTagUp");
    TCHEL_BAntiBTagDown = EventAntiScaleFactor("TCHEL_B", "BTagDown");
    TCHEL_CAntiBTagUp = EventAntiScaleFactor("TCHEL_C", "BTagUp");
    TCHEL_CAntiBTagDown = EventAntiScaleFactor("TCHEL_C", "BTagDown");
    TCHEL_LAntiMisTagUp = EventAntiScaleFactor("TCHEL_L", "MisTagUp");
    TCHEL_LAntiMisTagDown = EventAntiScaleFactor("TCHEL_L", "MisTagDown");
}

double SingleTopSystematicsTreesDumper_tW::SFMap(string algo )
{
    if (algo == "TCHPT_B")return 0.89;
    if (algo == "TCHPT_C")return 0.89;
    if (algo == "TCHPT_L")return 1.17;

    if (algo == "TCHPM_B")return 0.91;
    if (algo == "TCHPM_C")return 0.91;
    if (algo == "TCHPM_L")return 0.91;

    if (algo == "TCHEL_B")return 0.95;
    if (algo == "TCHEL_C")return 0.95;
    if (algo == "TCHEL_L")return 1.11;


    return 0.9;
}

double SingleTopSystematicsTreesDumper_tW::SFErrMap(string algo )
{
    if (algo == "TCHPT_B")return 0.092;
    if (algo == "TCHPT_C")return 0.092;
    if (algo == "TCHPT_L")return 0.18;

    if (algo == "TCHPM_B")return 0.10;
    if (algo == "TCHPM_C")return 0.10;
    if (algo == "TCHPM_L")return 0.11;

    if (algo == "TCHEL_B")return 0.10;
    if (algo == "TCHEL_C")return 0.10;
    if (algo == "TCHEL_L")return 0.11;

    return 0.1;
}

double SingleTopSystematicsTreesDumper_tW::EFFMap(string algo )
{
    if (algo == "TCHPT_B")return 0.365 * 1.;
    if (algo == "TCHPT_C")return 0.0365;
    if (algo == "TCHPT_L")return 0.0017;

    if (algo == "CSVT_B")return 0.5;
    if (algo == "CSVT_C")return 0.05;
    if (algo == "CSVT_L")return 0.003;

    if (algo == "CSVM_B")return 0.365;
    if (algo == "CSVM_C")return 0.0365;
    if (algo == "CSVM_L")return 0.0017;

    if (algo == "CSVL_B")return 0.8;
    if (algo == "CSVL_C")return 0.36;
    if (algo == "CSVL_L")return 0.2;

    return 0.36;
}

double SingleTopSystematicsTreesDumper_tW::EFFMap(string algo, string channel )
{

    if (channel == "TChannel" || channel == "TbarChannel" || channel == "SChannel" || channel == "SbarChannel" || channel == "TWChannel" || channel == "TbarWChannel")
    {
        if (algo == "CSVT_B")return 0.54;
        if (algo == "CSVT_C")return 0.037;
        if (algo == "CSVT_L")return 0.002;

        if (algo == "CSVL_B")return 0.84;
        if (algo == "CSVL_C")return 0.33;
        if (algo == "CSVL_L")return 0.2;

    }

    if (channel == "TTBar")
    {
        if (algo == "CSVT_B")return 0.66;
        if (algo == "CSVT_C")return 0.052;
        if (algo == "CSVT_L")return 0.047;

        if (algo == "CSVL_B")return 0.92;
        if (algo == "CSVL_C")return 0.44;
        if (algo == "CSVL_L")return 0.3;



    }

    if (channel == "WJets")
    {
        if (algo == "CSVT_B")return 0.31;
        if (algo == "CSVT_C")return 0.046;
        if (algo == "CSVT_L")return 0.0015;

        if (algo == "CSVL_B")return 0.63;
        if (algo == "CSVL_C")return 0.40;
        if (algo == "CSVL_L")return 0.14;


    }

    if (channel == "ZJets")
    {

        if (algo == "CSVT_B")return 0.41;
        if (algo == "CSVT_C")return 0.047;
        if (algo == "CSVT_L")return 0.002;

        if (algo == "CSVL_B")return 0.76;
        if (algo == "CSVL_C")return 0.41;
        if (algo == "CSVL_L")return 0.2;


    }



    return EFFMap(algo);

}

double SingleTopSystematicsTreesDumper_tW::EFFErrMap(string algo )
{
    if (algo == "TCHPT_B")return 0.05;
    if (algo == "TCHPT_C")return 0.05;
    if (algo == "TCHPT_L")return 0.0004;

    if (algo == "TCHEL_B")return 0.05;
    if (algo == "TCHEL_C")return 0.05;
    if (algo == "TCHEL_L")return 0.03;

    if (algo == "TCHEL_B")return 0.05;
    if (algo == "TCHEL_C")return 0.05;
    if (algo == "TCHEL_L")return 0.004;

    return 0.05;
}
double SingleTopSystematicsTreesDumper_tW::EventScaleFactor(string algo, string syst_name) //,double sf, double eff, double sferr){
{

    //  double mistagcentral = sf;
    //double mistagerr = sferr;
    //double tcheeff = eff;

    double mistagcentral = SFMap(algo);
    double mistagerr = SFErrMap(algo);
    double tcheeff = EFFMap(algo);


    if (syst_name == "MisTagUp" || syst_name == "BTagUp")
    {
        return mistagcentral + mistagerr;
    }

    if (syst_name == "MisTagDown" || syst_name == "BTagDown")
    {
        return mistagcentral - mistagerr;
    }

    return mistagcentral;
}

//EventAntiScaleFactor

double SingleTopSystematicsTreesDumper_tW::EventAntiScaleFactor(string algo, string syst_name )
{
    //,double sf, double eff, double sferr){


    //double mistagcentral = sf;
    //double mistagerr = sferr;
    //double tcheeff = eff;

    double mistagcentral = SFMap(algo);
    double mistagerr = SFErrMap(algo);
    double tcheeff = EFFMap(algo);


    if (syst_name == "MisTagUp" || syst_name == "BTagUp")
    {
        return (1 - tcheeff) / (1 - tcheeff / (mistagcentral + mistagerr));
    }

    if (syst_name == "MisTagDown" || syst_name == "BTagDown")
    {
        return (1 - tcheeff) / (1 - tcheeff / (mistagcentral - mistagerr));

    }

    return (1 - tcheeff) / (1 - tcheeff / (mistagcentral));

}


//MisTag veto weight as function of jet flavour, systematics and scale factors:
//WILL BE CHANGED VERY SOON ACCORDING TO NEW PRESCRIPTIONS
double SingleTopSystematicsTreesDumper_tW::AntiMisTagScaleFactor(string algo, string syst_name, double sf, double eff, double sferr)
{
    double mistagcentral = sf;
    double mistagerr = sferr;
    double tcheeff = eff;
    double tchpeff = eff;

    if (syst_name == "MisTagUp")
    {
        if (algo == "TCHP_L")
        {
            return (1 - tchpeff) / (1 - tchpeff / (mistagcentral + mistagerr));
        }
        if (algo == "TCHE_L")
        {
            return (1 - tcheeff) / (1 - tcheeff / (mistagcentral + mistagerr));
        }

    }

    if (syst_name == "MisTagDown")
    {
        if (algo == "TCHP_L")
        {
            return (1 - tchpeff) / (1 - tchpeff / (mistagcentral - mistagerr));
        }
        if (algo == "TCHE_L")
        {
            return (1 - tcheeff) / (1 - tcheeff / (mistagcentral - mistagerr));
        }
    }

    if (algo == "TCHP_L")
    {
        return (1 - tchpeff) / (1 - tchpeff / (mistagcentral));
    }
    if (algo == "TCHE_L")
    {
        return (1 - tcheeff) / (1 - tcheeff / (mistagcentral));
    }

    return 0.9;


}


double SingleTopSystematicsTreesDumper_tW::turnOnWeight (std::vector<double> probabilities, int njets_req = 1)
{
    double prob = 0;
    for (unsigned int i = 0; i < pow(2, probabilities.size()); ++i)
    {
        //at least njets_req objects for trigger required
        int ntrigobj = 0;
        for (unsigned int j = 0; j < probabilities.size(); ++j)
        {
            if ((int)(i / pow(2, j)) % 2) ntrigobj++;
        }
        if (ntrigobj < njets_req) continue;
        double newprob = 1;
        for (unsigned int j = 0; j < probabilities.size(); ++j)
        {
            if ((int)(i / pow(2, j)) % 2) newprob *= probabilities[j];
            else newprob *= 1 - probabilities[j];
        }
        prob += newprob;
    }
    return prob;
}


int SingleTopSystematicsTreesDumper_tW::eventFlavour(string ch, int nb, int nc, int nl)
{
    if (ch !=  "WJets" && ch != "ZJets") return 0;
    else
    {
        if ( flavourFilter("WJets_wlight", nb, nc, nl) ) return 1;
        if ( flavourFilter("WJets_wcc", nb, nc, nl) ) return 2;
        if ( flavourFilter("WJets_wbb", nb, nc, nl) ) return 3;
    }
    return 0;
}

bool SingleTopSystematicsTreesDumper_tW::flavourFilter(string ch, int nb, int nc, int nl)
{

    if (ch == "WJets_wbb" || ch == "ZJets_wbb") return (nb > 0 );
    if (ch == "WJets_wcc" || ch == "ZJets_wcc") return (nb == 0 && nc > 0);
    if (ch == "WJets_wlight" || ch == "ZJets_wlight") return (nb == 0 && nc == 0);

    return true;
}

/*double SingleTopSystematicsTreesDumper_tW::jetprob(double pt, double btag){
  double prob=0.993*(exp(-51.0*exp(-0.160*pt)));
  prob*=0.902*exp((-5.995*exp(-0.604*btag)));
  return prob;
  }*/

double SingleTopSystematicsTreesDumper_tW::jetprob(double pt, double btag)
{
    double prob = 0.982 * exp(-30.6 * exp(-0.151 * pt)); //PT turnOn
    prob *= 0.844 * exp((-6.72 * exp(-0.720 * btag))); //BTag turnOn
    return prob;
}


double SingleTopSystematicsTreesDumper_tW::jetprobpt(double pt)
{
    double prob = 0.982 * exp(-30.6 * exp(-0.151 * pt)); //PT turnOn
    return prob;
}

double SingleTopSystematicsTreesDumper_tW::jetprobbtag(double btag)
{
    double prob = 0.844 * exp((-6.72 * exp(-0.720 * btag))); //BTag turnOn
    return prob;
}

double SingleTopSystematicsTreesDumper_tW::turnOnProbs(string syst, int n)
{
    if (syst == "JetTrig1Up")
    {
        return turnOnWeight(jetprobs_j1up, 1)
               ;
    }
    else if (syst == "JetTrig2Up")
    {
        return turnOnWeight(jetprobs_j2up, 1)
               ;
    }
    else if (syst == "JetTrig3Up")
    {
        return turnOnWeight(jetprobs_j3up, 1)
               ;
    }

    if (syst == "JetTrig1Down")
    {
        return turnOnWeight(jetprobs_j1down, 1)
               ;
    }
    else if (syst == "JetTrig2Down")
    {
        return turnOnWeight(jetprobs_j2down, 1)
               ;
    }
    else if (syst == "JetTrig3Down")
    {
        return turnOnWeight(jetprobs_j3down, 1)
               ;
    }

    if (syst == "BTagTrig1Up")
    {
        return turnOnWeight(jetprobs_b1up, 1)
               ;
    }
    else if (syst == "BTagTrig2Up")
    {
        return turnOnWeight(jetprobs_b2up, 1)
               ;
    }
    else if (syst == "BTagTrig3Up")
    {
        return turnOnWeight(jetprobs_b3up, 1)
               ;
    }

    if (syst == "BTagTrig1Down")
    {
        return turnOnWeight(jetprobs_b1down, 1)
               ;
    }
    else if (syst == "BTagTrig2Down")
    {
        return turnOnWeight(jetprobs_b2down, 1)
               ;
    }
    else if (syst == "BTagTrig3Down")
    {
        return turnOnWeight(jetprobs_b3down, 1)
               ;
    }

    return turnOnWeight(jetprobs, 1);


}

void SingleTopSystematicsTreesDumper_tW::pushJetProbs(double pt, double btag, double eta)
{

    jetprobs.push_back(jetprob(pt, btag, eta, "noSyst"));

    jetprobs_j1up.push_back(jetprob(pt, btag, eta, "JetTrig1Up"));
    jetprobs_j1down.push_back(jetprob(pt, btag, eta, "JetTrig1Down"));

    jetprobs_j2up.push_back(jetprob(pt, btag, eta, "JetTrig2Up"));
    jetprobs_j2down.push_back(jetprob(pt, btag, eta, "JetTrig2Down"));

    jetprobs_j3up.push_back(jetprob(pt, btag, eta, "JetTrig3Up"));
    jetprobs_j3down.push_back(jetprob(pt, btag, eta, "JetTrig3Down"));


    jetprobs_b1up.push_back(jetprob(pt, btag, eta, "BTagTrig1Up"));
    jetprobs_b1down.push_back(jetprob(pt, btag, eta, "BTagTrig1Down"));

    jetprobs_b2up.push_back(jetprob(pt, btag, eta, "BTagTrig2Up"));
    jetprobs_b2down.push_back(jetprob(pt, btag, eta, "BTagTrig2Down"));

    jetprobs_b3up.push_back(jetprob(pt, btag, eta, "BTagTrig3Up"));
    jetprobs_b3down.push_back(jetprob(pt, btag, eta, "BTagTrig3Down"));




}

void SingleTopSystematicsTreesDumper_tW::InitializeTurnOnReWeight(string rootFile = "CentralJet30BTagIP_2ndSF_mu.root")
{

    TFile f("CentralJet30BTagIP_2ndSF_mu.root");
    TH2D *histSF = dynamic_cast<TH2D *>(f.Get("ScaleFactor"));

    histoSFs = *histSF;
    f.Close();
    //  cout << " histo random test bin " <<histoSFs.FindFixBin(61,6.5)<< " content "<<histoSFs.GetBinContent(histoSFs.FindFixBin(61,6.5)) << endl;
    //  for
    //  recorrection_weights[7][7];

    //  float pt_bin_extremes[8];
    //float tchpt_bin_extremes[8];

    ;
}

double SingleTopSystematicsTreesDumper_tW::turnOnReWeight (double preWeight, double pt, double tchpt)
{
  //    cout << "reweight pt" <<  pt << " tchpt " << tchpt << endl;
  //  cout << " bin " << histoSFs.FindFixBin(pt, tchpt) << " sf ";
  //    cout << histoSFs.GetBinContent(histoSFs.FindFixBin(pt, tchpt)) << endl;
    double a = histoSFs.GetBinContent(histoSFs.FindFixBin(pt, tchpt));
    return a;
    //  return 1;//preWeight;
}


double SingleTopSystematicsTreesDumper_tW::jetprob(double pt, double btag, double eta, string syst)
{
    double prob = 1.;
    if (fabs(eta) > 2.6) return 0.;

    double a = 0, b = 1, c = 1;

    if (syst == "BTagTrig1Up")
    {
        if (btag < -10.)
        {
            a = 0.0142;
            b = -27.7;
            c = -0.128;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0735;
            b = -4.24;
            c = -0.0615;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0196;
            b = -7.71;
            c = -0.0647;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -16.3;
            c = -0.0933;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.071;
            b = -50.;
            c = -0.138;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.255;
            b = -109.4;
            c = -0.172;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.39;
            b = -112.;
            c = -0.168;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.534;
            b = -113.;
            c = -0.166;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.647;
            b = -69.3;
            c = -0.15;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.734;
            b = -107;
            c = -0.164;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.816;
            b = -102;
            c = -0.162;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.868;
            b = -96.2;
            c = -0.158;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.878;
            b = -111;
            c = -0.165;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.893;
            b = -83.9;
            c = -0.156;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -59.6;
            c = -0.141;
        };
    }

    else if (syst == "BTagTrig1Down")
    {
        if (btag < -10.)
        {
            a = 0.0138;
            b = -45.4;
            c = -0.146;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.065;
            b = -14.6;
            c = -0.104;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.019;
            b = -9.33;
            c = -0.0719;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.0266;
            b = -20.7;
            c = -0.0102;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0706;
            b = -65.1;
            c = -0.147;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.253;
            b = -192.;
            c = -0.191;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.387;
            b = -192.;
            c = -0.186;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.529;
            b = -188.;
            c = -0.183;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.642;
            b = -106.;
            c = -0.164;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.73;
            b = -161.;
            c = -0.179;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.813;
            b = -129.;
            c = -0.17;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.865;
            b = -123.;
            c = -0.166;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.881;
            b = -151.;
            c = -0.176;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.891;
            b = -103.;
            c = -0.162;
        };
        if (btag > 10.0 )
        {
            a = 0.885;
            b = -70.6;
            c = -0.146;
        };
    }
    else if (syst == "BTagTrig2Up")
    {
        if (btag < -10.)
        {
            a = 0.0141;
            b = -36.5;
            c = -0.136;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0727;
            b = -9.42;
            c = -0.0797;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0195;
            b = -8.52;
            c = -0.0677;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -18.5;
            c = -0.0969;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.071;
            b = -57.5;
            c = -0.142;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.256;
            b = -150.;
            c = -0.181;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.392;
            b = -152.;
            c = -0.176;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.536;
            b = -151.;
            c = -0.174;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.649;
            b = -87.5;
            c = -0.156;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.737;
            b = -134.0;
            c = -0.171;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.818;
            b = -115.;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.869;
            b = -110.;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.883;
            b = -131.;
            c = -0.171;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.894;
            b = -93.4;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.887;
            b = -65.1;
            c = -0.144;
        };

    }
    else if (syst == "BTagTrig2Down")
    {
        if (btag < -10.)
        {
            a = 0.0138;
            b = -36.5;
            c = -0.138;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0658;
            b = -9.42;
            c = -0.0859;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0191;
            b = -8.52;
            c = -0.0689;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.0267;
            b = -18.5;
            c = -0.098;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0706;
            b = -57.5;
            c = -0.144;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.252;
            b = -150;
            c = -0.182;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.384;
            b = -152.;
            c = -0.177;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.527;
            b = -151.;
            c = -0.175;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.639;
            b = -87.5;
            c = -0.157;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.727;
            b = -134.0;
            c = -0.172;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.812;
            b = -115.;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.863;
            b = -110.;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.877;
            b = -131.;
            c = -0.170;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.89;
            b = -93.4;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.884;
            b = -65.1;
            c = -0.144;
        };

    }
    else if (syst == "BTagTrig3Up")
    {
        if (btag < -10.)
        {
            a = 0.0139;
            b = -36.5;
            c = -0.137;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0702;
            b = -9.42;
            c = -0.0839;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0192;
            b = -8.52;
            c = -0.0683;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.0267;
            b = -18.5;
            c = -0.0974;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0705;
            b = -57.5;
            c = -0.143;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.254;
            b = -150.;
            c = -0.183;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.388;
            b = -152.;
            c = -0.178;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.531;
            b = -151.;
            c = -0.175;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.644;
            b = -87.5;
            c = -0.158;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.732;
            b = -134.0;
            c = -0.172;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.815;
            b = -115.;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.866;
            b = -110.;
            c = -0.163;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.880;
            b = -131.;
            c = -0.171;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.892;
            b = -93.4;
            c = -0.160;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -65.1;
            c = -0.144;
        };
    }
    else if (syst == "BTagTrig3Down")
    {
        if (btag < -10.)
        {
            a = 0.0141;
            b = -36.5;
            c = -0.137;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.0683;
            b = -9.42;
            c = -0.0817;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.0194;
            b = -8.52;
            c = -0.0684;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -18.5;
            c = -0.0975;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.0711;
            b = -57.5;
            c = -0.143;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.253;
            b = -150.;
            c = -0.18;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.388;
            b = -152.;
            c = -0.176;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.531;
            b = -151.;
            c = -0.174;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.644;
            b = -87.5;
            c = -0.156;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.732;
            b = -134.0;
            c = -0.171;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.815;
            b = -115.;
            c = -0.165;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.866;
            b = -110.;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.880;
            b = -131.;
            c = -0.170;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.892;
            b = -93.4;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -65.11;
            c = -0.143;
        };

    }
    else
    {
        if (btag < -10.)
        {
            a = 0.014;
            b = -36.55;
            c = -0.137;
        };
        if (btag > -10. && btag < -4)
        {
            a = 0.069;
            b = -9.42;
            c = -0.083;
        };
        if (btag > -4. && btag < 0.0)
        {
            a = 0.019;
            b = -8.52;
            c = -0.068;
        };
        if (btag > 0. && btag < 1.0)
        {
            a = 0.027;
            b = -18.51;
            c = -0.097;
        };
        if (btag > 1. && btag < 2.0)
        {
            a = 0.071;
            b = -57.54;
            c = -0.143;
        };
        if (btag > 2. && btag < 2.4)
        {
            a = 0.254;
            b = -150.48;
            c = -0.182;
        };
        if (btag > 2.4 && btag < 2.8)
        {
            a = 0.388;
            b = -151.97;
            c = -0.177;
        };
        if (btag > 2.8 && btag < 3.2)
        {
            a = 0.531;
            b = -150.73;
            c = -0.175;
        };
        if (btag > 3.2 && btag < 3.6)
        {
            a = 0.644;
            b = -87.52;
            c = -0.157;
        };
        if (btag > 3.6 && btag < 4.0)
        {
            a = 0.732;
            b = -134.05;
            c = -0.172;
        };
        if (btag > 4.0 && btag < 5.0)
        {
            a = 0.815;
            b = -115.25;
            c = -0.166;
        };
        if (btag > 5.0 && btag < 6.0)
        {
            a = 0.866;
            b = -109.53;
            c = -0.162;
        };
        if (btag > 6.0 && btag < 7.0)
        {
            a = 0.880;
            b = -130.84;
            c = -0.170;
        };
        if (btag > 7.0 && btag < 10.0)
        {
            a = 0.892;
            b = -93.41;
            c = -0.159;
        };
        if (btag > 10.0 )
        {
            a = 0.886;
            b = -65.11;
            c = -0.144;
        };
    }
    prob = a * exp(b * exp(c * pt));
    return prob;
}

double SingleTopSystematicsTreesDumper_tW::jetprobold(double pt, double btag, double eta, string syst)
{
    double prob = 1.;

    if (fabs(eta) > 2.6) return 0.;
    //PT turnOn
    if (syst == "JetTrig1Up")
    {

        if (eta < -1.4)prob = 0.981 * exp(-37.49 * exp(-0.158 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.51 * exp(-0.146 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.63 * exp(-0.145 * pt));
        if (eta > 1.4)prob = 0.984 * exp(-42.17 * exp(-0.158 * pt));
        ;
    }
    else if (syst == "JetTrig2Up")
    {
        if (eta < -1.4)prob = 0.982 * exp(-41.17 * exp(-0.161 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.983 * exp(-27.03 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.983 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.986 * exp(-45.11 * exp(-0.161 * pt));
        ;
    }
    else if (syst == "JetTrig3Up")
    {
        if (eta < -1.4)prob = 0.981 * exp(-41.17 * exp(-0.162 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.03 * exp(-0.146 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.985 * exp(-45.11 * exp(-0.161 * pt));

        prob = 0.982 * exp(-30.6 * exp(-0.151 * pt));
        ;
    }
    else if (syst == "JetTrig1Down")
    {
        if (eta < -1.4)prob = 0.981 * exp(-44.84 * exp(-0.164 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-26.56 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.983 * exp(-25.72 * exp(-0.147 * pt));
        if (eta > 1.4)prob = 0.985 * exp(-48.05 * exp(-0.164 * pt))
                                 ;
    }
    else if (syst == "JetTrig2Down")
    {
        if (eta < -1.4)prob = 0.98 * exp(-41.17 * exp(-0.161 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.03 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.984 * exp(-45.11 * exp(-0.161 * pt));

        ;
    }
    else if (syst == "JetTrig3Down")
    {
        if (eta < -1.4)prob = 0.981 * exp(-41.17 * exp(-0.161 * pt));
        if (eta > -1.4 && eta < 0)prob = 0.982 * exp(-27.03 * exp(-0.147 * pt));
        if (eta < 1.4 && eta > 0)prob = 0.982 * exp(-26.18 * exp(-0.146 * pt));
        if (eta > 1.4)prob = 0.985 * exp(-45.11 * exp(-0.16 * pt));

        ;
    }
    else prob = 0.982 * exp(-30.6 * exp(-0.151 * pt));


    //BTag turnOn
    if (syst == "BTagTrig1Up")
    {
        prob *= 0.85 * exp(-6.35 * exp(-0.681 * btag));
    }
    else if (syst == "BTagTrig1Down")
    {
        prob *= 0.839 * exp(-7.1 * exp(-0.759 * btag));
    }
    else if (syst == "BTagTrig2Up")
    {
        prob *= 0.824 * exp(-6.72 * exp(-0.733 * btag));
    }
    else if (syst == "BTagTrig2Down")
    {
        prob *= 0.865 * exp(-6.73 * exp(-0.707 * btag));
    }
    else if (syst == "BTagTrig3Up")
    {
        prob *= 0.838 * exp(-6.73 * exp(-0.71 * btag));
    }
    else if (syst == "BTagTrig3Down")
    {
        prob *= 0.851 * exp(-6.72 * exp(-0.73 * btag));
    }
    else prob *= 0.844 * exp((-6.72 * exp(-0.720 * btag)));

    return prob;

}

double SingleTopSystematicsTreesDumper_tW::bTagSF(int B)
{
    //  cout<< " B " << " ntchhpt "<<   ntchpt_tags << " jsfshpt size "<<
    //  jsfshpt.size() << " ntchel " << ntchel_tags<< " jsfshel size " << jsfshel.size()<<endl;

    if (algo_ == "TCHPT")
    {
        if (B == 0 || B == 3)
        {
            return b_tchpt_0_tags.weight(jsfshpt, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
        }
        if (B == 1 || B == 4)
        {
            return b_tchpt_1_tag.weight(jsfshpt, ntchpt_tags);
        }
        if (B == 2 || B == 5)
        {
            return b_tchpt_2_tags.weight(jsfshpt, ntchpt_tags);
        }
    }

    if(doLooseBJetVeto_){
     if(B==1 || B == 4) return b_csvt_1_tag.weightWithVeto(jsfscsvt,ncsvt_tags,jsfscsvm,ncsvl_tags);
    }


    if (B == 0 || B == 3)
    {
        return b_csvt_0_tags.weight(jsfscsvt, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
    }
    if (B == 1 || B == 4)
    {
        return b_csvt_1_tag.weight(jsfscsvt, ncsvt_tags);
    }
    if (B == 2 || B == 5)
    {
        return b_csvt_2_tags.weight(jsfscsvt, ncsvt_tags);
    }
    return 1.;
}


/*double SingleTopSystematicsTreesDumper_tW::vetoSF(int B, string syst){

  if (B==1 || B==4){

    return 1;
  }

  return 1;
  }*/

double SingleTopSystematicsTreesDumper_tW::bTagSF(int B, string syst)
{
    //  cout<< " B " << " ntchhpt "<<   ntchpt_tags << " jsfshpt size "<<
    // jsfshpt.size() << " ntchel " << ntchel_tags<< " jsfshel size " << jsfshel.size()<<endl;
    if (algo_ == "TCHPT")
    {
        if (B == 0 || B == 3)
        {
            if (syst == "BTagUp")    return b_tchpt_0_tags.weight(jsfshpt_b_tag_up, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_up,ntchel_tags);
            if (syst == "BTagDown")    return b_tchpt_0_tags.weight(jsfshpt_b_tag_down, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_down,ntchel_tags);
            if (syst == "MisTagUp")    return b_tchpt_0_tags.weight(jsfshpt_mis_tag_up, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_up,ntchel_tags);
            if (syst == "MisTagDown")    return b_tchpt_0_tags.weight(jsfshpt_mis_tag_down, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_down,ntchel_tags);
            return b_tchpt_0_tags.weight(jsfshpt, ntchpt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
        }
        if (B == 1 || B == 4)
        {

            if (syst == "BTagUp")    return b_tchpt_1_tag.weight(jsfshpt_b_tag_up, ntchpt_tags);
            if (syst == "BTagDown")    return b_tchpt_1_tag.weight(jsfshpt_b_tag_down, ntchpt_tags);
            if (syst == "MisTagUp")    return b_tchpt_1_tag.weight(jsfshpt_mis_tag_up, ntchpt_tags);
            if (syst == "MisTagDown")    return b_tchpt_1_tag.weight(jsfshpt_mis_tag_down, ntchpt_tags);

            return b_tchpt_1_tag.weight(jsfshpt, ntchpt_tags);
        }
        if (B == 2 || B == 5)
        {

            if (syst == "BTagUp")    return b_tchpt_2_tags.weight(jsfshpt_b_tag_up, ntchpt_tags);
            if (syst == "BTagDown")    return b_tchpt_2_tags.weight(jsfshpt_b_tag_down, ntchpt_tags);
            if (syst == "MisTagUp")    return b_tchpt_2_tags.weight(jsfshpt_mis_tag_up, ntchpt_tags);
            if (syst == "MisTagDown")    return b_tchpt_2_tags.weight(jsfshpt_mis_tag_down, ntchpt_tags);

            return b_tchpt_2_tags.weight(jsfshpt, ntchpt_tags);
        }
    }

    //Loose jet veto:
    if(doLooseBJetVeto_){
      if (B == 1 || B == 4)
	{
	  //	  if(syst ) return b_csvt_1_tag.weightWithVeto(jsfscsvt,ncsvt_tags,jsfscsvm,ncsvl_tags);	  
	  if (syst == "BTagUp")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_b_tag_up, ncsvt_tags,jsfscsvm_b_tag_up, ncsvl_tags);
	  if (syst == "BTagDown")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_b_tag_down, ncsvt_tags,jsfscsvm_b_tag_down, ncsvl_tags);
	  if (syst == "MisTagUp")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_mis_tag_up, ncsvt_tags,jsfscsvm_mis_tag_up, ncsvl_tags);
	  if (syst == "MisTagDown")    return b_csvt_1_tag.weightWithVeto(jsfscsvt_mis_tag_down, ncsvt_tags,jsfscsvm_mis_tag_down, ncsvl_tags);

	  return b_csvt_1_tag.weightWithVeto(jsfscsvt,ncsvt_tags,jsfscsvm,ncsvl_tags);	  
	
	}
    }


    //Default case: use csvt

    if (B == 0 || B == 3)
    {
      if (syst == "BTagUp")    return b_csvt_0_tags.weight(jsfscsvt_b_tag_up, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_up,ntchel_tags);
      if (syst == "BTagDown")    return b_csvt_0_tags.weight(jsfscsvt_b_tag_down, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_b_tag_down,ntchel_tags);
      if (syst == "MisTagUp")    return b_csvt_0_tags.weight(jsfscsvt_mis_tag_up, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_up,ntchel_tags);
      if (syst == "MisTagDown")    return b_csvt_0_tags.weight(jsfscsvt_mis_tag_down, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel_mis_tag_down,ntchel_tags);
      return b_csvt_0_tags.weight(jsfscsvt, ncsvt_tags); //*b_tchel_0_tags.weight(jsfshel,ntchel_tags);
    }
    
    if (B == 1 || B == 4)
    {

        if (syst == "BTagUp")    return b_csvt_1_tag.weight(jsfscsvt_b_tag_up, ncsvt_tags);
        if (syst == "BTagDown")    return b_csvt_1_tag.weight(jsfscsvt_b_tag_down, ncsvt_tags);
        if (syst == "MisTagUp")    return b_csvt_1_tag.weight(jsfscsvt_mis_tag_up, ncsvt_tags);
        if (syst == "MisTagDown")    return b_csvt_1_tag.weight(jsfscsvt_mis_tag_down, ncsvt_tags);

        return b_csvt_1_tag.weight(jsfscsvt, ncsvt_tags);
    }
    if (B == 2 || B == 5)
    {

        if (syst == "BTagUp")    return b_csvt_2_tags.weight(jsfscsvt_b_tag_up, ncsvt_tags);
        if (syst == "BTagDown")    return b_csvt_2_tags.weight(jsfscsvt_b_tag_down, ncsvt_tags);
        if (syst == "MisTagUp")    return b_csvt_2_tags.weight(jsfscsvt_mis_tag_up, ncsvt_tags);
        if (syst == "MisTagDown")    return b_csvt_2_tags.weight(jsfscsvt_mis_tag_down, ncsvt_tags);

        return b_csvt_2_tags.weight(jsfscsvt, ncsvt_tags);
    }

    return 1.;
}


double SingleTopSystematicsTreesDumper_tW::pileUpSF(string syst,string run)
{

    //  if(syst=="PUUp" )return LumiWeightsUp_.weight3D( *nm1,*n0,*np1);
    //if(syst=="PUDown" )return LumiWeightsDown_.weight3D( *nm1,*n0,*np1);
    //return LumiWeights_.weight3D( *nm1,*n0,*np1);

  if (run == "A"){
    if (syst == "PUUp" )return LumiWeightsAUp_.weight( *n0);
    if (syst == "PUDown" )return LumiWeightsADown_.weight( *n0);
    return LumiWeightsA_.weight( *n0);
  }
  if (run == "B"){
    if (syst == "PUUp" )return LumiWeightsBUp_.weight( *n0);
    if (syst == "PUDown" )return LumiWeightsBDown_.weight( *n0);
    return LumiWeightsB_.weight( *n0);
  }
  if (run == "C"){
    if (syst == "PUUp" )return LumiWeightsCUp_.weight( *n0);
    if (syst == "PUDown" )return LumiWeightsCDown_.weight( *n0);
    return LumiWeightsC_.weight( *n0);
  }
  if (run == "D"){
    if (syst == "PUUp" )return LumiWeightsDUp_.weight( *n0);
    if (syst == "PUDown" )return LumiWeightsDDown_.weight( *n0);
    return LumiWeightsD_.weight( *n0);
  }

  return 1;
}

double SingleTopSystematicsTreesDumper_tW::pileUpSFNew()
{
   return NewPUWeights_.weight(npv);
}


double SingleTopSystematicsTreesDumper_tW::resolSF(double eta, string syst)
{
//     double fac = 0.;
//     if (syst == "JERUp")fac = 1.;
//     if (syst == "JERDown")fac = -1.;
//     if (eta <= 0.5) return 0.05 + 0.06 * fac;
//     else if ( eta > 0.5 && eta <= 1.1 ) return 0.06 + 0.06 * fac;
//     else if ( eta > 1.1 && eta <= 1.7 ) return 0.1 + 0.06 * fac;
//     else if ( eta > 1.7 && eta <= 2.3 ) return 0.13 + 0.1 * fac;
//     else if ( eta > 2.3 && eta <= 5. ) return 0.29 + 0.2 * fac;
//     return 0.1;

//     if (syst == "JERDown"){
//       if (eta <= 1.1) return -0.006;
//       else if (eta <= 1.7) return 0.129;
//       else if (eta <= 2.3) return 0.011;
//       else return 0.1461;
//     }
//     else if (syst == "JERDown"){
//       if (eta <= 1.1) return 0.136;
//       else if (eta <= 1.7) return 0.251;
//       else if (eta <= 2.3) return 0.176;
//       else return 0.356;
//     }
//     else {
//       if (eta <= 1.1) return 0.066;
//       else if (eta <= 1.7) return 0.191;
//       else if (eta <= 2.3) return 0.096;
//       else return 0.166;
//     }


//     if (syst == "JERDown"){
//       if (eta <= 1.1) return -0.00634;
//       else if (eta <= 1.7) return 0.1262;
//       else if (eta <= 2.3) return 0.0059;
//       else return 0.1122;
//     }
//     else if (syst == "JERDown"){
//       if (eta <= 1.1) return 0.1363;
//       else if (eta <= 1.7) return 0.254;
//       else if (eta <= 2.3) return 0.1814;
//       else return 0.3625;
//     }
//     else {
//       if (eta <= 1.1) return 0.066;
//       else if (eta <= 1.7) return 0.191;
//       else if (eta <= 2.3) return 0.096;
//       else return 0.166;
//     }

    if (syst == "JERDown"){
      if (eta <= 0.5) return -0.01;
      else if (eta <= 1.1) return 0.001;
      else if (eta <= 1.7) return 0.032;
      else if (eta <= 2.3) return 0.042;
      else return 0.089;
    }
    else if (syst == "JERUp"){
      if (eta <= 0.5) return 0.115;
      else if (eta <= 1.1) return 0.114;
      else if (eta <= 1.7) return 0.161;
      else if (eta <= 2.3) return 0.228;
      else return 0.488;
    }
    else {
      if (eta <= 0.5) return 0.052;
      else if (eta <= 1.1) return 0.57;
      else if (eta <= 1.7) return 0.096;
      else if (eta <= 2.3) return 0.134;
      else return 0.288;
    }

    

}


//BTag weighter
bool SingleTopSystematicsTreesDumper_tW::BTagWeight::filter(int t)
{
    return (t >= minTags && t <= maxTags);
}

float SingleTopSystematicsTreesDumper_tW::BTagWeight::weight(vector<JetInfo> jets, int tags)
{
    if (!filter(tags))
    {
        //   std::cout << "nThis event should not pass the selection, what is it doing here?" << std::endl;
        return 0;
    }
    int njets = jets.size();
    int comb = 1 << njets;
    float pMC = 0;
    float pData = 0;
    for (int i = 0; i < comb; i++)
    {
        float mc = 1.;
        float data = 1.;
        int ntagged = 0;
        for (int j = 0; j < njets; j++)
        {
            bool tagged = ((i >> j) & 0x1) == 1;
            if (tagged)
            {
                ntagged++;
                mc *= jets[j].eff;
                data *= jets[j].eff * jets[j].sf;
            }
            else
            {
                mc *= (1. - jets[j].eff);
                data *= (1. - jets[j].eff * jets[j].sf);
            }
        }

        if (filter(ntagged))
        {
            //  std::cout << mc << " " << data << endl;
            pMC += mc;
            pData += data;
        }
    }

    if (pMC == 0) return 0;
    return pData / pMC;
}



float SingleTopSystematicsTreesDumper_tW::BTagWeight::weightWithVeto(vector<JetInfo> jetsTags, int tags, vector<JetInfo> jetsVetoes, int vetoes)
{//This function takes into account cases where you have n b-tags and m vetoes, but they have different thresholds. 
    if (!filter(tags))
    {
        //   std::cout << "nThis event should not pass the selection, what is it doing here?" << std::endl;
        return 0;
    }
    int njets = jetsTags.size();
    if(njets != (int)(jetsVetoes.size()))return 0;//jets tags and vetoes must have same size!
    int comb = 1 << njets;
    float pMC = 0;
    float pData = 0;
    for (int i = 0; i < comb; i++)
    {
        float mc = 1.;
        float data = 1.;
        int ntagged = 0;
        for (int j = 0; j < njets; j++)
        {
            bool tagged = ((i >> j) & 0x1) == 1;
            if (tagged)
            {
                ntagged++;
                mc *= jetsTags[j].eff;
                data *= jetsTags[j].eff * jetsTags[j].sf;
            }
            else
            {
                mc *= (1. - jetsVetoes[j].eff);
                data *= (1. - jetsVetoes[j].eff * jetsVetoes[j].sf);
            }
        }

        if (filter(ntagged))
        {
            //  std::cout << mc << " " << data << endl;
            pMC += mc;
            pData += data;
        }
    }

    if (pMC == 0) return 0;
    return pData / pMC;
}


void SingleTopSystematicsTreesDumper_tW::resetWeightsDoubles()
{
    /*  cout << "start doubles removal...";

    for(int bj = 0; bj<=5;++bj){
      for (size_t j = 0; j < systematics.size();++j){
        string syst = systematics[j];

        trees2J[bj][syst]->Branch("weightDoubles",&miscWeightTree);
        int nentries =  trees2J[bj][syst]->GetEntries();

        if(bj==1|| bj==4){

    int idtmp, runtmp;
    map<long int,int> ids;

    for (int i =0; i< nentries;++i){
      trees2J[bj][syst]->GetEntry(i);
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
      //cout << "entries " << trees2J[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  << " weight"<< miscWeightTree<< endl;
      if(trees2J[bj][syst]->GetEntries(cond.c_str())>1){
        ids[idtmp]+=1;
        if(ids[idtmp]>1)miscWeightTree=0;
        //  cout << " found cond "<<endl;
      }
      //cout << "entries after" << trees2J[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  << " weight"<< miscWeightTree<< endl;
      trees2J[bj][syst]->GetBranch("weightDoubles")->Fill();
      //      cout << cond << endl;
      //     cout << "entries " << trees2J[bj][syst]->GetEntries(cond.c_str())<< " idn "<< ids[idtmp]  <<endl;
    }
        }
        else{
    for (int i =0; i< nentries;++i){
      trees2J[bj][syst]->GetEntry(i);
      miscWeightTree = 1.;
      trees2J[bj][syst]->GetBranch("weightDoubles")->Fill();
    }

        }
      }
    }
    */;
}


//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopSystematicsTreesDumper_tW);
