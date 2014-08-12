
#ifndef PhysicsTools_Utilities_interface_LumiReWeighting_cc_asd
#define PhysicsTools_Utilities_interface_LumiReWeighting_cc_asd


/**
  \class    LumiReWeighting LumiReWeighting.h "PhysicsTools/Utilities/interface/LumiReWeighting.h"
  \brief    Class to provide lumi weighting for analyzers to weight "flat-to-N" MC samples to data

  This class will trivially take two histograms:
  1. The generated "flat-to-N" distributions from a given processing (or any other generated input)
  2. A histogram generated from the "estimatePileup" macro here:

  https://twiki.cern.ch/twiki/bin/view/CMS/LumiCalc#How_to_use_script_estimatePileup

  and produce weights to convert the input distribution (1) to the latter (2).

  \author Andres Tiko
  
*/
#include "TRandom1.h"
#include "TRandom2.h"
#include "TRandom3.h"
#include "TStopwatch.h"
#include "TH1.h"
#include "TFile.h"
#include <string>
#include <algorithm>
#include <boost/shared_ptr.hpp>
#include "SimDataFormats/PileupSummaryInfo/interface/PileupSummaryInfo.h" 
#include "../interface/ReWeighting.h"
#include "DataFormats/Common/interface/Handle.h"
#include "DataFormats/Provenance/interface/ProcessHistory.h"
#include "DataFormats/Provenance/interface/Provenance.h"
#include "FWCore/Common/interface/EventBase.h"

using namespace edm;

ReWeighting::ReWeighting( std::string generatedFile,
		   std::string dataFile,
		   std::string GenHistName = "pileup",
		   std::string DataHistName = "pileup") :
      generatedFileName_( generatedFile), 
      dataFileName_     ( dataFile ), 
      GenHistName_        ( GenHistName ), 
      DataHistName_        ( DataHistName )
      {
	generatedFile_ = boost::shared_ptr<TFile>( new TFile(generatedFileName_.c_str()) ); //MC distribution
	dataFile_      = boost::shared_ptr<TFile>( new TFile(dataFileName_.c_str()) );      //Data distribution

	Data_distr_ = boost::shared_ptr<TH1>(  (static_cast<TH1*>(dataFile_->Get( DataHistName_.c_str() )->Clone() )) );
	MC_distr_ = boost::shared_ptr<TH1>(  (static_cast<TH1*>(generatedFile_->Get( GenHistName_.c_str() )->Clone() )) );

	// MC * data/MC = data, so the weights are data/MC:

	// normalize both histograms first

	Data_distr_->Scale( 1.0/ Data_distr_->Integral() );
	MC_distr_->Scale( 1.0/ MC_distr_->Integral() );

	weights_ = boost::shared_ptr<TH1>( static_cast<TH1*>(Data_distr_->Clone()) );

	weights_->SetName("weightPUNew");

	TH1* den = dynamic_cast<TH1*>(MC_distr_->Clone());

	//den->Scale(1.0/ den->Integral());

	weights_->Divide( den );  // so now the average weight should be 1.0

	//std::cout << " Lumi/Pileup Reweighting: Computed Weights per In-Time Nint " << std::endl;

	int NBins = weights_->GetNbinsX();

	for(int ibin = 1; ibin<NBins+1; ++ibin){	
	  std::cout << "MyW:   " << ibin-1 << " " << weights_->GetBinContent(ibin) << std::endl;
	}


	//FirstWarning_ = true;
	//OldLumiSection_ = -1;
}

double ReWeighting::weight( int npv ) {
  int bin = weights_->GetXaxis()->FindBin( npv );
  return weights_->GetBinContent( bin );
}

double ReWeighting::weight( float npv ) {
  int bin = weights_->GetXaxis()->FindBin( npv );
  return weights_->GetBinContent( bin );
}

double ReWeighting::weight3BX( float ave_npv ) {
  int bin = weights_->GetXaxis()->FindBin( ave_npv );
  return weights_->GetBinContent( bin );
}


#endif 
