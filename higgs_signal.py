import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector

background_file = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/GluGluHToZZTo4L_M125_CP5TuneDown_13TeV_powheg2_JHUGenV7011_pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2540000/17C2B325-DBA6-8145-9237-5A1859E9C2BA.root")

tree = background_file["Events;1"]

muons = tree.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"], entry_stop = 10000, library = "ak")

# cuts

muon_mask = (abs(muons["Muon_eta"]) < 2.4) & (muons["Muon_pt"] > 5)

filtered_muons = muons[muon_mask]

good_muons = filtered_muons[(ak.num(filtered_muons["Muon_pt"]) == 4) & (ak.sum(filtered_muons["Muon_charge"], axis=1) == 0)]



muons_p = vector.zip({
    "pt": good_muons["Muon_pt"],
    "eta": good_muons["Muon_eta"],
    "phi": good_muons["Muon_phi"],
    "mass": good_muons["Muon_mass"]})


electrons = tree.arrays(["Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", "Electron_charge"], entry_stop = 10000, library = "ak")

electron_mask = (abs(electrons["Electron_eta"]) < 2.4) & (electrons["Electron_pt"] > 5)

filtered_electrons = electrons[electron_mask]
good_electrons = filtered_electrons[(ak.num(filtered_electrons["Electron_pt"]) == 4) & (ak.sum(filtered_electrons["Electron_charge"], axis=1) == 0)]

electron_p = vector.zip({
    "pt": good_electrons["Electron_pt"],
    "eta": good_electrons["Electron_eta"],
    "phi": good_electrons["Electron_phi"],
    "mass": good_electrons["Electron_mass"]})

muonelectron = tree.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge",
                             "Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", "Electron_charge"],
                               entry_stop = 10000, library = "ak")

muonelectron_e_mask = (abs(muonelectron["Electron_eta"]) < 2.4) & (muonelectron["Electron_pt"] > 5)
muonelectron_m_mask = (abs(muonelectron["Muon_eta"]) < 2.4) & (muonelectron["Muon_pt"] > 5)

filtered_muonelectron_e = muonelectron[["Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", "Electron_charge"]][muonelectron_e_mask]
filtered_muonelectron_m = muonelectron[["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"]][muonelectron_m_mask]

good_muonelectron_mask =(ak.num(filtered_muonelectron_e["Electron_pt"]) == 2) & (ak.sum(filtered_muonelectron_e["Electron_charge"], axis=1) == 0) & (ak.num(filtered_muonelectron_m["Muon_pt"]) == 2) & (ak.sum(filtered_muonelectron_m["Muon_charge"], axis=1) == 0)

good_muonelectron_m = filtered_muonelectron_m[good_muonelectron_mask]  
good_muonelectron_e = filtered_muonelectron_e[good_muonelectron_mask]

muonelectron_p = vector.zip({
    "pt": ak.concatenate([good_muonelectron_m["Muon_pt"], good_muonelectron_e["Electron_pt"]], axis=1),
    "eta": ak.concatenate([good_muonelectron_m["Muon_eta"], good_muonelectron_e["Electron_eta"]], axis=1),
    "phi": ak.concatenate([good_muonelectron_m["Muon_phi"], good_muonelectron_e["Electron_phi"]], axis=1),
    "mass": ak.concatenate([good_muonelectron_m["Muon_mass"], good_muonelectron_e["Electron_mass"]], axis=1)})


sum_muons = muons_p[:, 0] + muons_p[:, 1] + muons_p[:, 2] + muons_p[:, 3]
muon_electron_sum = muonelectron_p[:, 0] + muonelectron_p[:, 1] + muonelectron_p[:, 2] + muonelectron_p[:, 3]
sum_electrons = electron_p[:, 0] + electron_p[:, 1] + electron_p[:, 2] + electron_p[:, 3]

electrons_mass = sum_electrons.mass
muons_mass = sum_muons.mass
muon_electron_mass = muon_electron_sum.mass

lepton_mass = ak.concatenate([muons_mass, electrons_mass, muon_electron_mass], axis=0)

# print("Success")
# # print(muonelectron.keys())