#include "TopQuarkAnalysis/SingleTop/interface/CandidateBooster.h" 
#include "DataFormats/Candidate/interface/NamedCompositeCandidate.h"
#include "DataFormats/Candidate/interface/NamedCompositeCandidateFwd.h"

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"



//typedef CandidateBooster< edm::View<reco::NamedCompositeCandidate> > NamedCompositeCandidateBooster;
typedef CandidateBooster< reco::NamedCompositeCandidateCollection > NamedCompositeCandidateBooster;

DEFINE_FWK_MODULE(NamedCompositeCandidateBooster);
