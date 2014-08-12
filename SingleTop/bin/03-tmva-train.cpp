#include "TFile.h"
#include "TTree.h"
#include "TMVA/Factory.h"
#include "TCut.h"
using namespace std;
int main(){

  std::map<string, std::map< string, map<string, TTree*> > > channelSystMap ;
  std::vector<string>  channels, systematics, variables;
  systematics.push_back("noSyst");
  //  systematics.push_back("BTagUp");
  //systematics.push_back("BTagDown");
  //  systematics.push_back("MisTagUp");
  //  systematics.push_back("MisTagDown");
  //  systematics.push_back("JESUp");
  //  systematics.push_back("JESDown");
  //  systematics.push_back("PUUp");
  //  systematics.push_back("PUDown");
  //  systematics.push_back("UnclusteredMETUp");
  //  systematics.push_back("UnclusteredMETDown");


  /*  systematics.push_back("WLightUp");
  systematics.push_back("WLightDown");
  systematics.push_back("VqqUp");
  systematics.push_back("VqqDown");
  systematics.push_back("WcUp");
  systematics.push_back("WcDown");
  systematics.push_back("TTBarUp");
  systematics.push_back("TTBarDown");
  systematics.push_back("QCDUp");
  systematics.push_back("QCDDown");
  */ 

  channels.push_back("TChannel");
  channels.push_back("TbarChannel");
  channels.push_back("TWChannel");
  channels.push_back("TbarWChannel");
  channels.push_back("SChannel");
  channels.push_back("SbarChannel");
  channels.push_back("TTBar");
  channels.push_back("WJets_wlight");
  channels.push_back("WJets_wbb");
  channels.push_back("WJets_wcc");
  channels.push_back("WW");
  channels.push_back("WZ");
  channels.push_back("ZZ");
  //  channels.push_back("Vqq_wbb");
  //  channels.push_back("Vqq_wcc");
  channels.push_back("ZJets_wlight");
  channels.push_back("ZJets_wbb");
  channels.push_back("ZJets_wcc");
  channels.push_back("QCDMu");

  channels.push_back("QCD_Pt_20to30_EMEnriched.root");
  channels.push_back("QCD_Pt_30to80_EMEnriched.root");
  channels.push_back("QCD_Pt_80to170_EMEnriched.root");
  channels.push_back("QCD_Pt_20to30_BCtoE.root");
  channels.push_back("QCD_Pt_30to80_BCtoE.root");
  channels.push_back("QCD_Pt_80to170_BCtoE.root");

  //  channels.push_back("QCDMu");
  

  string leptons[2] ={"Mu","Ele"};

  char variableList[][100] = {
    "eta", // 0
    "costhetalj", // 1
    "topMass", // 2
    // "mtwMass", // 3
    //    "charge", // 4
    //    "runid", // 5
    //    "lumiid", // 6
    //    "eventid", // 7
    //    "weight", // 8
    //    "leptonPt", // 9
    //    "leptonPz", // 10
    //    "leptonPhi", // 11
    //    "leptonRelIso", // 12
    //    "fJetPt", // 13
    //    "fJetE", // 14
    //    "fJetPz", // 15
    //    "fJetPhi", // 16
    //    "bJetPt", // 17
    //    "bJetE", // 18
    //    "bJetPz", // 19
    //    "bJetPhi", // 20
    //    "metPt", // 21
    //    "metPhi", // 22
    //    "topPt", // 23
    //    "topPhi", // 24
    //    "topPz", // 25
    //    "topE", // 26
    //    "totalEnergy", // 27
    //    "totalMomentum" // 28
  };

  variables.push_back("eta");
  //variables.push_back("costhetalj");
    variables.push_back("topMass");
  
  // std::map <string,double >var_addresses;
  //  variables.push_back("eta");
  //variables.push_back("topMass");
  
  double eta=-1.,topMass=-1.,weight=-1.,costhetalj=-1,metPt=-1,mtwMass=-1;

  //  string folder = "./";
  string folder = "/tmp/oiorio/";
  //string postfix_file ="_newBTag";
  string postfix_file ="";

    for(std::vector<string>::const_iterator it_s = systematics.begin(); it_s != systematics.end(); ++it_s){
      string syst = (*it_s);

      bool isRate = (
		     syst =="WLightUp" ||
		     syst =="WLightDown" ||
		     syst =="VqqUp" ||
		     syst =="VqqDown" ||
		     syst =="WcUp" ||
		     syst =="WcDown" ||
		     syst =="TTBarUp" ||
		     syst =="TTBarDown" ||
		     syst =="QCDUp" ||
		     syst =="QCDDown" 
		     );
      

      for (int lep = 0; lep <2;++lep){
	string lepton = leptons[lep];
	TString tmvaName = "tmva" + syst +"_" + lepton;
	TString fileName = tmvaName +".root";
	
	TFile *file = new TFile(fileName, "RECREATE");
	TMVA::Factory factory(tmvaName, file, "");
		
	for(std::vector<string>::const_iterator it = channels.begin(); it != channels.end(); ++it){
	  string channel = (*it);
	  string filename = (folder + "/"+channel+postfix_file+".root");
	  string treename = (channel+"_"+syst);
	  
	  channelSystMap[channel][syst][lepton] = new TTree(treename.c_str(),treename.c_str());
	  
	  channelSystMap[channel][syst][lepton]->Branch("eta",&eta); 
	  channelSystMap[channel][syst][lepton]->Branch("costhetalj",&costhetalj); 
	  channelSystMap[channel][syst][lepton]->Branch("topMass",&topMass); 
	  channelSystMap[channel][syst][lepton]->Branch("mtwMass",&mtwMass); 
	  channelSystMap[channel][syst][lepton]->Branch("metPt",&metPt); 
	  channelSystMap[channel][syst][lepton]->Branch("weight",&weight); 
	  
	  TFile f(filename.c_str(),"OPEN");
	  if( !f.IsOpen() ){
	    cout<< " WARNING FILE " << filename << endl;
	    continue;
	  }
	  bool isW = ( channel == "WJets_wlight" ||
		       channel == "WJets_wcc" ||
		       channel == "WJets_wbb" ||
		       channel == "Wc_wc" ||
		       channel == "Vqq_wbb" ||
		       channel == "Vqq_wcc" 
		       );		       
  
	  string path = "Trees"+lepton+"/"+channel+"_"+syst;      
	  string pathNoSyst = "Trees"+lepton+"/"+channel+"_noSyst";      
	  //channelSystMap[channel][syst][lepton] = ((TTree*)f.Get(path.c_str()))->CopyTree("");
	  //channelSystMap[channel][syst][lepton] = (TTree*)f.Get(path.c_str());
	  if(isRate){
	    channelSystMap[channel][syst][lepton]->CopyAddresses((TTree*)f.Get(pathNoSyst.c_str()));
	    channelSystMap[channel][syst][lepton]->CopyEntries((TTree*)f.Get(pathNoSyst.c_str()));
	  }
	  else{
	    channelSystMap[channel][syst][lepton]->CopyAddresses((TTree*)f.Get(path.c_str()));
	    channelSystMap[channel][syst][lepton]->CopyEntries((TTree*)f.Get(path.c_str()));
	  }
	  
	  if(channel == "TChannel" || channel == "TbarChannel"){  factory.AddSignalTree(channelSystMap[channel][syst][lepton]);}
	  else{factory.AddBackgroundTree(channelSystMap[channel][syst][lepton]);}
	  //if(channel == "TChannel"){  factory.AddSignalTree(dynamic_cast<TTree*>(f.Get(path.c_str())));}
	  //else{factory.AddBackgroundTree(dynamic_cast<TTree*>(f.Get(path.c_str())));}
	  
	}
      
	for(std::vector<string>::const_iterator it_v = variables.begin(); it_v != variables.end(); ++it_v){
	  string var = (*it_v);
	  factory.AddVariable(var.c_str(), 'F');
	  if(lepton =="Mu") factory.SetWeightExpression("weight*(mtwMass>40)");
	  if(lepton =="Ele") factory.SetWeightExpression("weight*(metPt>35)");
	  //	 else  factory.SetWeightExpression("weight*31314./24170.");
	}
      	cout << " test signal channel " << channelSystMap["TChannel"][syst][lepton]<< " syst "<< syst<< endl;
	//	cout << " test ttbar channel " << channelSystMap["TTBar"][syst][lepton]<< " syst "<< syst << endl;

	cout << " test signal channel entries " << channelSystMap["TChannel"][syst][lepton]->GetEntries()<< " syst "<< syst<< endl;
	//	cout << " test ttbar channel entries " << channelSystMap["TTBar"][syst][lepton]->GetEntries()<< " syst "<< syst << endl;

	//	cout << " test ttbar channel eta entries " << channelSystMap["TTBar"][syst][lepton]->GetBranch("eta")->GetEntries()<< " syst "<< syst << endl;
	TCut preselection = "";
	factory.PrepareTrainingAndTestTree(preselection, TString("nTrain_Signal=0:nTrain_Background=0:nTest_Signal=0:nTest_Background=0:SplitMode=Random:VerboseLevel=Info"));
	
	factory.BookMethod(TMVA::Types::kLikelihood, "Likelihood", "H:V:!TransformOutput:PDFInterpol=Spline2:NSmooth=5:VarTransform=Decorrelate");
	//  factory.BookMethod(TMVA::Types::kFisher, "Fisher", "Method=Fisher");
	//  factory.BookMethod(TMVA::Types::kMLP, "MLP", "H:V:NCycles=200:HiddenLayers=N+2:VarTransform=N:NeuronType=tanh:LearningRate=0.0
	//2:DecayRate=0.01:TestRate=5:TrainingMethod=BFGS");
	//  factory.BookMethod(TMVA::Types::kBDT, "BDT", "nTrees=200");
	cout<<" test1 "<<endl;
	factory.TrainAllMethods();
	cout<<" test2 "<<endl;
	factory.TestAllMethods();
	cout<<" test3 "<<endl;
	factory.EvaluateAllMethods();
	cout<<" test4"<<endl<<endl<<endl<< " test "<<endl;
	file->Close();
      }
    }
    
    




  //factory.AddVariable("eta", 'F');
  //factory.AddVariable("costhetalj", 'F');

  //factory->SetWeightExpression( "sqrt(eta/costhetalj)" );


  //efficiencies("tmva_out.root", 2, kTRUE, selVars);
}

