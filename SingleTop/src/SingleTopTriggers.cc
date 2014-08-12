#include <memory>
#include <vector>
#include <map>
#include <set>

// user include files
#include "TopQuarkAnalysis/SingleTop/interface/SingleTopTriggers.h"

#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/Frameworkfwd.h"
//#include "FWCore/Framework/interface/EDFilter.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GtFdlWord.h"
#include "DataFormats/L1GlobalTrigger/interface/L1GlobalTriggerReadoutRecord.h"
#include "DataFormats/Common/interface/TriggerResults.h"
#include "FWCore/Common/interface/TriggerNames.h"

using namespace edm;
using namespace std;

SingleTopTriggers::SingleTopTriggers(const edm::ParameterSet& iConfig)
{
  hlTriggerResults_ = iConfig.getParameter<edm::InputTag> ("HLTriggerResults");
  init_ = false;
  triggersList = iConfig.getParameter<std::vector< std::string > >("triggerList");

  runRangesList = iConfig.getParameter<std::vector< int > >("runRangesList");
  
  isMC = iConfig.getUntrackedParameter<bool>("isMC",true);
  channel = iConfig.getUntrackedParameter<int>("channel",1);

  verbose = iConfig.getUntrackedParameter<bool>("verbose",false);

}

SingleTopTriggers::~SingleTopTriggers()
{
}

bool SingleTopTriggers::filter( edm::Event& iEvent,const  edm::EventSetup& c)
{
  
  int ievt = iEvent.id().event();
  int irun = iEvent.id().run();
  int ils = iEvent.luminosityBlock();
  int bx = iEvent.bunchCrossing();
  
  //
  // trigger type
  //
  int trigger_type=-1;
  if (iEvent.isRealData())  trigger_type = iEvent.experimentType();
  
  
  //hlt info
  edm::Handle<TriggerResults> HLTR;

  if(triggersList.size()==1)if(triggersList.at(0)=="" || triggersList.at(0)=="none") return true;

  if(triggersList.size()!= runRangesList.size()) {cout << " warning! trigger list and run ranges list do not match!" <<endl; return false;}

  //  if(isMC)hlTriggerResults_ = edm::InputTag("TriggerResults","","REDIGI311X");
  iEvent.getByLabel(hlTriggerResults_,HLTR);

  
  bool eleNonIso = false;
  bool muonNonIso = false;

  if(HLTR.isValid() == false) {
    std::cout<< " HLTInspect Error - Could not access Results with name "<<hlTriggerResults_<<std::endl;
  }
  if(HLTR.isValid())
    {
      if (!init_) {
	//    init_=true;
	const edm::TriggerNames & triggerNames = iEvent.triggerNames(*HLTR);
	hlNames_=triggerNames.triggerNames();
      }

      //string muonBit;
      //string eleBit;

    
      string tmptrig="";      
      string tmptrig2="";      
      TriggerResults tr;
      tr = *HLTR;
      bool passesTrigger = false;
      bool tmppass=false;
      //      Std::cout << "List of triggers: \n";
      for (unsigned int i=0;i<HLTR->size();++i){

	//	std::cout << " - " <<  hlNames_[i] << "   " << tr.accept(i) << std::endl;
	    	
	tmptrig = hlNames_[i];
	tmppass = tr.accept(i);
	tmptrig.erase(tmptrig.end()-1);
	tmptrig2 = tmptrig;
	tmptrig2.erase(tmptrig2.end()-1);
	
	//	std::cout.width(3); std::cout << i;
	//	std::cout << " - 2" <<  tmptrig << "   " << tmppass << std::endl;
	
	if(!isMC){for(size_t r = 0; r< runRangesList.size();++r){
	    int lowerRange = runRangesList.at(r);
	    int upperRange = -1;
	    //	  if (i ==0) cout <<" runRange "<< r << " lowRange " << lowerRange << " upperRange "<<upperRange << " "<< endl;
	    if(r!=runRangesList.size()-1){
	      upperRange = runRangesList.at(r+1);
	    }  
	    bool isInRange= (irun >= lowerRange && (irun < upperRange || upperRange <0));
	    if (!isInRange)continue;
	    /*for( int j =1; j <= 10 ;++j){
	      stringstream number;
	      //if (i ==0) cout <<" j "<< j<<endl;
	      
	      number << j;
	      string triggerVersion;
	      number >> triggerVersion;
	      
	      //	    if (i ==0) cout <<" triggerVersion "<< triggerVersion<<endl;
	      }*/
	    string trigger = triggersList.at(r);
	    
	    //+ triggerVersion;	  //	    if (i ==0) cout <<" trigger "<< trigger<< " " <<endl;
	    if((tmptrig == trigger) && (tmppass)) { 
	      if (verbose)cout << " run " << irun << " passes trigger "<< trigger << endl; 
	      return true;
	    }
	    if((tmptrig2 == trigger) && (tmppass)){
	      if (verbose)cout << " run " << irun << " passes trigger "<< trigger << endl; 
	      return true;
	    }
	  }
	}
	else{
	  for(size_t r = 0; r< triggersList.size();++r){
	    string trigger =triggersList.at(r); 	
	    if((tmptrig == trigger) && (tmppass)) return true;// muonNonIso =true;
	    if((tmptrig2 == trigger) && (tmppass)) return true;// muonNonIso =true;
	  }
	}
      }
      //	if (muonTrigger){
      //	  cout << "channel Electron BUT Muon trigger " << endl;


	//	  return false;
	//	}
    }
      
    
      
  return false;
}

//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopTriggers);
