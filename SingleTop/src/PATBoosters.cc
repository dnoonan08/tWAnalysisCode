#include "TopQuarkAnalysis/SingleTop/interface/CandidateBooster.h" 

#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/MakerMacros.h"


#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/PFParticle.h"

//typedef CandidateBooster< edm::View<reco::NamedCompositeCandidate> > NamedCompositeCandidateBooster;
typedef CandidateBooster< std::vector<pat::Electron> > PATElectronBooster;

typedef CandidateBooster< std::vector<pat::Muon> > PATMuonBooster;

typedef CandidateBooster< std::vector<pat::Jet> > PATJetBooster;

typedef CandidateBooster< std::vector<pat::MET> > PATMETBooster;

typedef CandidateBooster< std::vector<pat::Photon> > PATPhotonBooster;

typedef CandidateBooster< std::vector<pat::PFParticle> > PATPFParticleBooster;

DEFINE_FWK_MODULE(PATElectronBooster);
DEFINE_FWK_MODULE(PATMuonBooster);
DEFINE_FWK_MODULE(PATJetBooster);
DEFINE_FWK_MODULE(PATMETBooster);
DEFINE_FWK_MODULE(PATPhotonBooster);
DEFINE_FWK_MODULE(PATPFParticleBooster);
