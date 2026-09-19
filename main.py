import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector

# Loading files

#URL is obtained via DOI:

# cernopendata-client get-file-locations --doi insertdoi --protocol xrootdl
#75579 10.7483/OPENDATA.CMS.DXGP.LYO9

#37720 10.7483/OPENDATA.CMS.KW1G.2Z6J
# cernopendata-client get-file-locations --doi #37720 10.7483/OPENDATA.CMS.KW1G.2Z6J --protocol xrootdl

# Creating data structures

# Selection criteria and masks

# Statistics

# Visualisation

def kinematics(pT, eta, lepton):
    pass

def selection():
    pass

def leptoncreate(tree, lepton):
    pass

def leptonmass():
    pass

def good_lepton(pT, charge, number, filtered_lepton, filter_mask):
    return filtered_lepton[(ak.num(filter_mask["Muon_pt"]) == 4) & (ak.sum(filter_mask["Muon_charge"], axis=1) == 0)]
    pass

def vector_computer(pT, eta, phi, mass, lepton, number):
    zipped_lepton = vector.zip({
        "pt": lepton[f"lepton.capitalise_pT"],
        "eta": lepton[f"lepton.capitalise_pT"],
        "phi": lepton[f"lepton.capitalise_pT"],
        "mass": lepton[f"lepton.capitalise_pT"]})
    return (zipped_lepton[:,0] + zipped_lepton[:,1] + zipped_lepton[:,2] + zipped_lepton[:,3]).mass