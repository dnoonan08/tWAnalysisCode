/*
*\Author:  O.Iorio
*
*
*
*\version  $Id: SingleTopSystematicsDumper.cc,v 1.4 2011/04/23 22:59:20 oiorio Exp $ 
*/
// This analyzer dumps the histograms for all systematics listed in the cfg file 
//
//
//

#define DEBUG    0 // 0=false
#define MC_DEBUG 0 // 0=false   else -> dont process preselection
#define C_DEBUG  0 // currently debuging

#include "TopQuarkAnalysis/SingleTop/interface/SingleTopSystematicsDumper.h"
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


#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h";
#include "TopQuarkAnalysis/SingleTop/interface/EquationSolver.h"

SingleTopSystematicsDumper::SingleTopSystematicsDumper(const edm::ParameterSet& iConfig)
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
  loosePtCut = channelInfo.getUntrackedParameter<double>("loosePtCut",30); 


  leptonsPx_ =  iConfig.getParameter< edm::InputTag >("leptonsPx");
  leptonsPy_ =  iConfig.getParameter< edm::InputTag >("leptonsPy");
  leptonsPz_ =  iConfig.getParameter< edm::InputTag >("leptonsPz");
  leptonsEnergy_ =  iConfig.getParameter< edm::InputTag >("leptonsEnergy");
  leptonsCharge_ =  iConfig.getParameter< edm::InputTag >("leptonsCharge");

  jetsPz_ =  iConfig.getParameter< edm::InputTag >("jetsPz");
  jetsPx_ =  iConfig.getParameter< edm::InputTag >("jetsPx");
  jetsPy_ =  iConfig.getParameter< edm::InputTag >("jetsPy");
  jetsEnergy_ =  iConfig.getParameter< edm::InputTag >("jetsEnergy");
  
  jetsBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsBTagAlgo");
  jetsAntiBTagAlgo_ =  iConfig.getParameter< edm::InputTag >("jetsAntiBTagAlgo");
  jetsFlavour_ =  iConfig.getParameter< edm::InputTag >("jetsFlavour");

  METPhi_ =  iConfig.getParameter< edm::InputTag >("METPhi");
  METPt_ =  iConfig.getParameter< edm::InputTag >("METPt");
  
  //  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  //  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  UnclMETPx_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPx");
  UnclMETPy_ =  iConfig.getParameter< edm::InputTag >("UnclusteredMETPy");
  
  jetsCorrTotal_ =  iConfig.getParameter< edm::InputTag >("jetsCorrTotal");
  
  //  jetsPF_ =  iConfig.getParameter< edm::InputTag >("patJets");
  
  systematics.push_back("noSyst");
  
  Service<TFileService> fs;
  
  TFileDirectory SingleTopSystematics = fs->mkdir( "systematics_histograms" );
  TFileDirectory SingleTopTrees = fs->mkdir( "systematics_trees" );
  
  std::vector<std::string> all_syst = systematics;
  
  for(size_t i = 0; i < rate_systematics.size();++i){
    all_syst.push_back(rate_systematics.at(i));  
  }
  
  for(size_t i = 0; i < all_syst.size();++i){
    
    string syst = all_syst[i];
    
    TopMass[syst] = SingleTopSystematics.make<TH1F>(("TopMass_"+syst+"_"+channel).c_str(),("TopMass_"+syst+"_"+channel).c_str(),400,0,400);
    CosThetaLJ[syst] = SingleTopSystematics.make<TH1F>(("CosThetaLJ_"+syst+"_"+channel).c_str(),("CosThetaLJ_"+syst+"_"+channel).c_str(),100,-1,1);
    ForwardJetEta[syst] = SingleTopSystematics.make<TH1F>(("ForwardJetEta_"+syst+"_"+channel).c_str(),("ForwardJetEta_"+syst+"_"+channel).c_str(),100,0,5);
    MTW[syst] = SingleTopSystematics.make<TH1F>(("MTW_"+syst+"_"+channel).c_str(),("MTW_"+syst+"_"+channel).c_str(),200,0,200);
    CosThetaLJWSample[syst] = SingleTopSystematics.make<TH1F>(("CosThetaLJWSample_"+syst+"_"+channel).c_str(),("CosThetaLJWSample_"+syst+"_"+channel).c_str(),100,-1,1);
    ForwardJetEtaWSample[syst] = SingleTopSystematics.make<TH1F>(("ForwardJetEtaWSample_"+syst+"_"+channel).c_str(),("ForwardJetEtaWSample_"+syst+"_"+channel).c_str(),100,0,5);
    MTWWSample[syst] = SingleTopSystematics.make<TH1F>(("MTWWSample_"+syst+"_"+channel).c_str(),("MTWWSample_"+syst+"_"+channel).c_str(),200,0,200);
    TopMassWSample[syst] = SingleTopSystematics.make<TH1F>(("TopMassWSample_"+syst+"_"+channel).c_str(),("TopMassWSample_"+syst+"_"+channel).c_str(),400,0,400);

    //Asymmetry
    
    TopMassPlus[syst] = SingleTopSystematics.make<TH1F>(("TopMassPlus_"+syst+"_"+channel).c_str(),("TopMassPlus_"+syst+"_"+channel).c_str(),400,0,400);
    CosThetaLJPlus[syst] = SingleTopSystematics.make<TH1F>(("CosThetaLJPlus_"+syst+"_"+channel).c_str(),("CosThetaLJPlus_"+syst+"_"+channel).c_str(),100,-1,1);
    ForwardJetEtaPlus[syst] = SingleTopSystematics.make<TH1F>(("ForwardJetEtaPlus_"+syst+"_"+channel).c_str(),("ForwardJetEtaPlus_"+syst+"_"+channel).c_str(),100,0,5);
    MTWPlus[syst] = SingleTopSystematics.make<TH1F>(("MTWPlus_"+syst+"_"+channel).c_str(),("MTWPlus_"+syst+"_"+channel).c_str(),400,0,400);
    CosThetaLJWSamplePlus[syst] = SingleTopSystematics.make<TH1F>(("CosThetaLJWSamplePlus_"+syst+"_"+channel).c_str(),("CosThetaLJWSamplePlus_"+syst+"_"+channel).c_str(),100,-1,1);
    ForwardJetEtaWSamplePlus[syst] = SingleTopSystematics.make<TH1F>(("ForwardJetEtaWSamplePlus_"+syst+"_"+channel).c_str(),("ForwardJetEtaWSamplePlus_"+syst+"_"+channel).c_str(),100,0,5);
    MTWWSamplePlus[syst] = SingleTopSystematics.make<TH1F>(("MTWWSamplePlus_"+syst+"_"+channel).c_str(),("MTWWSamplePlus_"+syst+"_"+channel).c_str(),200,0,200);
    TopMassWSamplePlus[syst] = SingleTopSystematics.make<TH1F>(("TopMassWSamplePlus_"+syst+"_"+channel).c_str(),("TopMassWSamplePlus_"+syst+"_"+channel).c_str(),400,0,400);

    
    TopMassMinus[syst] = SingleTopSystematics.make<TH1F>(("TopMassMinus_"+syst+"_"+channel).c_str(),("TopMassMinus_"+syst+"_"+channel).c_str(),400,0,400);
    CosThetaLJMinus[syst] = SingleTopSystematics.make<TH1F>(("CosThetaLJMinus_"+syst+"_"+channel).c_str(),("CosThetaLJMinus_"+syst+"_"+channel).c_str(),100,-1,1);
    ForwardJetEtaMinus[syst] = SingleTopSystematics.make<TH1F>(("ForwardJetEtaMinus_"+syst+"_"+channel).c_str(),("ForwardJetEtaMinus_"+syst+"_"+channel).c_str(),100,0,5);
    MTWMinus[syst] = SingleTopSystematics.make<TH1F>(("MTWMinus_"+syst+"_"+channel).c_str(),("MTWMinus_"+syst+"_"+channel).c_str(),200,0,200);
    CosThetaLJWSampleMinus[syst] = SingleTopSystematics.make<TH1F>(("CosThetaLJWSampleMinus_"+syst+"_"+channel).c_str(),("CosThetaLJWSampleMinus_"+syst+"_"+channel).c_str(),100,-1,1);
    ForwardJetEtaWSampleMinus[syst] = SingleTopSystematics.make<TH1F>(("ForwardJetEtaWSampleMinus_"+syst+"_"+channel).c_str(),("ForwardJetEtaWSampleMinus_"+syst+"_"+channel).c_str(),100,0,5);
    MTWWSampleMinus[syst] = SingleTopSystematics.make<TH1F>(("MTWWSampleMinus_"+syst+"_"+channel).c_str(),("MTWWSampleMinus_"+syst+"_"+channel).c_str(),200,0,200);
    TopMassWSampleMinus[syst] = SingleTopSystematics.make<TH1F>(("TopMassWSampleMinus_"+syst+"_"+channel).c_str(),("TopMassWSampleMinus_"+syst+"_"+channel).c_str(),400,0,400);
  }



  JEC_PATH = "CondFormats/JetMETObjects/data/";
  fip = edm::FileInPath(JEC_PATH+"Spring10_Uncertainty_AK5PF.txt");
  jecUnc = new JetCorrectionUncertainty(fip.fullPath());
  JES_SW = 0.015;
  JES_b_cut = 0.02;
  JES_b_overCut = 0.03;

  //  cout<< "I work for now but I do nothing. But again, if you gotta do nothing, you better do it right. To prove my good will I will provide you with somse numbers later."<<endl;
}

