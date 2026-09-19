import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import vector

signal_file = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/GluGluHToZZTo4L_M125_CP5TuneDown_13TeV_powheg2_JHUGenV7011_pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2540000/17C2B325-DBA6-8145-9237-5A1859E9C2BA.root")
tree = signal_file["Events;1"]

#creating branches corresponding to lepton combinations

electrons = tree.arrays(["Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", "Electron_charge"], library = "ak")
muons = tree.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"], library = "ak")
muonelectron = tree.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge",
                             "Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", "Electron_charge"], library = "ak")
gen_weight = tree.arrays(["Generator_weight"], library = "ak")

# defining kinematic cuts for selected leptons

electron_mask = (abs(electrons["Electron_eta"]) < 2.4) & (electrons["Electron_pt"] > 5)

muon_mask = (abs(muons["Muon_eta"]) < 2.4) & (muons["Muon_pt"] > 5)

muonelectron_e_mask = (abs(muonelectron["Electron_eta"]) < 2.4) & (muonelectron["Electron_pt"] > 5)
muonelectron_m_mask = (abs(muonelectron["Muon_eta"]) < 2.4) & (muonelectron["Muon_pt"] > 5)

# applying masks and selecting events with 4 leptons and 0 charge

filtered_electrons = electrons[electron_mask]
good_electrons = filtered_electrons[(ak.num(filtered_electrons["Electron_pt"]) == 4) & (ak.sum(filtered_electrons["Electron_charge"], axis=1) == 0)]

filtered_muons = muons[muon_mask]
good_muons = filtered_muons[(ak.num(filtered_muons["Muon_pt"]) == 4) & (ak.sum(filtered_muons["Muon_charge"], axis=1) == 0)]

filtered_muonelectron_e = muonelectron[["Electron_pt", "Electron_eta", "Electron_phi", "Electron_mass", "Electron_charge"]][muonelectron_e_mask]
filtered_muonelectron_m = muonelectron[["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"]][muonelectron_m_mask]

good_muonelectron_mask =(ak.num(filtered_muonelectron_e["Electron_pt"]) == 2) & (ak.sum(filtered_muonelectron_e["Electron_charge"], axis=1) == 0) & (ak.num(filtered_muonelectron_m["Muon_pt"]) == 2) & (ak.sum(filtered_muonelectron_m["Muon_charge"], axis=1) == 0)
good_muonelectron_m = filtered_muonelectron_m[good_muonelectron_mask]  
good_muonelectron_e = filtered_muonelectron_e[good_muonelectron_mask]

# vector library is used to zip properties of leptons with their corresponding branches

electron_p = vector.zip({
    "pt": good_electrons["Electron_pt"],
    "eta": good_electrons["Electron_eta"],
    "phi": good_electrons["Electron_phi"],
    "mass": good_electrons["Electron_mass"]})

muons_p = vector.zip({
    "pt": good_muons["Muon_pt"],
    "eta": good_muons["Muon_eta"],
    "phi": good_muons["Muon_phi"],
    "mass": good_muons["Muon_mass"]})

muonelectron_p = vector.zip({
    "pt": ak.concatenate([good_muonelectron_m["Muon_pt"], good_muonelectron_e["Electron_pt"]], axis=1),
    "eta": ak.concatenate([good_muonelectron_m["Muon_eta"], good_muonelectron_e["Electron_eta"]], axis=1),
    "phi": ak.concatenate([good_muonelectron_m["Muon_phi"], good_muonelectron_e["Electron_phi"]], axis=1),
    "mass": ak.concatenate([good_muonelectron_m["Muon_mass"], good_muonelectron_e["Electron_mass"]], axis=1)})

# summing the 4 leptons to calculate the invariant masses in GeV

sum_electrons = electron_p[:, 0] + electron_p[:, 1] + electron_p[:, 2] + electron_p[:, 3]
sum_muons = muons_p[:, 0] + muons_p[:, 1] + muons_p[:, 2] + muons_p[:, 3]
muon_electron_sum = muonelectron_p[:, 0] + muonelectron_p[:, 1] + muonelectron_p[:, 2] + muonelectron_p[:, 3]

electrons_mass = sum_electrons.mass
muons_mass = sum_muons.mass
muon_electron_mass = muon_electron_sum.mass

lepton_mass = ak.concatenate([electrons_mass, muons_mass, muon_electron_mass], axis=0)

# lepton weights

electron_weights = gen_weight[(ak.num(filtered_electrons["Electron_pt"]) == 4) & (ak.sum(filtered_electrons["Electron_charge"], axis=1) == 0)]

muon_weights = gen_weight[(ak.num(filtered_muons["Muon_pt"]) == 4) & (ak.sum(filtered_muons["Muon_charge"], axis=1) == 0)]

muonelectron_weights = gen_weight[(ak.num(filtered_muonelectron_e["Electron_pt"]) == 2) & (ak.sum(filtered_muonelectron_e["Electron_charge"], axis=1) == 0)
                                  & (ak.num(filtered_muonelectron_m["Muon_pt"]) == 2) & (ak.sum(filtered_muonelectron_m["Muon_charge"], axis=1) == 0)]

lepton_weights = ak.concatenate([electron_weights,muon_weights,muonelectron_weights],axis=0)
print(lepton_weights["Generator_weight"])