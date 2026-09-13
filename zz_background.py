import uproot
import awkward as ak
import matplotlib.pyplot as plt
import numpy as np
import mplhep as hep
import vector

signal_file = uproot.open("root://eospublic.cern.ch//eos/opendata/cms/mc/RunIISummer20UL16NanoAODv9/ZZto4L_EWK_PolarizedZ0Z0_TuneCP5_13TeV-madgraph-pythia8/NANOAODSIM/106X_mcRun2_asymptotic_v17-v2/2550000/26A3DE6B-7295-F241-A2A7-54C94DCD1926.root")

inspection1 = signal_file["Events;1"]

muoninspect = inspection1.arrays(["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Muon_charge"], entry_stop = 10000, library = "ak")
mask = (abs(muoninspect["Muon_eta"]) < 2.4) & (muoninspect["Muon_pt"] > 5)
fmask1 = muoninspect[mask]

filtered1 = fmask1[(ak.num(fmask1["Muon_pt"]) == 4) & (ak.sum(fmask1["Muon_charge"], axis=1) == 0)]

muons_p1 = vector.zip({
    "pt": filtered1["Muon_pt"],
    "eta": filtered1["Muon_eta"],
    "phi": filtered1["Muon_phi"],
    "mass": filtered1["Muon_mass"]})

sum_muons1 = muons_p1[:, 0] + muons_p1[:, 1] + muons_p1[:, 2] + muons_p1[:, 3]
muons_mass = sum_muons1.mass