void SingleTopSystematicsDumper::analyze(const Event& iEvent, const EventSetup& iSetup)
{
  
  iEvent.getByLabel(leptonsPz_,leptonsPz);
  iEvent.getByLabel(leptonsPx_,leptonsPx);
  iEvent.getByLabel(leptonsPy_,leptonsPy);
  iEvent.getByLabel(leptonsEnergy_,leptonsEnergy);
  iEvent.getByLabel(leptonsCharge_,leptonsCharge);
  
  iEvent.getByLabel(jetsPz_,jetsPz);
  iEvent.getByLabel(jetsPx_,jetsPx);
  iEvent.getByLabel(jetsPy_,jetsPy);

  iEvent.getByLabel(jetsEnergy_,jetsEnergy);
  iEvent.getByLabel(jetsBTagAlgo_,jetsBTagAlgo);
  iEvent.getByLabel(jetsAntiBTagAlgo_,jetsAntiBTagAlgo);
  iEvent.getByLabel(jetsFlavour_,jetsFlavour);
  iEvent.getByLabel(jetsCorrTotal_,jetsCorrTotal);
  iEvent.getByLabel(METPhi_,METPhi);
  iEvent.getByLabel(METPt_,METPt);

  iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHPT",perfHP);
  iSetup.get<BTagPerformanceRecord>().get("MISTAGTCHEL",perfHE);
  
  BinningPointByMap measurePoint;
   
  //    measurePoint.insert(BinningVariables::JetEt,950);
  //   measurePoint.insert(BinningVariables::JetAbsEta,0.6);
  
  //   std::cout << "Is it OK? HPT Mistag " << perfHP->isResultOk(PerformanceResult::BTAGLEFF, measurePoint)
  //     << " result at 200 GeV, 0,6 |eta| " << perfHP->getResult( PerformanceResult::BTAGLEFF, measurePoint)
  //     << std::endl;
   
  //   measurePoint.reset();

   
  
  float metPx = 0; 
  float metPy = 0;
  
  metPx = METPt->at(0)*cos(METPhi->at(0));
  metPy = METPt->at(0)*sin(METPhi->at(0));

  float metPxTmp = metPx; 
  float metPyTmp = metPy;



  size_t nLeptons = leptonsPx->size();
  size_t nJets = jetsPx->size();
  
  double WeightLumi = finalLumi*crossSection/originalEvents;
  double BTagWeight = 1;
  double BTagWeightWSample = 1;
  double BTagWeightTTSample = 1;
  double Weight = 1;
  double MTWValue =0;
  
  float ptCut = 30;  
  if(channel=="Data")WeightLumi=1;
  
  for(size_t s = 0; s < systematics.size();++s){
    string syst_name =  systematics.at(s);
    
    Weight = WeightLumi;
    BTagWeight = 1;
    BTagWeightWSample = 1;
    BTagWeightTTSample = 1;
    
    //Setup for systematics

    
    double TCHP_CTag = BScaleFactor("TCHP_C",syst_name);
    double TCHP_BTag = BScaleFactor("TCHP_B",syst_name);
    
    double TCHE_CTag = BScaleFactor("TCHE_C",syst_name);
    double TCHE_BTag = BScaleFactor("TCHE_B",syst_name);

    //    double TCHP_MisTag = 1.4; //
    //    double TCHE_MisTag = 1.0; //DummyValues, to be changed in the next part of the code
    
    //    cout << " TCHP_BTag should be 0.9 "<< TCHP_BTag <<endl;    
    
    
    leptons.clear();
    jets.clear();
    bjets.clear();
    antibjets.clear();
    //    loosejets.clear();

    MTWValue =0;
    metPx = metPxTmp; 
    metPy = metPyTmp;

    
    int lowestBTagPosition=-1;
    double lowestBTag = 99999;
    
    int highestBTagPosition=-1;
    double highestBTag = -9999;


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
    
    //    cout <<" BTagWeight before "<< BTagWeight << endl;

    float eta;
    float ptCorr;
    int flavour;
    double unc =0;
    
    //    cout << " test 0 " << endl;
    //Loops to apply systematics on jets-leptons
    
    
    for(size_t i = 0;i<nJets;++i){
      //eta = jetsEta->at(i);
      eta = (math::XYZTLorentzVector(jetsPx->at(i),jetsPy->at(i),jetsPz->at(i),jetsEnergy->at(i) ) ).eta();
      ptCorr = sqrt(jetsPx->at(i)*jetsPx->at(i)+jetsPy->at(i)*jetsPy->at(i));
      flavour = jetsFlavour->at(i);
      
      bool passesPtCut = ptCorr>ptCut;
      //bool passesLoosePtCut = ptCorr>loosePtCut;
      if(passesPtCut && syst_name != "JESUp" && syst_name != "JESDown") jets.push_back(math::XYZTLorentzVector(jetsPx->at(i),jetsPy->at(i),jetsPz->at(i),jetsEnergy->at(i) ) ); 
      //if(passesLoosePtCut && syst_name != "JESUp" && syst_name != "JESDown") loosejets.push_back(math::XYZTLorentzVector(jetsPx->at(i),jetsPy->at(i),jetsPz->at(i),jetsEnergy->at(i)) );   
      else if(syst_name == "JESUp"){
	unc = jetUncertainty( eta,  ptCorr, flavour);
	passesPtCut = ptCorr * (1+unc) >ptCut;
	//passesLoosePtCut = ptCorr * (1+unc) > loosePtCut;
	metPx-=jetsPx->at(i)*unc;
	metPy-=jetsPy->at(i)*unc;
	if(passesPtCut) jets.push_back(math::XYZTLorentzVector(jetsPx->at(i) * (1+unc),jetsPy->at(i) * (1+unc),jetsPz->at(i) * (1+unc),jetsEnergy->at(i) * (1+unc)) ); 
	//if(passesLoosePtCut) loosejets.push_back(math::XYZTLorentzVector(jetsPx->at(i) * (1+unc),jetsPy->at(i)*(1+unc),jetsPz->at(i)*(1+unc),jetsEnergy->at(i)*(1+unc)) );   
      }
      else if(syst_name == "JESDown"){
	unc = jetUncertainty( eta,  ptCorr, flavour);
	passesPtCut = ptCorr * (1-unc) > ptCut;
	//passesLoosePtCut = ptCorr * (1-unc) > loosePtCut;
	metPx-= -jetsPx->at(i)*unc;
	metPy-= -jetsPy->at(i)*unc;
	if(passesPtCut) jets.push_back(math::XYZTLorentzVector(jetsPx->at(i) * (1-unc),jetsPy->at(i)*(1-unc),jetsPz->at(i)*(1-unc),jetsEnergy->at(i)*(1-unc)) ); 
	//if(passesLoosePtCut) loosejets.push_back(math::XYZTLorentzVector(jetsPx->at(i) * (1-unc),jetsPy->at(i)*(1-unc),jetsPz->at(i)*(1-unc),jetsEnergy->at(i)*(1-unc)) );   
      }
      //      if(passesPtCut) cout <<" jet "<< i <<" passes pt cut, flavor "<< abs(flavour)<< " syst " << syst_name << " pt "<< ptCorr<< " pt with unc "<< jets.back().pt() <<" unc "<< unc << endl;
      
      bool passesBTag = jetsBTagAlgo->at(i)>3.41;
      bool passesAntiBTag = jetsAntiBTagAlgo->at(i)<1.7;
      //bool passesAntiBTag = jetsBTagAlgo->at(i)<3.41;
      
      
      if(passesPtCut && passesBTag) {
	
	bjets.push_back(jets.back()); 
	
	if(abs(flavour)==4) BTagWeight*=TCHP_CTag ;
	if(abs(flavour)==5) BTagWeight*=TCHP_BTag ;
	if(abs(flavour)<4 && abs(flavour)>0){
	  
	  double etaMin =  min(fabs(eta),(float)2.3999);
	  double ptMin =  min(jets.back().pt(),998.0);
	  
	  measurePoint.insert(BinningVariables::JetAbsEta,etaMin);
	  measurePoint.insert(BinningVariables::JetEt,ptMin);
	  
	  double eff =(perfHP->getResult(PerformanceResult::BTAGLEFF,measurePoint));
	  double SF = (perfHP->getResult(PerformanceResult::BTAGLEFFCORR,measurePoint));
	  double SFErr = (perfHP->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
	  
	  BTagWeight*=  MisTagScaleFactor("TCHP_L",syst_name,SF,eff,SFErr);
	  measurePoint.reset();
	  
	  //	  cout <<" jet "<< i <<" passes direct btag, flavor "<< abs(flavour)<< " b weight " << BTagWeight << " eff "<<  eff<<" SF "<< SF << " sf unc "<< SFErr <<endl;
	}
	//	cout <<" jet "<< i <<" passes direct btag, flavor "<< abs(flavour)<< " b weight " << BTagWeight << endl;
      }
      if(passesPtCut && passesAntiBTag){
	
	antibjets.push_back(jets.back());
	if(abs(flavour)==4) BTagWeight*=TCHE_CTag ;
	if(abs(flavour)==5) BTagWeight*=TCHE_BTag ;
	if(abs(flavour)<4 && abs(flavour)>0){
	  
	  double etaMin =  min(fabs(eta),(float)2.3999);
	  double ptMin =  min(jets.back().pt(),998.0);
	  
	  measurePoint.insert(BinningVariables::JetAbsEta,etaMin);
	  measurePoint.insert(BinningVariables::JetEt,ptMin);
	  
	  double eff =(perfHE->getResult(PerformanceResult::BTAGLEFF,measurePoint));
	  double SF = (perfHE->getResult(PerformanceResult::BTAGLEFFCORR,measurePoint));
	  double SFErr = (perfHE->getResult(PerformanceResult::BTAGLERRCORR,measurePoint));
	  
	  BTagWeight*=  MisTagScaleFactor("TCHE_L",syst_name,SF,eff,SFErr);
	  
	  measurePoint.reset();
	  //	  cout <<" jet "<< i <<" passes anti-btag, flavor "<< abs(flavour)<< " b weight " << BTagWeight << " eff "<<  eff<<" SF "<< SF << " sf unc "<< SFErr <<endl;
	}
      }
      
      //      if(!passesLoosePtCut)continue;
      if(passesPtCut && jetsAntiBTagAlgo->at(i) > highestBTag){
	highestBTag=jetsAntiBTagAlgo->at(i);
	highestBTagPosition=jets.size()-1;
      } 
      
      //if(!passesPtCut)continue;
      if(passesPtCut && jetsAntiBTagAlgo->at(i) < lowestBTag){
	lowestBTag=jetsAntiBTagAlgo->at(i);
	lowestBTagPosition=jets.size()-1;
      }
    }
  
    for(size_t i = 0;i<nLeptons;++i){
      //   float leptonPx = cos(leptonsPhi->at(i))* leptonsPt->at(i);
      //   float leptonPy = sin(leptonsPhi->at(i))* leptonsPt->at(i);
      
      float leptonPx = leptonsPx->at(i);
      float leptonPy = leptonsPy->at(i);
      float leptonPz = leptonsPz->at(i);
      float leptonPt = sqrt(leptonPx*leptonPx + leptonPy*leptonPy);
      
      float leptonP = sqrt( (leptonPt*leptonPt) + (leptonPz*leptonPz));
      float leptonE = leptonsEnergy->at(i);
      leptons.push_back(math::XYZTLorentzVector(leptonPx,leptonPy,leptonsPz->at(i),leptonP));
    }
    
    
    //Part of the effective selection and filling
    if(leptons.size()!=1)return;
    
    if(leptons.size()==1){
      double metPt = sqrt(metPx*metPx+metPy*metPy);
      MTWValue =  sqrt((leptons.at(0).pt()+metPt)*(leptons.at(0).pt()+metPt)  -(leptons.at(0).px()+metPx)*(leptons.at(0).px()+metPx) -(leptons.at(0).py()+metPy)*(leptons.at(0).py()+metPy));
    }

    
    
    //    cout << " test 1 " << endl;
    
    //W control Sample
    
    //    if( lowestBTagPosition > -1 && highestBTagPosition > -1 && jets.size()>=1 && loosejets.size() ==2 &&  bjets.size()==0 ){
    if( lowestBTagPosition > -1 && highestBTagPosition > -1 && jets.size() ==2 &&  bjets.size()==0 ){
      
      //      cout << " test 2 low " <<  lowestBTagPosition << " high "<< highestBTagPosition << " nleptons " << leptons.size() << endl;
      
      //      cout << " syst " <<syst_name <<" histo? "<< MTWWSample[syst_name] <<endl;
      
      MTWWSample[syst_name]->Fill(MTWValue,Weight);
      if(leptonsCharge->at(0)>0)MTWWSamplePlus[syst_name]->Fill(MTWValue,Weight);
      if(leptonsCharge->at(0)<0)MTWWSampleMinus[syst_name]->Fill(MTWValue,Weight);
      if(MTWValue<MTWCut) continue;
      
      
      //      if(highestBTagPosition == lowestBTagPosition)      cout << " test 3: loosejets size "<<jets.size() << " jets size "<<jets.size() << " highestB pos " << highestBTagPosition<< " lowestB pos " << lowestBTagPosition << " highestBTag "<< highestBTag << " lowestBTag  "<< lowestBTag<< endl;
    //      cout << " test 3: loosejets size "<<loosejets.size() << " jets size "<<jets.size() << " highestB pos " << highestBTagPosition<< " lowestB pos " << lowestBTagPosition << endl;
      
      if(highestBTagPosition == lowestBTagPosition)continue;
      
      math::XYZTLorentzVector top = top4Momentum(leptons.at(0),jets.at(highestBTagPosition),metPx,metPy);
      
      //      cout << " test 3 " << endl;
      
      float fCosThetaLJ =  cosThetaLJ(leptons.at(0),jets.at(lowestBTagPosition),top);
      
      //cout << " test 4 " << endl;
      
      TopMassWSample[syst_name]->Fill(top.mass(),Weight);
      CosThetaLJWSample[syst_name]->Fill(fCosThetaLJ,Weight);
      ForwardJetEtaWSample[syst_name]->Fill(fabs(jets.at(0).eta()),Weight);
      ForwardJetEtaWSample[syst_name]->Fill(fabs(jets.at(1).eta()),Weight);
      

      if(leptonsCharge->at(0)>0){
	TopMassWSamplePlus[syst_name]->Fill(top.mass(),Weight);
      CosThetaLJWSamplePlus[syst_name]->Fill(fCosThetaLJ,Weight);
      ForwardJetEtaWSamplePlus[syst_name]->Fill(fabs(jets.at(0).eta()),Weight);
      ForwardJetEtaWSamplePlus[syst_name]->Fill(fabs(jets.at(1).eta()),Weight);
      }
      
      if(leptonsCharge->at(0)<0){
      TopMassWSampleMinus[syst_name]->Fill(top.mass(),Weight);
      CosThetaLJWSampleMinus[syst_name]->Fill(fCosThetaLJ,Weight);
      ForwardJetEtaWSampleMinus[syst_name]->Fill(fabs(jets.at(0).eta()),Weight);
      ForwardJetEtaWSampleMinus[syst_name]->Fill(fabs(jets.at(1).eta()),Weight);
      }
    }
    
    //Signal sample
    if( jets.size()==2 && bjets.size()==1 && antibjets.size()==1){

      //      cout << " passes cuts pre-mtw, syst " << syst_name << " b tag weight " <<  BTagWeight<< " Weight " << Weight  <<endl;
      
      Weight*=BTagWeight;
      
      MTW[syst_name]->Fill(MTWValue,Weight);
      if(leptonsCharge->at(0)>0)MTWPlus[syst_name]->Fill(MTWValue,Weight);
      if(leptonsCharge->at(0)<0)MTWMinus[syst_name]->Fill(MTWValue,Weight);
      if(MTWValue<MTWCut) continue;
      
      math::XYZTLorentzVector top = top4Momentum(leptons.at(0),bjets.at(0),metPx,metPy);
      float fCosThetaLJ =  cosThetaLJ(leptons.at(0), antibjets.at(0), top);

      cout << " passes cuts pre-mtw, syst " << syst_name << " top mass "<< top.mass() << " cosTheta* "<< fCosThetaLJ << " fjetEta " << fabs(antibjets.at(0).eta()) << " top mass integral"  << TopMass[syst_name]->Integral() << " Forward jet eta integral  "<< ForwardJetEta[syst_name]->Integral()<< " CosThetaLJ integral " << CosThetaLJ[syst_name]->Integral()<< " Weight "  << Weight << " B Weight "<< BTagWeight <<endl;

      
      TopMass[syst_name]->Fill(top.mass(),Weight);
      CosThetaLJ[syst_name]->Fill(fCosThetaLJ,Weight);
      //      Weight=Weight/BTagWeight;
      ForwardJetEta[syst_name]->Fill(fabs(antibjets.at(0).eta()),Weight);
      
      if(leptonsCharge->at(0)>0){
	TopMassPlus[syst_name]->Fill(top.mass(),Weight);
	CosThetaLJPlus[syst_name]->Fill(fCosThetaLJ,Weight);
	ForwardJetEtaPlus[syst_name]->Fill(fabs(antibjets.at(0).eta()),Weight);
      }
      
      if(leptonsCharge->at(0)<0){
	TopMassMinus[syst_name]->Fill(top.mass(),Weight);
	CosThetaLJMinus[syst_name]->Fill(fCosThetaLJ,Weight);
	ForwardJetEtaMinus[syst_name]->Fill(fabs(antibjets.at(0).eta()),Weight);
      }
    }
  }
}


float SingleTopSystematicsDumper::cosThetaLJ(math::XYZTLorentzVector lepton, math::XYZTLorentzVector jet, math::XYZTLorentzVector top){
  
  math::XYZTLorentzVector boostedLepton = ROOT::Math::VectorUtil::boost(lepton,top.BoostToCM());
  math::XYZTLorentzVector boostedJet = ROOT::Math::VectorUtil::boost(jet,top.BoostToCM());

  return  ROOT::Math::VectorUtil::CosTheta(boostedJet.Vect(),boostedLepton.Vect());
  
}

math::XYZTLorentzVector SingleTopSystematicsDumper::top4Momentum(math::XYZTLorentzVector lepton, math::XYZTLorentzVector jet, float metPx, float metPy){
  return top4Momentum(lepton.px(),lepton.py(),lepton.pz(),lepton.energy(),jet.px(),jet.py(),jet.pz(),jet.energy(),metPx,metPy);
}

math::XYZTLorentzVector SingleTopSystematicsDumper::top4Momentum(float leptonPx, float leptonPy, float leptonPz, float leptonE, float jetPx, float jetPy, float jetPz,float jetE, float metPx, float metPy){
  //float leptonP = sqrt( (leptonPx*leptonPx)+  (leptonPy*leptonPy) +  (leptonPz*leptonPz));
  float lepton_Pt = sqrt( (leptonPx*leptonPx)+  (leptonPy*leptonPy) );
  
  math::XYZTLorentzVector neutrino = NuMomentum(leptonPx,leptonPy,leptonPz,lepton_Pt,leptonE,metPx,metPy).at(0);
  
  math::XYZTLorentzVector lep(leptonPx,leptonPy,leptonPz,leptonE);
  math::XYZTLorentzVector jet(jetPx,jetPy,jetPz,jetE);
  
  math::XYZTLorentzVector top = lep + jet + neutrino;
  return top;  
}

std::vector<math::XYZTLorentzVector> SingleTopSystematicsDumper::NuMomentum(float leptonPx, float leptonPy, float leptonPz, float leptonPt, float leptonE, float metPx, float metPy ){

    
  double  mW = 80.38;
  
  std::vector<math::XYZTLorentzVector> result;
  
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
    
    result.push_back(p4nu_rec);
    
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
	  
      //      std::cout<<"intermediate solution1 met x "<<metpx << " min px " << p_x  <<" met y "<<metpy <<" min py "<< p_y << std::endl; 

      if(Delta2< deltaMin && Delta2 > 0){deltaMin = Delta2;
      minPx=p_x;
      minPy=p_y;}
      //     std::cout<<"solution1 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
      }
	
	//    } 
  
	//if(usePxPlusSolutions_){
      for( int i =0; i< (int)solutions2.size();++i){
	if(solutions2[i]<0 ) continue;
	double p_x = (solutions2[i]*solutions2[i]-mW*mW)/(4*pxlep); 
	double p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x +mW*ptlep*solutions2[i])/(2*pxlep*pxlep);
	double Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy); 
	//  std::cout<<"intermediate solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
	if(Delta2< deltaMin && Delta2 > 0){deltaMin = Delta2;
	  minPx=p_x;
	  minPy=p_y;}
	//	std::cout<<"solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
      }
      //}
  
    double pyZeroValue= ( mW*mW*pxlep + 2*pxlep*pylep*zeroValue);
    double delta2ZeroValue= (zeroValue-metpx)*(zeroValue-metpx) + (pyZeroValue-metpy)*(pyZeroValue-metpy);
    
    if(deltaMin==14000*14000)return result;    
    //    else std::cout << " test " << std::endl;

    if(delta2ZeroValue < deltaMin){
      deltaMin = delta2ZeroValue;
      minPx=zeroValue;
      minPy=pyZeroValue;}
  
    //    std::cout<<" MtW2 from min py and min px "<< sqrt((minPy*minPy+minPx*minPx))*ptlep*2 -2*(pxlep*minPx + pylep*minPy)  <<std::endl;
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
    
      result.push_back(p4nu_rec);
  }
  return result;    
}



