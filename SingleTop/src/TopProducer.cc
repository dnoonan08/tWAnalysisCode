/*
 *\Author: A. Orso M. Iorio 
 *
 *
 *\version  $Id: TopProducer.cc,v 1.9 2010/05/17 08:07:47 oiorio Exp $ 
 */

// Single Top producer: produces a top candidate made out of a Lepton, a B jet and a MET

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



#include "TopQuarkAnalysis/SingleTop/interface/TopProducer.h"

#include <vector>
#include <memory>

#include "DataFormats/Math/interface/LorentzVector.h"


//using namespace pat;


TopProducer::TopProducer(const edm::ParameterSet& iConfig) 
{
  // initialize the configurables
  electronsSrc_		          = iConfig.getParameter<edm::InputTag>	      ( "electronsSource" );
  muonsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "muonsSource" );
  jetsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "jetsSource" );
  METsSrc_                 = iConfig.getParameter<edm::InputTag>	      ( "METsSource" );
  
  useNegativeDeltaSolutions_ = iConfig.getUntrackedParameter<bool> ("useNegativeDeltaSolutions",true); 
  usePositiveDeltaSolutions_ = iConfig.getUntrackedParameter<bool> ("usePositiveDeltaSolutions",true); 

  usePzMinusSolutions_ = iConfig.getUntrackedParameter<bool> ("usePzMinusSolutions",false); 
  usePzPlusSolutions_ = iConfig.getUntrackedParameter<bool> ("usePzPlusSolutions",false); 
  usePzAbsValMinimumSolutions_ = iConfig.getUntrackedParameter<bool> ("usePzAbsValMinimumSolutions",true); 

  useMetForNegativeSolutions_=iConfig.getUntrackedParameter<bool> ("useMetForNegativeSolutions",false);

  usePxMinusSolutions_ = iConfig.getUntrackedParameter<bool> ("usePxMinusSolutions",true); 
  usePxPlusSolutions_ = iConfig.getUntrackedParameter<bool> ("usePxPlusSolutions",true); 

produces<std::vector<pat::Electron> >();
produces<std::vector<pat::Muon> >();
produces<std::vector<pat::Jet> >();
produces<std::vector<pat::MET> >();



//produces<std::vector< pat::TopLeptonic > >();
produces<std::vector< reco::NamedCompositeCandidate > >();
 
}

void TopProducer::produce(edm::Event & iEvent, const edm::EventSetup & iEventSetup){


edm::Handle<edm::View<pat::Electron> > electrons;
iEvent.getByLabel(electronsSrc_,electrons);


edm::Handle<edm::View<pat::Muon> > muons;
iEvent.getByLabel(muonsSrc_,muons);


edm::Handle<edm::View<pat::Jet> > jets;
iEvent.getByLabel(jetsSrc_,jets);


edm::Handle<edm::View<pat::MET> > mets;
iEvent.getByLabel(METsSrc_,mets);




 std::vector< reco::NamedCompositeCandidate > * TopCandidates = new std::vector<reco::NamedCompositeCandidate>();

 
 for(size_t i = 0; i < electrons->size(); ++i){
   for(size_t j = 0; j < jets->size(); ++j){
     for(size_t m = 0; m < mets->size(); ++m){
       
       reco::NamedCompositeCandidate Top,W,Nu;

       Top.addDaughter(electrons->at(i),"Lepton");
       Top.addDaughter(electrons->at(i),"Electron");
       Top.addDaughter(jets->at(j),"BJet");
       Top.addDaughter(mets->at(m),"MET");
       

       std::vector<math::XYZTLorentzVector> NuMomenta = Nu4Momentum(electrons->at(i),mets->at(m));
       
       if(NuMomenta.size()>0){
	 Nu.setP4((math::XYZTLorentzVector)NuMomenta.at(0));
	 W.setP4(Nu.p4()+(electrons->at(i).p4()));
	 Top.setP4(W.p4()+jets->at(j).p4());
       }
       else{W.setP4(electrons->at(i).p4()+mets->at(m).p4());}
       


       Top.addDaughter(W,"W");
       Top.addDaughter(Nu,"RecoNu");
       TopCandidates->push_back(Top);
     }
   }
 }


 for(size_t i = 0; i < muons->size(); ++i){
   for(size_t j = 0; j < jets->size(); ++j){
     for(size_t m = 0; m < mets->size(); ++m){
       
       reco::NamedCompositeCandidate Top,W,Nu;

       Top.addDaughter(muons->at(i),"Lepton");
       Top.addDaughter(muons->at(i),"Muon");
       Top.addDaughter(jets->at(j),"BJet");
       Top.addDaughter(mets->at(m),"MET");
 


       std::vector<math::XYZTLorentzVector> NuMomenta = Nu4Momentum(muons->at(i),mets->at(m));

       //       W.setP4(muons->at(i).p4()+mets->at(m).p4());
       if(NuMomenta.size()>0){
	 Nu.setP4((math::XYZTLorentzVector)NuMomenta.at(0));
	 W.setP4(Nu.p4()+(muons->at(i).p4()));
	 Top.setP4(W.p4()+jets->at(j).p4());
       }
       else{W.setP4(muons->at(i).p4()+mets->at(m).p4());}
     

       /*       if(NuMomenta.size()>0)std::cout << "top mass is: "<< Top.mass()<< "RecoNuPt "<< Nu.pt()  <<std::endl;       
       else{std::cout<< "no neutrino solution given!"  <<std::endl;}
       */

       Top.addDaughter(W,"W");
       Top.addDaughter(Nu,"RecoNu");
       TopCandidates->push_back(Top);
     }
   }
 } 
 
 
 std::auto_ptr< std::vector< reco::NamedCompositeCandidate > > newTopCandidate(TopCandidates);
 
////////

//iEvent.put(newTopLeptonic);

iEvent.put(newTopCandidate);

}

