// -*- C++ -*-
//
// Package:    SingleTopRecoFilter
// Class:      SingleTopRecoFilter
//
/**\class SingleTopRecoFilter SingleTopRecoFilter.cc SingleTopRecoFilter/src/SingleTopRecoFilter.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Joosep Pata,510 R-020,+41227671640,
//         Created:  Tue Jul 31 14:30:54 CEST 2012
// $Id: SingleTopRecoFilter.cc,v 1.1.2.1 2012/08/10 08:18:05 jpata Exp $
//
//

// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDFilter.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"
#include "DataFormats/JetReco/interface/PFJet.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

//
// class declaration
//

class SingleTopRecoFilter : public edm::EDFilter
{
public:
    explicit SingleTopRecoFilter(const edm::ParameterSet &);
    ~SingleTopRecoFilter();

    static void fillDescriptions(edm::ConfigurationDescriptions &descriptions);

private:
    virtual void beginJob() ;
    virtual bool filter(edm::Event &, const edm::EventSetup &);
    virtual void endJob() ;

    virtual bool beginRun(edm::Run &, edm::EventSetup const &);
    virtual bool endRun(edm::Run &, edm::EventSetup const &);
    virtual bool beginLuminosityBlock(edm::LuminosityBlock &, edm::EventSetup const &);
    virtual bool endLuminosityBlock(edm::LuminosityBlock &, edm::EventSetup const &);

    float PFDeltaBetaRelIso(reco::Muon const *mu);

    int minMuons;
    int minJets;

    double minJetPt;
    double minMuonPt;

    double maxMuonEta;
    double maxMuonRelIso;
    double maxJetEta;

    // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
SingleTopRecoFilter::SingleTopRecoFilter(const edm::ParameterSet &iConfig)
{
    //now do what ever initialization is needed
    minMuons = iConfig.getUntrackedParameter<int>("minMuons", 0);
    minJets = iConfig.getUntrackedParameter<int>("minJets", 0);
    minJetPt = iConfig.getUntrackedParameter<double>("minJetPt", 0.0);
    minMuonPt = iConfig.getUntrackedParameter<double>("minMuonPt", 0.0);

    maxMuonEta = iConfig.getUntrackedParameter<double>("maxMuonEta", 10.0);
    maxMuonRelIso = iConfig.getUntrackedParameter<double>("maxMuonRelIso", 10.0);
    maxJetEta = iConfig.getUntrackedParameter<double>("maxJetEta", 10.0);

}


SingleTopRecoFilter::~SingleTopRecoFilter()
{

    // do anything here that needs to be done at desctruction time
    // (e.g. close files, deallocate resources etc.)

}

//Calculate the delta-beta corrected relative isolation
float SingleTopRecoFilter::PFDeltaBetaRelIso(reco::Muon const *mu)
{
    float sumChHadPt = (*mu).pfIsolationR04().sumChargedHadronPt;
    float sumNeHadEt = (*mu).pfIsolationR04().sumNeutralHadronEt;
    float sumPhotEt = (*mu).pfIsolationR04().sumPhotonEt;
    float sumPUPt = (*mu).pfIsolationR04().sumPUPt;

    float relIso = (sumChHadPt + std::max(0.0F, sumNeHadEt + sumPhotEt - 0.5F * sumPUPt)) / (*mu).pt();
    return relIso;
}


//
// member functions
//

// ------------ method called on each new Event  ------------
bool
SingleTopRecoFilter::filter(edm::Event &iEvent, const edm::EventSetup &iSetup)
{
    using namespace edm;
    using namespace reco;
    Handle<View<Muon>> muons;
    iEvent.getByLabel("muons", muons);

    Handle<View<GsfElectron>> electrons;
    iEvent.getByLabel("gsfElectrons", electrons);

    Handle<View<PFJet>> jets;
    iEvent.getByLabel("ak5PFJets", jets);

    int nMuons = 0;
    int nElectrons = 0;
    int nJets = 0;

    std::list<Muon const *> goodMuons;
    for (View<Muon>::const_iterator mu = muons->begin(); mu != muons->end(); mu++)
    {
        if ((*mu).pt() > minMuonPt
                && (*mu).isGlobalMuon()
                && abs((*mu).eta()) < maxMuonEta
                && (*mu).isPFMuon()
                && PFDeltaBetaRelIso(&(*mu)) < maxMuonRelIso
                && (*mu).globalTrack()->hitPattern().numberOfValidMuonHits() > 0
                && (*mu).globalTrack()->hitPattern().trackerLayersWithMeasurement() > 5
           )
        {
            goodMuons.push_back(&*mu);
            LogDebug("muon") << "Found a good muon with pt: " << (*mu).pt() << " eta " << (*mu).eta();
        }
    }
    nMuons = goodMuons.size();

    std::list<PFJet const *> goodJets;
    for (View<PFJet>::const_iterator jet = jets->begin(); jet != jets->end(); jet++)
    {
        if ((*jet).pt() > minJetPt
                && abs((*jet).eta()) < maxJetEta
                && (*jet).numberOfDaughters() > 1
           )
        {
            goodJets.push_back(&*jet);
            LogDebug("jet") << "Jet pt " << (*jet).pt();
        }
    }
    nJets = goodJets.size();

    LogDebug("muon") << "nMuons=" << nMuons;
    LogDebug("electron") << "nElectrons=" << nMuons;

    bool passesMuons = false;
    bool passesJets = false;
    if (nMuons >= minMuons)
    {
        LogDebug("cuts") << "We have at least " << minMuons << " good muons";
        passesMuons = true;
    }
    if (nJets >= minJets)
    {
        LogDebug("cuts") << "We have at least " << minJets << " good jets";
        passesJets = true;
    }

    bool passes = false;
    passes = passesMuons && passesJets;
    if (passes)
    {
        LogDebug("filter") << "This event passes the filter";
    }

    return passes;
}

// ------------ method called once each job just before starting event loop  ------------
void
SingleTopRecoFilter::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void
SingleTopRecoFilter::endJob()
{
}

// ------------ method called when starting to processes a run  ------------
bool
SingleTopRecoFilter::beginRun(edm::Run &, edm::EventSetup const &)
{
    return true;
}

// ------------ method called when ending the processing of a run  ------------
bool
SingleTopRecoFilter::endRun(edm::Run &, edm::EventSetup const &)
{
    return true;
}

// ------------ method called when starting to processes a luminosity block  ------------
bool
SingleTopRecoFilter::beginLuminosityBlock(edm::LuminosityBlock &, edm::EventSetup const &)
{
    return true;
}

// ------------ method called when ending the processing of a luminosity block  ------------
bool
SingleTopRecoFilter::endLuminosityBlock(edm::LuminosityBlock &, edm::EventSetup const &)
{
    return true;
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
SingleTopRecoFilter::fillDescriptions(edm::ConfigurationDescriptions &descriptions)
{
    //The following says we do not know what parameters are allowed so do no validation
    // Please change this to state exactly what you do use, even if it is no parameters
    edm::ParameterSetDescription desc;
    desc.setUnknown();
    descriptions.addDefault(desc);
}
//define this as a plug-in
DEFINE_FWK_MODULE(SingleTopRecoFilter);