double SingleTopSystematicsDumper::BScaleFactor(string algo,string syst_name){

  double bcentral =0.9;  
  double berr = 0.15;
  double cerr =0.3;
  double tcheeff =0.7;
  
  if(syst_name == "BTagUp"){
    if(algo == "TCHP_B"){
      return bcentral+berr;
    }
    if(algo == "TCHP_C"){
      return bcentral+cerr;
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
      return bcentral-berr;
    }
    if(algo == "TCHP_C"){
      return bcentral-cerr;
    }
  
    if(algo == "TCHE_B"){
      return (1-tcheeff*(bcentral-berr))/(1-tcheeff);
    }
    if(algo == "TCHE_C"){
      return (1-tcheeff*(bcentral-cerr))/(1-tcheeff);
    }
  }

  if(algo == "TCHP_B"){
    return bcentral;
  }
  if(algo == "TCHP_C"){
    return bcentral;
  }
  if(algo == "TCHE_B"){
    return (1-tcheeff*(bcentral))/(1-tcheeff);
  }
  if(algo == "TCHE_C"){
    return (1-tcheeff*(bcentral))/(1-tcheeff);
  }
    
  return 0.9;
}

double SingleTopSystematicsDumper::MisTagScaleFactor(string algo,string syst_name,double sf, double eff, double sferr){
  double mistagcentral = sf;  
  double mistagerr = sferr;
  double tcheeff = eff;

  
  if(syst_name == "MisTagUp"){
    if(algo == "TCHP_L"){
      return mistagcentral+mistagerr;
    }
    if(algo == "TCHE_L"){
      return (1-tcheeff)/(1-tcheeff/(mistagcentral+mistagerr));
    }
    
  }
  
  if(syst_name == "MisTagDown"){
    if(algo == "TCHP_L"){
      return mistagcentral-mistagerr;
    }
    if(algo == "TCHE_L"){
      return (1-tcheeff)/(1-tcheeff/(mistagcentral-mistagerr));
    }
  }

  if(algo == "TCHP_L"){
    return mistagcentral;
  }
  if(algo == "TCHE_L"){
    return (1-tcheeff)/(1-tcheeff/(mistagcentral));
  }
  
  return 0.9;


}