TopProducer::~TopProducer(){;}

std::vector<math::XYZTLorentzVector> TopProducer::Nu4Momentum(const reco::Candidate & Lepton,const reco::Candidate & MET){

  double  mW = 80.38;

  std::vector<math::XYZTLorentzVector> result;
  
  //  double Wmt = sqrt(pow(Lepton.et()+MET.pt(),2) - pow(Lepton.px()+MET.px(),2) - pow(Lepton.py()+MET.py(),2) );
    
  double MisET2 = (MET.px()*MET.px() + MET.py()*MET.py());
  double mu = (mW*mW)/2 + MET.px()*Lepton.px() + MET.py()*Lepton.py();
  double a  = (mu*Lepton.pz())/(Lepton.energy()*Lepton.energy() - Lepton.pz()*Lepton.pz());
  double a2 = TMath::Power(a,2);
  double b  = (TMath::Power(Lepton.energy(),2.)*(MisET2) - TMath::Power(mu,2.))/(TMath::Power(Lepton.energy(),2) - TMath::Power(Lepton.pz(),2));
  double pz1(0),pz2(0),pznu(0);
  int nNuSol(0);

  math::XYZTLorentzVector p4nu_rec;
  math::XYZTLorentzVector p4W_rec;
  math::XYZTLorentzVector p4b_rec;
  math::XYZTLorentzVector p4Top_rec;
  math::XYZTLorentzVector p4lep_rec;    

  p4lep_rec.SetPxPyPzE(Lepton.px(),Lepton.py(),Lepton.pz(),Lepton.energy());
  
  math::XYZTLorentzVector p40_rec(0,0,0,0);

  if(a2-b > 0 ){
    if(!usePositiveDeltaSolutions_)
      {
	result.push_back(p40_rec);
	return result;
      }
    double root = sqrt(a2-b);
    pz1 = a + root;
    pz2 = a - root;
    nNuSol = 2;     
  
  
    

    if(usePzPlusSolutions_)pznu = pz1;    
    if(usePzMinusSolutions_)pznu = pz2;
    if(usePzAbsValMinimumSolutions_){
      pznu = pz1;
      if(fabs(pz1)>fabs(pz2)) pznu = pz2;
    }
    

  double Enu = sqrt(MisET2 + pznu*pznu);
  
  p4nu_rec.SetPxPyPzE(MET.px(), MET.py(), pznu, Enu);
    
  result.push_back(p4nu_rec);
  
  }
  else{

    if(!useNegativeDeltaSolutions_){
      result.push_back(p40_rec);
      return result;
    }
    //    double xprime = sqrt(mW;


    double ptlep = Lepton.pt(),pxlep=Lepton.px(),pylep=Lepton.py(),metpx=MET.px(),metpy=MET.py();

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
      
    if(usePxMinusSolutions_){
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
    } 
    
    if(usePxPlusSolutions_){
      for( int i =0; i< (int)solutions2.size();++i){
	if(solutions2[i]<0 ) continue;
	double p_x = (solutions2[i]*solutions2[i]-mW*mW)/(4*pxlep); 
	double p_y = ( mW*mW*pylep + 2*pxlep*pylep*p_x +mW*ptlep*solutions2[i])/(2*pxlep*pxlep);
	double Delta2 = (p_x-metpx)*(p_x-metpx)+(p_y-metpy)*(p_y-metpy); 
	//  std::cout<<"intermediate solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
	if(Delta2< deltaMin && Delta2 > 0){deltaMin = Delta2;
	  minPx=p_x;
	  minPy=p_y;
	}
	//	std::cout<<"solution2 met x "<<metpx << " min px " << minPx  <<" met y "<<metpy <<" min py "<< minPy << std::endl; 
      }
    }
    
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
    double a_Minimum  = (mu_Minimum*Lepton.pz())/(Lepton.energy()*Lepton.energy() - Lepton.pz()*Lepton.pz());
    pznu = a_Minimum;
    
    if(!useMetForNegativeSolutions_){
      double Enu = sqrt(minPx*minPx+minPy*minPy + pznu*pznu);
      p4nu_rec.SetPxPyPzE(minPx, minPy, pznu , Enu);
    }
    else{
      pznu = a;
      double Enu = sqrt(metpx*metpx+metpy*metpy + pznu*pznu);
      p4nu_rec.SetPxPyPzE(metpx, metpy, pznu , Enu);
    }
    result.push_back(p4nu_rec);}
  return result;    
}

DEFINE_FWK_MODULE( TopProducer );