double SingleTopSystematicsDumper::jetUncertainty(double eta, double ptCorr, int flavour){
  jecUnc->setJetEta(eta); 
  jecUnc->setJetPt(ptCorr);
  double JetCorrection = jecUnc->getUncertainty(true); // In principle, boolean controls if uncertainty on +ve or -ve side is returned (asymmetric errors) but not yet implemented.
  bool cut = ptCorr> 50 && ptCorr < 200 && fabs(eta) < 2.0;
  // JES_SW = 0.015;                                                                                                                                 
  double JES_PU=0.75*0.8*2.2/ptCorr;
  double JES_b=0;
  if(abs(flavour)==5);
  if(cut) JES_b = JES_b_cut;
  else JES_b = JES_b_overCut;
  //    float JESUncertaintyTmp = sqrt(JESUncertainty*JESUncertainty + JetCorrection*JetCorrection);                                                 
  return sqrt(JES_b*JES_b + JES_PU*JES_PU +JES_SW*JES_SW + JetCorrection*JetCorrection);
}

void SingleTopSystematicsDumper::endJob(){
  
  for(size_t i = 0; i < rate_systematics.size();++i){
    
    string syst = rate_systematics[i];
    cout <<" topmasstest "<<  TopMass["noSyst"]->Integral()  << endl;

    cout<< " syst  "<< TopMass[syst]->Integral()  <<endl;
    
    TopMass[syst]->Add(TopMass["noSyst"]);
    CosThetaLJ[syst]->Add(CosThetaLJ["noSyst"]); 
    ForwardJetEta[syst]->Add(ForwardJetEta["noSyst"]); 
    MTW[syst]->Add(MTW["noSyst"]); 
    CosThetaLJWSample[syst]->Add(CosThetaLJWSample["noSyst"]); 
    ForwardJetEtaWSample[syst]->Add(ForwardJetEtaWSample["noSyst"]); 
    MTWWSample[syst]->Add(MTWWSample["noSyst"]); 
    TopMassWSample[syst]->Add(TopMassWSample["noSyst"]); 
    
    //Asymmetry
    
    TopMassPlus[syst]->Add(TopMassPlus["noSyst"]); 
    CosThetaLJPlus[syst]->Add(CosThetaLJPlus["noSyst"]); 
    ForwardJetEtaPlus[syst]->Add(ForwardJetEtaPlus["noSyst"]); 
    MTWPlus[syst]->Add(MTWPlus["noSyst"]); 
    CosThetaLJWSamplePlus[syst]->Add(CosThetaLJWSamplePlus["noSyst"]); 
    ForwardJetEtaWSamplePlus[syst]->Add(ForwardJetEtaWSamplePlus["noSyst"]); 
    MTWWSamplePlus[syst]->Add(MTWWSamplePlus["noSyst"]); 
    TopMassWSamplePlus[syst]->Add(TopMassWSamplePlus["noSyst"]); 
    
    TopMassMinus[syst]->Add(TopMassMinus["noSyst"]); 
    CosThetaLJMinus[syst]->Add(CosThetaLJMinus["noSyst"]); 
    ForwardJetEtaMinus[syst]->Add(ForwardJetEtaMinus["noSyst"]); 
    MTWMinus[syst]->Add(MTWMinus["noSyst"]); 
    CosThetaLJWSampleMinus[syst]->Add(CosThetaLJWSampleMinus["noSyst"]); 
    ForwardJetEtaWSampleMinus[syst]->Add(ForwardJetEtaWSampleMinus["noSyst"]); 
    MTWWSampleMinus[syst]->Add(MTWWSampleMinus["noSyst"]); 
    TopMassWSampleMinus[syst]->Add(TopMassWSampleMinus["noSyst"]);

 
  }
}
  



//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopSystematicsDumper);
